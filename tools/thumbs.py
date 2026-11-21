"""Draw one small picture (240 x 240 SVG) for every poem of a kandam.

    python3 tools/thumbs.py 1            # all of பால காண்டம் -> img/1/<pp>/p<n>.svg
    python3 tools/thumbs.py 1 10 12      # only padalams 10 and 12

Each picture is chosen from the poem's own words and its பதவுரை (poem_subjects.py): up to two
figures (or an animal, or a thing), the setting (palace, river, night, forest ...) and small
accents. It also writes content/<k>/pics.json with a Tamil alt text for every picture.
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *            # noqa: F401,F403
from kit import *            # noqa: F401,F403
from art import valmiki as valmiki_fig, brahma as brahma_fig, crane
from art_bala import blossom_tree, gopuram, leaf_meal, mirror, olai_stack, splash
import kit_more as KM
from poem_subjects import features, F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = 240

# ============================================================== sky / defs
SKIES = {
    'day': ('#bfe6f6', '#dff3fa', '#f4fbfd'),
    'dawn': ('#ffd2a6', '#fdebd0', '#d6eef6'),
    'evening': ('#ee9f74', '#f8cca2', '#f6e3cf'),
    'night': ('#1b2850', '#30457a', '#56699a'),
    'divine': ('#fff0c4', '#ffe4a6', '#fbd39a'),
    'desert': ('#f4bd6c', '#fadca6', '#fdf0d5'),
    'indoor': ('#f6e3c0', '#f9ecd6', '#f9ecd6'),
    'storm': ('#56627c', '#7d8aa2', '#aeb8c6'),
}


def tdefs(kind):
    a, b, c = SKIES[kind]
    w0, w1 = ('#4b6fa0', '#36557f') if kind == 'night' else (WATER, WATER_D)
    return (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/>'
            f'<stop offset=".6" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>'
            f'<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{w0}"/>'
            f'<stop offset="1" stop-color="{w1}"/></linearGradient>'
            '<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fffbe6"/>'
            '<stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>')


def xesc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


NUM = re.compile(r'(-?\d+\.\d{2,})')


def tsvg(body, kind, title):
    body = NUM.sub(lambda m: f'{float(m.group(1)):.1f}', body)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {T} {T}" width="{T}" height="{T}" role="img">'
            f'<title>{xesc(title)}</title><defs>{tdefs(kind)}</defs>{body}</svg>')


# ============================================================== small props
def conch(s=1.0):
    return G(P("M-14,8 C-22,-6 -14,-24 2,-26 C18,-28 26,-14 20,0 C16,10 4,14 -14,8 Z", "#fbf6ea", sw=2) +
             P("M-14,8 L-24,16 L-10,13 Z", "#fbf6ea", sw=1.8) +
             P("M-4,-18 C6,-20 14,-12 10,-2", stroke="#d9c09a", sw=2) + P("M0,-10 C6,-10 8,-4 4,2", stroke="#d9c09a", sw=1.6), s=s)


def discus(s=1.0):
    fl = "".join(P(f"M{24*math.cos(a):.1f},{24*math.sin(a):.1f} L{32*math.cos(a+.13):.1f},{32*math.sin(a+.13):.1f} "
                   f"L{24*math.cos(a+.26):.1f},{24*math.sin(a+.26):.1f} Z", "#ff9f2e", stroke="none")
                 for a in [i * math.pi / 6 for i in range(12)])
    sp = "".join(P(f"M0,0 L{18*math.cos(a):.1f},{18*math.sin(a):.1f}", stroke=GOLD_D, sw=2)
                 for a in [i * math.pi / 4 for i in range(8)])
    return G(fl + C(0, 0, 24, GOLD, sw=2.2) + C(0, 0, 18, "#fff1b8", sw=1.6) + sp + C(0, 0, 5, JEWEL_RED, sw=1.6), s=s)


def veena(s=1.0):
    frets = "".join(P(f"M{-12+k*10},{12-k*10} l4,4", stroke=GOLD_D, sw=1.6) for k in range(5))
    return G(P("M-30,30 L40,-40", stroke=OUT, sw=10) + P("M-30,30 L40,-40", stroke="#b07a3e", sw=6) +
             C(-34, 34, 18, "#a0582e", sw=2.2) + C(-34, 34, 9, "#d58c4a", stroke="none") + C(40, -44, 9, "#a0582e", sw=2) +
             P("M-26,26 L36,-36", stroke="#f3e3c3", sw=1) + frets, s=s)


def parrot(s=1.0, flip=False):
    """A green parrot sitting, facing right; feet at (0,0)."""
    b = (P("M-4,-8 L-10,20 L2,-2 Z", "#3e8f3b", sw=1.6) + E(0, -18, 10, 15, "#4fb04a", sw=2) +
         P("M-5,-26 C1,-18 1,-10 -5,-4", stroke="#3e8f3b", sw=2) + C(4, -33, 9, "#5cc356", sw=2) +
         P("M11,-36 C19,-35 18,-27 12,-26 Z", "#e2483d", sw=1.6) + C(6, -35, 1.7, "#1e1e1e", stroke="none") +
         P("M-2,-28 C3,-25 8,-25 12,-27", stroke="#e2483d", sw=1.4) + P("M-2,-3 L-3,1 M4,-3 L5,1", stroke="#8a6a4a", sw=1.8))
    return G(b, s=s, flip=flip)


def songbird(color="#2b2b2b", s=1.0, flip=False, eye="#d33"):
    """A small bird (cuckoo, myna) perched, facing right; feet at (0,0)."""
    b = (P("M-10,-12 L-24,-4 L-12,-6 Z", color, sw=1.6) + E(0, -12, 13, 8, color, sw=1.8) + C(11, -20, 6.5, color, sw=1.8) +
         P("M17,-21 L24,-19 L17,-17 Z", "#d9b06a", sw=1.2) + C(12.5, -21.5, 1.5, eye, stroke="none") +
         P("M-2,-4 L-3,0 M4,-4 L5,0", stroke="#8a6a4a", sw=1.6))
    return G(b, s=s, flip=flip)


def flying_birds(x, y, n=3, s=1.0, color=OUT):
    out = ""
    for k in range(n):
        dx, dy = k * 18, (k % 2) * 9 - k * 2
        out += P(f"M{dx-8},{dy} q4,-5 8,0 q4,-5 8,0", stroke=color, sw=2)
    return G(out, x=x, y=y, s=s)


def lion(s=1.0):
    c, m = "#e3a947", "#b8681f"
    legs = "M-30,-24 L-32,0 M-18,-24 L-16,0 M18,-24 L16,0 M30,-24 L34,0"
    b = (P(legs, stroke=OUT, sw=9) + P(legs, stroke=c, sw=5.5) + P("M-38,-36 C-56,-40 -60,-60 -50,-66", stroke=OUT, sw=4) +
         C(-50, -67, 5, m, sw=1.6) + E(0, -36, 40, 16, c, sw=2.4) +
         C(40, -50, 24, m, sw=2.4) + C(44, -48, 14, c, sw=2) + C(40, -52, 1.8, "#2a1c14", stroke="none") +
         C(50, -52, 1.8, "#2a1c14", stroke="none") + P("M43,-45 L47,-45 L45,-42 Z", "#5a3a22", sw=1) +
         P("M41,-39 Q45,-36 49,-39", sw=1.4))
    return G(b, s=s)


def cobra(s=1.0):
    g, gl = "#6f9a3c", "#cfe08f"
    b = (E(0, -6, 26, 9, g, sw=2.2) + E(-2, -14, 18, 7, "#7fab4a", sw=2) +
         P("M8,-16 C14,-30 6,-42 4,-54", stroke=OUT, sw=11) + P("M8,-16 C14,-30 6,-42 4,-54", stroke="#7fab4a", sw=7.5) +
         E(4, -62, 13, 15, "#7fab4a", sw=2.2) + E(4, -58, 6, 9, gl, stroke="none") +
         C(0, -66, 1.6, "#2a1c14", stroke="none") + C(8, -66, 1.6, "#2a1c14", stroke="none") +
         P("M4,-54 L4,-48 M4,-48 l-3,4 M4,-48 l3,4", stroke=JEWEL_RED, sw=1.4))
    return G(b, s=s)


def boat(s=1.0, sail=True):
    b = P("M-50,-14 L50,-14 C42,4 -42,4 -50,-14 Z", "#a0682e", sw=2.4) + P("M-46,-9 L46,-9", stroke="#7a4c22", sw=1.6)
    if sail:
        b = P("M0,-14 L0,-78", stroke="#7a4c22", sw=3) + P("M3,-74 C30,-58 30,-34 3,-20 Z", MILK, sw=2.2) + b
    return G(b, s=s)


def cup(s=1.0):
    return G(P("M-10,-16 L10,-16 L7,0 L-7,0 Z", GOLD, sw=1.8) + E(0, -16, 10, 3, "#7a2e4a", sw=1.4), s=s)


def pot(s=1.0, color="#b9583a"):
    return G(E(0, -16, 18, 16, color, sw=2.2) + R(-8, -38, 16, 8, color, stroke=OUT, sw=2) + E(0, -38, 10, 3, "#5a2a1a", sw=1.6) +
             P("M-14,-18 Q0,-12 14,-18", stroke="#f2c14e", sw=2), s=s)


def necklace_big(s=1.0):
    out = []
    for k in range(17):
        t = k / 16
        a = math.pi * t
        out.append(C(-34 * math.cos(a), 26 * math.sin(a), 4.2, "#fffaf0" if k % 4 else GOLD, sw=1.2))
    out.append(P("M-6,26 L6,26 L0,42 Z", GOLD, sw=1.6))
    out.append(C(0, 32, 4.5, JEWEL_RED, sw=1.4))
    return G(*out, s=s)


def arrow(x1, y1, x2, y2, w=3):
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 + 12 * math.cos(a), y2 + 12 * math.sin(a)
    l, r = a + 2.6, a - 2.6
    return (P(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", stroke="#8a5a2b", sw=w) +
            P(f"M{hx:.1f},{hy:.1f} L{x2+7*math.cos(l):.1f},{y2+7*math.sin(l):.1f} L{x2+7*math.cos(r):.1f},{y2+7*math.sin(r):.1f} Z",
              "#cfd6dc", sw=1.4) +
            P(f"M{x1:.1f},{y1:.1f} l{-8*math.cos(a-.5):.1f},{-8*math.sin(a-.5):.1f} M{x1:.1f},{y1:.1f} "
              f"l{-8*math.cos(a+.5):.1f},{-8*math.sin(a+.5):.1f}", stroke="#f6f0e0", sw=2.6))


def big_axe(s=1.0):
    return G(P("M0,60 L0,-60", stroke=OUT, sw=8) + P("M0,60 L0,-60", stroke="#8a5a2b", sw=5) +
             P("M0,-58 C30,-70 40,-36 36,-18 C24,-28 10,-30 0,-32 Z", "#cfd6dc", sw=2.4) +
             P("M6,-52 C22,-58 30,-42 30,-30", stroke="#ffffff", sw=2, opacity=.7), s=s)


def sword(s=1.0):
    return G(P("M0,0 L0,-70", stroke=OUT, sw=7) + P("M0,0 L0,-70", stroke="#dfe5ea", sw=4.5) +
             P("M-10,-2 L10,-2", stroke=GOLD_D, sw=5) + P("M0,0 L0,12", stroke="#6b4421", sw=5), s=s)


def spear(s=1.0):
    return G(P("M0,40 L0,-60", stroke="#8a5a2b", sw=4) + P("M0,-60 L-6,-72 L0,-92 L6,-72 Z", "#cfd6dc", sw=1.8), s=s)


def shield(s=1.0):
    return G(C(0, 0, 22, "#a0582e", sw=2.2) + C(0, 0, 15, "#c9733a", sw=1.6) + C(0, 0, 5, GOLD, sw=1.4), s=s)


def bolt(x, y, s=1.0):
    return G(P("M0,0 L-12,30 L0,30 L-14,64 L16,22 L4,22 L14,0 Z", "#fff1a0", stroke="#f0c53a", sw=1.6), x=x, y=y, s=s)


def wind_lines(x, y, s=1.0, color="#ffffff"):
    return G(P("M0,0 C20,-8 40,8 60,0 C70,-4 72,-14 64,-16", stroke=color, sw=2.4, opacity=.85) +
             P("M10,16 C30,8 46,22 70,14", stroke=color, sw=2, opacity=.7), x=x, y=y, s=s)


def sugarcane(x, y, s=1.0):
    out = ""
    for k, dx in enumerate((-10, 0, 10)):
        h = 110 + k * 8
        out += P(f"M{dx},0 L{dx+2},{-h}", stroke="#5f8f3a", sw=6) + "".join(
            P(f"M{dx-3},{-j} L{dx+4},{-j}", stroke="#3f6a26", sw=1.6) for j in range(18, h, 22))
        out += P(f"M{dx+2},{-h} C{dx+20},{-h-18} {dx+30},{-h-6} {dx+36},{-h+8}", stroke=LEAF, sw=3)
        out += P(f"M{dx+2},{-h} C{dx-16},{-h-16} {dx-26},{-h-4} {dx-32},{-h+10}", stroke=LEAF_D, sw=3)
    return G(out, x=x, y=y, s=s)


def dead_tree(x, y, s=1.0):
    d = "M0,0 L-2,-60 M-2,-40 L-22,-62 M-1,-50 L18,-74 M-2,-60 L-10,-84 M18,-74 L28,-80 M-22,-62 L-30,-60"
    return G(P(d, stroke=OUT, sw=8) + P(d, stroke="#8a6a4a", sw=5), x=x, y=y, s=s)


def cushion(w=90):
    return (P(f"M{-w/2},0 C{-w/2},-14 {w/2},-14 {w/2},0 C{w/2},10 {-w/2},10 {-w/2},0 Z", ROYAL_RED, sw=2.2) +
            C(-w / 2, 0, 4, GOLD, sw=1.2) + C(w / 2, 0, 4, GOLD, sw=1.2))


def hood_fan():
    """Adisesha's five hoods spread behind Vishnu's head (head at about y=-128), coils at his feet."""
    out = [P("M-40,-4 C-60,-14 -60,-40 -40,-50 C-30,-56 -26,-80 -30,-110", stroke=OUT, sw=15),
           P("M-40,-4 C-60,-14 -60,-40 -40,-50 C-30,-56 -26,-80 -30,-110", stroke="#5f8f3a", sw=11)]
    for k in range(5):
        a = math.pi + 0.35 + k * (math.pi - 0.7) / 4
        x, y = 40 * math.cos(a), -150 + 34 * math.sin(a)
        out.append(E(x, y, 12, 15, "#5f8f3a", sw=2.2))
        out.append(E(x, y + 3, 6, 8, "#d9e6a0", stroke="none"))
        out.append(C(x - 3, y - 6, 1.4, "#1e1e1e", stroke="none") + C(x + 3, y - 6, 1.4, "#1e1e1e", stroke="none"))
    out.append(P("M-44,-150 Q0,-210 44,-150 L30,-136 Q0,-180 -30,-136 Z", "#5f8f3a", sw=2.2))
    return "".join(out)


def baby_glow(s=1.0):
    return G(baby(), s=s)


# ============================================================== figures
WOMEN_CLOTH = [(TEAL_CLOTH, TEAL_CLOTH_D, GOLD), (PINK_CLOTH, PINK_CLOTH_D, GOLD), (PURPLE_CLOTH, PURPLE_CLOTH_D, GOLD),
               (BLUE_CLOTH, BLUE_CLOTH_D, PINK_CLOTH), (GREEN_CLOTH, GREEN_CLOTH_D, GOLD), (SAFFRON, SAFFRON_D, GREEN_CLOTH)]
KING_CLOTH = [(ROYAL_RED, ROYAL_RED_D), (BLUE_CLOTH, BLUE_CLOTH_D), (GREEN_CLOTH, GREEN_CLOTH_D), (PURPLE_CLOTH, PURPLE_CLOTH_D)]
MAN_TOP = [OCHRE, TEAL_CLOTH, PINK_CLOTH, GREEN_CLOTH, "#e9dfc8"]
FEMALE = {'sita', 'women', 'queen', 'ahalya', 'thadagai', 'musicians', 'kaikeyi', 'manthara', 'surpanakha', 'sabari',
          'tara', 'mandodari', 'trijata'}
HOLDS = {'dasaratha', 'janaka', 'vasishtha', 'vishwamitra', 'kamban', 'rama', 'lakshmana', 'sita', 'parasurama', 'gautama'}


CUR = {'k': 1}
HERMIT = {'on': False}      # Rama, Sita, Lakshmana and Bharata wear bark cloth in the forest years
BIRDS = ('jatayu', 'sampati', 'garuda')


def fig(key, pose='down', eye='happy', mk='smile', hold='', sitting=False, v=0, hood=False):
    """One figure, feet (or seat) at (0,0). hold='' means 'the usual thing for this person'."""
    if HERMIT['on'] and key in ('rama', 'lakshmana', 'sita', 'bharata'):
        h = hold if hold != '' else ('bow' if key in ('rama', 'lakshmana') else None)
        if pose != 'down':
            h = None
        if key == 'sita':
            return person(skin=SKIN_WOMAN, hair='braid', outfit='saree', cloth=BARK_L, cloth_d=BARK_D, top=BARK, pose=pose,
                          sitting=sitting, eye=eye, mouth_kind=mk, tilak='bindi', female=True, flowers=True)
        skin = {'rama': RAMA_BLUE, 'lakshmana': SKIN_GOLD, 'bharata': RAMA_BLUE_D}[key]
        return person(skin=skin, hair='jata', outfit='bark', cloth=BARK, cloth_d=BARK_D, pose=pose, sitting=sitting, eye=eye,
                      mouth_kind=mk, tilak='namam', quiver=(h == 'bow'), hold=h, thread=True)
    extra = {
        'kaikeyi': lambda: KM.kaikeyi(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'manthara': lambda: KM.manthara(pose=pose if pose != 'down' else 'point', eye=eye if eye != 'happy' else 'stern', mk='open'),
        'guha': lambda: KM.guha(pose=pose, eye=eye, mk=mk, sitting=sitting, hold='bow' if pose == 'down' else None),
        'sumantra': lambda: KM.sumantra(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'surpanakha': lambda: KM.surpanakha(pose=pose, eye=eye, mk=mk, beautiful=(v % 3 == 0)),
        'khara': lambda: KM.khara(pose=pose, hold='sword' if pose == 'down' else None),
        'ravana': lambda: KM.ravana(pose=pose, eye=eye if eye != 'happy' else 'stern', mk=mk, sitting=sitting,
                                    hold='sword' if pose == 'down' else None),
        'maricha': lambda: KM.rakshasa(pose=pose, hold=None, eye=eye, skin='#6a6a8a'),
        'viradha': lambda: KM.viradha(pose=pose if pose != 'down' else 'raise'),
        'sabari': lambda: KM.sabari(pose=pose if pose != 'down' else 'namaste', eye=eye, mk=mk, sitting=sitting),
        'agastya': lambda: KM.agastya(pose=pose if pose != 'down' else 'bless', eye=eye, mk=mk, sitting=sitting),
        'hanuman': lambda: KM.hanuman(pose=pose, eye=eye, mk=mk, sitting=sitting, hold='mace' if pose == 'down' else None),
        'sugriva': lambda: KM.sugriva(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'vali': lambda: KM.vali(pose=pose, eye=eye if eye != 'happy' else 'stern', mk=mk, sitting=sitting),
        'tara': lambda: KM.tara(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'angada': lambda: KM.angada(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'jambavan': lambda: KM.jambavan(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'nala': lambda: KM.nala(pose=pose, eye=eye, mk=mk),
        'vanara': lambda: KM.vanara(pose=pose, eye=eye, mk=mk, skin=['#b9824a', '#a8784a', '#c39a62'][v % 3],
                                    cloth=[SAFFRON, TEAL_CLOTH, GREEN_CLOTH][v % 3],
                                    cloth_d=[SAFFRON_D, TEAL_CLOTH_D, GREEN_CLOTH_D][v % 3]),
        'vibhishana': lambda: KM.vibhishana(pose=pose if pose != 'down' else 'namaste', eye=eye, mk=mk, sitting=sitting),
        'kumbhakarna': lambda: KM.kumbhakarna(pose=pose, eye=eye if eye != 'happy' else 'stern', hold='trident' if pose == 'down' else None),
        'indrajit': lambda: KM.indrajit(pose=pose, eye=eye if eye != 'happy' else 'stern', hold='bow' if pose == 'down' else None),
        'mandodari': lambda: KM.mandodari(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'trijata': lambda: KM.trijata(pose=pose, eye=eye, mk=mk),
        'samudra': lambda: KM.samudra(pose=pose if pose != 'down' else 'namaste', eye=eye, mk=mk),
        'jatayu': lambda: G(KM.big_bird(wings='open' if pose != 'down' else 'closed'), x=-10, s=1.15),
        'sampati': lambda: G(KM.big_bird(wings='none', color='#6a5a4a', wing='#4f4234'), x=-10, s=1.15),
        'garuda': lambda: G(KM.big_bird(gold=True), x=-10, s=1.15),
        'kabandha': lambda: G(KM.kabandha(), s=1.0),
    }
    if key in extra:
        return extra[key]()
    if key == 'rama':
        h = 'bow' if hold == '' else hold
        if pose == 'draw':
            h = None
        return rama(pose=pose, hold=h, eye=eye, mouth_kind=mk, sitting=sitting)
    if key == 'lakshmana':
        h = 'bow' if hold == '' else hold
        if pose == 'draw':
            h = None
        return lakshmana(pose=pose, hold=h, eye=eye, mouth_kind=mk, sitting=sitting)
    if key == 'sita':
        return sita(pose=pose, eye=eye, mouth_kind=mk, sitting=sitting, bride=(v % 1000 >= 1117), hold=hold or None)
    if key == 'dasaratha':
        return dasaratha(pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, hold=hold or None)
    if key == 'janaka':
        return janaka(pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, hold=hold or None)
    if key == 'vasishtha':
        return vasishtha(pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, hold=('kamandalu' if hold == '' else hold or None))
    if key == 'vishwamitra':
        return vishwamitra(pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, hold=('staff' if hold == '' else hold or None))
    if key == 'shatananda':
        return shatananda(pose=pose, sitting=sitting, eye=eye, hold=hold or None)
    if key == 'gautama':
        return person(skin=SKIN_SAGE, hair="jata", hair_color=WHITE_HAIR, beard=WHITE_HAIR, outfit="bark", cloth=BARK,
                      cloth_d=BARK_D, pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="ash",
                      hold=('kamandalu' if hold == '' else hold or None), old=True, thread=True)
    if key == 'ahalya':
        return person(skin=SKIN_WOMAN, hair="long", outfit="saree", cloth=MILK, cloth_d=WHITE_CLOTH_D, top="#e9dfc8",
                      pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="bindi", female=True)
    if key == 'parasurama':
        return parasurama(pose=pose, eye=eye, mouth_kind=mk, hold=('axe' if hold == '' else hold or None))
    if key == 'bharata':
        return bharata(pose=pose, eye=eye, sitting=sitting)
    if key == 'shatrughna':
        return shatrughna(pose=pose, eye=eye, sitting=sitting)
    if key == 'queen':
        c, cd, t = [(ROYAL_RED, ROYAL_RED_D, GOLD), (PURPLE_CLOTH, PURPLE_CLOTH_D, GOLD), (BLUE_CLOTH, BLUE_CLOTH_D, GOLD)][v % 3]
        return woman(cloth=c, cloth_d=cd, top=t, pose=pose, eye=eye, mouth_kind=mk, sitting=sitting, queen=True)
    if key == 'thadagai':
        return demon(pose=pose, hold=('trident' if hold == '' else hold or None), skin="#6e4a72", female=True,
                     eye='stern', mouth_kind='open', cloth="#4a2f3f")
    if key == 'demon':
        return demon(pose=pose, hold=('mace' if hold == '' else hold or None), eye='stern', mouth_kind='open')
    if key == 'rishyasringa':
        return (person(skin=SKIN_YOUNG, hair="jata", hair_color=BLACK_HAIR, outfit="bark", cloth=BARK, cloth_d=BARK_D,
                       pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="ash", thread=True) +
                G(P("M-3,-137 C-1,-150 4,-160 9,-166 C7,-154 5,-146 4,-136 Z", "#efe4c8", sw=1.6), y=34 if sitting else 0))
    if key == 'vishnu':
        body = person(skin=RAMA_BLUE, hair="long", outfit="dhoti", cloth=YELLOW_ROBE, cloth_d=OCHRE_D, sash=JEWEL_RED,
                      pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="namam", jewels=True, crown_kind="tall", thread=True)
        dy = 34 if sitting else 0
        return (G(hood_fan(), y=dy) if hood else '') + body + G(conch(.62), x=-44, y=-150 + dy) + G(discus(.52), x=46, y=-152 + dy)
    if key == 'shiva':
        dy = 34 if sitting else 0
        body = person(skin="#cdd7de", hair="jata", hair_color="#6b4a2e", outfit="dhoti", cloth="#e8a33a", cloth_d="#b5782a",
                      pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="ash", hold=('trident' if hold == '' else hold or None),
                      thread=True)
        return body + G(P("M2,-162 A9,9 0 1 0 14,-150 A7,7 0 1 1 2,-162 Z", "#fff6c8", sw=1.2) +
                        P("M-16,-106 C-8,-96 8,-96 16,-106", stroke="#5f8f3a", sw=4), y=dy)
    if key == 'brahma':
        return brahma_fig(pose='bless' if pose == 'down' else pose, sitting=sitting, eye=eye, mouth_kind=mk)
    if key == 'gods':
        return person(skin=SKIN_GOLD, hair="long", outfit="dhoti", cloth=MILK, cloth_d=WHITE_CLOTH_D, sash=GOLD,
                      pose=('bless' if pose == 'down' else pose), sitting=sitting, eye=eye, mouth_kind=mk, tilak="namam",
                      jewels=True, crown_kind="tall")
    if key == 'valmiki':
        return valmiki_fig(pose=pose if pose in ('down', 'bless', 'namaste', 'speak', 'think') else 'down', sitting=sitting,
                           eye=eye, mouth_kind=mk)
    if key == 'kamban':
        return kamban(pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, hold=('leaf' if hold == '' else hold or None))
    if key == 'patron':
        return patron(pose=pose, sitting=sitting, eye=eye)
    if key == 'king':
        c, cd = KING_CLOTH[v % 4]
        return person(skin=SKIN_KING, hair="none", moustache=BLACK_HAIR, outfit="robe", cloth=c, cloth_d=cd, top=GOLD,
                      pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="namam", jewels=True, crown_kind="tall")
    if key == 'sage':
        return person(skin=SKIN_SAGE, hair="jata", hair_color=GREY_HAIR, beard=GREY_HAIR, outfit="robe", cloth=OCHRE,
                      cloth_d=OCHRE_D, top=MILK, pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="ash",
                      hold=('kamandalu' if hold == '' and pose == 'down' else hold or None), old=True, thread=True)
    if key == 'brahmin':
        return person(skin=SKIN_YOUNG, hair="bun", outfit="dhoti", cloth=MILK, cloth_d=WHITE_CLOTH_D, pose=pose,
                      sitting=sitting, eye=eye, mouth_kind=mk, tilak="namam", thread=True,
                      hold=('pot' if hold == '' and pose == 'down' else hold or None))
    if key in ('women', 'musicians'):
        c, cd, t = WOMEN_CLOTH[v % len(WOMEN_CLOTH)]
        return woman(cloth=c, cloth_d=cd, top=t, pose=pose, eye=eye, mouth_kind=mk, sitting=sitting,
                     hold=(None if hold == '' else hold))
    if key == 'farmers':
        return person(skin="#b07448", hair="turban", hair_color=MILK, moustache=BLACK_HAIR, outfit="dhoti", cloth="#e9dfc8",
                      cloth_d="#cfc4a8", pose=pose, sitting=sitting, eye=eye, mouth_kind=mk,
                      hold=('basket' if hold == '' and pose == 'down' else hold or None))
    if key == 'soldiers':
        return person(skin=SKIN_YOUNG, hair="turban", hair_color=ROYAL_RED, moustache=BLACK_HAIR, outfit="dhoti", cloth=RUST,
                      cloth_d=RUST_D, top="#9aa3ad", pose=pose, sitting=sitting, eye=eye, mouth_kind=mk,
                      hold=('sword' if hold == '' and pose == 'down' else hold or None))
    # men, people
    return man(cloth=MILK, top=MAN_TOP[v % len(MAN_TOP)], pose=pose, eye=eye, mouth_kind=mk, sitting=sitting,
               hold=(None if hold == '' else hold))


BIG = {'jatayu': (.62, 236), 'sampati': (.62, 236), 'garuda': (.62, 220), 'kabandha': (.55, 240)}


def put(svg_, s, x, yh, female=False, sitting=False, flip=False, key=None):
    """Place a figure so that its head centre is at height yh. Birds and Kabandha stand on the ground instead."""
    if key in BIG:
        f, gy = BIG[key]
        return G(svg_, x=x, y=gy, s=s * f, flip=flip)
    hy = (-121 if female else -128) + (34 if sitting else 0)
    return G(svg_, x=x, y=yh - hy * s, s=s, flip=flip)


# ============================================================== settings
def sky_bits(tm, v, hy=150, side=None):
    out = []
    left = (v % 2 == 0) if side is None else side == 'left'
    if tm == 'night':
        mx = 46 if left else 194
        out.append(C(mx, 40, 30, "#fffbe6", stroke="none", opacity=.16))
        out.append(moon(mx, 40, 15, crescent=(v % 3 == 0)))
        pts = [(24, 26), (84, 16), (124, 40), (160, 18), (216, 64), (60, 70), (146, 76), (230, 22), (104, 64)]
        out.append(stars([(x, y, .42 + .12 * ((x + v) % 3)) for x, y in pts if abs(x - mx) > 26]))
    elif tm == 'evening':
        sx = 52 if left else 188
        out.append(C(sx, hy - 18, 34, "#ffd08a", stroke="none", opacity=.45))
        out.append(C(sx, hy - 18, 19, "#ff9e5e", stroke="none"))
        out.append(G(cloud(0, 0, .55, .55), x=240 - sx, y=46))
        out.append(flying_birds(240 - sx - 20, 70, 3, .9, "#6a4a3a"))
    elif tm == 'dawn':
        sx = 60 if left else 180
        out.append(rays(sx, hy, n=12, r1=12, r2=200, color="#fff0c8", opacity=.45))
        out.append(C(sx, hy, 22, "#ffbf6a", stroke="none"))
    elif tm == 'storm':
        out += [dark_cloud(50, 34, .85), dark_cloud(170, 26, 1.05), dark_cloud(112, 58, .75, "#5a6a85"),
                bolt(150, 40, .8), rain(0, 240, 70, 140, "#e6f2ff", 22)]
    elif tm == 'divine':
        out.append(rays(120, -20, n=12, r1=12, r2=280, color="#fff3c4", opacity=.5))
        out.append(cloud(44, 52, .7))
        out.append(cloud(196, 36, .6))
    elif tm == 'desert':
        sx = 190 if left else 50
        out.append(C(sx, 40, 34, "#fff3c0", stroke="none", opacity=.5) + C(sx, 40, 20, "#fff0b0", stroke="none"))
    else:
        out.append(cloud(52 if left else 188, 38, .6))
        out.append(cloud(170 if left else 70, 64, .42, .8))
    return "".join(out)


def room(v, tm, lay, court=False):
    wall = ['#f6e3c0', '#f3dccb', '#efe3c4', '#f1dfc9'][v % 4]
    out = [R(0, 0, T, 200, wall), R(0, 200, T, 40, "#e3c793"), P("M0,200 L240,200", stroke="#c9a46a", sw=2)]
    out += [P(f"M{i},200 L{i-40},240", stroke="#d6b47c", sw=1.2) for i in range(0, 300, 30)]
    wx = 120 if lay in ('two', 'none', 'thing') else (60 if v % 2 else 180)
    if not court:
        outside = {'night': "#2c3d6b", 'evening': "#f4c497", 'dawn': "#fbe0c0"}.get(tm, "#cfeaf7")
        out.append(P(f"M{wx-30},128 L{wx-30},64 Q{wx},26 {wx+30},64 L{wx+30},128 Z", outside, sw=2.4))
        if tm == 'night':
            out.append(moon(wx + 8, 64, 9, crescent=(v % 3 == 0)))
            out.append(stars([(wx - 14, 84, .35), (wx + 14, 100, .3), (wx - 6, 112, .3)]))
        elif tm == 'evening':
            out.append(C(wx, 112, 10, "#ff9e5e", stroke="none"))
        else:
            out.append(G(cloud(0, 0, .3), x=wx - 4, y=82))
        out.append(P(f"M{wx},34 L{wx},128 M{wx-30},92 L{wx+30},92", stroke="#a0784a", sw=2))
        out.append(R(wx - 36, 128, 72, 8, MARBLE, stroke=OUT, sw=2))
    else:
        out.append(P("M86,200 L154,200 L196,240 L44,240 Z", ROYAL_RED, stroke="none", opacity=.85))
        out.append(P("M86,200 L154,200 L196,240 L44,240 Z", stroke=GOLD, sw=2))
        out.append(garland(120, 22, 1.6))
    for x in (14, 226):
        out += [R(x - 11, 18, 22, 182, MARBLE, stroke=OUT, sw=2), R(x - 15, 12, 30, 10, GOLD, stroke=OUT, sw=1.8),
                R(x - 15, 190, 30, 10, GOLD, stroke=OUT, sw=1.8)]
    out.append(R(0, 0, T, 12, ROYAL_RED))
    out += [P(f"M{k},12 Q{k+15},30 {k+30},12", ROYAL_RED, sw=1.8) for k in range(0, T, 30)]
    if tm == 'night':
        out.append(R(0, 0, T, T, "#1d2b52", opacity=.18))
        out.append(G(lamp(.55), x=40 if wx > 120 else 200, y=200))
    return "".join(out)


def far_layer(extra, place):
    """Something on the horizon taken from the poem: mountains, a city, fields."""
    if 'mountain' in extra and place not in ('mountain', 'tents'):
        return mountain(60, 132, .5, '#a7bccb') + mountain(176, 128, .58, '#97b0c2')
    if 'city' in extra and place not in ('city', 'street'):
        return palace(120, 124, .36) + tower(58, 126, .4) + tower(184, 126, .4)
    if 'paddy' in extra and place in ('river', 'pond'):
        return hills(110, '#c7e29a', '#b7d9a0')
    return ''


def land(place, v, tm, lay, extra=()):
    out = [far_layer(extra, place)]
    if place == 'river' and v % 3 == 1:          # a river winding towards the viewer
        out.append(R(0, 120, T, 120, "#a9d68b"))
        out.append(P("M0,120 L240,120", stroke=GRASS_D, sw=2))
        out.append(P("M96,120 C80,150 30,170 20,240 L170,240 C150,190 150,150 132,120 Z", "url(#water)", stroke="none"))
        out += [P(f"M{x},{y} q6,-3 12,0 t12,0", stroke=WATER_L, sw=2) for x, y in ((92, 140), (70, 170), (90, 200), (40, 222))]
        out += [tree(200, 168, .55, 1), tree(226, 140, .4, 2), tree(28, 140, .42, 0), bush(214, 214, .6)]
    elif place == 'river' and v % 3 == 2:        # bathing steps (ghat) with a small shrine
        out.append(P("M0,126 C60,116 140,124 240,114 L240,152 L0,152 Z", "#9cc99a", stroke="none"))
        out += [tree(20, 140, .42, 1), tree(64, 140, .38, 2)]
        out.append(P("M0,146 C80,138 160,152 240,140 L240,240 L0,240 Z", "url(#water)", stroke="none"))
        out += [P(f"M{x},{y} q8,-4 16,0 t16,0", stroke=WATER_L, sw=2, opacity=.9) for x, y in ((20, 170), (80, 196), (40, 222), (110, 160))]
        for k in range(5):
            out.append(P(f"M{150 + k*8},{240 - k*20} L240,{240 - k*20} L240,{220 - k*20} L{158 + k*8},{220 - k*20} Z", "#e8d8b8", sw=1.6))
        out.append(G(R(-22, -40, 44, 40, "#f1dfbd", stroke=OUT, sw=2) + P("M-28,-40 L0,-62 L28,-40 Z", "#c9673d", sw=2) +
                     R(-8, -26, 16, 26, "#6b4a2e", stroke=OUT, sw=1.6, rx=6), x=212, y=140))
    elif place == 'river':
        out.append(P("M0,126 C60,116 140,124 240,114 L240,152 L0,152 Z", "#9cc99a", stroke="none"))
        for k, x in enumerate((18, 58, 186, 228)):
            out.append(tree(x + (v % 3) * 4, 140, .42, k))
        out.append(P("M0,146 C80,138 160,152 240,140 L240,206 C160,214 80,200 0,210 Z", "url(#water)", stroke="none"))
        out += [P(f"M{x},{y} q8,-4 16,0 t16,0", stroke=WATER_L, sw=2, opacity=.9)
                for x, y in ((20, 166), (120, 160), (180, 182), (60, 190), (200, 158))]
        out.append(P("M0,206 C80,198 160,214 240,204 L240,240 L0,240 Z", SAND, stroke="none"))
        out.append(grass_tufts([(16, 236), (226, 232)]))
    elif place == 'sea':
        out.append(P("M0,140 L240,140 L240,240 L0,240 Z", "url(#water)", stroke="none"))
        out += [P(f"M{x},{y} q8,-5 16,0 t16,0", stroke=WATER_L, sw=2.2, opacity=.9)
                for x, y in ((14, 160), (100, 154), (176, 168), (40, 190), (150, 196), (196, 222), (70, 226))]
        out.append(P("M0,140 L240,140", stroke="#ffffff", sw=2, opacity=.6))
    elif place == 'milksea':
        out.append(P("M0,150 C80,144 160,156 240,146 L240,240 L0,240 Z", "#fbfaf2", stroke="none"))
        out += [P(f"M{x},{y} q10,-6 20,0 t20,0", stroke="#d9dccd", sw=2.4) for x, y in ((10, 172), (120, 168), (60, 200), (170, 210), (20, 228))]
    elif place == 'pond':
        out.append(P("M0,124 C70,116 160,122 240,114 L240,160 L0,160 Z", "#9cc99a", stroke="none"))
        for k, x in enumerate((24, 70, 176, 222)):
            out.append(tree(x, 140, .4, k))
        out.append(R(0, 150, T, 90, GRASS))
        out.append(E(120, 196, 128, 44, "url(#water)", stroke=OUT, sw=2.2))
        out.append(E(120, 196, 120, 38, "none", stroke=WATER_L, sw=2, opacity=.7))
        for k, (x, y) in enumerate(((36, 200), (82, 222), (164, 224), (206, 198))):
            out.append(lotus(x, y, .7, "#f28aa6" if k % 2 else "#f7d0dc"))
    elif place == 'mountain':
        out.append(mountain(70, 168, .62, "#a7bccb"))
        out.append(mountain(186, 172, .7, "#97b0c2"))
        if v % 2:
            out.append(waterfall(208, 168, 64, 16))
        out.append(P("M0,160 C80,150 160,166 240,156 L240,240 L0,240 Z", "#9cc99a", stroke="none"))
        out.append(P("M0,190 C80,182 160,196 240,188 L240,240 L0,240 Z", GRASS, stroke="none"))
        out.append(tree(26, 200, .45, 1))
        out.append(tree(218, 206, .4, 2))
    elif place == 'forest':
        out.append(R(0, 150, T, 90, "#8fbf72"))
        for k, (x, y, s) in enumerate(((10, 160, .62), (60, 150, .55), (110, 146, .5), (160, 152, .55), (214, 160, .62), (36, 196, .7), (206, 200, .72))):
            out.append(tree(x + (v % 3) * 3, y, s, k))
        out.append(grass_tufts([(80, 232), (160, 236)]))
    elif place == 'garden':
        out.append(R(0, 150, T, 90, GRASS))
        out.append(blossom_tree(26, 176, .62, "#f7a8c0" if v % 2 else "#ffffff"))
        out.append(blossom_tree(214, 176, .62, "#ffd34e" if v % 2 else "#f7a8c0"))
        out.append(bush(120, 162, .7))
        out.append(petals([(40, 120, 10), (80, 98, -20), (200, 110, 30), (160, 90, 0), (110, 120, 45)]))
        for x in (14, 70, 172, 228):
            out.append(C(x, 228, 5, "#f28aa6", sw=1.2) + C(x + 10, 234, 4, "#ffd34e", sw=1.2))
    elif place == 'field':
        out.append(hills(132, "#b7d9b0", "#a3cf9c"))
        out.append(R(0, 160, T, 80, "#c7e29a"))
        out.append(P("M0,160 L240,160", stroke="#8fb86a", sw=2))
        out.append(paddy(6, 240, 184, rows=4, ripe=(v % 3 == 0)))
        out.append(coconut(22, 172, .52, 8))
        out.append(coconut(224, 176, .48, -8))
    elif place == 'desert':
        out.append(P("M0,150 C60,136 120,152 240,140 L240,240 L0,240 Z", "#e9c986", stroke="none"))
        out.append(P("M0,186 C70,172 150,192 240,178 L240,240 L0,240 Z", "#e2b96e", stroke="none"))
        out.append(dead_tree(30, 170, .7))
        out.append(dead_tree(212, 182, .6))
        out += [P(f"M{x},{y} q6,-4 12,0 t12,0", stroke="#f6e2b0", sw=2) for x, y in ((90, 160), (150, 170), (60, 210))]
        out.append(stone(184, 222, .35))
    elif place in ('city', 'street'):
        if place == 'city' and v % 3 == 1:     # a temple tower and houses
            out.append(gopuram(120, 172, .62))
            for x0, c in ((6, "#f1dfbd"), (178, "#f3e3c9")):
                out.append(R(x0, 120, 56, 70, c, stroke=OUT, sw=2) + P(f"M{x0-6},120 L{x0+28},96 L{x0+62},120 Z", "#c9673d", sw=2) +
                           R(x0 + 20, 150, 16, 40, "#6b4a2e", stroke=OUT, sw=1.6, rx=6))
            out += [flag(40, 100, ROYAL_RED, .5, 40, 2), flag(200, 100, "#e7a13d", .5, 40, 4)]
            out.append(R(0, 190, T, 50, "#e8d3a6"))
            out.append(P("M0,190 L240,190", stroke="#c9a46a", sw=2))
        elif place == 'city' and v % 3 == 2:   # the gate in the city wall, with the moat
            out.append(palace(120, 120, .42))
            out.append(city_wall(186, 0, 240, "#e3c48a", 56, gate_x=120))
            out.append(R(0, 186, T, 54, "url(#water)"))
            out.append(P("M90,186 L150,186 L156,240 L84,240 Z", "#c9a46a", sw=1.6))
            out += [lotus(30, 214, .6), lotus(206, 222, .6, "#f7d0dc")]
        elif place == 'city':
            out.append(palace(120, 150, .56))
            out.append(tower(28, 160, .62))
            out.append(tower(212, 160, .62))
            out.append(flag(28, 56, ROYAL_RED, .6, 50, v % 5))
            out.append(flag(212, 56, "#e7a13d", .6, 50, v % 5))
            out.append(city_wall(196, 0, 240, "#e3c48a", 46))
            out.append(R(0, 196, T, 44, "#e8d3a6"))
            out.append(P("M0,196 L240,196", stroke="#c9a46a", sw=2))
        else:
            out.append(R(0, 180, T, 60, "#e8d3a6"))
            for x0 in (0, 172):
                out.append(R(x0, 40, 68, 140, "#f1dfbd", stroke=OUT, sw=2))
                out.append(P(f"M{x0-6},40 L{x0+34},10 L{x0+74},40 Z", "#c9673d", sw=2))
                out.append(balcony(x0 + 34, 120, 46, 40))
            out.append(P("M0,180 L240,180", stroke="#c9a46a", sw=2))
            out += [flag(70, 120, ROYAL_RED, .5, 60, 2), flag(170, 120, "#e7a13d", .5, 60, 4)]
    elif place == 'yagna':
        out.append(R(0, 160, T, 80, "#d9c08f"))
        out.append(P("M0,160 L240,160", stroke="#b89a64", sw=2))
        out.append(tree(20, 166, .5, 1))
        out.append(tree(222, 168, .45, 2))
        fx = 120 if lay in ('none', 'two', 'thing') else (54 if v % 2 else 186)
        out.append(fire_altar(fx, 196, .62))
        out.append(P(f"M{fx},120 C{fx-10},100 {fx+10},84 {fx},60", stroke="#ffffff", sw=6, opacity=.5))
        out.append(G(kalasha(full=True), x=fx + 46 if fx < 200 else fx - 46, y=214, s=.6))
    elif place == 'wedding':
        out.append(R(0, 196, T, 44, "#e8cf9f"))
        out.append(P("M0,196 L240,196", stroke="#c9a46a", sw=2))
        for x in (14, 226):
            out += [R(x - 9, 34, 18, 162, "#f6e7c4", stroke=OUT, sw=2),
                    P(f"M{x-9},70 L{x+9},70 M{x-9},160 L{x+9},160", stroke=GOLD_D, sw=2)]
            out.append(banana(x + (16 if x < 120 else -16), 196, .55))
        out.append(P("M-10,36 L30,6 L210,6 L250,36 Z", ROYAL_RED, sw=2.2))
        out.append(P("M-10,36 L250,36", stroke=GOLD, sw=4))
        out += [P(f"M{k},38 l5,13 l5,-13", "#5aa060", sw=1.4) for k in range(0, 240, 18)]
        for k in (60, 180):
            out.append(P(f"M{k-36},50 Q{k},76 {k+36},50", stroke="#ffffff", sw=4))
            out.append(P(f"M{k-36},50 Q{k},76 {k+36},50", stroke="#f28aa6", sw=4, stroke_dasharray="3 6"))
        if lay in ('none', 'two', 'thing'):
            out.append(fire_altar(120, 222, .42))
    elif place == 'battle':
        out.append(R(0, 150, T, 90, '#d8c49a'))
        out.append(P('M0,150 L240,150', stroke='#b89a64', sw=2))
        out.append(E(60, 162, 70, 14, '#eadcb8', stroke='none', opacity=.85))
        out.append(E(190, 158, 60, 12, '#eadcb8', stroke='none', opacity=.85))
        out.append(flag(18, 166, ROYAL_RED, .55, 76, v % 4))
        out.append(flag(222, 166, '#3f3a52', .55, 76, (v + 2) % 4))
        for x, y, r in ((40, 226, -18), (196, 232, 24), (120, 236, 8)):
            out.append(G(P('M-14,0 L14,0', stroke='#8a5a2b', sw=2.4) + P('M14,-3 L21,0 L14,3 Z', '#cfd6dc', sw=1), x=x, y=y, rot=r))
    elif place == 'tents':
        out.append(mountain(120, 140, .7, "#a7bccb"))
        out.append(P("M0,140 C80,130 160,146 240,136 L240,240 L0,240 Z", "#a6cf8f", stroke="none"))
        out.append(tent(34, 180, .6))
        out.append(tent(206, 184, .56, stripe="#e7a13d"))
        out.append(tent(120, 160, .4, stripe=TEAL_CLOTH))
    elif place == 'sky':
        out.append(cloud(30, 200, 1.4))
        out.append(cloud(200, 210, 1.5))
        out.append(cloud(110, 230, 1.6))
    elif place == 'ashram':
        out.append(R(0, 170, T, 70, "#a9d68b"))
        out.append(P("M0,170 L240,170", stroke=GRASS_D, sw=2))
        hx = 192 if v % 2 == 0 else 48
        out.append(hut(hx, 176, .55))
        out.append(tree(240 - hx, 176, .55, 1))
    return "".join(out)


TIME_TINT = {'night': ("#14204a", .30), 'evening': ("#f08a4a", .10), 'storm': ("#2a3550", .22), 'dawn': ("#ffb070", .06)}


def setting(place, tm, v, lay, bare=False, extra=()):
    """Background for the picture; returns (svg, sky-gradient kind). bare: no sun/moon in the sky."""
    if place in ('palace', 'court'):
        return room(v, tm, lay, court=(place == 'court')), 'indoor'
    kind = {'desert': 'desert', 'milksea': 'divine', 'sky': 'divine'}.get(place) or \
        {'night': 'night', 'evening': 'evening', 'dawn': 'dawn', 'storm': 'storm', 'divine': 'divine'}.get(tm, 'day')
    out = [R(0, 0, T, T, "url(#sky)")]
    side = 'right' if lay == 'one' and v % 2 else None
    if not bare:
        out.append(sky_bits('desert' if kind == 'desert' else ('divine' if kind == 'divine' else tm), v, side=side))
    out.append(land(place, v, tm, lay, extra))
    if tm in TIME_TINT and kind not in ('divine', 'desert'):
        c, o = TIME_TINT[tm]
        out.append(R(0, 0, T, T, c, opacity=o))
        if tm == 'night' and not bare and place != 'wedding':
            out.append(sky_bits('night', v, side=side))
        elif tm == 'night':
            out.append(stars([(24, 26, .5), (84, 16, .4), (216, 64, .45), (60, 70, .4), (230, 22, .5)]))
    return "".join(out), kind


# ============================================================== subjects without people
ANIMAL_PLACE = {'elephant': 'city', 'horse': 'city', 'peacock': 'garden', 'swan': 'pond', 'parrot': 'garden',
                'cuckoo': 'garden', 'bees': 'garden', 'fish': 'river', 'deer': 'forest', 'monkey': 'forest',
                'lion': 'forest', 'snake': 'forest', 'cow': 'field', 'birds': 'pond', 'cat': 'milksea', 'camel': 'desert'}
INDOOR = ('palace', 'court')


def animal_main(key, v, joy=False):
    if key == 'elephant':
        return G(elephant(deco=v % 2 == 0, trunk='up' if joy or v % 3 == 0 else 'down', howdah=v % 4 == 1,
                          umbrella=v % 4 == 1), x=104, y=226, s=.92)
    if key == 'horse':
        return G(horse(color=["#c98b5a", "#f2efe6", "#8a5a3a"][v % 3], prance=v % 2 == 1), x=112, y=226, s=1.12)
    if key == 'peacock':
        return G(peacock(dance=True), x=124, y=222, s=1.45)
    if key == 'swan':
        return G(swan(), x=86, y=200, s=1.45) + G(swan(), x=164, y=214, s=1.2, flip=True)
    if key == 'parrot':
        return (P("M40,150 C90,140 150,150 210,136", stroke=OUT, sw=9) + P("M40,150 C90,140 150,150 210,136", stroke=TRUNK, sw=6) +
                G(parrot(), x=96, y=146, s=2.3) + G(parrot(flip=True), x=170, y=142, s=1.8) +
                C(60, 140, 6, LEAF, sw=1.4) + C(200, 128, 6, LEAF, sw=1.4))
    if key == 'cuckoo':
        return (P("M30,140 C90,128 150,140 220,126", stroke=OUT, sw=9) + P("M30,140 C90,128 150,140 220,126", stroke=TRUNK, sw=6) +
                G(songbird(), x=110, y=136, s=2.4) + C(190, 120, 7, LEAF, sw=1.4) + C(60, 128, 7, LEAF, sw=1.4) +
                note(160, 90, 1.4, "#7a4fa3") + note(186, 70, 1.1, "#7a4fa3"))
    if key == 'bees':
        return (G(lotus(0, 0, 2.4), x=120, y=210) + bee(70, 120, 2) + bee(168, 104, 2.2) + bee(150, 150, 1.8) + bee(92, 86, 1.6) +
                P("M70,120 q20,-30 50,-8", stroke=OUT, sw=1, stroke_dasharray="3 4"))
    if key == 'fish':
        return G(fish("#f08a3a", 2.2), x=80, y=170, rot=-25) + G(fish("#e2c040", 2.0, True), x=160, y=184, rot=20) + \
            G(fish("#e05a3a", 1.6), x=120, y=214) + splash(80, 150, 1.2)
    if key == 'deer':
        if CUR['k'] == 3:
            return G(KM.golden_deer(), x=110, y=222, s=1.9)
        return G(deer(), x=110, y=222, s=1.9)
    if key == 'monkey':
        return G(monkey(pose='wave'), x=120, y=214, s=2.6)
    if key == 'lion':
        return G(lion(), x=100, y=222, s=1.7)
    if key == 'snake':
        return G(cobra(), x=118, y=222, s=1.9)
    if key == 'cow':
        return G(bull(color="#f4efe4"), x=110, y=222, s=1.7)
    if key == 'birds':
        return G(crane("stand"), x=120, y=226, s=.9) + flying_birds(150, 60, 3, 1.3)
    if key == 'cat':
        return G(cat("lap"), x=120, y=196, s=1.7)
    return G(horse(), x=112, y=226, s=1.1)


THING_PLACE = {'ring': 'mountain', 'chudamani': 'garden', 'padukas': 'court', 'bridge': 'sea', 'pushpaka': 'sky',
               'fire': 'yagna', 'yagna': 'yagna', 'boat': 'river', 'lotus': 'pond', 'flowers': 'garden', 'garland': 'palace',
               'jewels': 'palace', 'crown': 'court', 'throne': 'court', 'umbrella': 'court', 'drum': 'city', 'music': 'palace',
               'lamp': 'palace', 'mirror': 'palace', 'food': 'palace', 'drink': 'palace', 'chariot': 'city', 'flags': 'city',
               'cradle': 'palace', 'birth': 'palace', 'leaf': 'ashram', 'stone': 'forest', 'weapons': 'city', 'conch': 'palace',
               'discus': 'sky', 'bow': 'court', 'arrow': 'forest', 'axe': 'forest', 'wedding': 'wedding', 'palace': 'city',
               'temple': 'city', 'house': 'city', 'gate': 'city', 'wall': 'city', 'tent': 'tents'}


def thing_main(key, v, broken=False):
    if key == 'ring':
        return C(120, 130, 70, "url(#glow)", stroke="none") + G(KM.ring(), x=120, y=140, s=3.2)
    if key == 'chudamani':
        return C(120, 130, 70, "url(#glow)", stroke="none") + G(KM.chudamani(), x=120, y=140, s=3.4)
    if key == 'padukas':
        return G(cushion(130), x=120, y=200) + G(KM.padukas(), x=120, y=196, s=2.2)
    if key == 'bridge':
        return KM.bridge(-10, 250, 186, 3) + G(KM.vanara(pose='raise'), x=120, y=196, s=.5)
    if key == 'pushpaka':
        return G(KM.pushpaka(), x=120, y=170, s=.55)
    if key == 'bow':
        if broken:
            return (G(P("M0,-70 Q-26,-30 -6,0", stroke=OUT, sw=11) + P("M0,-70 Q-26,-30 -6,0", stroke="#6b4421", sw=7), x=86, y=200, rot=-30) +
                    G(P("M0,70 Q-26,30 -6,0", stroke=OUT, sw=11) + P("M0,70 Q-26,30 -6,0", stroke="#6b4421", sw=7), x=160, y=110, rot=-30) +
                    sparkle(122, 150, 2, "#fff1a0") + sparkle(100, 120, 1.2, "#fff1a0") + sparkle(146, 176, 1.2, "#fff1a0"))
        return (R(36, 196, 168, 16, GOLD, stroke=OUT, sw=2, rx=4) + R(48, 212, 12, 20, GOLD_D, stroke=OUT, sw=1.8) +
                R(180, 212, 12, 20, GOLD_D, stroke=OUT, sw=1.8) +
                P("M24,190 Q120,110 216,190", stroke=OUT, sw=12) + P("M24,190 Q120,110 216,190", stroke="#6b4421", sw=8) +
                P("M24,190 L216,190", stroke="#efe6cc", sw=2) + C(24, 190, 5, GOLD, sw=1.6) + C(216, 190, 5, GOLD, sw=1.6) +
                sparkle(120, 120, 1.4))
    if key == 'arrow':
        return arrow(40, 190, 170, 80, 4) + arrow(70, 210, 200, 110, 4) + arrow(30, 150, 150, 60, 3.5)
    if key == 'axe':
        return G(big_axe(), x=120, y=150, s=1.4, rot=20)
    if key in ('fire', 'yagna'):
        return G(fire_altar(0, 0, 1.0), x=120, y=224) + G(kalasha(full=True), x=36, y=226, s=.7) + \
            P("M120,96 C108,70 132,54 118,24", stroke="#ffffff", sw=8, opacity=.45)
    if key == 'lotus':
        return lotus(80, 210, 1.7) + lotus(160, 220, 1.4, "#f7d0dc") + lotus(122, 190, 1.2)
    if key == 'flowers':
        return (bush(120, 226, 1.4, LEAF) + "".join(C(x, y, 7, c, sw=1.4) + C(x, y, 2.6, "#ffd34e", stroke="none") for x, y, c in
                ((84, 176, "#f28aa6"), (110, 160, "#ffffff"), (140, 168, "#f7a8c0"), (166, 184, "#ffffff"), (100, 196, "#f7a8c0"), (150, 200, "#f28aa6"))) +
                petals([(60, 120, 10), (90, 96, -20), (170, 110, 30), (196, 140, 0), (130, 80, 45)]))
    if key == 'garland':
        return garland(120, 70, 3.2) + garland(120, 150, 2.2, "#ffd34e", "#ffffff")
    if key == 'jewels':
        return (P("M40,200 C40,184 200,184 200,200 C200,214 40,214 40,200 Z", ROYAL_RED, sw=2.2) + G(necklace_big(), x=120, y=110, s=1.9) +
                C(70, 190, 7, GOLD, sw=1.6) + C(170, 190, 7, GOLD, sw=1.6) + C(70, 190, 3, JEWEL_RED, stroke="none") +
                C(170, 190, 3, JEWEL_RED, stroke="none"))
    if key == 'crown':
        return G(cushion(120), x=120, y=196) + G(crown("tall", y=0), x=120, y=186, s=2.4)
    if key in ('throne', 'umbrella'):
        return G(throne(110), x=120, y=196, s=1.0) + G(white_umbrella(), x=120, y=100, s=1.1)
    if key == 'drum':
        return drum(80, 226, 2.4) + drum(164, 226, 2.0) + P("M60,100 L100,140 M184,96 L150,136", stroke="#8a5a2b", sw=5) + \
            note(196, 60, 1.3, OUT) + note(40, 70, 1.1, OUT)
    if key == 'music':
        return G(veena(), x=120, y=150, s=1.8) + note(50, 70, 1.6) + note(196, 60, 1.4) + note(184, 120, 1.1)
    if key == 'lamp':
        return C(120, 120, 70, "url(#glow)", stroke="none") + G(lamp(1.6), x=120, y=226)
    if key == 'mirror':
        return mirror(120, 220, 2.6)
    if key == 'food':
        return leaf_meal(120, 206, 2.2) + G(pot(), x=200, y=224, s=.9) + G(kalasha(full=True), x=40, y=226, s=.6)
    if key == 'drink':
        return G(pot(color="#9a5a3a"), x=96, y=226, s=1.7) + G(cup(), x=168, y=220, s=2) + G(cup(), x=196, y=230, s=1.5)
    if key == 'boat':
        return G(boat(), x=120, y=196, s=1.3)
    if key == 'chariot':
        return G(chariot(), x=92, y=226, s=.82)
    if key == 'flags':
        return flag(60, 220, ROYAL_RED, 1.4, 120, 4) + flag(130, 226, "#e7a13d", 1.2, 120, 2) + flag(196, 224, TEAL_CLOTH, 1.1, 120, 6)
    if key in ('cradle', 'birth'):
        return G(cradle(0, 0), x=120, y=220, s=1.15) + G(baby(), x=120, y=170, s=1.4)
    if key == 'leaf':
        return olai_stack(120, 210, 2.4) + P("M160,120 L200,70", stroke="#8a8a8a", sw=4)
    if key == 'stone':
        return stone(120, 222, 1.6, glow=True)
    if key == 'weapons':
        return G(sword(), x=96, y=200, s=1.6, rot=-30) + G(spear(), x=150, y=200, s=1.3, rot=25) + G(shield(), x=120, y=196, s=1.4)
    if key == 'conch':
        return C(120, 140, 70, "url(#glow)", stroke="none") + G(conch(), x=120, y=150, s=2.6)
    if key == 'discus':
        return G(discus(), x=120, y=130, s=2.4)
    if key in ('palace', 'temple', 'house', 'gate', 'wall'):
        return ""
    return ""


ACC_SLOT = {'ring': 'ground', 'chudamani': 'ground', 'padukas': 'ground', 'moon': 'sky', 'sun': 'sky', 'stars': 'sky', 'bees': 'sky', 'birds': 'sky', 'parrot': 'sky', 'cuckoo': 'sky',
            'rainbow': 'sky', 'music': 'sky', 'flowers': 'sky', 'discus': 'sky', 'conch': 'sky', 'cloud': 'sky', 'arrow': 'sky',
            'garland': 'sky', 'lotus': 'ground', 'swan': 'ground', 'fish': 'ground', 'lamp': 'ground', 'drum': 'ground',
            'jewels': 'ground', 'food': 'ground', 'drink': 'ground', 'mirror': 'ground', 'crown': 'ground', 'flags': 'ground',
            'fire': 'ground', 'peacock': 'ground', 'umbrella': 'sky', 'wind': 'sky', 'lightning': 'sky', 'rain': 'sky',
            'deer': 'ground', 'cat': 'ground', 'monkey': 'ground', 'cow': 'ground', 'leaf': 'ground',
            'elephant': 'ground', 'horse': 'ground', 'boat': 'ground', 'chariot': 'ground',
            'farmers': 'ground', 'women': 'ground', 'men': 'ground', 'people': 'ground', 'brahmin': 'ground',
            'soldiers': 'ground', 'musicians': 'ground'}


def accent(key, x, y, tm):
    if key == 'moon':
        return C(x, y, 24, "#fffbe6", stroke="none", opacity=.25) + moon(x, y, 13, crescent=False)
    if key == 'sun':
        return sun(x, y, 14)
    if key == 'stars':
        return stars([(x - 14, y - 6, .5), (x + 10, y - 12, .4), (x + 2, y + 10, .45)])
    if key == 'bees':
        return bee(x - 10, y + 4, 1.4) + bee(x + 12, y - 8, 1.2)
    if key == 'birds':
        return flying_birds(x - 18, y, 3, .9)
    if key == 'parrot':
        return G(parrot(), x=x, y=y + 22, s=1.1)
    if key == 'cuckoo':
        return G(songbird(), x=x, y=y + 16, s=1.1)
    if key == 'rainbow':
        return G(rainbow(0, 0, 60, .7), x=x, y=y + 30, s=.6)
    if key == 'music':
        return note(x - 8, y + 6, 1.1) + note(x + 10, y - 6, .9)
    if key == 'flowers':
        return petals([(x - 14, y, 10), (x, y - 12, -20), (x + 14, y + 4, 30), (x + 4, y + 14, 0)])
    if key == 'discus':
        return G(discus(), x=x, y=y, s=.7)
    if key == 'conch':
        return G(conch(), x=x, y=y, s=.8)
    if key == 'cloud':
        return cloud(x, y + 6, .5)
    if key == 'arrow':
        return arrow(x - 24, y + 16, x + 18, y - 12, 2.6)
    if key == 'garland':
        return garland(x, y - 8, .9)
    if key == 'umbrella':
        return G(white_umbrella(), x=x, y=y + 34, s=.5)
    if key == 'wind':
        return wind_lines(x - 30, y, .7)
    if key == 'lightning':
        return bolt(x, y - 20, .6)
    if key == 'rain':
        return dark_cloud(x, y - 8, .5) + rain(x - 24, x + 24, y, y + 30, "#bcd6f0", 10)
    if key == 'lotus':
        return lotus(x, y, .9)
    if key == 'swan':
        return G(swan(), x=x, y=y, s=.7)
    if key == 'fish':
        return G(fish("#f08a3a", 1.2), x=x - 8, y=y - 6, rot=-20) + G(fish("#e2c040", 1.0, True), x=x + 10, y=y + 6)
    if key == 'lamp':
        return C(x, y - 26, 20, "url(#glow)", stroke="none") + G(lamp(.62), x=x, y=y + 10)
    if key == 'drum':
        return drum(x, y + 12, .9)
    if key == 'jewels':
        if tm == 'water':
            return sparkle(x - 12, y, .9, '#fff6c8') + sparkle(x + 10, y - 8, .7, '#fff6c8') + C(x, y + 6, 3, '#fffaf0', sw=1) + C(x + 8, y + 8, 3, '#fffaf0', sw=1)
        return G(necklace_big(), x=x, y=y - 14, s=.55)
    if key == 'food':
        return leaf_meal(x, y, .6)
    if key == 'drink':
        return G(cup(), x=x, y=y + 10, s=1.1)
    if key == 'mirror':
        return mirror(x, y + 12, .7)
    if key == 'crown':
        return G(crown("tall", y=0), x=x, y=y + 10, s=.8)
    if key == 'flags':
        return flag(x - 10, y + 14, ROYAL_RED, .5, 50, 3)
    if key == 'fire':
        return fire_altar(x, y + 14, .35)
    if key == 'peacock':
        return G(peacock(dance=False), x=x, y=y + 14, s=.6)
    if key == 'deer':
        return G(deer(), x=x, y=y + 14, s=.6)
    if key == 'cat':
        return G(cat("sit"), x=x, y=y + 12, s=.6)
    if key == 'monkey':
        return G(monkey(), x=x, y=y + 12, s=.8)
    if key == 'cow':
        return G(bull(), x=x, y=y + 14, s=.45)
    if key == 'leaf':
        return G(palm_leaf(), x=x, y=y, s=.8)
    if key == 'ring':
        return G(KM.ring(), x=x, y=y, s=1.1)
    if key == 'chudamani':
        return G(KM.chudamani(), x=x, y=y, s=1.1)
    if key == 'padukas':
        return G(KM.padukas(), x=x, y=y + 14, s=.8)
    if key in ('farmers', 'women', 'men', 'people', 'brahmin', 'soldiers', 'musicians'):
        k2 = 'men' if key == 'people' else key
        pose = {'women': 'wave', 'musicians': 'raise', 'farmers': 'down'}.get(key, 'walk')
        return G(fig(k2, pose, 'happy', 'smile', v=x), x=x, y=y + 22, s=.36)
    if key == 'elephant':
        return G(elephant(deco=False), x=x - 6, y=y + 16, s=.3)
    if key == 'horse':
        return G(horse(), x=x - 4, y=y + 16, s=.34)
    if key == 'boat':
        return G(boat(), x=x, y=y + 8, s=.42)
    if key == 'chariot':
        return G(chariot(), x=x - 10, y=y + 16, s=.26)
    return ""


# ============================================================== per-padalam context
PAD = {
    0: dict(place='ashram', actors=['kamban'], king='dasaratha', sage='valmiki', w={'group': .5}, mmin=99, amin=1.5, stick=2.0),
    1: dict(place='river', actors=[], w={'group': .25, 'char': .5}, land=True, amin=2.5, stick=1.2),
    2: dict(place='field', actors=[], w={'group': .7}, land=True, amin=1.6, stick=1.2),
    3: dict(place='city', actors=[], w={'group': .7}, land=True, amin=1.6, stick=1.2),
    4: dict(place='court', actors=['dasaratha'], king='dasaratha', sage='vasishtha', stick=3.5),
    5: dict(place='court', actors=['dasaratha'], king='dasaratha', sage='vasishtha', stick=2.2),
    6: dict(place='court', actors=['dasaratha', 'vishwamitra'], king='dasaratha', sage='vishwamitra', stick=3.5),
    7: dict(place='desert', actors=['rama', 'vishwamitra'], king='dasaratha', sage='vishwamitra'),
    8: dict(place='yagna', actors=['vishwamitra', 'rama'], king='dasaratha', sage='vishwamitra'),
    9: dict(place='forest', actors=['rama', 'vishwamitra'], king='dasaratha', sage='vishwamitra'),
    10: dict(place='city', actors=['rama'], king='janaka', sage='vishwamitra'),
    11: dict(place='court', actors=['janaka', 'vishwamitra'], king='janaka', sage='shatananda', stick=3.5),
    12: dict(place='court', actors=['rama'], king='janaka', sage='vishwamitra', stick=3.5),
    13: dict(place='city', actors=['dasaratha'], king='dasaratha', sage='vasishtha'),
    14: dict(place='tents', actors=[], king='dasaratha', sage='vasishtha', w={'group': .8}, land=True, amin=1.6, stick=1.2),
    15: dict(place='mountain', actors=[], king='dasaratha', sage='vasishtha', w={'group': .8}, land=True, amin=1.6, stick=1.2),
    16: dict(place='garden', actors=['women'], king='dasaratha', sage='vasishtha'),
    17: dict(place='pond', actors=['women'], king='dasaratha', sage='vasishtha'),
    18: dict(place='palace', time='night', actors=['women'], king='dasaratha', sage='vasishtha', stick=3.0),
    19: dict(place='city', actors=['dasaratha', 'janaka'], king='janaka', sage='vasishtha'),
    20: dict(place='street', actors=['rama'], king='dasaratha', sage='vasishtha'),
    21: dict(place='palace', actors=['sita'], king='janaka', sage='vasishtha', stick=3.5),
    22: dict(place='wedding', actors=['rama', 'sita'], king='janaka', sage='vasishtha', stick=3.0),
    23: dict(place='forest', actors=['parasurama'], king='dasaratha', sage='vasishtha'),
}

def _p(place, actors, king='dasaratha', sage='vasishtha', **kw):
    d = dict(place=place, actors=actors, king=king, sage=sage, stick=kw.pop('stick', 2.4))
    d.update(kw)
    return d


H = dict(hermit=True)
PADS = {1: PAD, 2: {
    1: _p('court', ['dasaratha']), 2: _p('palace', ['manthara'], time='night'), 3: _p('palace', ['kaikeyi'], time='night'),
    4: _p('palace', ['rama']), 5: _p('forest', ['rama'], **H), 6: _p('river', ['rama', 'sita'], **H),
    7: _p('river', ['guha', 'rama'], **H), 8: _p('mountain', ['rama', 'sita'], **H), 9: _p('city', ['bharata'], stick=2.0),
    10: _p('forest', ['bharata'], **H), 11: _p('river', ['guha', 'bharata'], **H), 12: _p('mountain', ['bharata', 'rama'], **H),
}, 3: {
    1: _p('forest', ['rama', 'viradha'], king='rama', sage='sage', **H), 2: _p('ashram', ['rama'], king='rama', sage='sage', **H),
    3: _p('ashram', ['agastya', 'rama'], king='rama', sage='agastya', **H), 4: _p('forest', ['jatayu', 'rama'], king='rama', sage='sage', **H),
    5: _p('ashram', ['surpanakha', 'rama'], king='rama', sage='sage', **H), 6: _p('forest', ['rama', 'khara'], king='rama', sage='sage', **H),
    7: _p('court', ['surpanakha', 'ravana'], king='ravana', sage='sage', **H), 8: _p('forest', ['ravana'], king='ravana', sage='sage', **H),
    9: _p('ashram', ['ravana', 'sita'], king='ravana', sage='sage', **H), 10: _p('forest', ['jatayu', 'ravana'], king='ravana', sage='sage', **H),
    11: _p('forest', ['lakshmana'], king='rama', sage='sage', **H), 12: _p('forest', ['kabandha', 'rama'], king='rama', sage='sage', **H),
    13: _p('ashram', ['sabari', 'rama'], king='rama', sage='sage', **H),
}, 4: {
    1: _p('pond', ['rama', 'lakshmana'], king='rama', sage='sage', **H), 2: _p('mountain', ['hanuman', 'rama'], king='sugriva', **H),
    3: _p('mountain', ['sugriva', 'rama'], king='sugriva', **H), 4: _p('forest', ['rama'], king='sugriva', **H),
    5: _p('forest', ['rama'], king='sugriva', **H), 6: _p('mountain', ['sugriva', 'rama'], king='sugriva', **H),
    7: _p('forest', ['vali', 'rama'], king='vali', **H), 8: _p('court', ['sugriva'], king='sugriva', **H),
    9: _p('mountain', ['rama', 'lakshmana'], king='sugriva', time='storm', **H), 10: _p('city', ['lakshmana', 'tara'], king='sugriva', **H),
    11: _p('mountain', ['sugriva', 'rama'], king='sugriva', **H), 12: _p('mountain', ['hanuman', 'rama'], king='sugriva', **H),
    13: _p('forest', ['hanuman', 'angada'], king='sugriva', **H), 14: _p('forest', ['angada', 'hanuman'], king='sugriva', **H),
    15: _p('mountain', ['sampati', 'angada'], king='sugriva', **H), 16: _p('mountain', ['hanuman', 'jambavan'], king='sugriva', **H),
}, 5: {
    1: _p('sea', ['hanuman'], king='ravana', **H), 2: _p('city', ['hanuman'], king='ravana', time='night', **H),
    3: _p('garden', ['sita', 'ravana'], king='ravana', **H), 4: _p('garden', ['hanuman', 'sita'], king='ravana', **H),
    5: _p('garden', ['sita', 'hanuman'], king='ravana', **H), 6: _p('garden', ['hanuman'], king='ravana', **H),
    7: _p('garden', ['hanuman', 'demon'], king='ravana', **H), 8: _p('city', ['hanuman', 'demon'], king='ravana', **H),
    9: _p('city', ['hanuman', 'demon'], king='ravana', **H), 10: _p('city', ['hanuman', 'demon'], king='ravana', **H),
    11: _p('city', ['hanuman', 'indrajit'], king='ravana', **H), 12: _p('court', ['hanuman', 'ravana'], king='ravana', **H),
    13: _p('city', ['hanuman'], king='ravana', **H), 14: _p('mountain', ['hanuman', 'rama'], king='sugriva', **H),
}, 6: {}}
_Y = ['sea:rama', 'court:ravana', 'court:vibhishana', 'sea:vibhishana,rama', 'sea:rama,vibhishana', 'sea:rama',
      'sea:nala', 'court:ravana', 'mountain:rama', 'city:ravana', 'city:sugriva,ravana', 'battle:rama,sugriva',
      'court:angada,ravana', 'battle:rama,ravana', 'battle:kumbhakarna,rama', 'garden:sita,ravana', 'battle:lakshmana,demon',
      'battle:indrajit,lakshmana', 'battle:vanara,demon', 'battle:rama,demon', 'battle:indrajit', 'battle:sita,trijata',
      'mountain:hanuman', 'palace:ravana', 'battle:indrajit', 'yagna:indrajit,lakshmana', 'battle:lakshmana,indrajit',
      'court:ravana', 'city:ravana', 'battle:rama,demon', 'battle:lakshmana,ravana', 'battle:vanara', 'battle:ravana',
      'battle:ravana', 'battle:rama', 'battle:rama,ravana', 'sky:rama,sita', 'court:rama,sita', 'court:rama,hanuman']
for _i, _d in enumerate(_Y, start=1):
    _pl, _a = _d.split(':')
    _pl = {'battle': 'battle'}.get(_pl, _pl)
    PADS[6][_i] = _p(_pl, _a.split(','), king='rama' if _i >= 37 else 'ravana', hermit=_i < 38, time='storm' if _i in (36,) else 'day')

PLACE_FEATS = {
    'river': {'river': 1, 'water': .4, 'boat': .6, 'fish': .2},
    'sea': {'sea': .6, 'boat': .3},
    'milksea': {'milksea': 2},
    'pond': {'pond': 1, 'lotus': .3, 'swan': .4, 'water': .4},
    'mountain': {'mountain': 1, 'waterfall': 1},
    'forest': {'forest': 1, 'tree': .4, 'deer': .3, 'monkey': .3, 'lion': .2},
    'garden': {'garden': 1, 'flowers': .3, 'bees': .3, 'cuckoo': .3, 'parrot': .3, 'peacock': .2},
    'field': {'paddy': 1, 'sugarcane': .8, 'farmers': .6, 'cow': .3},
    'desert': {'desert': 1.2},
    'city': {'city': .7, 'wall': .9, 'gate': .7, 'flags': .4, 'house': .4},
    'palace': {'palace': .9, 'mirror': .5, 'lamp': .3, 'cradle': .5, 'jewels': .15},
    'court': {'throne': 1, 'crown': .5, 'umbrella': .3},
    'wedding': {'wedding': 1.3},
    'yagna': {'yagna': 1.2, 'fire': .3},
    'tents': {'tent': 1},
    'battle': {'battle': .5, 'weapons': .5, 'arrow': .3, 'soldiers': .4},
    'sky': {},
    'ashram': {},
    'street': {},
}
PLACE_LABEL = {'river': 'ஆறு', 'sea': 'கடல்', 'milksea': 'பாற்கடல்', 'pond': 'பொய்கை', 'mountain': 'மலை', 'forest': 'காடு',
               'garden': 'சோலை', 'field': 'வயல்', 'desert': 'பாலை நிலம்', 'city': 'நகரம்', 'palace': 'அரண்மனை',
               'court': 'அரசவை', 'wedding': 'மணமண்டபம்', 'yagna': 'வேள்விச் சாலை', 'tents': 'பாசறை', 'sky': 'வானுலகம்',
               'ashram': 'தவச்சாலை', 'street': 'வீதி', 'battle': 'போர்க்களம்'}
TIME_LABEL = {'night': 'இரவு', 'evening': 'மாலைப் பொழுது', 'dawn': 'விடியல்', 'storm': 'கருமேகம்'}
NAME = {'king': 'மன்னன்', 'sage': 'முனிவர்', 'women': 'மகளிர்', 'men': 'ஆடவர்', 'farmers': 'உழவர்', 'soldiers': 'வீரர்கள்',
        'musicians': 'கலைஞர்', 'people': 'மக்கள்', 'brahmin': 'அந்தணர்', 'gods': 'தேவர்கள்'}
DEITIES = ('gods', 'brahma', 'shiva')
SKY_FIGS = ('gods', 'brahma', 'shiva')
NATURE_MAIN = ('moon', 'sun', 'stars', 'cloud', 'rain', 'lightning', 'rainbow', 'wind', 'waterfall', 'sky', 'dust')


def kinds(sc, kind):
    return sorted(((k, v) for k, v in sc.items() if F[k][0] == kind), key=lambda x: -x[1])


LAND_KEYS = ('river', 'sea', 'milksea', 'pond', 'mountain', 'waterfall', 'forest', 'garden', 'tree', 'paddy', 'sugarcane',
             'desert', 'city')
OUTDOOR = {'river', 'sea', 'milksea', 'pond', 'mountain', 'forest', 'garden', 'field', 'desert', 'tents', 'ashram', 'sky',
           'city', 'street', 'yagna', 'wedding', 'battle'}
WATERY = {'river', 'sea', 'pond', 'milksea', 'garden'}
ROYAL = {'palace', 'court', 'city', 'street', 'wedding', 'tents'}
ACC_OK = {
    'moon': OUTDOOR, 'sun': OUTDOOR, 'stars': OUTDOOR, 'birds': OUTDOOR - {'sky', 'milksea'}, 'cloud': OUTDOOR,
    'rain': OUTDOOR - {'sky'}, 'lightning': OUTDOOR - {'sky'}, 'rainbow': OUTDOOR, 'wind': OUTDOOR - {'sky', 'milksea'},
    'music': None, 'flowers': None,
    'bees': OUTDOOR - {'desert', 'sea', 'sky', 'milksea'}, 'parrot': (OUTDOOR - {'desert', 'sea', 'sky', 'milksea'}) | {'palace'},
    'cuckoo': {'garden', 'forest', 'mountain', 'field', 'river', 'pond', 'city', 'street', 'ashram'},
    'peacock': {'garden', 'forest', 'mountain', 'city', 'street', 'ashram', 'field', 'river', 'pond'},
    'deer': {'forest', 'mountain', 'garden', 'ashram', 'field', 'river', 'desert'},
    'monkey': {'forest', 'mountain', 'garden', 'ashram'}, 'cow': {'field', 'river', 'ashram', 'city', 'street'},
    'lotus': WATERY, 'swan': {'river', 'pond', 'garden', 'sea'}, 'fish': {'river', 'pond', 'sea'}, 'boat': {'river', 'sea'},
    'elephant': {'city', 'street', 'forest', 'mountain', 'river', 'field', 'tents'},
    'horse': {'city', 'street', 'field', 'tents', 'desert', 'forest'}, 'chariot': {'city', 'street', 'field', 'tents'},
    'lamp': ROYAL | {'yagna', 'ashram'}, 'mirror': {'palace'}, 'jewels': {'palace', 'court', 'wedding'},
    'crown': {'palace', 'court', 'wedding'}, 'umbrella': ROYAL, 'garland': None, 'drum': ROYAL | {'yagna', 'field', 'mountain'},
    'food': {'palace', 'court', 'wedding', 'tents', 'garden', 'field', 'ashram'}, 'drink': {'palace', 'tents', 'garden', 'mountain'},
    'conch': {'palace', 'court', 'wedding', 'sky', 'milksea', 'yagna', 'city'}, 'discus': {'sky', 'milksea', 'palace', 'court'},
    'flags': {'city', 'street', 'tents', 'wedding', 'field'}, 'fire': {'yagna', 'wedding', 'ashram', 'desert', 'forest'},
    'arrow': {'desert', 'forest', 'yagna', 'mountain', 'sky'}, 'leaf': {'ashram', 'palace', 'court'},
    'farmers': {'field', 'river', 'pond', 'city', 'street'}, 'women': OUTDOOR - {'sky', 'milksea', 'desert'},
    'men': OUTDOOR - {'sky', 'milksea'}, 'people': OUTDOOR - {'sky', 'milksea', 'desert'},
    'brahmin': {'river', 'city', 'street', 'yagna', 'ashram', 'field'}, 'soldiers': {'city', 'street', 'tents', 'field', 'desert'},
    'musicians': {'city', 'street', 'garden', 'tents', 'mountain'},
}
INDOOR_THINGS = {'jewels', 'crown', 'mirror', 'lamp', 'food', 'drink', 'cradle', 'birth', 'music', 'throne', 'umbrella', 'conch', 'garland'}
# a few poems everyone knows get a hand-made plan
OVERRIDE = {
    1: dict(combo='invocation', place='sky', tm='divine'),
    4: dict(actors=[], main='cat', place='milksea', tm='day'),
    514: dict(combo='balcony', place='street', tm='day'),
    699: dict(combo='bowbreak', place='court', tm='day'),
    475: dict(actors=['vishwamitra', 'rama'], place='forest', tm='day'),
}


def decide(n, pp, sc, kdm=1):
    """Turn the feature scores of one poem into a picture plan. pp is offset by 100 outside பால காண்டம்."""
    pad = PADS[kdm][pp if kdm == 1 else pp - 100]
    w = pad.get('w', {})
    sc = dict(sc)

    def fold(src, dst, f=1.0):
        if src in sc:
            sc[dst] = sc.get(dst, 0) + sc.pop(src) * f
    # ---- name the generic people for this padalam, and fold aliases
    if pp >= 6:
        fold('vishnu', 'rama')
    if pp == 7:
        fold('demon', 'thadagai', .8)
    if pp == 12:
        fold('shiva', 'bow', .8)
    if pp != 0:
        sc.pop('kamban', None)
        sc.pop('valmiki', None)
    if pp >= 4 and 'king' in sc:
        kname = pad['king']
        if kname in sc and pp in (19, 22):
            kname = 'dasaratha' if kname == 'janaka' else 'janaka'
        fold('king', kname, .9)
    if pp >= 5 and 'sage' in sc and not (pp == 5 and sc.get('rishyasringa')):
        fold('sage', pad['sage'], .9)
    for k in ('gods', 'brahma', 'shiva'):
        if k in sc:
            sc[k] *= .6
    fold('vanara', 'monkey')
    # people who only appear later in the story are just being mentioned: leave them out of the picture
    if kdm < 4:
        for x in ('vali', 'sugriva', 'hanuman', 'angada', 'jambavan', 'tara', 'nala', 'sampati'):
            sc.pop(x, None)
    if kdm < 3:
        for x in ('ravana', 'vibhishana', 'kumbhakarna', 'indrajit', 'mandodari', 'trijata', 'surpanakha', 'khara',
                  'maricha', 'jatayu', 'sabari', 'kabandha', 'viradha', 'agastya'):
            sc.pop(x, None)
    for k in list(sc):
        kd = F[k][0]
        if kd in w:
            sc[k] *= w[kd]
    amin = pad.get('amin', 1.0)
    chars = [(k, v) for k, v in kinds(sc, 'char') if v >= amin]
    groups = [(k, v) for k, v in kinds(sc, 'group') if v >= max(amin, 1.0)]
    animals = [(k, v) for k, v in kinds(sc, 'animal') if v >= 1]
    things = [(k, v) for k, v in kinds(sc, 'thing') if v >= 1 and k not in ('broken', 'palace', 'temple', 'house', 'gate', 'wall', 'tent', 'wedding')]
    nat = [(k, v) for k, v in kinds(sc, 'nature') if v >= 1]
    mood = dict(kinds(sc, 'mood'))
    act = dict(kinds(sc, 'act'))
    ov = OVERRIDE.get(n, {})

    # ---- people in the picture
    actors = [k for k, v in chars[:2]]
    sky_fig = None
    for k in list(actors):
        if k in SKY_FIGS and (len(actors) > 1 or groups):
            actors.remove(k)
            sky_fig = sky_fig or k
    ladies = False
    if len(actors) < 2 and groups:
        g = groups[0][0]
        if pp == 20 and g == 'women' and actors:
            ladies = True
        elif g not in actors:
            actors.append(g)
    land_f = 1.5 if pad.get('land') else 1.0
    land_score = max([sc.get(k, 0) * land_f for k in LAND_KEYS] + [0])
    cand = [(k, v * 1.15) for k, v in animals] + [(k, v) for k, v in things] + [(k, v * .9) for k, v in nat if k in NATURE_MAIN]
    if mood.get('battle', 0) < 1 and pp not in (7, 8, 23):
        cand = [(k, v) for k, v in cand if k not in ('arrow', 'weapons', 'axe')]
    cand.sort(key=lambda x: -x[1])
    best_other = cand[0][1] if cand else 0
    if not actors and pad['actors'] and best_other < pad.get('mmin', 2.0) and land_score < 2.5 * land_f:
        actors = list(pad['actors'][:1 if best_other >= 1 else 2])
    main = None
    if not actors and cand and cand[0][1] > land_score:
        main = cand[0][0]
    if not actors and pad['actors'] and (pp == 0 or (main is None and not pad.get('land'))):
        actors = list(pad['actors'][:1])
        main = None
    if 'actors' in ov:
        actors = list(ov['actors'])
    if 'main' in ov:
        main = ov['main']
    rider = None
    if actors and animals and animals[0][0] in ('elephant', 'horse') and animals[0][1] >= 1.5 and pp in (3, 4, 13, 19, 20):
        rider = animals[0][0]
    if actors and things and things[0][0] == 'chariot' and things[0][1] >= 1.5:
        rider = 'chariot'
    if rider and actors[0] in ('women', 'people', 'men', 'farmers', 'brahmin', 'sita', 'queen'):
        rider = None

    # ---- place and time
    ps = {p: sum(sc.get(k, 0) * f for k, f in feats.items()) for p, feats in PLACE_FEATS.items()}
    ps[pad['place']] = ps.get(pad['place'], 0) + pad.get('stick', 2.0)
    if pp in (1, 5):
        ps['sea'] += .4 * sc.get('sea', 0)
    if actors and actors[0] == 'sita' and pp in (10, 21) and not (sc.get('garden', 0) or sc.get('pond', 0)):
        ps['palace'] += 2.5
    if pp < 19 or kdm > 1:
        ps['wedding'] *= .3
    if 'milksea' in sc or (pp == 5 and sc.get('vishnu', 0) >= 1 and sc.get('sea', 0) >= 1):
        ps['milksea'] += 3
    if main in ANIMAL_PLACE:
        ps[ANIMAL_PLACE[main]] = ps.get(ANIMAL_PLACE[main], 0) + 1.3
    if main in THING_PLACE:
        ps[THING_PLACE[main]] = ps.get(THING_PLACE[main], 0) + 1.0
    if actors and actors[0] in SKY_FIGS + ('vishnu',) and pp < 6 and ps['milksea'] < 3:
        ps['sky'] += 3
    place = max(ps.items(), key=lambda x: x[1])[0]
    if (main in ANIMAL_PLACE or rider) and place in INDOOR:
        place = ANIMAL_PLACE.get(main, 'city')
    if main in INDOOR_THINGS and place not in ROYAL | {'palace', 'court', 'wedding'}:
        place = THING_PLACE.get(main, 'palace')
    if place == 'sky' and not (actors and actors[0] in SKY_FIGS + ('vishnu',)):
        place = pad['place']
    if pp == 20 and place == 'city':
        place = 'street'
    storm_push = False
    if pad.get('land') and place in INDOOR:
        place = pad['place']
    if kdm == 1 and actors and actors[0] in ('demon', 'thadagai') and place in INDOOR:
        place = 'mountain' if pp == 5 else 'forest'
        storm_push = True
    tm = pad.get('time', 'day')
    ts = {'night': sc.get('night', 0) + .7 * sc.get('moon', 0) * (1 if pp in (10, 14, 18) else .5) + .8 * sc.get('stars', 0),
          'evening': 1.2 * sc.get('evening', 0), 'dawn': 1.2 * sc.get('dawn', 0) + .3 * sc.get('sun', 0),
          'storm': sc.get('lightning', 0) + .5 * sc.get('rain', 0) + .3 * sc.get('cloud', 0)}
    if pp == 23 and (mood.get('anger', 0) + mood.get('fear', 0) + mood.get('battle', 0)) >= 1:
        ts['storm'] += 1
    if pp == 18:
        ts['night'] += 1
    if storm_push:
        ts['storm'] = max(ts['storm'], 1.5)
    best_t = max(ts.items(), key=lambda x: x[1])
    if best_t[1] >= 1:
        tm = best_t[0]
    if main in ('moon', 'stars'):
        tm = 'night'
    if main == 'sun' and tm == 'night':
        tm = 'day'
    if main in NATURE_MAIN and place in INDOOR:
        place = pad['place'] if pad['place'] not in INDOOR else 'city'
    place = ov.get('place', place)
    tm = ov.get('tm', tm)
    if sky_fig and place in INDOOR:
        sky_fig = None

    # ---- faces and poses
    sad = mood.get('sad', 0)
    joy = mood.get('joy', 0)
    face = ('happy', 'smile')
    if sad >= 1 and sad >= joy:
        face = ('sad', 'sad')
    elif mood.get('anger', 0) >= 1:
        face = ('stern', 'open')
    elif mood.get('wonder', 0) >= 1 or mood.get('fear', 0) >= 1:
        face = ('wonder', 'open')
    elif n % 3 == 0 and joy < 1:
        face = ('open', 'smile')
    poses = []
    for i, a in enumerate(actors):
        p = 'down'
        if mood.get('worship', 0) >= 1 and a not in DEITIES + ('vishnu',):
            p = 'namaste'
        elif mood.get('battle', 0) >= 1 and a in ('rama', 'lakshmana') and (sc.get('arrow', 0) + sc.get('bow', 0)) >= 1 and (pp in (7, 8, 23) if kdm == 1 else kdm in (3, 6)):
            p = 'draw'
        elif act.get('hug', 0) >= 1 and len(actors) == 2 and (pp == 19 or not (set(actors) & FEMALE)) and not (set(actors) & {'women', 'men', 'people', 'soldiers', 'farmers'}):
            p = 'hug'
        elif act.get('bless', 0) >= 1 and a in ('vasishtha', 'vishwamitra', 'sage', 'shatananda', 'gautama', 'gods', 'brahma', 'vishnu', 'shiva', 'valmiki'):
            p = 'bless'
        elif sc.get('garland', 0) >= 1 and a in ('sita', 'women'):
            p = 'garland'
        elif act.get('dance', 0) >= 1 and a in ('women', 'musicians'):
            p = 'raise'
        elif mood.get('speak', 0) >= 1 and i == 0:
            p = 'speak'
        elif act.get('give', 0) >= 1 and a in ('dasaratha', 'janaka', 'king'):
            p = 'give'
        elif act.get('point', 0) >= 1 and i == 0:
            p = 'point'
        elif act.get('think', 0) >= 1 and sad >= 1:
            p = 'think'
        elif joy >= 2 and a in ('women', 'men', 'people', 'farmers'):
            p = 'raise'
        elif act.get('walk', 0) >= 1 and i == 0 and a not in ('sita',):
            p = 'walk'
        poses.append(p)
    sitting = [False] * len(actors)
    if place in INDOOR and len(actors) == 1 and actors[0] in ('dasaratha', 'janaka', 'king') and poses[0] in ('down', 'speak', 'give', 'bless'):
        sitting[0] = True
    if pp == 10 and actors and actors[0] == 'sita' and tm == 'night' and len(actors) == 1:
        sitting[0] = True
        poses[0] = 'think' if poses[0] == 'down' else poses[0]
    if actors and actors[0] in ('kamban', 'valmiki') and pp == 0 and poses[0] == 'down':
        sitting[0] = True
    # ---- small accents that belong in this place
    used = set(actors) | {main, rider, sky_fig}
    acc = []
    nacc = 3 if (not actors and not main) else 2
    for k, v in sorted(sc.items(), key=lambda x: -x[1]):
        if v < 1 or k in used or k not in ACC_SLOT:
            continue
        ok = ACC_OK.get(k, None)
        if ok is not None and place not in ok and not (k == 'jewels' and place in WATERY):
            continue
        if k == 'arrow' and mood.get('battle', 0) < 1:
            continue
        if F[k][0] == 'group' and (actors or main):
            continue
        if k == 'jewels' and place in WATERY and (actors or main):
            continue
        if k in ('moon', 'stars') and tm == 'night':
            continue
        if k == 'sun' and tm in ('night', 'evening', 'dawn', 'storm'):
            continue
        if k in ('rain', 'lightning', 'cloud') and tm == 'storm':
            continue
        if k == 'lotus' and place == 'pond':
            continue
        if k == 'fire' and place in ('yagna', 'wedding'):
            continue
        if k == 'flags' and place in ('city', 'street'):
            continue
        acc.append(k)
        if len(acc) == nacc:
            break
    extra = tuple(k for k in ('mountain', 'city', 'paddy') if sc.get(k, 0) >= 1.5)
    return dict(actors=actors, poses=poses, sitting=sitting, face=face, main=main, rider=rider, sky_fig=sky_fig, extra=extra,
                ladies=ladies, place=place, tm=tm, acc=acc, broken=sc.get('broken', 0) >= 1, joy=joy >= 1,
                combo=ov.get('combo'))


# ============================================================== drawing a plan
def draw(n, pp, plan):
    v = n
    actors, poses, sitting = plan['actors'], plan['poses'], plan['sitting']
    eye, mk = plan['face']
    lay = 'one' if len(actors) == 1 else ('two' if len(actors) >= 2 else ('thing' if plan['main'] else 'none'))
    if plan['rider'] or plan['combo']:
        lay = 'thing'
    bg, kind = setting(plan['place'], plan['tm'], v, lay, bare=plan['main'] in ('moon', 'sun', 'stars'), extra=plan['extra'])
    out = [bg]
    labels = []
    if plan['combo']:
        body, labels = combo(plan['combo'], v, eye, mk)
        out.append(body)
        actors = []
    # deity in the sky, small, behind the people
    if plan['sky_fig']:
        sx = 196 if v % 2 else 44
        out.append(cloud(sx, 92, .9) + put(fig(plan['sky_fig'], 'bless', 'happy', 'smile', v=v), .55, sx, 46))
        labels.append(F[plan['sky_fig']][1])
    if plan['ladies']:
        c = WOMEN_CLOTH[v % len(WOMEN_CLOTH)]
        c2 = WOMEN_CLOTH[(v + 2) % len(WOMEN_CLOTH)]
        out.append(put(woman(cloth=c[0], cloth_d=c[1], top=c[2], pose='namaste', eye='wonder', mouth_kind='open'), .5, 34, 78, female=True))
        out.append(put(woman(cloth=c2[0], cloth_d=c2[1], top=c2[2], pose='raise', eye='happy'), .5, 206, 78, female=True))
    if plan['rider']:
        a = actors[0]
        rid = fig(a, 'down' if a not in ('rama', 'lakshmana') else 'down', eye, mk, hold=None, v=v)
        if plan['rider'] == 'elephant':
            out.append(G(elephant(howdah=True, umbrella=True, rider=rid, trunk='up' if plan['joy'] else 'down'), x=100, y=232, s=.88))
        elif plan['rider'] == 'horse':
            out.append(G(horse(rider=rid, prance=v % 2 == 1), x=108, y=228, s=1.1))
        else:
            out.append(G(chariot(rider=rid), x=86, y=228, s=.8))
        labels.append(NAME.get(a, F[a][1] if a in F else a))
        labels.append(F[plan['rider']][1])
    elif len(actors) == 1:
        a = actors[0]
        fem = a in FEMALE
        if a in ('women', 'people', 'men', 'farmers', 'soldiers') and plan['place'] not in INDOOR or (a == 'women' and pp in (16, 17, 18, 20, 21)):
            # a group: two people side by side
            b = {'people': 'women', 'men': 'men', 'women': 'women', 'farmers': 'farmers', 'soldiers': 'soldiers'}[a]
            p1 = poses[0]
            p2 = poses[0] if poses[0] not in ('speak', 'point', 'walk') else 'down'
            h1 = h2 = ''
            if a == 'women' and p1 == 'down':
                p2 = ['down', 'wave', 'offer', 'chest', 'namaste'][v % 5]
                if pp == 16:
                    h1, p2, h2 = 'basket', 'offer', ''
                elif pp == 17:
                    p1 = 'pour'
                elif pp == 18:
                    p2 = 'offer'
            f1 = fig('men' if a == 'people' else a, p1, eye, mk, hold=h1, v=v)
            f2 = fig(b, p2, eye, mk, hold=h2, v=v + 3)
            out.append(put(f1, 1.32, 74, 116, female=(a == 'women'), flip=True))
            out.append(put(f2, 1.32, 166, 120, female=(b == 'women')))
        elif sitting[0]:
            if a in ('dasaratha', 'janaka', 'king'):
                out.append(G(throne(118), x=120, y=212, s=1.0))
                out.append(G(white_umbrella(), x=120, y=78, s=.85) if v % 2 else "")
            elif a in ('kamban', 'valmiki'):
                out.append(G(seat(80), x=120, y=224))
            out.append(put(fig(a, poses[0], eye, mk, sitting=True, v=v), 1.32, 120, 100, female=fem, sitting=True))
        else:
            s = 1.55 if poses[0] != 'draw' else 1.25
            x = 120 if poses[0] != 'draw' else 70
            if plan['acc'] and poses[0] != 'draw':
                x = 112 if v % 2 else 128
            out.append(put(fig(a, poses[0], eye, mk, v=v, hood=plan['place'] == 'milksea'), s, x, 110 if poses[0] != 'draw' else 120, female=fem, key=a))
        labels.append(NAME.get(a, F[a][1] if a in F else a))
    elif len(actors) >= 2:
        a, b = actors[:2]
        figs = []
        for i, k in enumerate((a, b)):
            fem = k in FEMALE
            sit = sitting[i] if i < len(sitting) else False
            p = poses[i]
            if p == 'draw':
                p = 'down'
            yh = 114 + (6 if fem else 0)
            figs.append(put(fig(k, p, eye, mk, sitting=sit, v=v + i * 2, hood=plan['place'] == 'milksea'), 1.34 if not sit else 1.15, 74 if i == 0 else 166,
                            yh if not sit else 118, female=fem, sitting=sit, flip=((i == 0 and p not in ('hug',)) or (i == 1 and p == 'hug')) if k not in BIG else (i == 1), key=k))
        out += figs
        labels += [NAME.get(k, F[k][1] if k in F else k) for k in (a, b)]
    elif plan['main'] and not plan['combo']:
        m = plan['main']
        if F[m][0] == 'animal':
            out.append(animal_main(m, v, plan['joy']))
        elif F[m][0] == 'thing':
            out.append(thing_main(m, v, plan['broken']))
        else:
            out.append(nature_main(m, v))
        labels.append(F[m][1])
    # ---- accents
    big = 1.0
    if lay in ('one',):
        slots = {'sky': [(200, 44), (40, 44)] if (v % 2 == 0) else [(40, 44), (200, 44)], 'ground': [(34, 214), (206, 214)]}
    elif lay == 'two':
        slots = {'sky': [(120, 34)], 'ground': [(120, 222)]}
    elif lay == 'none':
        big = 1.6
        gy = {'river': 180, 'sea': 186, 'pond': 196, 'milksea': 190}.get(plan['place'], 212)
        slots = {'sky': [(190, 44), (50, 44)] if v % 2 else [(50, 44), (190, 44)],
                 'ground': [(70, gy), (172, gy + 8), (120, gy + 14)] if v % 2 else [(172, gy), (70, gy + 8), (120, gy + 14)]}
    else:
        slots = {'sky': [(200, 40), (40, 40)], 'ground': [(30, 220), (210, 220)]}
    for k in plan['acc']:
        sl = ACC_SLOT[k]
        if slots.get(sl):
            x, y = slots[sl].pop(0)
            tmk = 'water' if (k == 'jewels' and plan['place'] in WATERY) else plan['tm']
            out.append(G(accent(k, 0, 0, tmk), x=x, y=y, s=big if sl == 'ground' else (1.25 if big > 1 else 1)))
            labels.append(F[k][1])
    place_l = PLACE_LABEL[plan['place']]
    tl = TIME_LABEL.get(plan['tm'])
    where = f"{tl}, {place_l}" if tl and plan['place'] not in INDOOR else place_l
    if tl and plan['place'] in INDOOR:
        where = f"{place_l} ({tl})"
    seen, labs = set(), []
    for l in labels:
        if l and l not in seen:
            seen.add(l)
            labs.append(l)
    alt = (", ".join(labs) + " — " + where) if labs else where
    return tsvg("".join(out), kind, alt), alt


def combo(kind, v, eye, mk):
    """Hand-made compositions for a few famous poems."""
    if kind == 'invocation':
        body = (C(130, 100, 96, "url(#glow)", stroke="none") + put(fig('vishnu', 'abhaya', 'happy', 'smile', v=v), 1.08, 136, 104) +
                cloud(160, 226, 1.3) + cloud(230, 214, 1.0) +
                G(seat(70), x=50, y=232, s=.9) + put(fig('kamban', 'namaste', 'closed', 'smile', hold=None, sitting=True, v=v), .86, 50, 176, sitting=True))
        return body, ['திருமால்', 'கம்பர்']
    if kind == 'balcony':
        body = (balcony(64, 132, 104, 92) + put(sita(pose='down', eye='happy', mouth_kind='smile'), .62, 64, 70, female=True) +
                R(4, 132, 120, 8, MARBLE, stroke=OUT, sw=2) +
                put(rama(pose='down', hold='bow', eye='happy'), 1.24, 172, 120))
        return body, ['சீதை', 'இராமன்']
    if kind == 'bowbreak':
        halves = (G(P("M0,-60 Q-24,-26 -6,0", stroke=OUT, sw=11) + P("M0,-60 Q-24,-26 -6,0", stroke="#6b4421", sw=7), x=40, y=150, rot=-40) +
                  G(P("M0,60 Q-24,26 -6,0", stroke=OUT, sw=11) + P("M0,60 Q-24,26 -6,0", stroke="#6b4421", sw=7), x=204, y=110, rot=40))
        body = (halves + put(rama(pose='raise', hold=None, eye='happy'), 1.4, 120, 118) +
                sparkle(40, 120, 1.6, "#fff1a0") + sparkle(206, 80, 1.6, "#fff1a0") + sparkle(120, 36, 1.2, "#fff1a0"))
        return body, ['இராமன்', 'முறிந்த வில்']
    return "", []


def nature_main(key, v):
    if key == 'moon':
        return C(120, 70, 54, "#fffbe6", stroke="none", opacity=.22) + moon(120, 70, 30, crescent=False)
    if key == 'sun':
        return rays(120, 70, n=14, r1=20, r2=200, color="#fff0b8", opacity=.5) + C(120, 70, 30, "#ffd65a", stroke="#f2a93a", sw=2)
    if key == 'stars':
        return stars([(40, 40, 1.2), (90, 26, .9), (150, 50, 1.1), (200, 30, 1), (70, 80, .8), (180, 90, .9), (120, 100, .7)])
    if key in ('cloud', 'rain'):
        return dark_cloud(80, 60, 1.2) + dark_cloud(170, 50, 1.0) + rain(30, 220, 80, 170, "#e6f2ff", 14)
    if key == 'lightning':
        return dark_cloud(110, 50, 1.4) + bolt(110, 60, 1.6)
    if key == 'rainbow':
        return rainbow(120, 170, 110, .8)
    if key == 'wind':
        return wind_lines(40, 80, 1.6) + wind_lines(90, 130, 1.2) + petals([(150, 70, 20), (180, 100, -10), (210, 60, 40)], LEAF_L)
    if key == 'waterfall':
        return waterfall(120, 210, 150, 40)
    if key == 'dust':
        return E(120, 190, 90, 30, "#d9c49a", stroke="none", opacity=.7) + E(80, 170, 50, 24, "#e6d4ac", stroke="none", opacity=.7)
    return ""


# ============================================================== main
def run(k, only=None):
    out_meta = {}
    meta_path = os.path.join(ROOT, 'content', str(k), 'pics.json')
    if only and os.path.exists(meta_path):
        out_meta = json.load(open(meta_path, encoding='utf-8'))
    count = 0
    for pp in range(0, 100):
        src = os.path.join(ROOT, 'content', str(k), f'{pp:02d}.src.json')
        if not os.path.exists(src):
            continue
        if only and pp not in only:
            continue
        data = json.load(open(src, encoding='utf-8'))
        head = ''
        os.makedirs(os.path.join(ROOT, 'img', str(k), f'{pp:02d}'), exist_ok=True)
        for it in data['items']:
            if it['type'] == 'heading':
                head = it['text']
                continue
            if it['type'] != 'poem':
                continue
            n = it['n']
            sc = features(it, head)
            ppx = pp if k == 1 else 100 + pp
            HERMIT['on'] = PADS[k][pp].get('hermit', False)
            CUR['k'] = k
            plan = decide(n, ppx, sc, k)
            svg_, alt = draw(n, ppx, plan)
            with open(os.path.join(ROOT, 'img', str(k), f'{pp:02d}', f'p{n}.svg'), 'w', encoding='utf-8') as fh:
                fh.write(svg_)
            out_meta[str(n)] = {'pic': f'img/{k}/{pp:02d}/p{n}.svg', 'alt': alt}
            count += 1
    out_meta = dict(sorted(out_meta.items(), key=lambda x: int(x[0])))
    with open(meta_path, 'w', encoding='utf-8') as fh:
        json.dump(out_meta, fh, ensure_ascii=False, indent=0, separators=(',', ':'))
    print(f'{count} pictures written')


if __name__ == '__main__':
    kk = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    only = {int(a) for a in sys.argv[2:]} or None
    run(kk, only)
