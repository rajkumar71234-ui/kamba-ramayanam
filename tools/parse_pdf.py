"""Turn the decoded PDF lines (see decode_pdf.py) into one content file per padalam.

Reads   work/lines.jsonl
Writes  content/1/<pp>.src.json   (poems, word meanings, notes, sub-headings, metre names)

Layout of the source PDF (Word 2016 export):
  * padalam titles: 18-20 pt, centred
  * poems: 16 pt bold, first line "N. ..." at x=108, other lines at x=144
  * word meanings (பதவுரை): 14 pt paragraph right after the poem, poem words in bold
  * notes (விளக்கம்): following 14 pt paragraphs; quoted verses inside them are 16 pt
  * sub-headings / metre names: short 14 pt lines just before a poem
The source uses '.' where the printed book has ',' — fixed here (see fix_poem_punct / fix_prose_punct).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINES = ROOT / 'work' / 'lines.jsonl'
LAST_PAGE = 840            # 'பாலகாண்டம் நிறைந்தது'; the மிகைப் பாடல்கள் after it are not included yet

SECTIONS = [  # (start page, title) — பாயிரம் is section 0
    (3, 'பாயிரம்'), (14, 'ஆற்றுப் படலம்'), (29, 'நாட்டுப் படலம்'), (67, 'நகரப் படலம்'),
    (114, 'அரசியற் படலம்'), (121, 'திரு அவதாரப் படலம்'), (201, 'கையடைப் படலம்'),
    (218, 'தாடகை வதைப் படலம்'), (251, 'வேள்விப் படலம்'), (285, 'அகலிகைப் படலம்'),
    (307, 'மிதிலைக் காட்சிப் படலம்'), (400, 'குலமுறை கிளத்து படலம்'), (421, 'கார்முகப் படலம்'),
    (460, 'எழுச்சிப் படலம்'), (504, 'சந்திரசயிலப் படலம்'), (524, 'வரைக் காட்சிப் படலம்'),
    (552, 'பூக்கொய் படலம்'), (584, 'நீர் விளையாட்டுப் படலம்'), (606, 'உண்டாட்டுப் படலம்'),
    (644, 'எதிர்கொள் படலம்'), (668, 'உலாவியற் படலம்'), (702, 'கோலம் காண் படலம்'),
    (737, 'கடிமணப் படலம்'), (803, 'பரசுராமப் படலம்'),
]
NOT_HEADINGS = {  # short note lines that only look like sub-headings
    'கணை + கண்ணை: தொகுத்தல் விகாரம்', 'தன்மை நவிற்சியணி', 'உலகளித்தல்: பரிபாலித்தல் மன்: பெருமை',
    'வள்ளல்: அகலிகைக்கு அருள் செய்தமை கருதியது', 'முனிவன் முன்னிய',
}


def clean_heading(h):
    h = h.replace(' ◌', '').replace('◌', '')
    h = re.sub(r'^\d+\s+', '', h).rstrip('.').strip()
    h = h.replace('சனகன் எதிர்கௌ வருதல்', 'சனகன் எதிர்கொள வருதல்').replace('மிதிலையில யாவரும்', 'மிதிலையில் யாவரும்')
    h = h.replace('விளங்கி காட்சி', 'விளங்கிய காட்சி')
    return h


METER_RE = re.compile(r'(விருத்தம்|கலித்துறை|தாழிசை|வெண்பா|சந்த[ம்]?)\s*$')
TA = r'஀-௿'


def line_text(d):
    return re.sub(r'\s+', ' ', ''.join(t for t, b in d['runs']).replace(' ◌', '').replace('◌', '')).strip()


def runs_markup(runs):
    """[[text, bold], ...] -> 'plain **bold** plain' (markers wrap trimmed bold text)."""
    out = []
    for t, b in runs:
        if b and t.strip():
            lead = t[:len(t) - len(t.lstrip())]
            trail = t[len(t.rstrip()):]
            out.append(lead + '**' + t.strip() + '**' + trail)
        else:
            out.append(t)
    s = ''.join(out).replace(' ◌', '').replace('◌', '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def tidy_markup(s):
    s = re.sub(r'\*\*\s*\*\*', ' ', s)          # **a** **b** -> **a b**
    s = re.sub(r'\*\*(\s*[-–:;,.]\s*)\*\*', r'\1', s)
    s = re.sub(r'\*\*\s+', '** ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # drop bold that wraps nothing but punctuation
    s = re.sub(r'\*\*([\s\-–:;,.!?‘’“”()]*)\*\*', r'\1', s)
    return s


FIXES = {  # obvious typos in the source PDF, corrected here (poem number: (wrong, right))
    514: ('நோன்கினாள்', 'நோக்கினாள்'),
}
LINE_FIXES = {  # poems whose line breaks are misplaced in the source PDF
    699: ['தடுத்து இமையாமல் இருந்தவர், தாளில்', 'மடுத்ததும், நாண் நுதி வைத்ததும், நோக்கார்;',
          'கடுப்பினில் யாரும் அறிந்திலர்; கையால்', 'எடுத்தது கண்டனர்; இற்றது கேட்டார்.'],
}


def fix_poem_punct(lines):
    """Inside a poem every '.' except the very last one was a comma in the printed book."""
    if lines:
        last = re.sub(r'\s*\*+\s*$', '', lines[-1])          # '*' = see the extra verses (மிகைப் பாடல்கள்), not shown yet
        last = re.sub(r'[\s.,]+\d{1,3}\s*$', '.', last)       # stray note number at the end
        lines = lines[:-1] + [last]
    out = []
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1
        if last:   # keep the final full stop, even when quote marks follow it ("கண்டேன்.’")
            m = re.search(r'\.([\s’‘“”"\'!?)]*)$', ln)
            if m:
                body, end = ln[:m.start()], '.' + m.group(1)
            else:
                body, end = ln, ''
            ln = body.replace('.', ',') + end
        else:
            ln = ln.replace('.', ',')
        ln = re.sub(r',(?=\S)', ', ', ln)
        ln = re.sub(r'\s+,', ',', ln)
        out.append(ln.strip())
    return out


def fix_prose_punct(s):
    """Short list items 'அ. ஆ. இ' were 'அ, ஆ, இ'. Convert only clear cases."""
    res = []
    depth = 0
    seg_start = 0
    i = 0
    plain = s
    chars = list(plain)
    last_break = 0
    for i, ch in enumerate(chars):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth = max(0, depth - 1)
        if ch in ';:!?—–-(' or (ch == ',' ):
            last_break = i + 1
            continue
        if ch == '.' and depth == 0:
            nxt = plain[i + 1:i + 3]
            if i + 1 >= len(plain) or not nxt.startswith(' '):
                last_break = i + 1
                continue
            after = plain[i + 2:i + 3]
            seg = plain[last_break:i].replace('*', '').strip()
            words = seg.split()
            if (after and re.match(f'[{TA}]', after) and 0 < len(words) <= 2
                    and all(len(re.sub(f'[^{TA}]', '', w)) >= 4 for w in words)
                    and not re.search(r'\d', seg)):
                chars[i] = ','
            last_break = i + 1
    return ''.join(chars)


def is_poem_start(d, expect):
    t = line_text(d)
    m = re.match(r'^(?:\d+\s+)?(\d+)\s*(?:\.\s*|\s+)(.*)$', t)
    if not m or int(m.group(1)) != expect:
        return None
    if d['size'] >= 15 or d['bold'] >= 0.8:
        return m
    return None


def main():
    L = [json.loads(l) for l in open(LINES)]
    L = [d for d in L if 3 <= d['page'] <= LAST_PAGE]
    # drop the section title lines themselves and the closing line
    sec_of_page = []
    starts = [p for p, t in SECTIONS]

    def section_index(page):
        k = 0
        for i, p in enumerate(starts):
            if page >= p:
                k = i
        return k

    expect = 1
    sections = [{'id': i, 'title': t, 'start_page': p, 'items': [], 'intro': []} for i, (p, t) in enumerate(SECTIONS)]
    cur_poem = None
    para = None          # current prose paragraph being collected: {'kind','runs_text','x0','y','page'}
    quote = None
    prev = None

    def flush_para():
        nonlocal para
        if para is None:
            return
        sec = sections[para['sec']]
        text = tidy_markup(' '.join(para['parts']))
        para_obj = {'kind': 'p', 'text': text}
        target_poem = para['poem']
        if target_poem is None:
            sec['intro'].append(para_obj)
        else:
            target_poem['paras'].append(para_obj)
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

    big_prose = False
    for idx, d in enumerate(L):
        s = section_index(d['page'])
        t = line_text(d)
        if d['size'] >= 18:          # section titles
            flush_para(); flush_quote()
            prev = d
            continue
        if t in ('பாலகாண்டம் நிறைந்தது',):
            continue
        big = d['size'] >= 15
        m = is_poem_start(d, expect)
        if not m and big:
            # a poem number in the middle of a line ("… அளிப்பது.    573.  ‘’அறு")
            mm = re.search(r'(^|\s)' + str(expect) + r'\s*\.\s+(\S.*)$', t)
            if mm and mm.start() > 0:
                pre = t[:mm.start()].strip()
                if pre and para is not None:
                    para['parts'].append(pre)
                m = mm
                class _M:
                    def __init__(self, g): self.g = g
                    def group(self, i): return self.g
                m = _M(mm.group(2))
        if m:
            flush_para(); flush_quote()
            big_prose = False
            cur_poem = {'n': expect, 'sec': s, 'lines': [m.group(2).strip()], 'paras': [], 'page': d['page'],
                        'in_poem': True}
            sections[s]['items'].append({'type': 'poem', 'ref': cur_poem})
            expect += 1
            prev = d
            continue
        if cur_poem and cur_poem.get('in_poem') and big and (
                (prev is not None and prev['page'] == d['page'] and d['y'] - prev['y'] < 25) or
                (prev is not None and prev['page'] != d['page'] and (d['x0'] > 120 or len(cur_poem['lines']) < 4))):
            raw = ''.join(x for x, b in d['runs'])
            lead = len(raw) - len(raw.lstrip(' '))
            if lead >= 12 and len(t) <= 16 and cur_poem['lines']:
                cur_poem['lines'][-1] = cur_poem['lines'][-1].rstrip() + ' ' + t   # wrapped tail of a long line
            else:
                cur_poem['lines'].append(t)
            prev = d
            continue
        if cur_poem:
            cur_poem['in_poem'] = False
        owner = cur_poem if (cur_poem and cur_poem['sec'] == s) else None
        if big and not big_prose and len(t) < 46 and ' - ' not in t:
            flush_para()            # quoted verse inside the notes
            if quote is None:
                quote = {'sec': s, 'poem': owner, 'lines': []}
            quote['lines'].append(t)
            prev = d
            continue
        flush_quote()
        if big:
            new_para = not big_prose or para is None
            big_prose = True
        else:
            big_prose = False
            new_para = (para is None or d['x0'] > 75 or
                        (prev is not None and prev['page'] == d['page'] and d['y'] - prev['y'] > 20) or
                        para['sec'] != s)
        if new_para:
            flush_para()
            para = {'sec': s, 'poem': owner, 'parts': [], 'first': d, 'nlines': 0}
        para['parts'].append(runs_markup(d['runs']))
        para['nlines'] += 1
        para['last'] = d
        prev = d
    flush_para(); flush_quote()

    # ---- post-process: split each poem's paragraphs into பதவுரை / notes; detect headings & metres
    total = 0
    for sec in sections:
        items_out = []
        pending = []      # headings/metres that belong before the next poem
        poems = [it['ref'] for it in sec['items']]
        # sub-headings: the last short paragraph(s) of the previous poem's notes (or of the intro)
        for k, p in enumerate(poems):
            # look at the previous holder of paragraphs
            holder = poems[k - 1]['paras'] if k > 0 else sec['intro']
            moved = []
            while holder:
                last = holder[-1]
                if last['kind'] != 'p':
                    break
                plain = last['text'].replace('*', '').strip()
                words = plain.split()
                looks_heading = (len(plain) <= 48 and len(words) <= 6 and ' - ' not in plain and ';' not in plain.rstrip(';')
                                 and plain.count('.') <= (1 if plain.endswith('.') else 0) and not re.fullmatch(r'[\d.\s]+', plain))
                if looks_heading and clean_heading(plain) not in NOT_HEADINGS:
                    moved.insert(0, clean_heading(plain))
                    holder.pop()
                    continue
                break
            # strip a stray trailing number left at the end of the preceding paragraph ("… கருத்து. 8")
            if moved and holder and holder[-1]['kind'] == 'p':
                holder[-1]['text'] = re.sub(r'\s+\d+\.?$', '', holder[-1]['text'])
            for h in moved:
                if METER_RE.search(h):
                    items_out.append({'type': 'metre', 'text': h})
                else:
                    items_out.append({'type': 'heading', 'text': h})
            items_out.append({'type': 'poem', 'ref': p})
        sec['items'] = items_out
        for it in sec['items']:
            if it['type'] != 'poem':
                continue
            p = it['ref']
            paras = p['paras']
            pad, notes = '', []
            if paras and paras[0]['kind'] == 'p' and ('**' in paras[0]['text'] or ' - ' in paras[0]['text'] or ' -' in paras[0]['text']):
                pad = paras[0]['text']
                rest = paras[1:]
            else:
                rest = paras
            for q in rest:
                if q['kind'] == 'p':
                    txt = q['text']
                    if re.fullmatch(r'\s*\d+\.?\s*', txt.replace('*', '')):
                        continue
                    notes.append({'p': fix_prose_punct(txt)})
                else:
                    notes.append({'q': q['lines']})
            plines = [x for x in p['lines'] if x]
            if p['n'] in FIXES:
                a, b = FIXES[p['n']]
                plines = [x.replace(a, b) for x in plines]
            it.update({'n': p['n'], 'lines': LINE_FIXES.get(p['n']) or fix_poem_punct(plines),
                       'pad': fix_prose_punct(pad), 'notes': notes, 'page': p['page']})
            del it['ref']
            total += 1
        sec['intro'] = [({'p': fix_prose_punct(q['text'])} if q['kind'] == 'p' else {'q': q['lines']}) for q in sec['intro']]
        ns = [it['n'] for it in sec['items'] if it['type'] == 'poem']
        sec['from'], sec['to'] = (ns[0], ns[-1]) if ns else (0, 0)
        out = ROOT / 'content' / '1' / f"{sec['id']:02d}.src.json"
        out.write_text(json.dumps(sec, ensure_ascii=False, indent=1), encoding='utf-8')
        nh = sum(1 for it in sec['items'] if it['type'] == 'heading')
        print(f"{sec['id']:2d} {sec['title']:28s} poems {sec['from']:4d}-{sec['to']:4d} ({len(ns):3d})  headings {nh:3d}  intro {len(sec['intro'])}")
    print('total poems', total, 'last expected', expect - 1)


if __name__ == '__main__':
    main()
