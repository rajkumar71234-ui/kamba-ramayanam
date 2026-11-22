# கம்ப ராமாயணம் — Kamba Ramayanam (Tamil)

A free reading site for Kamban's **இராமாவதாரம்**, padalam by padalam:

- a Tamil story summary (கதைச் சுருக்கம்) for every padalam,
- every poem, with its விளக்கம் (the commentary) right under it, and the word-by-word meaning (பதவுரை) folded away
  below that — tap “பதவுரை” to open it. Verses the commentator quotes from other works are marked “மேற்கோள்”,
- sub-headings and metre names as in the source edition,
- simple cartoon-style pictures: one for every padalam, one for every scene in பால காண்டம்'s padalams,
  and a small picture beside every poem,
- read-aloud using the phone's own Tamil voice: tap a poem (or its ▶ கேட்க button) and it reads the poem and its
  விளக்கம் (its பதவுரை when a poem has no விளக்கம்), then carries on to the next poems; previous / pause / next / stop
  in the player bar,
- a bar that stays at the top while reading, with the breadcrumb and the reading settings:
  speed (வேகம்), pitch (சுருதி) and text size. The settings are remembered on the device.

All six kandams are ready — 10,357 poems (numbered 1–10,368) in 117 padalams, plus பால காண்டம்'s பாயிரம்:

| காண்டம் | padalams | poems |
|---|---|---|
| பால காண்டம் | பாயிரம் + 23 | 1–1312 |
| அயோத்தியா காண்டம் | 12 | 1313–2515 |
| ஆரணிய காண்டம் | 13 | 2516–3707 |
| கிட்கிந்தா காண்டம் | 16 | 3708–4739 |
| சுந்தர காண்டம் | 14 | 4740–6058 |
| யுத்த காண்டம் | 39 | 6059–10368 |

Poem numbers run on through the whole work, as in the source edition. A few numbers are missing from the source PDFs
themselves: 3983 (கிட்கிந்தா) and 7779–7782, 8056, 8136, 8137, 9829, 9830 (யுத்த).
The extra verses (மிகைப் பாடல்கள்) printed after each kandam are not included.

Live site: https://rajkumar71234-ui.github.io/kamba-ramayanam/

Sister site: [வால்மீகி ராமாயணம்](https://rajkumar71234-ui.github.io/valmiki-ramayanam/) (same layout).

## How the site is organised

| Path | What it is |
|---|---|
| `index.html` | The one page (home, kandam list, padalam pages are drawn by `assets/app.js`) |
| `assets/` | Styles, script, logo |
| `data/kandams.json` | The six kandams and their padalams |
| `data/<k>/<pp>.json` | One file per padalam; k = 1 பால … 6 யுத்த (பால காண்டம் 00 = பாயிரம்; the others start at 01) |
| `img/<k>/<pp>/` | Pictures for that padalam (SVG): `chapter.svg`, `scene-*.svg` (பால காண்டம்), and `p<n>.svg` beside poem n |
| `content/<k>/<pp>.src.json` | Poems, பதவுரை, விளக்கம், sub-headings — taken from the source PDF |
| `content/<k>/<pp>.ta.json` | Story summary and picture caption — written for this site |
| `content/<k>/pics.json` | The small picture for each poem and its Tamil alt text (made by `tools/thumbs.py`) |
| `content/site.json` | Site title and the six kandams |
| `tools/` | The PDF decoder, build script and drawing kit |

Links: `#bala` (padalam list), `#bala-10` (a padalam), `#bala-10-p514` or `#bala-p514` (poem 514).
The other kandams are `#ayodhya`, `#aranya`, `#kishkindha`, `#sundara`, `#yuddha`; `#p6500` finds poem 6500 in any kandam.

## Rebuilding from the PDF

The source PDFs themselves are not kept in this repository (one per kandam; யுத்த காண்டம் comes in three parts).

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

For the other kandams (k = 2 … 6) each PDF is decoded into its own work folder, then parsed by `parse_kandam.py`:

```
python3 tools/fontmap.py    02-ayodhya.pdf work/k2
python3 tools/decode_pdf.py 02-ayodhya.pdf work/k2 split   # split: poem text and prose that share a line
python3 tools/parse_kandam.py 2         # -> content/2/*.src.json  (parts and poem ranges: KANDAMS in the script)
python3 tools/art_scenes.py 2           # padalam pictures from tools/scene_specs.json -> img/2/*/chapter.svg
python3 tools/thumbs.py 2               # a picture beside every poem
```

`tools/pad_notes.py` (used by `build_site.py`) puts the பதவுரை / விளக்கம் boundary where the meaning of the last
bold word ends: the PDFs often print the விளக்கம் straight on in the same paragraph, or carry the பதவுரை over a page
break. No words are added, dropped or reordered; a check of every PDF line against `data/` finds them all on the site.
For kandams 2–6 the punctuation is kept exactly as printed.

`parse_kandam.py` takes the padalams from each PDF's table of contents, follows the running poem numbers (a misprinted
or missing number does not stop it), puts the கடவுள் வாழ்த்து at the head of padalam 1, and lifts the sub-headings and
metre names printed just above a poem out of the previous poem's notes. `art_scenes.py` draws each padalam picture
from a short description in `tools/scene_specs.json` (background, time of day, figures and their poses, props), using
the figures in `tools/kit.py` and `tools/kit_more.py`.

`parse_pdf.py` also: turns the source's stray full stops inside poems back into commas (the printed
book has commas there), removes stray note numbers and `*` marks, and fixes a few obvious typos
(listed in `FIXES`).

`thumbs.py` picks each poem's picture from its own words and its பதவுரை (`poem_subjects.py` lists the Tamil word
patterns: people, animals, things, places, time of day, moods). It draws up to two figures, the setting and small
details in the same cartoon style as the padalam pictures. A few well-known poems have a hand-made picture
(`OVERRIDE` in `thumbs.py`).

## Credits

- Poems, பதவுரை and விளக்கம்: from the annotated edition in the source PDFs; poem numbers follow it.
- Story summaries and pictures: written and drawn fresh for this site.
