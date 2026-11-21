"""Step 1 — work out what every Tamil glyph in the PDF really is.

The PDF was exported from Word 2016. Its ToUnicode tables are wrong for many Tamil glyphs
(for example the ை sign is labelled க), so normal copy/paste gives garbled Tamil.
The embedded Vijaya fonts still carry their own cmap and GSUB (ligature) tables, so the real
character(s) behind each glyph id can be recovered from the font itself.

Usage (from the repo root):  python3 tools/fontmap.py <book.pdf> [work dir, default work]
Writes <work dir>/g2u.json  {font name: {glyph id: text}}
Needs: pip install pymupdf fonttools
"""
import collections, io, json, sys
from pathlib import Path
import pymupdf as fitz
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
EXTRA = {86: 'ீ', 87: 'ு', 88: 'ூ'}   # ீ ு ூ: never used alone, so the subset cmap dropped them


def font_map(font):
    order = font.getGlyphOrder()
    gid_of = {g: i for i, g in enumerate(order)}
    g2u = {}
    for u, gname in font.getBestCmap().items():
        g2u.setdefault(gid_of[gname], chr(u))
    for g, s in EXTRA.items():
        g2u.setdefault(g, s)
    lookups = font['GSUB'].table.LookupList.Lookup
    for _ in range(6):
        for lk in lookups:
            for st in lk.SubTable:
                t = lk.LookupType
                if t == 7:
                    st = st.ExtSubTable; t = st.LookupType
                if t == 4:
                    for first, ligs in st.ligatures.items():
                        for lig in ligs:
                            comps = [first] + list(lig.Component)
                            if all(gid_of[c] in g2u for c in comps):
                                g2u.setdefault(gid_of[lig.LigGlyph], ''.join(g2u[gid_of[c]] for c in comps))
    return g2u


def main():
    doc = fitz.open(sys.argv[1])
    # which glyphs are used, and what the PDF claims they are (used only where the font has no answer)
    pdf_says = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for page in doc:
        for span in page.get_texttrace():
            seq = []
            for u, gid, *_ in span['chars']:
                if gid is None or gid < 0:
                    if seq: seq[-1][1] += chr(u)
                else:
                    seq.append([gid, chr(u)])
            for gid, s in seq:
                pdf_says[span['font']][gid][s] += 1
    # one embedded Type0 font file per font name is enough: the glyph numbering is the original font's
    files = {}
    for pno in range(len(doc)):
        for xref, ext, ftype, basefont, *_ in doc.get_page_fonts(pno, full=True):
            name = basefont.split('+', 1)[-1]
            if ftype == 'Type0' and name not in files:
                files[name] = xref
    out = {}
    for name, used in pdf_says.items():
        g2u = font_map(TTFont(io.BytesIO(doc.extract_font(files[name])[3]))) if name in files else {}
        final = {}
        for gid, claims in used.items():
            final[str(gid)] = g2u.get(gid) or max(claims, key=claims.get)
        out[name] = final
        fixed = sum(1 for g, c in used.items() if g in g2u and set(c) != {g2u[g]})
        print(f'{name}: {len(used)} glyphs used, {fixed} corrected from the font tables')
    wd = ROOT / (sys.argv[2] if len(sys.argv) > 2 else 'work')
    wd.mkdir(parents=True, exist_ok=True)
    (wd / 'g2u.json').write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding='utf-8')


if __name__ == '__main__':
    main()
