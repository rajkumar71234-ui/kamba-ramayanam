"""Padalam pictures (800 x 500) for அயோத்தியா … யுத்த காண்டம், drawn from a short description.

    python3 tools/art_scenes.py 2          # every padalam of அயோத்தியா காண்டம் -> img/2/<pp>/chapter.svg

A description (scene_specs.py) names a background, the time of day, the figures from left to right and a few
props, e.g.  dict(bg='court', figs=['dasaratha:give:sit', 'vasishtha:bless', 'rama:namaste'], props=['umbrella'])
A figure is 'name[:pose[:mood or sit]]'; poses are those of kit.person (namaste, speak, point, bless, give, raise,
walk, draw, think, hug, offer, garland, chest, wave …); moods: happy, sad, stern, wonder, closed.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *            # noqa: F401,F403
from kit import *            # noqa: F401,F403
from kit_more import *       # noqa: F401,F403
from art_bala import blossom_tree, gopuram, leaf_meal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOUTH = {'happy': 'smile', 'sad': 'sad', 'stern': 'open', 'wonder': 'open', 'closed': 'smile', 'open': 'smile'}
FEMALE = {'sita', 'kaikeyi', 'kausalya', 'sumitra', 'manthara', 'surpanakha', 'surpanakha_b', 'mandodari', 'trijata',
          'sabari', 'tara', 'woman', 'women', 'ahalya'}


def F(name, pose='down', eye='happy', sitting=False, v=0):
    """One figure by name; feet (or seat) at (0,0)."""
    mk = MOUTH.get(eye, 'smile')
    hold_ok = pose == 'down'
    table = {
        'rama': lambda: rama(pose=pose, hold='bow' if hold_ok else None, eye=eye, mouth_kind=mk, sitting=sitting),
        'rama_plain': lambda: rama(pose=pose, hold=None, eye=eye, mouth_kind=mk, sitting=sitting),
        'rama_hermit': lambda: person(skin=RAMA_BLUE, hair='jata', outfit='bark', cloth=BARK, cloth_d=BARK_D, pose=pose,
                                      sitting=sitting, eye=eye, mouth_kind=mk, tilak='namam', quiver=hold_ok,
                                      hold='bow' if hold_ok else None, thread=True),
        'lakshmana': lambda: lakshmana(pose=pose, hold='bow' if hold_ok else None, eye=eye, mouth_kind=mk, sitting=sitting),
        'lakshmana_hermit': lambda: person(skin=SKIN_GOLD, hair='jata', outfit='bark', cloth=BARK, cloth_d=BARK_D, pose=pose,
                                           sitting=sitting, eye=eye, mouth_kind=mk, tilak='namam', quiver=hold_ok,
                                           hold='bow' if hold_ok else None, thread=True),
        'sita': lambda: sita(pose=pose, eye=eye, mouth_kind=mk, sitting=sitting),
        'sita_hermit': lambda: person(skin=SKIN_WOMAN, hair='braid', outfit='saree', cloth=BARK_L, cloth_d=BARK_D, top=BARK,
                                      pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak='bindi', female=True, flowers=True),
        'bharata': lambda: bharata(pose=pose, eye=eye, sitting=sitting),
        'bharata_hermit': lambda: person(skin=RAMA_BLUE_D, hair='jata', outfit='bark', cloth=BARK, cloth_d=BARK_D, pose=pose,
                                         sitting=sitting, eye=eye, mouth_kind=mk, tilak='namam', thread=True),
        'shatrughna': lambda: shatrughna(pose=pose, eye=eye, sitting=sitting),
        'dasaratha': lambda: dasaratha(pose=pose, sitting=sitting, eye=eye, mouth_kind=mk),
        'kaikeyi': lambda: kaikeyi(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'kausalya': lambda: kausalya(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'sumitra': lambda: sumitra(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'manthara': lambda: manthara(pose=pose if pose != 'down' else 'point', eye=eye, mk=mk, sitting=sitting),
        'vasishtha': lambda: vasishtha(pose=pose, sitting=sitting, eye=eye, mouth_kind=mk),
        'guha': lambda: guha(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'sumantra': lambda: sumantra(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'hunter': lambda: hunter(pose=pose, eye=eye, mk=mk),
        'man': lambda: man(cloth=MILK, top=[OCHRE, TEAL_CLOTH, PINK_CLOTH, GREEN_CLOTH][v % 4], pose=pose, eye=eye, mouth_kind=mk, sitting=sitting),
        'woman': lambda: woman(cloth=[TEAL_CLOTH, PINK_CLOTH, PURPLE_CLOTH, GREEN_CLOTH][v % 4],
                               cloth_d=[TEAL_CLOTH_D, PINK_CLOTH_D, PURPLE_CLOTH_D, GREEN_CLOTH_D][v % 4],
                               pose=pose, eye=eye, mouth_kind=mk, sitting=sitting),
        'soldier': lambda: person(skin=SKIN_YOUNG, hair='turban', hair_color=ROYAL_RED, moustache=BLACK_HAIR, outfit='dhoti',
                                  cloth=RUST, cloth_d=RUST_D, top='#9aa3ad', pose=pose, eye=eye, mouth_kind=mk,
                                  hold='sword' if hold_ok else None),
        'sage': lambda: sage2(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'agastya': lambda: agastya(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'surpanakha': lambda: surpanakha(pose=pose, eye=eye, mk=mk),
        'surpanakha_b': lambda: surpanakha(pose=pose, eye=eye, mk=mk, beautiful=True),
        'ravana': lambda: ravana(pose=pose, eye=eye if eye != 'happy' else 'stern', mk=mk, sitting=sitting,
                                 hold='sword' if hold_ok else None),
        'ravana_hermit': lambda: person(skin='#b17a58', hair='jata', beard=GREY_HAIR, outfit='robe', cloth=OCHRE, cloth_d=OCHRE_D,
                                        pose=pose, eye=eye, mouth_kind=mk, tilak='ash', hold='staff' if hold_ok else None, old=True),
        'demon': lambda: rakshasa(pose=pose, hold='mace' if hold_ok else None, eye='stern'),
        'demoness': lambda: rakshasa(pose=pose, hold=None, eye='stern', female=True, skin='#7a5a7a', cloth='#4a2f4a'),
        'khara': lambda: khara(pose=pose, hold='sword' if hold_ok else None),
        'viradha': lambda: viradha(pose=pose if pose != 'down' else 'raise', hold='trident'),
        'maricha': lambda: rakshasa(pose=pose, hold=None, eye=eye, skin='#6a6a8a'),
        'vibhishana': lambda: vibhishana(pose=pose if pose != 'down' else 'namaste', eye=eye, mk=mk, sitting=sitting),
        'kumbhakarna': lambda: kumbhakarna(pose=pose, eye=eye if eye != 'happy' else 'stern', hold='trident' if hold_ok else None),
        'indrajit': lambda: indrajit(pose=pose, eye=eye if eye != 'happy' else 'stern', hold='bow' if hold_ok else None),
        'mandodari': lambda: mandodari(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'trijata': lambda: trijata(pose=pose, eye=eye, mk=mk),
        'sabari': lambda: sabari(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'hanuman': lambda: hanuman(pose=pose, eye=eye, mk=mk, sitting=sitting, hold='mace' if hold_ok else None),
        'sugriva': lambda: sugriva(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'vali': lambda: vali(pose=pose, eye=eye if eye != 'happy' else 'stern', mk=mk, sitting=sitting),
        'angada': lambda: angada(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'tara': lambda: tara(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'jambavan': lambda: jambavan(pose=pose, eye=eye, mk=mk, sitting=sitting),
        'nala': lambda: nala(pose=pose, eye=eye, mk=mk),
        'vanara': lambda: vanara(pose=pose, eye=eye, mk=mk, skin=[MONKEY, '#a8784a', '#c39a62'][v % 3],
                                 cloth=[SAFFRON, TEAL_CLOTH, GREEN_CLOTH][v % 3], cloth_d=[SAFFRON_D, TEAL_CLOTH_D, GREEN_CLOTH_D][v % 3]),
        'samudra': lambda: samudra(pose=pose if pose != 'down' else 'namaste', eye=eye, mk=mk),
        'agni': lambda: agni(pose=pose if pose != 'down' else 'bless', eye=eye, mk=mk),
        'brahma': lambda: brahma(pose='bless', sitting=sitting, eye='happy', mouth_kind='smile'),
        'shiva': lambda: person(skin='#cdd7de', hair='jata', hair_color='#6b4a2e', outfit='dhoti', cloth='#e8a33a',
                                cloth_d='#b5782a', pose=pose if pose != 'down' else 'bless', eye=eye, mouth_kind=mk, tilak='ash',
                                hold='trident' if hold_ok else None, thread=True),
        'deva': lambda: person(skin=SKIN_GOLD, hair='long', outfit='dhoti', cloth=MILK, cloth_d=WHITE_CLOTH_D, sash=GOLD,
                               pose=pose if pose != 'down' else 'bless', eye=eye, mouth_kind=mk, tilak='namam', jewels=True,
                               crown_kind='tall'),
        'kausalya_sad': lambda: kausalya(pose=pose, eye='sad', mk='sad', sitting=sitting),
    }
    if name not in table:
        raise KeyError(name)
    return table[name]()


# ------------------------------------------------------------------ backgrounds (800 x 500)
def defs_for(tm):
    return {'night': night_defs(), 'desert': desert_defs(), 'indoor': indoor_defs()}.get(tm) or sky_defs(
        {'day': 'day', 'dawn': 'dawn', 'evening': 'evening', 'divine': 'divine', 'storm': 'day'}.get(tm, 'day'))


def sky_layer(tm, side=1):
    out = [sky()]
    if tm == 'night':
        out += [moon(640 if side > 0 else 140, 80, 30), stars([(90, 60, 1), (220, 40, .8), (330, 90, .7), (470, 50, 1),
                                                               (560, 110, .7), (720, 140, .8), (400, 30, .6)])]
    elif tm == 'evening':
        out += [C(640, 250, 60, '#ffd08a', stroke='none', opacity=.5), C(640, 250, 36, '#ff9e5e', stroke='none'),
                flying_birds_big(180, 110)]
    elif tm == 'dawn':
        out += [rays(150, 300, n=14, r1=30, r2=420, color='#fff0c8', opacity=.45), C(150, 300, 40, '#ffbf6a', stroke='none')]
    elif tm == 'storm':
        out += [R(0, 0, W, H, '#56627c', opacity=.5), dark_cloud(150, 80, 1.6), dark_cloud(420, 60, 2), dark_cloud(660, 90, 1.5),
                rain(0, 800, 120, 330, '#dbe6f2', 26)]
    elif tm == 'divine':
        out += [rays(400, -40, n=16, r1=40, r2=600, color='#fff3c4', opacity=.5)]
    else:
        out += [sun(660, 80, 30), cloud(160, 90, 1.1), cloud(420, 60, .8)]
    return ''.join(out)


def flying_birds_big(x, y):
    return ''.join(P(f"M{x + k * 34},{y + (k % 2) * 14} q8,-9 16,0 q8,-9 16,0", stroke='#5a4a3a', sw=2.4) for k in range(4))


def bg_art(kind, tm):
    """The background picture; returns (svg, defs)."""
    out = []
    if kind in ('court', 'room'):
        d = indoor_defs()
        out.append(hall(floor=400, curtain=ROYAL_RED if kind == 'court' else '#7a3a6a'))
        if tm == 'night':
            out.append(R(0, 0, W, H, '#1d2b52', opacity=.25))
            out.append(G(lamp(.9), x=60, y=400) + G(lamp(.9), x=740, y=400))
        return ''.join(out), d
    d = defs_for('night' if tm == 'night' else ('desert' if kind == 'desert' else tm))
    out.append(sky_layer(tm))
    if kind == 'city':
        out += [palace(400, 330, 1.25), tower(110, 340, 1.0), tower(690, 340, 1.0), flag(110, 170, ROYAL_RED, 1, 60),
                flag(690, 170, '#e7a13d', 1, 60), city_wall(380, 0, 800, '#e3c48a', 70), R(0, 380, W, 120, '#e8d3a6'),
                P('M0,380 L800,380', stroke='#c9a46a', sw=2)]
    elif kind == 'street':
        out.append(R(0, 360, W, 140, '#e8d3a6'))
        for x0 in (0, 560):
            out += [R(x0, 110, 240, 250, '#f1dfbd', stroke=OUT, sw=2.4), P(f'M{x0 - 10},110 L{x0 + 120},50 L{x0 + 250},110 Z', '#c9673d', sw=2.4),
                    balcony(x0 + 120, 250, 150, 90)]
        out += [flag(280, 360, ROYAL_RED, 1, 120, 3), flag(520, 360, '#e7a13d', 1, 120, 5), P('M0,360 L800,360', stroke='#c9a46a', sw=2)]
    elif kind in ('river', 'ganga'):
        out += [hills(250), river(290, 400), bank(400)]
        out += [tree(60, 300, .9, 1), tree(740, 300, .8, 2), coconut(700, 320, .9, -8)]
        if kind == 'ganga':
            out.append(G(boat_big(), x=560, y=380, s=1))
    elif kind in ('forest', 'ashram', 'panchavati'):
        out += [hills(280, '#a9cf9a', '#8fbf82'), ground(360, '#9acb7a')]
        for i, (x, y, s) in enumerate(((40, 330, 1.2), (150, 300, .9), (660, 300, .9), (760, 340, 1.2), (290, 280, .7), (520, 285, .7))):
            out.append(tree(x, y, s, i))
        if kind in ('ashram', 'panchavati'):
            out.append(hut(600, 372, 1.0))
        if kind == 'panchavati':
            out.append(river(400, 470))
        out.append(grass_tufts([(200, 470), (380, 480), (560, 470)]))
    elif kind == 'mountain':
        out += [mountain(220, 330, 1.4), mountain(600, 340, 1.5, '#97b0c2'), waterfall(660, 340, 150, 36),
                ground(340, '#9acb7a'), tree(80, 380, 1, 1), tree(740, 400, .9, 2)]
    elif kind in ('sea', 'shore'):
        out += [sea(250, 500), P('M0,360 C200,340 500,380 800,350 L800,500 L0,500 Z', SAND, stroke='none'),
                coconut(80, 380, 1, 8), coconut(730, 370, .9, -8)]
    elif kind == 'lanka':
        out += [sea(300, 500), lanka_city(560, 300, .9), P('M0,420 C200,400 400,430 800,410 L800,500 L0,500 Z', SAND, stroke='none')]
    elif kind == 'lanka_city':
        out += [lanka_city(400, 340, 1.4), R(0, 340, W, 160, '#e8d09a'), P('M0,340 L800,340', stroke='#c9a46a', sw=2)]
    elif kind == 'battle':
        out += [ground(340, '#cdb98a'), E(200, 340, 180, 30, '#e3d2a8', stroke='none', opacity=.8),
                E(620, 330, 200, 34, '#e3d2a8', stroke='none', opacity=.8), flag(60, 340, ROYAL_RED, 1.1, 150, 4),
                flag(740, 340, '#3f3a52', 1.1, 150, 2)]
        for x, y, r in ((300, 470, -20), (520, 480, 30), (680, 460, -40), (120, 480, 10)):
            out.append(G(P('M-30,0 L30,0', stroke='#8a5a2b', sw=4) + P('M30,-5 L42,0 L30,5 Z', '#cfd6dc', sw=1.4), x=x, y=y, rot=r))
    elif kind == 'sky':
        out += [cloud(120, 420, 2.4), cloud(420, 450, 2.8), cloud(700, 420, 2.2)]
    elif kind in ('garden', 'asoka'):
        out += [ground(360, GRASS)]
        if kind == 'asoka':
            out += [asoka_tree(130, 380, 1.5), asoka_tree(660, 370, 1.4), asoka_tree(400, 330, 1.0)]
        else:
            out += [blossom_tree(120, 370, 1.4), blossom_tree(680, 370, 1.4, '#ffd34e'), lotus_pond(400, 440, 180, 34)]
    elif kind == 'lake':
        out += [hills(260), ground(320, GRASS), lotus_pond(400, 410, 330, 60), tree(60, 330, 1, 1), tree(740, 330, 1, 2)]
    elif kind == 'cave':
        out += [mountain(400, 420, 2.4, '#8a8f99'), P('M300,420 C300,300 500,300 500,420 Z', '#2a2430', sw=2.4),
                ground(420, '#8a8070')]
    elif kind == 'desert':
        out += [P('M0,330 C200,300 400,340 800,310 L800,500 L0,500 Z', '#e9c986', stroke='none'),
                dead_tree_big(120, 380), dead_tree_big(700, 370)]
    elif kind == 'camp':
        out += [mountain(400, 330, 1.6), ground(330, '#a6cf8f'), tent(150, 380, 1.1), tent(650, 390, 1.0, stripe='#e7a13d'),
                tent(420, 350, .7, stripe=TEAL_CLOTH)]
    else:
        out += [hills(280), ground(360)]
    if tm == 'night' and kind not in ('court', 'room'):
        out.append(R(0, 0, W, H, '#14204a', opacity=.25))
        out.append(moon(640, 80, 30) + stars([(90, 60, 1), (220, 40, .8), (470, 50, 1), (720, 140, .8)]))
    return ''.join(out), d


def boat_big():
    return (P('M-110,-24 L110,-24 C92,10 -92,10 -110,-24 Z', '#a0682e', sw=2.6) + P('M-100,-14 L100,-14', stroke='#7a4c22', sw=2) +
            P('M60,-24 L120,-90', stroke='#7a4c22', sw=4))


def dead_tree_big(x, y):
    d = 'M0,0 L-4,-120 M-4,-80 L-44,-124 M-2,-100 L36,-148 M-4,-120 L-20,-168'
    return G(P(d, stroke=OUT, sw=12) + P(d, stroke='#8a6a4a', sw=8), x=x, y=y)


# ------------------------------------------------------------------ props (800 x 500 coordinates)
def prop(name, x=None, y=None, s=1.0):
    table = {
        'umbrella': lambda: G(white_umbrella(), x=x or 400, y=y or 150, s=s * 1.3),
        'throne': lambda: G(throne(140), x=x or 400, y=y or 360, s=s),
        'padukas': lambda: G(padukas(), x=x or 400, y=y or 330, s=s * 1.6),
        'ring': lambda: G(ring(), x=x or 400, y=y or 160, s=s * 1.8),
        'chudamani': lambda: G(chudamani(), x=x or 400, y=y or 160, s=s * 1.8),
        'fire': lambda: fire_altar(x or 400, y or 430, s * 1.0),
        'burning': lambda: burning(x or 400, y or 300, s * 2.2),
        'lamp': lambda: G(lamp(1), x=x or 400, y=y or 400, s=s),
        'drum': lambda: drum(x or 400, y or 430, s * 2),
        'garland': lambda: garland(x or 400, y or 120, s * 2.5),
        'pushpaka': lambda: pushpaka(s * 1.0) if False else G(pushpaka(), x=x or 400, y=y or 260, s=s),
        'bridge': lambda: bridge(x or 120, (x or 120) + 560, y or 330, 3),
        'deer': lambda: G(golden_deer(), x=x or 600, y=y or 420, s=s * 2.4),
        'jatayu': lambda: G(big_bird(), x=x or 560, y=y or 320, s=s * 1.4),
        'jatayu_down': lambda: G(big_bird(wings='closed'), x=x or 560, y=y or 440, s=s * 1.3),
        'sampati': lambda: G(big_bird(wings='none', color='#6a5a4a', wing='#4f4234'), x=x or 560, y=y or 430, s=s * 1.4),
        'garuda': lambda: G(big_bird(gold=True), x=x or 560, y=y or 230, s=s * 1.5),
        'kabandha': lambda: G(kabandha(), x=x or 560, y=y or 440, s=s * 1.3),
        'chariot': lambda: G(chariot(), x=x or 400, y=y or 440, s=s * 1.2),
        'elephant': lambda: G(elephant(howdah=True, umbrella=True), x=x or 400, y=y or 440, s=s * 1.2),
        'boat': lambda: G(boat_big(), x=x or 400, y=y or 400, s=s),
        'arrows': lambda: ''.join(G(P('M-40,0 L40,0', stroke='#8a5a2b', sw=4) + P('M40,-6 L56,0 L40,6 Z', '#cfd6dc', sw=1.4),
                                    x=(x or 400) + k * 60, y=(y or 150) + k * 30, rot=20) for k in range(3)),
        'mountain_held': lambda: G(mountain(0, 0, .5, '#8fbf72'), x=x or 400, y=y or 120, s=s),
        'sea_waves': lambda: sea(y or 380, 500),
        'stone': lambda: stone(x or 400, y or 440, s * 1.2),
        'flowers': lambda: petals([((x or 400) + dx, (y or 120) + dy, r) for dx, dy, r in
                                   ((-60, 10, 10), (-20, -20, 40), (30, 0, -20), (70, -30, 30), (0, 30, 0), (-90, -20, 60))]),
        'leaf_meal': lambda: leaf_meal(x or 400, y or 450, s * 1.6),
        'tent': lambda: tent(x or 400, y or 400, s),
        'moon': lambda: moon(x or 640, y or 80, 30),
        'lotus': lambda: lotus(x or 400, y or 450, s * 1.5),
    }
    return table[name]()


def put_fig(svg_, x, ground_y, s, flip=False):
    return G(svg_, x=x, y=ground_y, s=s, flip=flip)


def scene(spec):
    """Draw one padalam picture from its description."""
    bg, defs = bg_art(spec.get('bg', 'forest'), spec.get('tm', 'day'))
    out = [bg]
    for pr in spec.get('back', []):            # props behind the figures
        out.append(prop(*pr) if isinstance(pr, (tuple, list)) else prop(pr))
    figs = spec.get('figs', [])
    n = len(figs)
    gy = spec.get('ground', 482)
    s_default = spec.get('scale', {1: 1.8, 2: 1.75, 3: 1.6, 4: 1.45, 5: 1.3}.get(n, 1.15))
    span = {1: 0, 2: 300, 3: 440, 4: 540, 5: 600}.get(n, 640)
    xs = spec.get('xs') or ([400] if n == 1 else [int(400 - span / 2 + i * (span / (n - 1))) for i in range(n)])
    placed = []
    for i, f in enumerate(figs):
        if isinstance(f, (tuple, list)):  # (name, x, y, scale, pose, mood, flip)
            name, x, y, s, pose, mood, flip = (list(f) + [None] * 7)[:7]
            sit = False
        else:
            bits = f.split(':')
            name = bits[0]
            pose = bits[1] if len(bits) > 1 and bits[1] else 'down'
            mood = 'happy'
            sit = False
            for b in bits[2:]:
                if b == 'sit':
                    sit = True
                elif b == 'flip':
                    pose = pose
                else:
                    mood = b
            x, y, s, flip = xs[i], gy, s_default, ':flip' in f
        pose = pose or 'down'
        mood = mood or 'happy'
        svg_ = F(name, pose=pose, eye=mood, sitting=sit, v=i)
        if name == 'kumbhakarna':
            s = (s or s_default) * 1.5
        yy = y if y is not None else gy
        sc = s or s_default
        if sit and name in ('dasaratha', 'ravana', 'sugriva', 'vali', 'janaka', 'rama', 'bharata') and spec.get('bg') == 'court':
            yy -= 46 * sc / 1.45                     # a king sits on his throne
            out.append(G(throne(118), x=x, y=yy, s=sc * .9))
        out.append(put_fig(svg_, x, yy, sc, flip=bool(flip)))
        placed.append((x, yy, sc, sit))
    for pr in spec.get('props', []):
        if isinstance(pr, (tuple, list)) and len(pr) >= 2 and isinstance(pr[1], str) and pr[1].startswith('above:'):
            fx, fy, fs, fsit = placed[int(pr[1].split(':')[1])]
            top = fy - (200 if not fsit else 160) * fs           # just above the figure's head
            out.append(prop(pr[0], fx, top, pr[2] if len(pr) > 2 else 1.0))
            continue
        out.append(prop(*pr) if isinstance(pr, (tuple, list)) else prop(pr))
    return svg(*out, defs=defs, title=spec.get('alt', ''))


def load_specs():
    import json
    raw = json.load(open(os.path.join(ROOT, 'tools', 'scene_specs.json'), encoding='utf-8'))
    return {tuple(int(x) for x in key.split('-')): v for key, v in raw.items()}


def run(k, only=None):
    SPECS = load_specs()
    done = 0
    for (kk, pp), spec in sorted(SPECS.items()):
        if kk != k or (only and pp not in only):
            continue
        d = os.path.join(ROOT, 'img', str(k), f'{pp:02d}')
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'chapter.svg'), 'w', encoding='utf-8') as fh:
            fh.write(scene(spec))
        done += 1
    print(f'kandam {k}: {done} padalam pictures')


if __name__ == '__main__':
    run(int(sys.argv[1]), {int(a) for a in sys.argv[2:]} or None)
