"""One short story video per padalam: scene pictures with a slow zoom, Tamil captions and Tamil narration.

    python3 tools/make_video.py 5 4          # content/5/04.video.json -> img/5/04/video.mp4 and poster.jpg
    python3 tools/make_video.py 5            # every padalam of kandam 5 that has a .video.json

content/<k>/<pp>.video.json:
    {"scenes": [{"text": "narration ...", "spec": {...art_scenes spec...}},
                {"text": "...", "image": "scene-1.svg"},          # a picture already in img/<k>/<pp>/
                ...]}

The first shot is a title card (the padalam picture, the kandam and padalam names). The narration voice is
Meta's MMS Tamil text-to-speech model (facebook/mms-tts-tam, CC BY-NC 4.0), run locally.
Needs: ffmpeg, rsvg-convert, the Noto Sans/Serif Tamil fonts, torch, transformers, soundfile, uharfbuzz.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

W, H = 1280, 800            # layout size of captions and the title card
OUT_W, OUT_H = 1024, 640    # video size
SRC_W, SRC_H = 2560, 1600   # pictures are drawn larger, so the slow zoom stays smooth
FPS = 25
XFADE = 0.6                 # cross-fade between shots (s)
LEAD, TAIL = 0.5, 1.1       # silence before / after the narration of a shot (s)
SR = 16000
FONT_SANS = Path.home() / '.fonts' / 'NotoSansTamil-Regular.ttf'
CAP_SIZE = 36
CAP_MAX_W = W - 2 * 70

# tools/pronounce.json: {"written word": "spelling the voice says it right with"}
_PRON = Path(__file__).resolve().parent / 'pronounce.json'
PRONOUNCE = {}


def load_pronounce():
    """Re-read the list before every video, so a fix applies to the next render without a restart."""
    PRONOUNCE.clear()
    if _PRON.exists():
        PRONOUNCE.update(json.loads(_PRON.read_text(encoding='utf-8')))

KANDAM_TA = {1: 'பால காண்டம்', 2: 'அயோத்தியா காண்டம்', 3: 'ஆரணிய காண்டம்', 4: 'கிட்கிந்தா காண்டம்',
             5: 'சுந்தர காண்டம்', 6: 'யுத்த காண்டம்'}


# ---------------------------------------------------------------- voice
class Voice:
    def __init__(self, rate=0.92):
        import torch
        from transformers import AutoTokenizer, VitsModel
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained('facebook/mms-tts-tam')
        self.model = VitsModel.from_pretrained('facebook/mms-tts-tam')
        self.model.speaking_rate = rate
        self.model.eval()

    def say(self, text, seed=0):
        for word, spoken in PRONOUNCE.items():        # how the voice should say a word (captions keep the spelling)
            text = text.replace(word, spoken)
        text = re.sub(r'[“”‘’"\'`*()\[\]—–-]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if not re.search(r'[஀-௿]', text):
            return np.zeros(int(.2 * SR), dtype=np.float32)
        self.torch.manual_seed(seed)
        inputs = self.tok(text, return_tensors='pt')
        with self.torch.no_grad():
            wav = self.model(**inputs).waveform[0].numpy().astype(np.float32)
        peak = float(np.abs(wav).max()) or 1.0
        return wav * (0.89 / peak)

    def sentence(self, text, seed=0):
        """A sentence, spoken clause by clause with short pauses at the commas."""
        parts = [p for p in re.split(r'(?<=[,;:])\s+', text) if p.strip()]
        out = []
        for i, p in enumerate(parts):
            out.append(self.say(p, seed + i))
            if i < len(parts) - 1:
                out.append(np.zeros(int(.22 * SR), dtype=np.float32))
        return np.concatenate(out)


def sentences(text):
    """Split narration into sentences (keeps quotes with their sentence)."""
    text = re.sub(r'\s+', ' ', text).strip()
    parts = re.split(r'(?<=[.?!])\s+(?=[^\s”’])', text)
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------------- captions
_hb = {}


def text_width(text, size=CAP_SIZE, font=FONT_SANS):
    import uharfbuzz as hb
    if font not in _hb:
        blob = hb.Blob.from_file_path(str(font))
        face = hb.Face(blob)
        _hb[font] = (hb.Font(face), face.upem)
    f, upem = _hb[font]
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(f, buf, {})
    return sum(p.x_advance for p in buf.glyph_positions) * size / upem


def wrap(text, max_w=CAP_MAX_W, size=CAP_SIZE):
    lines, cur = [], ''
    for w in text.split():
        trial = (cur + ' ' + w).strip()
        if cur and text_width(trial, size) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def caption_svg(lines):
    lh = CAP_SIZE * 1.5
    box_h = lh * len(lines) + 34
    y0 = H - box_h - 26
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect x="40" y="{y0:.0f}" width="{W - 80}" height="{box_h:.0f}" rx="18" fill="#000" fill-opacity="0.58"/>']
    for i, line in enumerate(lines):
        y = y0 + 17 + lh * (i + 0.5) + CAP_SIZE * 0.36
        out.append(f'<text x="{W / 2}" y="{y:.0f}" text-anchor="middle" font-family="Noto Sans Tamil" '
                   f'font-size="{CAP_SIZE}" fill="#fff">{esc(line)}</text>')
    out.append('</svg>')
    return '\n'.join(out)


def title_svg(img_href, kandam, title, subtitle):
    sub_lines = wrap(subtitle, W - 220, 30) if subtitle else []
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">',
           '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
           '<stop offset="0" stop-color="#000" stop-opacity="0.05"/><stop offset="0.45" stop-color="#000" stop-opacity="0.25"/>'
           '<stop offset="1" stop-color="#000" stop-opacity="0.78"/></linearGradient></defs>',
           f'<image x="0" y="0" width="{W}" height="{H}" xlink:href="{img_href}" preserveAspectRatio="xMidYMid slice"/>',
           f'<rect width="{W}" height="{H}" fill="url(#g)"/>',
           f'<text x="{W / 2}" y="{H - 250 - 40 * max(0, len(sub_lines) - 1)}" text-anchor="middle" font-family="Noto Sans Tamil" '
           f'font-size="34" fill="#f5d98b">{esc(kandam)}</text>',
           f'<text x="{W / 2}" y="{H - 165 - 40 * max(0, len(sub_lines) - 1)}" text-anchor="middle" font-family="Noto Serif Tamil" '
           f'font-weight="bold" font-size="70" fill="#fff">{esc(title)}</text>']
    for i, line in enumerate(sub_lines):
        out.append(f'<text x="{W / 2}" y="{H - 95 - 40 * (len(sub_lines) - 1 - i)}" text-anchor="middle" '
                   f'font-family="Noto Sans Tamil" font-size="30" fill="#eee">{esc(line)}</text>')
    out.append('</svg>')
    return '\n'.join(out)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f'failed: {" ".join(map(str, cmd))[:300]}\n{r.stderr[-1500:]}')
    return r


def svg_to_png(svg_path, png_path, w, h):
    run(['rsvg-convert', '-w', str(w), '-h', str(h), '-o', str(png_path), str(svg_path)])


# ---------------------------------------------------------------- one padalam
def make(k, pp, voice, keep=False):
    load_pronounce()
    src = ROOT / 'content' / str(k) / f'{pp:02d}.video.json'
    ta = json.loads((ROOT / 'content' / str(k) / f'{pp:02d}.ta.json').read_text(encoding='utf-8'))
    spec = json.loads(src.read_text(encoding='utf-8'))
    out_dir = ROOT / 'img' / str(k) / f'{pp:02d}'
    tmp = Path(tempfile.mkdtemp(prefix=f'vid{k}_{pp}_'))
    import art_scenes
    shots = []      # (png, [(caption_png, t0, t1)], audio, duration)

    # title card
    chapter = out_dir / ta.get('chapter_image', {}).get('file', 'chapter.svg')
    svg_to_png(chapter, tmp / 'chapter.png', SRC_W, SRC_H)
    (tmp / 'title.svg').write_text(title_svg('chapter.png', KANDAM_TA[k], ta['title'], ta.get('subtitle', '')),
                                   encoding='utf-8')
    svg_to_png(tmp / 'title.svg', tmp / 'shot0.png', SRC_W, SRC_H)
    shutil.copy(tmp / 'shot0.png', tmp / 'poster_src.png')
    title_audio = voice.sentence(f'{KANDAM_TA[k]}. {ta["title"]}.', seed=pp * 100)
    shots.append(dict(png=tmp / 'shot0.png', caps=[], audio=[(0.0, title_audio)],
                      dur=LEAD + len(title_audio) / SR + TAIL + 0.4, zoom='in'))

    for si, sc in enumerate(spec['scenes'], start=1):
        if 'image' in sc:
            svg_path = out_dir / sc['image']
        else:
            svg_path = tmp / f'scene{si}.svg'
            svg_path.write_text(art_scenes.scene(sc['spec']), encoding='utf-8')
        png = tmp / f'shot{si}.png'
        svg_to_png(svg_path, png, SRC_W, SRC_H)
        caps, audio, t = [], [], LEAD
        for qi, sent in enumerate(sentences(sc['text'])):
            wav = voice.sentence(sent, seed=pp * 1000 + si * 37 + qi)
            dur = len(wav) / SR
            audio.append((t, wav))
            # the caption: two lines at a time, each pair shown for its share of the sentence
            lines = wrap(sent)
            pairs = [lines[i:i + 2] for i in range(0, len(lines), 2)]
            total = sum(len(' '.join(p)) for p in pairs) or 1
            tt = t
            for pi, pair in enumerate(pairs):
                share = dur * len(' '.join(pair)) / total
                cap_svg = tmp / f'cap{si}_{qi}_{pi}.svg'
                cap_svg.write_text(caption_svg(pair), encoding='utf-8')
                cap_png = tmp / f'cap{si}_{qi}_{pi}.png'
                svg_to_png(cap_svg, cap_png, OUT_W, OUT_H)
                caps.append((cap_png, tt - (0.25 if pi == 0 else 0), tt + share + (0.35 if pi == len(pairs) - 1 else 0)))
                tt += share
            t += dur + 0.45
        for ci in range(len(caps) - 1):           # one caption at a time: each stays until the next appears
            caps[ci] = (caps[ci][0], caps[ci][1], caps[ci + 1][1])
        shots.append(dict(png=png, caps=caps, audio=audio, dur=t - 0.45 + TAIL, zoom='in' if si % 2 else 'out'))

    # ---- audio track
    starts, T = [], 0.0
    for sh in shots:
        starts.append(T)
        T += sh['dur'] - XFADE
    total = T + XFADE
    track = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for st, sh in zip(starts, shots):
        for off, wav in sh['audio']:
            i0 = int((st + LEAD + off if off == 0.0 and not sh['caps'] else st + off) * SR)
            track[i0:i0 + len(wav)] += wav
    import soundfile as sf
    sf.write(tmp / 'voice.wav', np.clip(track, -1, 1), SR)

    # ---- video: one stream per shot, slow zoom + captions, cross-faded
    inputs, fc = [], []
    idx = 0
    pan = [(0.5, 0.5, 0.5, 0.45), (0.3, 0.5, 0.6, 0.5), (0.6, 0.4, 0.4, 0.55), (0.5, 0.6, 0.5, 0.4)]
    for si, sh in enumerate(shots):
        n = int(round(sh['dur'] * FPS))
        z0, z1 = (1.0, 1.1) if sh['zoom'] == 'in' else (1.1, 1.0)
        px0, py0, px1, py1 = pan[si % len(pan)]
        inputs += ['-i', str(sh['png'])]
        img = idx
        idx += 1
        prog = f'(on/{max(1, n - 1)})'
        fc.append(f"[{img}:v]zoompan=z='{z0}+({z1 - z0})*{prog}':"
                  f"x='(iw-iw/zoom)*({px0}+({px1 - px0})*{prog})':y='(ih-ih/zoom)*({py0}+({py1 - py0})*{prog})':"
                  f"d={n}:s={OUT_W}x{OUT_H}:fps={FPS},setsar=1,format=yuv420p[z{si}]")
        last = f'z{si}'
        for ci, (cap, a, b) in enumerate(sh['caps']):
            inputs += ['-i', str(cap)]
            cin = idx
            idx += 1
            fc.append(f"[{last}][{cin}:v]overlay=0:0:enable='gte(t,{max(0, a):.2f})*lt(t,{b:.2f})'[c{si}_{ci}]")
            last = f'c{si}_{ci}'
        fc.append(f'[{last}]format=yuv420p,settb=AVTB,fps={FPS}[s{si}]')
    prev = 's0'
    for si in range(1, len(shots)):
        fc.append(f'[{prev}][s{si}]xfade=transition=fade:duration={XFADE}:offset={starts[si]:.3f}[x{si}]')
        prev = f'x{si}'
    fc.append(f"[{prev}]fade=t=in:st=0:d=0.6,fade=t=out:st={total - 0.8:.2f}:d=0.8[vout]")
    inputs += ['-i', str(tmp / 'voice.wav')]
    out_dir.mkdir(parents=True, exist_ok=True)
    mp4 = out_dir / 'video.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(fc),
         '-map', '[vout]', '-map', f'{idx}:a', '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'animation', '-crf', '32',
         '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '48k', '-ac', '1', '-ar', '24000',
         '-t', f'{total:.2f}', '-movflags', '+faststart', str(mp4)])
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(tmp / 'poster_src.png'), '-vf', f'scale={OUT_W}:{OUT_H}',
         '-q:v', '4', str(out_dir / 'poster.jpg')])
    if not keep:
        shutil.rmtree(tmp, ignore_errors=True)
    return mp4, total


def main():
    k = int(sys.argv[1])
    pps = [int(x) for x in sys.argv[2:]] or sorted(int(p.name[:2]) for p in (ROOT / 'content' / str(k)).glob('*.video.json'))
    voice = Voice()
    for pp in pps:
        mp4, total = make(k, pp, voice)
        print(f'{k}/{pp:02d}: {total:5.1f} s, {mp4.stat().st_size / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
