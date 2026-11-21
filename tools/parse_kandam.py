"""Turn the decoded PDF lines of one kandam (அயோத்தியா … யுத்த) into one content file per padalam.

    python3 tools/parse_kandam.py 2        # அயோத்தியா காண்டம் -> content/2/<pp>.src.json

Reads work/<part>/lines.jsonl (made by fontmap.py + decode_pdf.py with that work dir).
பால காண்டம் uses parse_pdf.py; these PDFs differ a little:
  * a table of contents on page 1 gives every padalam's title and first page;
  * padalam titles and sub-headings are 16 pt (பால காண்டம்: 18-20 pt titles, 14 pt sub-headings);
  * poem lines are 16 pt bold at x = 72 / 108;
  * each kandam opens with a கடவுள் வாழ்த்து poem, which is put at the head of padalam 1;
  * the extra verses (மிகைப் பாடல்கள்) after the last padalam are left out, as for பால காண்டம்.
Poem numbers run on through the whole Ramayanam (பால காண்டம் 1-1312, அயோத்தியா 1313-2515, ...).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_pdf import (line_text, runs_markup, tidy_markup, fix_poem_punct, fix_prose_punct, METER_RE)

ROOT = Path(__file__).resolve().parent.parent

KANDAMS = {
    2: dict(parts=['k2'], first=1313, last=2515, inv_unnumbered=True),
    3: dict(parts=['k3'], first=2516, last=3707),
    4: dict(parts=['k4'], first=3708, last=4739),
    5: dict(parts=['k5'], first=4740, last=6058),
    6: dict(parts=['k6a', 'k6b', 'k6c'], first=6059, last=10368),
}
FIXES = {}        # poem number: [(wrong, right), ...] — typos in the source PDF
LINE_FIXES = {}   # poem number: [lines] — poems whose line breaks are wrong in the source


def norm(s):
    return re.sub(r'[\s.\d◌]+', '', s)


def toc(L):
    """[(title, page)] from the contents on the first pages; only the padalams and the கடவுள் வாழ்த்து."""
    out = []
    for d in L:
        if d['page'] > 3:
            break
        m = re.match(r'^(.*?)\s*\.{3,}\s*(\d+)\s*$', line_text(d))
        if not m:
            continue
        title = re.sub(r'\s+', ' ', m.group(1)).strip().rstrip('.').strip()
        if title.endswith('படலம்') or title == 'கடவுள் வாழ்த்து':
            out.append((title, int(m.group(2))))
    return out


def load(k):
    """All lines of the kandam in reading order, with the parts' pages made unique (part i: page + 1000*i)."""
    cfg = KANDAMS[k]
    lines, sections = [], []
    for pi, part in enumerate(cfg['parts']):
        L = [json.loads(l) for l in open(ROOT / 'work' / part / 'lines.jsonl', encoding='utf-8')]
        secs = toc(L)
        if not secs:
            raise SystemExit(f'{part}: no table of contents found')
        first_page = min(p for t, p in secs)
        last_start = max(p for t, p in secs)
        # where the extra verses begin: cut there (keep any text before the words on that line)
        cut = None
        for i, d in enumerate(L):
            if d['page'] < last_start:
                continue
            t = line_text(d)
            if re.search(r'மிகைப்\s*பாடல்கள்', t) and (len(t) < 40 or re.search(r'மிகைப்\s*பாடல்கள்\s*\d*\s*$', t)):
                cut = i
                break
        keep = L[:cut] if cut is not None else L
        if cut is not None:
            d = dict(L[cut])
            runs, acc = [], ''
            for t, b in d['runs']:
                if 'மிகைப்' in acc + t:
                    t = (acc + t).split('மிகைப்')[0][len(acc):]
                    runs.append([t, b])
                    break
                runs.append([t, b])
                acc += t
            d['runs'] = runs
            if line_text(d):
                keep = keep + [d]
        for d in keep:
            if d['page'] >= first_page:
                d = dict(d)
                d['page'] += 1000 * pi
                lines.append(d)
        for t, p in secs:
            sections.append((t, p + 1000 * pi))
    return lines, sections


# "2644. ...", "2645'...", "2692முந்து ...", "8682, ‘...", "(3)6010. ..."
START_RE = re.compile(r'^(?:\(\d{1,3}\)\s*)?(?:\d{1,2}\s+)?(\d{3,5})\s*(?:[.,]\s*|\s+|(?=[‘’\'"“\u0B80-\u0BFF]))(.*)$')
# a poem number after other text on the same line: "… உணர்க. 41 1532. ‘ஏவம் …", "… கேட்டல்4698."
MID_RE = re.compile(r'(?:^|\s|(?<=[\u0B80-\u0BFF.]))(\d{4,5})\s*(?:[.,]\s*|(?=[‘\'"“]))(\S.*)?$')


def find_starts(L, cfg):
    """Which lines begin a poem, and its number. The numbers are matched against the running sequence,
    so a misprinted number (1647 for 1674) or a poem missing from the PDF does not stop the count."""
    cands = []
    for i, d in enumerate(L):
        if not (d['size'] >= 15 or d['bold'] >= 0.8):
            continue
        t = line_text(d)
        m = START_RE.match(t)
        if m and d['size'] >= 15 and d['bold'] >= 0.5:
            cands.append((i, int(m.group(1)), '', m.group(2)))
            continue
        mm = MID_RE.search(t)
        if mm and mm.start() > 0 and d['size'] >= 15:
            cands.append((i, int(mm.group(1)), t[:mm.start()].strip(), mm.group(2) or ''))
    lo, hi = cfg['first'], cfg['last']
    cands = [c for c in cands if not c[2] or lo <= c[1] <= hi]      # a number inside a line must be in range
    expect = lo + (1 if cfg.get('inv_unnumbered') else 0)
    starts, missing, misprints = {}, [], []
    for j, (i, num, pre, rest) in enumerate(cands):
        nxt = [c[1] for c in cands[j + 1:j + 3]]
        if num == expect:
            pass
        elif expect < num <= expect + 12 and (not nxt or nxt[0] == num + 1) and (num <= expect + 3 or nxt[1:2] in ([], [num + 2])):
            missing += list(range(expect, num))
            expect = num
        elif nxt and nxt[0] in (expect + 1, expect + 2) and abs(num - expect) > 0:
            misprints.append((expect, num))
            num = expect
        else:
            continue
        starts[i] = (num, pre, rest)
        expect = num + 1
    return starts, expect, missing, misprints


class _M:
    def __init__(self, g):
        self.g = g

    def group(self, i):
        return self.g


def parse(k):
    cfg = KANDAMS[k]
    L, secs = load(k)
    starts = [p for t, p in secs]
    titles = {norm(t) for t, p in secs}

    def section_index(page):
        i = 0
        for j, p in enumerate(starts):
            if page >= p:
                i = j
        return i

    sections = [{'id': i, 'title': t, 'start_page': p, 'items': [], 'intro': []} for i, (t, p) in enumerate(secs)]
    starts_at, expect, missing, misprints = find_starts(L, cfg)
    cur_poem = None
    para = None
    quote = None
    prev = None
    inv_pending = False

    def flush_para():
        nonlocal para
        if para is None:
            return
        text = tidy_markup(' '.join(para['parts']))
        obj = {'kind': 'p', 'text': text, 'head': para.get('head', False)}
        if para['poem'] is None:
            sections[para['sec']]['intro'].append(obj)
        else:
            para['poem']['paras'].append(obj)
        para = None

    def flush_quote():
        nonlocal quote
        if quote is None:
            return
        q = {'kind': 'q', 'lines': [re.sub(r'\*\*', '', x) for x in quote['lines']]}
        if quote['poem'] is None:
            sections[quote['sec']]['intro'].append(q)
        else:
            quote['poem']['paras'].append(q)
        quote = None

    for idx, d in enumerate(L):
        s = section_index(d['page'])
        t = line_text(d)
        if not t:
            continue
        nt = norm(t)
        # padalam titles ("மந்திரப் படலம்", "1. மந்திரப் படலம்") and the கடவுள் வாழ்த்து title
        if (nt in titles or nt == norm('கடவுள் வாழ்த்து')) and len(t) < 60:
            flush_para(); flush_quote()
            if nt == norm('கடவுள் வாழ்த்து'):
                inv_pending = True
            prev = d
            continue
        big = d['size'] >= 15
        bold = d['bold'] >= 0.8
        m, num = None, None
        if idx in starts_at:
            num, pre, rest = starts_at[idx]
            if pre and big and d['bold'] < 0.5 and len(pre) < 70:
                flush_para(); flush_quote()          # a sub-heading printed on the same line as the number
                para = {'sec': s, 'poem': cur_poem if (cur_poem and cur_poem['sec'] == s) else None, 'parts': [pre], 'head': True}
            elif pre and para is not None:
                para['parts'].append(pre)
            m = _M(rest)
        elif inv_pending and big and bold and not starts_at.get(idx):
            m, num = _M(t), cfg['first']        # the unnumbered கடவுள் வாழ்த்து poem of அயோத்தியா காண்டம்
        if m:
            inv_pending = False
            flush_para(); flush_quote()
            first = m.group(2).strip()
            cur_poem = {'n': num, 'sec': s, 'lines': [first] if first else [], 'paras': [], 'page': d['page'], 'in_poem': True}
            sections[s]['items'].append({'type': 'poem', 'ref': cur_poem})
            prev = d
            continue
        if cur_poem and cur_poem.get('in_poem') and big and bold and len(cur_poem['lines']) < 8 and len(t) <= 60 and (
                (prev is not None and prev['page'] == d['page'] and d['y'] - prev['y'] < 62) or
                (prev is not None and prev['page'] != d['page'])):
            raw = ''.join(x for x, b in d['runs'])
            lead = len(raw) - len(raw.lstrip(' '))
            if lead >= 12 and len(t) <= 16 and cur_poem['lines']:
                cur_poem['lines'][-1] = cur_poem['lines'][-1].rstrip() + ' ' + t
            else:
                cur_poem['lines'].append(t)
            prev = d
            continue
        if cur_poem:
            cur_poem['in_poem'] = False
        owner = cur_poem if (cur_poem and cur_poem['sec'] == s) else None
        if big and not bold and len(t) < 70 and ' - ' not in t:
            # 16 pt plain lines are the sub-headings in these PDFs
            flush_para(); flush_quote()
            para = {'sec': s, 'poem': owner, 'parts': [t], 'head': True}
            flush_para()
            prev = d
            continue
        if big and bold and len(t) < 50 and ' - ' not in t and not re.search(r'\s-\S|\S-\s', t):
            # a quoted verse inside the notes (bold 16 pt, but not where a poem is expected)
            flush_para()
            if quote is None:
                quote = {'sec': s, 'poem': owner, 'lines': []}
            quote['lines'].append(t)
            prev = d
            continue
        flush_quote()
        new_para = (para is None or d['x0'] > 75 or para.get('head') or
                    (prev is not None and prev['page'] == d['page'] and d['y'] - prev['y'] > 20) or
                    para['sec'] != s)
        if new_para:
            flush_para()
            para = {'sec': s, 'poem': owner, 'parts': []}
        para['parts'].append(runs_markup(d['runs']))
        prev = d
    flush_para(); flush_quote()
    print('missing numbers:', missing, '| misprinted:', misprints)
    return sections, expect


HEAD_MAX = 80


def finish(k, sections, expect):
    cfg = KANDAMS[k]
    out_dir = ROOT / 'content' / str(k)
    out_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    built = []
    for sec in sections:
        items_out = []
        poems = [it['ref'] for it in sec['items']]
        for i, p in enumerate(poems):
            holder = poems[i - 1]['paras'] if i > 0 else sec['intro']
            moved = []
            while holder:
                last = holder[-1]
                if last['kind'] != 'p':
                    break
                plain = last['text'].replace('*', '').strip()
                words = plain.split()
                styled = last.get('head')
                limit_c, limit_w = (HEAD_MAX, 12) if styled else (48, 6)
                looks = (len(plain) <= limit_c and len(words) <= limit_w and ' - ' not in plain and ';' not in plain
                         and plain.count('.') <= (1 if plain.endswith('.') else 0) and not re.fullmatch(r'[\d.\s()]+', plain))
                if looks:
                    moved.insert(0, re.sub(r'^\d+\s+', '', plain.replace(' ◌', '').replace('◌', '')).rstrip('.').strip())
                    holder.pop()
                    continue
                break
            if moved and holder and holder[-1]['kind'] == 'p':
                holder[-1]['text'] = re.sub(r'\s+\(?\d{1,3}\)?\.?$', '', holder[-1]['text'])
            # a heading broken over two 16 pt lines comes out as two pieces: join them
            joined = []
            for h in moved:
                if joined and not METER_RE.search(h) and not METER_RE.search(joined[-1]) and len(joined[-1]) + len(h) < HEAD_MAX and \
                        not joined[-1].endswith(('.', ':')):
                    joined[-1] = joined[-1] + ' ' + h
                else:
                    joined.append(h)
            for h in joined:
                items_out.append({'type': 'metre' if METER_RE.search(h) else 'heading', 'text': h})
            items_out.append({'type': 'poem', 'ref': p})
        sec['items'] = items_out
        for it in sec['items']:
            if it['type'] != 'poem':
                continue
            p = it['ref']
            paras = p['paras']
            pad, notes = '', []
            # a short "(அனுமன்)" line saying who speaks may stand before the பதவுரை: keep it at its head
            lead = ''
            if len(paras) > 1 and paras[0]['kind'] == 'p' and re.fullmatch(r'\(?[^()]{1,60}\)?', paras[0]['text'].replace('*', '').strip()) \
                    and paras[0]['text'].replace('*', '').strip().startswith('('):
                lead = paras[0]['text'].replace('*', '').strip() + ' '
                paras = paras[1:]
            if paras and paras[0]['kind'] == 'p' and ('**' in paras[0]['text'] or ' - ' in paras[0]['text'] or ' -' in paras[0]['text']):
                pad = lead + paras[0]['text']
                rest = paras[1:]
            else:
                rest = ([{'kind': 'p', 'text': lead.strip()}] if lead else []) + paras
            for q in rest:
                if q['kind'] == 'p':
                    txt = re.sub(r'(?<=[.!?’”)])\s*\(?\d{1,3}\)?\s*$', '', q['text'])   # stray note number at the end
                    if re.fullmatch(r'\s*\(?\d+\)?\.?\s*', txt.replace('*', '')):
                        continue
                    notes.append({'p': fix_prose_punct(txt)})
                else:
                    notes.append({'q': q['lines']})
            pad = re.sub(r'(?<=[.!?’”;)])\s*\(?\d{1,3}\)?\s*$', '', pad)
            plines = [x for x in p['lines'] if x]
            for a, b in FIXES.get(p['n'], []):
                plines = [x.replace(a, b) for x in plines]
            it.update({'n': p['n'], 'lines': LINE_FIXES.get(p['n']) or fix_poem_punct(plines),
                       'pad': fix_prose_punct(pad), 'notes': notes, 'page': p['page']})
            del it['ref']
            total += 1
        sec['intro'] = [({'p': fix_prose_punct(q['text'])} if q['kind'] == 'p' else {'q': q['lines']}) for q in sec['intro']]
        built.append(sec)
    # the கடவுள் வாழ்த்து goes at the head of padalam 1
    if built and norm(built[0]['title']) == norm('கடவுள் வாழ்த்து'):
        inv = built.pop(0)
        head = [{'type': 'heading', 'text': 'கடவுள் வாழ்த்து'}]
        rest = [it for it in inv['items'] if not (it['type'] == 'heading' and it['text'] == 'கடவுள் வாழ்த்து')]
        built[0]['items'] = head + rest + built[0]['items']
        built[0]['intro'] = inv['intro'] + built[0]['intro']
    for i, sec in enumerate(built, start=1):
        sec['id'] = i
        ns = [it['n'] for it in sec['items'] if it['type'] == 'poem']
        sec['from'], sec['to'] = (ns[0], ns[-1]) if ns else (0, 0)
        (out_dir / f'{i:02d}.src.json').write_text(json.dumps(sec, ensure_ascii=False, indent=1), encoding='utf-8')
        nh = sum(1 for it in sec['items'] if it['type'] == 'heading')
        print(f"{i:2d} {sec['title']:30s} poems {sec['from']:5d}-{sec['to']:5d} ({len(ns):4d})  headings {nh:3d}  intro {len(sec['intro'])}")
    print(f'kandam {k}: {total} poems, numbers {cfg["first"]}-{expect - 1} (expected up to {cfg["last"]})')


if __name__ == '__main__':
    kk = int(sys.argv[1])
    secs, exp = parse(kk)
    finish(kk, secs, exp)
