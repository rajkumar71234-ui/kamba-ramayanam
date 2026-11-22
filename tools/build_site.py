"""Build the website data files.

Reads
  content/1/<pp>.src.json   poems, பதவுரை, விளக்கம், sub-headings (made by parse_pdf.py from the PDF)
  content/1/<pp>.ta.json    story summary, picture captions and scene list (written for this site)
  content/1/pics.json       the small picture beside each poem and its alt text (made by thumbs.py)
  content/site.json         site title, the six kandams
Writes
  data/1/<pp>.json          everything one padalam page needs
  data/kandams.json         the list of kandams and padalams

Usage (from the repo root):  python3 tools/build_site.py
"""
import json
import subprocess
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pad_notes import rebalance

ROOT = Path(__file__).resolve().parent.parent
SOURCE_NOTE = ("பாடல்களும் பதவுரை, விளக்கமும்: கம்ப ராமாயணம் — {kandam}, உரையுடன் கூடிய பதிப்பு (மூல PDF). "
               "கதைச் சுருக்கமும் ஓவியங்களும் இந்தத் தளத்துக்காகப் புதிதாக உருவாக்கப்பட்டவை.")
KANDAM_TA = {1: 'பால காண்டம்', 2: 'அயோத்தியா காண்டம்', 3: 'ஆரணிய காண்டம்', 4: 'கிட்கிந்தா காண்டம்',
             5: 'சுந்தர காண்டம்', 6: 'யுத்த காண்டம்'}



def video_ready(mp4):
    """A finished story video: it exists, has its poster, is not being written right now, and plays."""
    if not mp4.exists() or not (mp4.parent / 'poster.jpg').exists() or time.time() - mp4.stat().st_mtime < 10:
        return False
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(mp4)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip()) > 1
    except ValueError:
        return False

def build_padalam(k, n, errors):
    src = json.loads((ROOT / 'content' / str(k) / f'{n:02d}.src.json').read_text(encoding='utf-8'))
    tap = ROOT / 'content' / str(k) / f'{n:02d}.ta.json'
    if not tap.exists():
        errors.append(f'{n:02d}: no .ta.json (story) yet')
        return None
    ta = json.loads(tap.read_text(encoding='utf-8'))
    img_base = f'img/{k}/{n:02d}/'
    poems = [it['n'] for it in src['items'] if it['type'] == 'poem']
    scenes = []
    for sc in ta.get('scenes', []):
        scenes.append({'id': sc['id'], 'from': sc['from'], 'to': sc['to'], 'title': sc['title'],
                       'caption': sc['caption'], 'src': img_base + sc['image']})
    if scenes:
        covered = []
        for sc in scenes:
            covered += list(range(sc['from'], sc['to'] + 1))
        if covered != poems:
            errors.append(f'{n:02d}: scenes must cover every poem exactly once, in order')
    for sc in scenes + [{'src': img_base + ta['chapter_image']['file']}]:
        if not (ROOT / sc['src']).exists():
            errors.append(f'{n:02d}: missing picture {sc["src"]}')
    pics_path = ROOT / 'content' / str(k) / 'pics.json'
    pics = json.loads(pics_path.read_text(encoding='utf-8')) if pics_path.exists() else {}
    items = []
    for it in src['items']:
        if it['type'] == 'poem':
            pad, notes = rebalance(it['pad'], it['notes'], k)
            row = {'type': 'poem', 'n': it['n'], 'lines': it['lines'], 'pad': pad, 'notes': notes}
            pic = pics.get(str(it['n']))
            if pic and (ROOT / pic['pic']).exists():
                row['pic'] = pic['pic']
                row['alt'] = pic['alt']
            else:
                errors.append(f'{n:02d}: no picture for poem {it["n"]} (run tools/thumbs.py)')
            items.append(row)
        else:
            items.append({'type': it['type'], 'text': it['text']})
    data = {
        'kandam': k, 'padalam': n, 'title': ta.get('title', src['title']),
        'subtitle': ta.get('subtitle', ''), 'summary': ta.get('summary', ''),
        'story': ta['story'],
        'chapter_image': {'src': img_base + ta['chapter_image']['file'], 'alt': ta['chapter_image']['alt']},
        'video': ({'src': img_base + 'video.mp4', 'poster': img_base + 'poster.jpg'}
                  if video_ready(ROOT / img_base / 'video.mp4') else None),
        'scenes': scenes,
        'intro': src['intro'],
        'items': items,
        'from': src['from'], 'to': src['to'],
        'source': SOURCE_NOTE.format(kandam=KANDAM_TA.get(k, '')),
    }
    out = ROOT / 'data' / str(k) / f'{n:02d}.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    return {'n': n, 'title': data['title'], 'from': src['from'], 'to': src['to'],
            'summary': data['summary'], 'scenes': bool(scenes)}


def main():
    site = json.loads((ROOT / 'content' / 'site.json').read_text(encoding='utf-8'))
    errors = []
    for kd in site['kandams']:
        k = kd['n']
        srcs = sorted((ROOT / 'content' / str(k)).glob('*.src.json')) if (ROOT / 'content' / str(k)).exists() else []
        if not srcs:
            continue
        pads = []
        for p in srcs:
            n = int(p.name.split('.')[0])
            info = build_padalam(k, n, errors)
            if info:
                pads.append(info)
        kd['padalams'] = pads
        if not pads:
            continue
        kd['from'], kd['to'] = pads[0]['from'], pads[-1]['to']
        kd['poems'] = sum(len([1 for it in json.loads((ROOT / 'data' / str(k) / f"{x['n']:02d}.json").read_text(encoding='utf-8'))['items']
                               if it['type'] == 'poem']) for x in pads)
    (ROOT / 'data' / 'kandams.json').write_text(json.dumps(site, ensure_ascii=False, indent=1), encoding='utf-8')
    for e in errors:
        print('!!', e)
    for kd in site['kandams']:
        if kd.get('padalams'):
            print(kd['ta'], len(kd['padalams']), 'padalams,', kd['poems'], 'poems')
    if any('scenes must' in e or 'missing picture' in e for e in errors):
        sys.exit(1)


if __name__ == '__main__':
    main()
