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
from parse_pdf import (line_text, runs_markup, tidy_markup, METER_RE)


# பால காண்டம்'s PDF prints '.' where the book has ',' and parse_pdf.py puts the commas back. These PDFs have the
# book's own punctuation, so it is kept exactly as printed.
def fix_poem_punct(lines):
    return lines


def fix_prose_punct(s):
    return s

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


# ------------------------------------------------------------------ sub-headings and metre names before a poem
TAMIL = re.compile(r'[஀-௿]')
# a metre name at the end of a line: "கலிவிருத்தம்", "அறுசீர் ஆசிரிய விருத்தம்", "கலிநிலைத் துறை", "கொச்சகக் கலிப்பா" …
METRE_TAIL = re.compile(
    r'(?:\(\s*\d{1,3}\s*\)\s*|\d{1,3}\s*)?'
    r'((?:\(வேறு\)\s*)?'
    r'(?:(?:அறு|எழு|எண்|ஐ|நால்|பதின்|பன்னிரு|பதினான்கு)சீர்(?:க்|ச்)?\s*(?:கழிநெடிலடி\s*)?)?'
    r'(?:ஆசிரிய(?:ச்)?\s*)?(?:சந்த(?:க்)?\s*)?'
    r'(?:(?:கலி(?:நிலைத்?|த்)?|வஞ்சி(?:த்)?|கொச்சகக்?|கட்டளைக்?|முடுகு|நேரிசை|இன்னிசை|தரவு)\s*)*'
    r'(?:விருத்தம்|துறை|கலிப்பா|தாழிசை|வெண்பா|கலி)'
    r'(?:\s*\(\s*வேறு[^()]{0,12}\)|\s+வேறு(?:\s*வகை)?)?)\s*$')
# a metre name first, then a sub-heading: "கலி விருத்தம் (வேறு வகை) இராமன் அம்பு மதில் அமைத்தல்"
METRE_HEAD = re.compile(METRE_TAIL.pattern[:-len(r'\s*$')] + r'\s+(\S.*)$')
# "(வேறு)", "வேறு", "(வேறு வகை)": the metre changes (its name is not printed)
VERU_RE = re.compile(r'^\(?\s*வேறு(?:\s*வகை)?\s*\)?$')
# the last word of a sentence in the notes, not of a sub-heading
SENT_END = re.compile(r'(?:உளது|உள்ளது|என்பர்|என்க|ஆகும்|என்றார்|என்றான்|என்றாள்|எனப்பட்டது|பட்டது|படுகிறது|பட்டுள்ளது|தக்கது|'
                      r'காணலாம்|கூறினார்|குறிப்பு|அறிக|உணர்க|காண்க|கொள்க|போலும்|இல்லை|உண்டு|பொருந்தும்|வேண்டும்|அன்று|'
                      r'ஆயிற்று|என்பது|என்னும்|எனலாம்|ஆகலாம்|கூறுவர்|என்ப|பெற்றது|பெற்றன|பெறும்)$')
NOTE_WORDS = re.compile(r'(?:^|\s)(?:உம்மை|ஈற்றசை|அசைநிலை|அசை|அணி|என்பதில்|பாடலில்|இப்பாடலில்|இதில்|ஈண்டு|எனவே)(?:\s|$)')
METRE_OK = re.compile(r'சீர்|ஆசிரிய|சந்த|கலி|வஞ்சி|கொச்சக|கட்டளை|வெண்பா|தாழிசை')
HEAD_TERM = ('.', '?', '!', ',', ';', ':', '’', '”', ')', "'", '"', '-', '–')


def split_metre(text):
    """(text before, metre name) when the text ends with the name of a metre, else (text, None)."""
    plain = text.replace('*', '').rstrip()
    m = METRE_TAIL.search(plain)
    if not m or not METRE_OK.search(m.group(1)) or (re.search(r'கலி(?:\s*\(.*\)|\s+வேறு.*)?$', m.group(1)) and 'கொச்சக' not in m.group(1)
                                                   and not re.search(r'(விருத்தம்|துறை|கலிப்பா)', m.group(1))):
        return text, None
    if m.start() > 0 and TAMIL.match(plain[m.start() - 1]):
        return text, None                     # the match starts inside a word
    return plain[:m.start()].rstrip(), re.sub(r'\s+', ' ', m.group(1)).strip()


def heading_like(t, min_words=2, max_words=12):
    """(ok, cleaned) — could this short text be a sub-heading such as "இராமன் சீதைக்குச் சித்திரகூடத்தைக் காட்டுதல்"?"""
    t = re.sub(r'\s+', ' ', re.sub(r'^\(?\d{1,3}\)?\s+', '', t.replace('*', '').replace('◌', '').strip())).strip()
    w = t.split()
    ok = (bool(t) and len(t) <= 80 and min_words <= len(w) <= max_words and not t.endswith(HEAD_TERM) and
          ' - ' not in t and ';' not in t and ':' not in t and not re.search(r'\d', t) and bool(TAMIL.search(t))
          and not SENT_END.search(t) and not NOTE_WORDS.search(t))
    return ok, t


BREAK_RE = re.compile(r'\s{4,}|\(\d{1,3}\)\s*|(?:^|(?<=\s))\d{1,3}\s+|(?<=[.!?])(?![’\'”"?!.])\s*')


def last_break(raw):
    """(text before, text after, strong) for the last break inside a printed line — a wide gap, a note number
    "(51)" or "84", or the end of a sentence. strong is False for a plain sentence end; (None…) when there is none."""
    s = raw.rstrip()
    best = None
    for m in BREAK_RE.finditer(s):
        if m.end() < len(s) and (m.end() > m.start() or m.start() > 0):
            best = m
    if best is None:
        return None, s.strip(), None
    g = best.group(0)
    strong = len(g) >= 4 and not g.strip() or bool(re.search(r'\d', g)) or (best.start() == 0 and len(g) >= 4) or g.startswith('  ')
    return s[:best.start()].strip(), s[best.end():].strip(), strong


def raw_text(d):
    return ''.join(t for t, b in d['runs']).replace(' ◌', '').replace('◌', '')


def find_heads(L, starts):
    """Sub-headings and metre names printed in 14 pt just above a poem. Left alone they would end up in the
    notes of the poem before (or the padalam's introduction). Returns {line index: [(kind, text), ...]} with
    kind 'text' (stays in the notes), 'head' or 'metre'."""
    out = {}

    def nonempty_before(i):
        j = i - 1
        while j >= 0 and not line_text(L[j]):
            j -= 1
        return j

    def gap_ok(j, nxt):
        a, b = L[j], L[nxt]
        return b['page'] != a['page'] or b['y'] - a['y'] >= 20

    def try_heading(j, nxt):
        """Mark line j (just above line nxt) as a heading if it looks like one; True if marked."""
        d = L[j]
        if d['size'] >= 15 or not gap_ok(j, nxt):
            return False
        raw = raw_text(d)
        pre, tail, strong = last_break(raw)
        p = nonempty_before(j)
        above = L[p] if p >= 0 else None
        gap_above = above is None or above['page'] != d['page'] or d['y'] - above['y'] >= 20
        indented = len(raw) - len(raw.lstrip(' ')) >= 4
        prev_num = above is not None and re.search(r'(?:^|\s)\(?\d{1,3}\)?\s*$', line_text(above)) is not None
        ok, head = heading_like(tail)
        # a heading wrapped over two lines: "… கூறப்பெறுவன. தயரதன் மந்திராலோசனை" / "மண்டபத்தை அடைதல்"
        if above is not None and above['page'] == d['page'] and d['y'] - above['y'] < 20 and strong is None:
            ok_short, short = heading_like(line_text(d), min_words=1, max_words=6)
            a_pre, a_tail, a_strong = last_break(raw_text(above))
            if ok_short and a_strong is not None and (a_strong or d['x0'] >= 120):
                ok2, both = heading_like(a_tail + ' ' + short)
                ok_t, _ = heading_like(a_tail, min_words=1)
                if ok2 and ok_t:
                    out[p] = [('text', a_pre), ('head', both)]
                    out[j] = []
                    return True
        if not ok:
            return False
        if strong or (strong is None and (d['x0'] >= 80 or indented or gap_above or prev_num)) or \
                (strong is False and gap_above):
            out[j] = ([('text', pre)] if pre else []) + [('head', head)]
            return True
        return False

    for i in sorted(starts):
        j = nonempty_before(i)
        if j < 0 or L[j]['size'] >= 15:
            continue
        pre, metre = split_metre(raw_text(L[j]))
        if metre:
            segs = []
            if pre.strip():
                b_pre, b_tail, b_strong = last_break(pre)
                ok, head = heading_like(b_tail)
                if ok and b_strong is not False:
                    segs = ([('text', b_pre)] if b_pre else []) + [('head', head)]
                else:
                    segs = [('text', pre.strip())]
            out[j] = segs + [('metre', metre)]
            if not pre.strip():
                k = nonempty_before(j)
                if k >= 0:
                    try_heading(k, j)
        else:
            try_heading(j, i)
    return out


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
    overrides = find_heads(L, starts_at)
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
        if idx in overrides:
            # a line holding a sub-heading or a metre name (perhaps after the last words of a note)
            for kind, txt in overrides[idx]:
                txt = re.sub(r'\s+', ' ', txt).strip()
                if not txt:
                    continue
                flush_quote()
                if kind == 'text':      # the end of the paragraph above: it goes on in the same paragraph
                    if (para is None or para.get('head') or para['sec'] != s or
                            (prev is not None and prev['page'] == d['page'] and d['y'] - prev['y'] > 20)):
                        flush_para()
                        para = {'sec': s, 'poem': owner, 'parts': []}
                    para['parts'].append(txt)
                else:
                    flush_para()
                    para = {'sec': s, 'poem': owner, 'parts': [txt], 'head': True}
                    flush_para()
            prev = d
            continue
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
                if looks and not split_metre(plain)[1] and not VERU_RE.match(plain):
                    bare = re.sub(r'^\(?\d{1,3}\)?\s*', '', plain).rstrip('.').strip()
                    looks = not (SENT_END.search(bare) or NOTE_WORDS.search(bare) or re.search(r'\d', bare))
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
                if joined and not split_metre(h)[1] and not split_metre(joined[-1])[1] and len(joined[-1]) + len(h) < HEAD_MAX and \
                        not joined[-1].endswith(('.', ':')):
                    joined[-1] = joined[-1] + ' ' + h
                else:
                    joined.append(h)
            for h in joined:
                head, metre = split_metre(h)
                head = re.sub(r'^\(?\d{1,3}\)?\s*', '', head.replace('*', '')).strip()
                mh = METRE_HEAD.match(head) if head else None
                if mh and METRE_OK.search(mh.group(1)) and not split_metre(mh.group(1))[0].strip():
                    head, metre = mh.group(2).strip(), re.sub(r'\s+', ' ', mh.group(1)).strip()
                if head and VERU_RE.match(head):
                    head, metre = '', head
                if head and metre and not heading_like(head, min_words=1)[0] and holder is not sec['intro']:
                    holder.append({'kind': 'p', 'text': head})     # the end of a note, not a heading
                    head = ''
                if head:
                    items_out.append({'type': 'metre' if METER_RE.search(head) else 'heading', 'text': head})
                if metre:
                    items_out.append({'type': 'metre', 'text': metre})
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
        # the padalam's title broken over two lines comes out as a "quote" in the introduction: drop it
        sec['intro'] = [q for q in sec['intro'] if not (q['kind'] == 'q' and (
            norm(' '.join(q['lines'])) == norm(sec['title']) or not TAMIL.search(' '.join(q['lines']))))]
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
