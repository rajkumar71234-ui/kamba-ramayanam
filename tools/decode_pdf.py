"""Step 2 — decode the PDF into correct Unicode Tamil, line by line, keeping bold runs.

Usage (from the repo root):  python3 tools/decode_pdf.py <book.pdf>
Writes work/lines.jsonl (run tools/fontmap.py first).

Why: the PDF was made by Word 2016; its ToUnicode tables map many Tamil glyphs wrongly
(for example the ை sign comes out as க). We use the embedded Vijaya font's own cmap + GSUB
tables (kamba/fonts/g2u.json, made by fontmap.py) and put the prefix vowel signs (ெ ே ை)
back after their consonant.

Output: one JSON object per line: page, y, x0, size, runs [[text, bold], ...]
"""
import pymupdf as fitz, json, re, sys
from pathlib import Path

PDF = sys.argv[1] if len(sys.argv) > 1 else 'book.pdf'
ROOT = Path(__file__).resolve().parent.parent
G2U = json.load(open(ROOT / 'work' / 'g2u.json', encoding='utf-8'))
PRE = {'ெ', 'ே', 'ை'}
CONS = set(chr(c) for c in range(0x0B95, 0x0BBA))
TO_O = {'ெ': 'ொ', 'ே': 'ோ'}


def glyph_text(font, gid, pdf_u):
    m = G2U.get(font)
    s = m.get(str(gid)) if m else None
    return s if s is not None else pdf_u


def reorder(units, flags):
    """Visual glyph order -> logical Unicode. Returns list of (text, flag)."""
    out = []
    i, n = 0, len(units)
    while i < n:
        u = units[i]
        if u in PRE and i + 1 < n and units[i + 1] and units[i + 1][0] in CONS:
            base, fl = units[i + 1], flags[i + 1]
            k = i + 2
            vs = u
            if base.endswith('ா') and len(base) >= 2 and base[-2] in CONS and u in TO_O:
                base, vs = base[:-1], TO_O[u]           # ணா னா றா ligature glyphs
            elif k < n and units[k] == 'ா' and u in TO_O:
                vs, k = TO_O[u], k + 1
            elif k < n and units[k] == 'ௗ' and u == 'ெ':
                vs, k = 'ௌ', k + 1
            out.append((base + vs, fl))
            i = k
            continue
        out.append((u, flags[i]))
        i += 1
    return out


def page_lines(page, pno):
    lines, cur = [], None
    for span in page.get_texttrace():
        font = span['font']
        bold = 'Bold' in font
        size = round(span['size'], 1)
        units, org = [], []
        for ch in span['chars']:
            u, gid, origin = ch[0], ch[1], ch[2]
            if gid is None or gid < 0:
                continue
            units.append(glyph_text(font, gid, chr(u)))
            org.append(origin)
        if not units:
            continue
        y = round(org[0][1], 1)
        if cur and abs(cur['y'] - y) < 2.0:
            cur['units'] += units
            cur['flags'] += [bold] * len(units)
            cur['sizes'].add(size)
        else:
            cur = {'page': pno + 1, 'y': y, 'x0': round(org[0][0], 1), 'units': units,
                   'flags': [bold] * len(units), 'sizes': {size}}
            lines.append(cur)
    res = []
    for ln in lines:
        pairs = reorder(ln['units'], ln['flags'])
        runs = []
        for t, b in pairs:
            if runs and runs[-1][1] == b:
                runs[-1][0] += t
            else:
                runs.append([t, b])
        text = ''.join(t for t, b in runs)
        if not text.strip():
            continue
        nb = sum(len(t) for t, b in runs if b and t.strip())
        nt = sum(len(t) for t, b in runs if t.strip()) or 1
        res.append({'page': ln['page'], 'y': ln['y'], 'x0': ln['x0'], 'size': max(ln['sizes']),
                    'bold': round(nb / nt, 2), 'runs': runs})
    return res


if __name__ == '__main__':
    doc = fitz.open(PDF)
    with open(ROOT / 'work' / 'lines.jsonl', 'w', encoding='utf-8') as out:
        for pno in range(len(doc)):
            for ln in page_lines(doc[pno], pno):
                out.write(json.dumps(ln, ensure_ascii=False) + '\n')
