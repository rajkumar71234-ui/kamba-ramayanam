# கம்ப ராமாயணம் — Kamba Ramayanam (Tamil)

A free reading site for Kamban's **இராமாவதாரம்**, padalam by padalam:

- a Tamil story summary (கதைச் சுருக்கம்) for every padalam,
- every poem, with its விளக்கம் (the commentary) right under it, and the word-by-word meaning (பதவுரை) folded away
  below that — tap “பதவுரை” to open it. Verses the commentator quotes from other works are marked “மேற்கோள்”,
- sub-headings and metre names as in the source edition,
- simple cartoon-style pictures: one for every padalam, one for every scene in the opening padalams,
  and a small picture beside every one of the 1,312 poems,
- read-aloud using the phone's own Tamil voice: tap a poem (or its ▶ கேட்க button) and it reads the poem and its
  விளக்கம் (its பதவுரை when a poem has no விளக்கம்), then carries on to the next poems; previous / pause / next / stop
  in the player bar,
- a bar that stays at the top while reading, with the breadcrumb and the reading settings:
  speed (வேகம்), pitch (சுருதி) and text size. The settings are remembered on the device.

Now ready: **பால காண்டம்** — பாயிரம் + 23 படலங்கள், 1,312 poems.
The extra verses (மிகைப் பாடல்கள்) printed after the kandam are not included yet.

Live site: https://rajkumar71234-ui.github.io/kamba-ramayanam/

Sister site: [வால்மீகி ராமாயணம்](https://rajkumar71234-ui.github.io/valmiki-ramayanam/) (same layout).

## How the site is organised

| Path | What it is |
|---|---|
| `index.html` | The one page (home, kandam list, padalam pages are drawn by `assets/app.js`) |
| `assets/` | Styles, script, logo |
| `data/kandams.json` | The six kandams and the padalams that are ready |
| `data/1/<pp>.json` | One file per padalam (00 = பாயிரம், 01 = ஆற்றுப் படலம் … 23 = பரசுராமப் படலம்) |
| `img/1/<pp>/` | Pictures for that padalam (SVG): `chapter.svg`, `scene-*.svg`, and `p<n>.svg` beside poem n |
| `content/1/<pp>.src.json` | Poems, பதவுரை, விளக்கம், sub-headings — taken from the source PDF |
| `content/1/<pp>.ta.json` | Story summary, picture captions and scene list — written for this site |
| `content/1/pics.json` | The small picture for each poem and its Tamil alt text (made by `tools/thumbs.py`) |
| `content/site.json` | Site title and the six kandams |
| `tools/` | The PDF decoder, build script and drawing kit |

Links: `#bala` (padalam list), `#bala-10` (a padalam), `#bala-10-p514` or `#bala-p514` (poem 514).

## Rebuilding from the PDF

The source PDF itself is not kept in this repository.

The source PDF was exported from Word with a broken font map (copy-paste gives garbled Tamil:
ை comes out as க, ெ as ப, and so on). The tools rebuild the real text from the fonts themselves:

```
pip install pymupdf fonttools
python3 tools/fontmap.py   book.pdf     # which glyph is which letter  -> work/g2u.json
python3 tools/decode_pdf.py book.pdf    # Unicode Tamil, line by line  -> work/lines.jsonl
python3 tools/parse_pdf.py              # poems, meanings, notes       -> content/1/*.src.json
python3 tools/art_bala.py               # padalam and scene pictures   -> img/1/*/
python3 tools/thumbs.py 1               # a picture beside every poem  -> img/1/*/p<n>.svg, content/1/pics.json
python3 tools/build_site.py             # site data                    -> data/
python3 tools/bump_assets.py            # after changing assets/
```

`parse_pdf.py` also: turns the source's stray full stops inside poems back into commas (the printed
book has commas there), removes stray note numbers and `*` marks, and fixes a few obvious typos
(listed in `FIXES`).

`thumbs.py` picks each poem's picture from its own words and its பதவுரை (`poem_subjects.py` lists the Tamil word
patterns: people, animals, things, places, time of day, moods). It draws up to two figures, the setting and small
details in the same cartoon style as the padalam pictures. A few well-known poems have a hand-made picture
(`OVERRIDE` in `thumbs.py`).

## Credits

- Poems, பதவுரை and விளக்கம்: from the annotated Bala Kandam edition in the source PDF; poem numbers follow it.
- Story summaries and pictures: written and drawn fresh for this site. Found a mistake? Use the “பிழை தெரிவிக்க” link under any poem.
