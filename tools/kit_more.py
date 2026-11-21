"""More characters and props for அயோத்தியா … யுத்த காண்டம், in the same cartoon style as kit.py.

Every figure stands with its feet (or seat) at (0, 0), like the characters in kit.py.
"""
import math

from art import *          # noqa: F401,F403
from kit import *          # noqa: F401,F403

MONKEY, MONKEY_D = "#b9824a", "#9a6634"
BEAR = "#5b4030"


# ------------------------------------------------------------------ people of Ayodhya
def kaikeyi(pose="down", eye="happy", mk="smile", sitting=False, hold=None):
    return woman(cloth=PURPLE_CLOTH, cloth_d=PURPLE_CLOTH_D, top=GOLD, pose=pose, eye=eye, mouth_kind=mk,
                 sitting=sitting, hold=hold, queen=True)


def kausalya(pose="down", eye="happy", mk="smile", sitting=False, hold=None):
    return woman(cloth="#e8dcc0", cloth_d="#cbbd9c", top=GOLD, pose=pose, eye=eye, mouth_kind=mk,
                 sitting=sitting, hold=hold, queen=True)


def sumitra(pose="down", eye="happy", mk="smile", sitting=False, hold=None):
    return woman(cloth=BLUE_CLOTH, cloth_d=BLUE_CLOTH_D, top=GOLD, pose=pose, eye=eye, mouth_kind=mk,
                 sitting=sitting, hold=hold, queen=True)


def manthara(pose="point", eye="stern", mk="open", sitting=False):
    """கூனி: an old hunchbacked maid."""
    return person(skin="#d9a070", hair="bun", hair_color=GREY_HAIR, outfit="saree", cloth="#8a6a4a", cloth_d="#6b5038",
                  top="#a9876a", pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, female=True, old=True, hump=True,
                  hold="staff" if pose in ("down", "walk") else None)


def guha(pose="down", eye="happy", mk="smile", sitting=False, hold="bow"):
    """குகன்: chief of the boatmen-hunters of Sringiberapuram."""
    return person(skin=SKIN_HUNTER, hair="bun", beard=BLACK_HAIR, outfit="dhoti", cloth="#d9a548", cloth_d="#b5832e",
                  sash="#7a4a22", pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, hold=hold if pose == "down" else None,
                  quiver=(hold == "bow"))


def sumantra(pose="down", eye="happy", mk="smile", sitting=False):
    return person(skin=SKIN_SAGE, hair="turban", hair_color=MILK, moustache=GREY_HAIR, outfit="robe", cloth=MILK,
                  cloth_d=WHITE_CLOTH_D, top=TEAL_CLOTH, pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="namam", old=True)


def hunter(pose="down", eye="happy", mk="smile", hold="bow"):
    return person(skin=SKIN_HUNTER, hair="bun", moustache=BLACK_HAIR, outfit="dhoti", cloth="#c99a55", cloth_d="#a77a38",
                  pose=pose, eye=eye, mouth_kind=mk, hold=hold if pose == "down" else None)


# ------------------------------------------------------------------ the forest
def surpanakha(pose="down", eye="happy", mk="smile", beautiful=False):
    if beautiful:
        return woman(cloth=ROYAL_RED, cloth_d=ROYAL_RED_D, top=GOLD, pose=pose, eye=eye, mouth_kind=mk)
    return demon(pose=pose, hold=None, skin="#7a4f6e", eye=eye if eye != "happy" else "stern", mouth_kind="open",
                 female=True, cloth="#5a2f4a")


def ravana(pose="down", eye="stern", mk="smile", sitting=False, hold="sword"):
    """இராவணன்: king of Lanka, five of his ten crowned heads showing."""
    return person(skin="#b17a58", hair="long", hair_color=BLACK_HAIR, moustache=BLACK_HAIR, outfit="robe", cloth=ROYAL_RED,
                  cloth_d=ROYAL_RED_D, top=GOLD, pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, jewels=True,
                  crown_kind="tall", extra_heads=2, hold=hold if pose == "down" else None)


def rakshasa(pose="down", hold="mace", eye="stern", mk="open", skin=SKIN_DEMON, cloth="#3f3a52", female=False):
    return demon(pose=pose, hold=hold, skin=skin, eye=eye, mouth_kind=mk, female=female, cloth=cloth)


def khara(pose="down", hold="sword"):
    return demon(pose=pose, hold=hold, skin="#5d6f4a", cloth="#3a4a2a")


def viradha(pose="raise", hold="trident"):
    return demon(pose=pose, hold=hold, skin="#5a5a6a", cloth="#2f2f3a")


def vibhishana(pose="namaste", eye="happy", mk="smile", sitting=False):
    return person(skin="#8a7aa8", hair="long", outfit="robe", cloth=MILK, cloth_d=WHITE_CLOTH_D, top=TEAL_CLOTH, pose=pose,
                  sitting=sitting, eye=eye, mouth_kind=mk, tilak="namam", jewels=True, crown_kind="tall")


def kumbhakarna(pose="down", eye="stern", mk="open", hold="trident"):
    return demon(pose=pose, hold=hold, skin="#4f5a7a", eye=eye, mouth_kind=mk, cloth="#2a2f45")


def indrajit(pose="down", eye="stern", mk="smile", hold="bow"):
    return person(skin="#7d6a9a", hair="long", outfit="dhoti", cloth=BLUE_CLOTH, cloth_d=BLUE_CLOTH_D, sash=GOLD, pose=pose,
                  eye=eye, mouth_kind=mk, jewels=True, crown_kind="tall", hold=hold if pose == "down" else None,
                  quiver=(hold == "bow"))


def mandodari(pose="down", eye="sad", mk="sad", sitting=False):
    return woman(cloth="#3f2f6a", cloth_d="#2c2050", top=GOLD, pose=pose, eye=eye, mouth_kind=mk, sitting=sitting, queen=True)


def trijata(pose="down", eye="happy", mk="smile"):
    return demon(pose=pose, hold=None, skin="#6a7a6a", eye=eye, mouth_kind=mk, female=True, cloth="#3f5a4a")


def sabari(pose="namaste", eye="happy", mk="smile", sitting=False):
    """சவரி: the old ascetic woman who waited for Rama."""
    return person(skin="#b98256", hair="bun", hair_color=WHITE_HAIR, outfit="saree", cloth=BARK, cloth_d=BARK_D,
                  top=BARK_L, pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, female=True, old=True,
                  hold="basket" if pose == "down" else None)


def agastya(pose="bless", eye="happy", mk="smile", sitting=False):
    return person(skin=SKIN_SAGE, hair="jata", hair_color=WHITE_HAIR, beard=WHITE_HAIR, outfit="robe", cloth=OCHRE,
                  cloth_d=OCHRE_D, top=BARK_L, pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="ash",
                  hold="kamandalu" if pose == "down" else None, old=True, thread=True, big_head=1.08)


def sage2(pose="bless", eye="happy", mk="smile", sitting=False, cloth=OCHRE, cloth_d=OCHRE_D, beard=GREY_HAIR):
    return person(skin=SKIN_SAGE, hair="jata", hair_color=beard, beard=beard, outfit="robe", cloth=cloth, cloth_d=cloth_d,
                  top=MILK, pose=pose, sitting=sitting, eye=eye, mouth_kind=mk, tilak="ash",
                  hold="kamandalu" if pose == "down" else None, old=True, thread=True)


# ------------------------------------------------------------------ the vanaras
def vanara(pose="down", eye="happy", mk="smile", skin=MONKEY, cloth=SAFFRON, cloth_d=SAFFRON_D, crown_kind=None,
           hold=None, jewels=False, sitting=False, old=False):
    return person(skin=skin, hair="none", outfit="dhoti", cloth=cloth, cloth_d=cloth_d, pose=pose, sitting=sitting, eye=eye,
                  mouth_kind=mk, jewels=jewels, crown_kind=crown_kind, hold=hold if pose == "down" else None,
                  face="monkey", tail=not sitting, old=old)


def hanuman(pose="down", eye="happy", mk="smile", sitting=False, hold="mace"):
    return vanara(pose=pose, eye=eye, mk=mk, skin="#c98a4a", cloth=ROYAL_RED, cloth_d=ROYAL_RED_D, crown_kind="small",
                  hold=hold, jewels=True, sitting=sitting)


def sugriva(pose="down", eye="happy", mk="smile", sitting=False):
    return vanara(pose=pose, eye=eye, mk=mk, skin="#b07a48", cloth=GREEN_CLOTH, cloth_d=GREEN_CLOTH_D, crown_kind="tall",
                  jewels=True, sitting=sitting)


def vali(pose="down", eye="stern", mk="smile", sitting=False):
    return vanara(pose=pose, eye=eye, mk=mk, skin="#d0a060", cloth=GOLD, cloth_d=GOLD_D, crown_kind="tall", jewels=True,
                  sitting=sitting, hold="mace")


def angada(pose="down", eye="happy", mk="smile", sitting=False):
    return vanara(pose=pose, eye=eye, mk=mk, skin="#c8925a", cloth=BLUE_CLOTH, cloth_d=BLUE_CLOTH_D, crown_kind="small",
                  jewels=True, sitting=sitting)


def tara(pose="down", eye="sad", mk="sad", sitting=False):
    return woman(cloth="#e9e2d0", cloth_d="#cbbf9f", top=TEAL_CLOTH, pose=pose, eye=eye, mouth_kind=mk, sitting=sitting, queen=True)


def jambavan(pose="down", eye="happy", mk="smile", sitting=False):
    return person(skin=BEAR, hair="none", beard=WHITE_HAIR, outfit="dhoti", cloth=OCHRE, cloth_d=OCHRE_D, pose=pose,
                  sitting=sitting, eye=eye, mouth_kind=mk, face="bear", old=True, hold="staff" if pose == "down" else None)


def nala(pose="down", eye="happy", mk="smile"):
    return vanara(pose=pose, eye=eye, mk=mk, skin="#a8784a", cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D)


# ------------------------------------------------------------------ gods and wonders
def samudra(pose="namaste", eye="happy", mk="smile"):
    """The sea-king (வருணன்) rising from the waves."""
    return person(skin="#4fa3b5", hair="long", hair_color="#1f5f6f", outfit="dhoti", cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D,
                  sash="#ffffff", pose=pose, eye=eye, mouth_kind=mk, jewels=True, crown_kind="tall")


def agni(pose="bless", eye="happy", mk="smile"):
    flames = "".join(P(f"M{x},-150 C{x - 10},-176 {x + 6},-186 {x},-206 C{x + 14},-188 {x + 16},-170 {x + 8},-150 Z", "#ffb02e",
                       sw=1.6) for x in (-26, -6, 14))
    return flames + person(skin="#e0703a", hair="wild", hair_color="#ffb02e", outfit="dhoti", cloth=ROYAL_RED,
                           cloth_d=ROYAL_RED_D, pose=pose, eye=eye, mouth_kind=mk, jewels=True)


def big_bird(color="#8a5a34", wing="#6b4424", head="#f4efe4", wings="open", s=1.0, flip=False, gold=False):
    """சடாயு / சம்பாதி / கருடன்: a great eagle facing right; feet at (0,0). wings: open | closed | none."""
    if gold:
        color, wing, head = "#e2a23a", "#c47a1e", "#f6e2a8"
    out = []
    if wings == "open":
        out.append(P("M-10,-70 C-60,-130 -130,-128 -170,-104 C-130,-100 -100,-84 -86,-66 C-110,-60 -126,-46 -132,-30 "
                     "C-90,-40 -50,-44 -20,-50 Z", wing, sw=2.4))
        out.append(P("M-130,-108 L-100,-92 M-120,-60 L-90,-56", stroke="#4a2e18", sw=2))
    out += [E(0, -52, 40, 28, color, sw=2.4),
            P("M-34,-46 C-60,-40 -78,-26 -84,-12 C-60,-20 -42,-26 -26,-30 Z", wing, sw=2)]
    if wings == "closed":
        out.append(P("M-30,-70 C-10,-80 26,-70 30,-50 C10,-48 -14,-46 -36,-40 Z", wing, sw=2.2))
    elif wings == "none":
        out.append(P("M-20,-66 l10,6 l-4,8 M0,-70 l8,8 l-6,6", stroke="#3a2818", sw=2.4))
    out += [P("M22,-66 C26,-90 40,-100 52,-100", stroke=OUT, sw=17), P("M22,-66 C26,-90 40,-100 52,-100", stroke=head, sw=13),
            C(56, -100, 15, head, sw=2.2), P("M68,-104 C82,-102 84,-90 74,-88 L68,-94 Z", "#e2b23a", sw=1.8),
            C(58, -104, 2.4, "#2a1c14", stroke="none"),
            P("M-6,-26 L-10,0 M8,-26 L12,0 M-16,0 L-4,0 M4,0 L18,0", stroke="#d2a23a", sw=3.4)]
    return G(*out, s=s, flip=flip)


def golden_deer(s=1.0, flip=False):
    c = "#e6b84a"
    out = [P("M-20,-30 L-22,0 M-12,-30 L-10,0 M14,-30 L12,0 M22,-30 L26,0", stroke=OUT, sw=6),
           P("M-20,-30 L-22,0 M-12,-30 L-10,0 M14,-30 L12,0 M22,-30 L26,0", stroke=c, sw=3.4),
           E(0, -36, 28, 13, c), P("M20,-44 L30,-62", stroke=OUT, sw=9), P("M20,-44 L30,-62", stroke=c, sw=6),
           E(36, -64, 9, 6.5, c, sw=2), P("M30,-70 L28,-84 M28,-78 L22,-84 M34,-70 L38,-84 M37,-78 L44,-82", stroke="#b8862a", sw=2.2),
           E(32, -71, 3, 5, c, sw=1.6), C(39, -65, 1.4, "#2a1c14", stroke="none")]
    for x, y in ((-12, -38), (0, -42), (-4, -32), (10, -36)):
        out.append(C(x, y, 2.2, "#fff4c0", stroke="none"))
    out += [sparkle(-30, -60, .7, "#fff1a0"), sparkle(46, -88, .6, "#fff1a0")]
    return G(*out, s=s, flip=flip)


def kabandha(s=1.0):
    """கவந்தன்: a headless giant with a mouth in his belly and very long arms."""
    body = "#5a4a3a"
    out = [P("M-40,-60 C-120,-70 -150,-20 -160,10", stroke=OUT, sw=17), P("M-40,-60 C-120,-70 -150,-20 -160,10", stroke=body, sw=12),
           P("M40,-60 C120,-70 150,-20 160,10", stroke=OUT, sw=17), P("M40,-60 C120,-70 150,-20 160,10", stroke=body, sw=12),
           R(-22, -20, 16, 20, body, stroke=OUT, sw=2.2), R(6, -20, 16, 20, body, stroke=OUT, sw=2.2),
           E(0, -70, 60, 58, body, sw=2.6), E(0, -96, 14, 12, "#fff4d0", sw=2), C(0, -96, 5, "#2a1c14", stroke="none"),
           P("M-30,-52 Q0,-20 30,-52 Q0,-40 -30,-52 Z", "#7a2e2a", sw=2),
           P("M-24,-50 L-20,-42 L-16,-48 M16,-48 L20,-42 L24,-50", "#ffffff", sw=1.2)]
    return G(*out, s=s)


# ------------------------------------------------------------------ things
def padukas(s=1.0):
    """Rama's wooden sandals (பாதுகை) on a cushion."""
    one = (P("M-10,0 C-12,-24 -8,-44 0,-46 C8,-44 12,-24 10,0 C6,6 -6,6 -10,0 Z", "#a0682e", sw=2) +
           C(0, -30, 3.4, GOLD, sw=1.2) + P("M0,-30 L0,-40", stroke=GOLD_D, sw=2.4))
    return G(G(one, x=-14) + G(one, x=14), s=s)


def ring(s=1.0):
    """The signet ring (கணையாழி)."""
    return G(C(0, 0, 14, "none", stroke=GOLD_D, sw=6) + C(0, 0, 14, "none", stroke=GOLD, sw=3.4) +
             E(0, -16, 9, 7, JEWEL_RED, stroke=GOLD_D, sw=2) + sparkle(14, -24, .6, "#fff1a0"), s=s)


def chudamani(s=1.0):
    """Sita's hair jewel (சூடாமணி)."""
    return G(C(0, 0, 12, "#f6fbff", stroke=GOLD_D, sw=3) + C(0, 0, 6, "#9ad6f2", stroke="none") +
             P("M0,-12 L0,-22", stroke=GOLD_D, sw=2.4) + C(0, -24, 3, GOLD, sw=1.2) + sparkle(14, -10, .7, "#fff6c8"), s=s)


def pushpaka(s=1.0, rider_svg=""):
    """The flying chariot (புட்பக விமானம்): a small palace on clouds; base at (0,0)."""
    out = [cloud(-60, 4, 1.2), cloud(40, 8, 1.3), R(-110, -40, 220, 34, GOLD, stroke=OUT, sw=2.4, rx=10),
           R(-90, -100, 180, 60, MARBLE, stroke=OUT, sw=2.2),
           P("M-104,-100 L-60,-140 L60,-140 L104,-100 Z", GOLD, sw=2.4), P("M-40,-140 L0,-170 L40,-140 Z", GOLD_D, sw=2.2),
           C(0, -176, 6, JEWEL_RED, sw=1.6)]
    for x in (-70, -30, 10, 50):
        out.append(R(x, -92, 20, 44, "#f3d9a8", stroke=OUT, sw=1.6, rx=8))
    out += [P("M-110,-30 C-150,-60 -170,-30 -186,-50 C-170,-10 -140,-12 -110,-16 Z", "#ffffff", sw=2),
            P("M110,-30 C150,-60 170,-30 186,-50 C170,-10 140,-12 110,-16 Z", "#ffffff", sw=2)]
    return G(*out, s=s) + (rider_svg or "")


def bridge(x0, x1, y, rows=2):
    """Rocks laid across the sea (சேது)."""
    out = []
    for r in range(rows):
        yy = y + r * 18
        xx = x0 + (r % 2) * 14
        k = 0
        while xx < x1:
            w = 30 + (k * 7) % 14
            out.append(E(xx + w / 2, yy, w / 2, 10, ["#a9a39a", "#b8b2a8", "#9a948b"][k % 3], sw=2))
            xx += w - 4
            k += 1
    return "".join(out)


def burning(x, y, s=1.0):
    return G(P("M-20,0 C-26,-24 -10,-30 -8,-50 C2,-36 6,-44 4,-64 C18,-46 26,-30 18,-14 C26,-18 30,-8 26,0 Z", "#ff9a2e", sw=2) +
             P("M-8,0 C-10,-14 -2,-18 0,-32 C8,-20 12,-12 8,0 Z", "#ffe27a", sw=1.4), x=x, y=y, s=s)


def mace(s=1.0):
    return G(P("M0,40 L4,-40", stroke="#8a5a2b", sw=6) + C(5, -50, 16, GOLD, sw=2.2) + C(5, -50, 7, GOLD_D, stroke="none"), s=s)


def asoka_tree(x, y, s=1.0):
    pts = [(-40, -100), (-20, -128), (10, -136), (36, -110), (-30, -80), (20, -84), (0, -108), (44, -88), (-48, -118), (26, -126)]
    fl = "".join(C(px, py, 5.5, "#ff6a3a" if i % 2 else "#ffb030", sw=1.1) for i, (px, py) in enumerate(pts))
    return G(tree(0, 0, 1.0, 1) + fl, x=x, y=y, s=s)


def lanka_city(x, y, s=1.0):
    """The golden city of Lanka on its hill."""
    out = [P("M-260,0 C-200,-60 -120,-80 0,-84 C120,-80 200,-60 260,0 Z", "#8fa86a", sw=2.4)]
    for k, (dx, h) in enumerate(((-150, 70), (-90, 110), (-30, 150), (30, 130), (90, 100), (150, 70))):
        out.append(R(dx - 20, -84 - h + 20, 40, h, "#f2c14e", stroke=OUT, sw=2))
        out.append(P(f"M{dx - 26},{-84 - h + 20} L{dx},{-84 - h - 10} L{dx + 26},{-84 - h + 20} Z", "#e09a2a", sw=2))
        out.append(R(dx - 6, -84 - h + 40, 12, 18, "#7a4a22", stroke=OUT, sw=1.4, rx=5))
    out.append(R(-200, -94, 400, 18, "#e8b84a", stroke=OUT, sw=2))
    return G(*out, x=x, y=y, s=s)


def throne_pair(x, y, s=1.0):
    return G(throne(150), x=x, y=y, s=s)
