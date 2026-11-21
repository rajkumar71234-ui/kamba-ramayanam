"""Pictures for Bala Kandam (all padalams).

Run from the repo root:  python3 tools/art_bala.py [padalam numbers...]
Writes img/1/<pp>/chapter.svg and, where a padalam has scenes, scene-<k>.svg
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import *  # noqa: F401,F403
import art

OUT = Path(__file__).resolve().parent.parent / "img" / "1"


def gopuram(x, y, s=1.0, color="#e9c98a"):
    """Temple tower in the distance."""
    t = [R(-46, -40, 92, 40, color, stroke=OUT, sw=2.2), R(-14, -34, 28, 34, "#6b4a2e", stroke=OUT, sw=2, rx=12)]
    for k in range(5):
        w = 80 - k * 13
        t.append(R(-w / 2, -40 - (k + 1) * 24, w, 24, color, stroke=OUT, sw=2))
        t.append(P(f"M{-w/2+6},{-40 - (k+1)*24 + 12} L{w/2-6},{-40 - (k+1)*24 + 12}", stroke="#c9a46a", sw=1.4))
    t.append(P("M-20,-160 Q0,-178 20,-160 Z", GOLD, sw=2))
    t += [C(-8, -172, 3, GOLD, sw=1.2), C(0, -176, 3, GOLD, sw=1.2), C(8, -172, 3, GOLD, sw=1.2)]
    return G(*t, x=x, y=y, s=s)


def olai_stack(x, y, s=1.0):
    return G(G(palm_leaf(), y=0) + G(palm_leaf(), x=3, y=-12) + G(palm_leaf(), x=-2, y=-24) +
             P("M-20,-30 L-20,8 M20,-30 L20,8", stroke="#8a5a2b", sw=1.6), x=x, y=y, s=s)


def desk(x, y, s=1.0):
    return G(R(-46, -30, 92, 10, "#a9733f", stroke=OUT, sw=2.2, rx=3) +
             R(-40, -20, 8, 20, "#8a5a2b", stroke=OUT, sw=2) + R(32, -20, 8, 20, "#8a5a2b", stroke=OUT, sw=2) +
             G(palm_leaf(), x=0, y=-36, s=0.9), x=x, y=y, s=s)


# ======================= 00 பாயிரம் =======================
def p00_chapter():
    return svg(
        sky(), sun(660, 110, 32), cloud(170, 80, 1.0), cloud(470, 60, 0.7),
        hills(300), gopuram(640, 330, 1.05), tree(60, 330, 1.0, 1), tree(760, 340, 0.9, 0),
        ground(330, "#cfe3a2"),
        R(160, 392, 320, 22, "#d8c7a6", stroke=OUT, sw=2.2), R(170, 412, 300, 70, "#e6d6b6", stroke=OUT, sw=2.2),
        G(seat(150, "#b5452f"), x=300, y=392),
        G(kamban("lap", sitting=True, eye="closed"), x=300, y=390, s=1.35),
        G(desk(0, 0, 0.9), x=390, y=392),
        G(lamp(0.95), x=200, y=392),
        olai_stack(440, 380, 0.7),
        G(patron("namaste", hold=None), x=560, y=470, s=1.15),
        G(cat("sit"), x=120, y=486, s=0.9),
        grass_tufts([(60, 470), (700, 488), (760, 460)]),
        defs=sky_defs("dawn"),
        title="திருவெண்ணெய்நல்லூரில் கம்பர் இராமாவதாரம் இயற்றுதல்")


def p00_scene1():
    import math as m
    orbit = []
    for k, (r, col, a) in enumerate([(70, "#7ab8e8", 0.6), (100, "#e8b04a", 2.4), (130, "#9ad07a", 4.2), (160, "#e08080", 5.4)]):
        orbit.append(E(560, 190, r, r * 0.42, "none", stroke="#ffffff", sw=1.6, opacity=0.8))
        orbit.append(C(560 + r * m.cos(a), 190 + r * 0.42 * m.sin(a), 9 - k, col, sw=1.6))
    return svg(
        sky(), rays(560, 190, n=18, r1=50, r2=460, opacity=0.45),
        *orbit,
        C(560, 190, 38, "#fff4c9", sw=2.4), C(560, 190, 24, "#ffe38a", stroke="none"),
        moon(700, 80, 20, crescent=False), stars([(380, 70, 1.0), (450, 300, 0.8), (720, 260, 1.1), (300, 150, 0.7), (650, 330, 0.7)]),
        hills(380, "#e7d9a8", "#d9c98e"), ground(420, "#c9dc93"),
        G(kamban("namaste", eye="closed", hold=None), x=220, y=470, s=1.4),
        tree(60, 430, 0.9, 1),
        grass_tufts([(100, 486), (380, 470), (600, 488)]),
        defs=sky_defs("divine"),
        title="உலகங்களைப் படைத்து, காத்து, அழிக்கும் விளையாட்டை உடைய தலைவனுக்கே சரண்")


def p00_scene2():
    return svg(
        sky(), cloud(160, 80, 0.9), cloud(560, 70, 1.0),
        milk_sea(250, 500),
        P("M0,330 C120,320 220,350 330,380 C380,400 400,440 390,500 L0,500 Z", SAND, stroke="none"),
        G(cat("lap"), x=360, y=402, s=1.25),
        G(kamban("chest", eye="happy", hold=None), x=150, y=470, s=1.4),
        sparkle(470, 300, 0.9, "#ffffff"), sparkle(620, 360, 0.7, "#ffffff"),
        thought_bubble(620, 150, 220, 120, tail="left"),
        G(cat("sit"), x=560, y=180, s=0.6), G(palm_leaf(), x=650, y=160, s=1.1), sparkle(690, 120, 0.8),
        defs=sky_defs("day"),
        title="பாற்கடல் முழுவதையும் நக்கிக் குடிக்கப் புகுந்த பூனை போல")


def p00_scene3():
    return svg(
        sky(), sun(120, 100, 26), cloud(330, 70, 0.8),
        hills(300), gopuram(700, 330, 0.85), ground(330, "#cfe3a2"),
        thought_bubble(250, 140, 260, 150, tail="right"),
        G(art.valmiki("lap", sitting=True, eye="closed"), x=230, y=190, s=0.62),
        G(palm_leaf(), x=300, y=178, s=0.7), G(verse_dots(4, 8, 7, 2.2, glow=False), x=310, y=110, s=1.0),
        R(250, 396, 260, 20, "#d8c7a6", stroke=OUT, sw=2.2),
        G(seat(130, "#b5452f"), x=380, y=396),
        G(kamban("lap", sitting=True, eye="happy"), x=380, y=394, s=1.3),
        G(desk(0, 0, 0.8), x=470, y=396), G(lamp(0.8), x=290, y=396),
        G(patron("offer", hold=None), x=620, y=476, s=1.2),
        grass_tufts([(60, 470), (720, 488)]),
        defs=sky_defs("dawn"),
        title="வான்மீகியின் வழியில், சடையன் வெண்ணெய்நல்லூரில் பிறந்த காவியம்")


# ======================= 01 ஆற்றுப் படலம் =======================
def p01_chapter():
    river_path = ("M300,250 C330,300 260,330 300,370 C340,410 470,400 520,440 C560,470 600,490 640,500 "
                  "L760,500 C700,470 640,440 600,410 C540,370 420,370 380,340 C350,310 380,280 340,250 Z")
    return svg(
        sky(), mountain(300, 300, 1.25, gold=True),
        dark_cloud(230, 100, 1.2), dark_cloud(360, 80, 1.0), dark_cloud(300, 120, 0.9),
        rain(190, 400, 110, 220, "#e6f2ff", 14),
        hills(330, "#b7d9b0", "#9cc99a"), field_band(390, 110, "#c7e29a"),
        P(river_path, "url(#water)", sw=2.2),
        P("M330,280 C350,320 300,345 330,370 M420,380 C480,395 540,420 580,450", stroke=WATER_L, sw=2.4),
        paddy(30, 260, 440, 3), paddy(600, 790, 420, 2, ripe=True),
        coconut(80, 420, 0.75, 8), coconut(720, 400, 0.7, -6),
        G(peacock(), x=170, y=488, s=0.7), G(swan(), x=520, y=470, s=0.9),
        defs=sky_defs("day"),
        title="இமயத்தில் பொழிந்த மழை சரயு ஆறாகிக் கோசல நாட்டை வளப்படுத்துதல்")


def p01_scene1():
    return svg(
        sky(), sea(330, 500),
        cloud(110, 200, 1.3), P("M90,214 C96,250 110,290 120,330", stroke="#ffffff", sw=10, opacity=0.8),
        P("M150,210 C160,250 170,290 176,330", stroke="#ffffff", sw=7, opacity=0.7),
        cloud(250, 120, 1.0), dark_cloud(380, 100, 1.1, "#5a6fa0"), dark_cloud(470, 130, 0.9, "#4a5f90"),
        P("M300,110 q30,-30 60,-8", stroke="#ffffff", sw=3, stroke_dasharray="6 8"),
        mountain(640, 330, 1.2, gold=True), dark_cloud(600, 90, 1.2, "#4a5f90"), dark_cloud(700, 110, 0.9, "#4a5f90"),
        rain(560, 760, 110, 300, "#f2f6ff", 12),
        sparkle(600, 250, 0.8, "#ffffff"), sparkle(690, 220, 0.7, "#ffffff"),
        defs=sky_defs("day"),
        title="வெண்மேகம் கடல் நீரைப் பருகிக் கருமேகமாகி இமயத்தில் பொழிதல்")


def p01_scene2():
    flood = ("M0,330 C140,310 300,350 460,330 C600,312 700,340 800,320 L800,450 C640,470 460,440 300,460 C160,478 60,460 0,470 Z")
    bits = []
    for x, y in [(90, 380), (210, 410), (330, 370), (450, 420), (560, 380), (680, 410), (760, 370)]:
        bits.append(sparkle(x, y, 0.8, GOLD))
    for x, y, c in [(150, 360, "#f28aa6"), (280, 430, "#ffd34e"), (400, 390, "#ffffff"), (620, 440, "#f28aa6"), (720, 360, "#ffd34e")]:
        bits.append(C(x, y, 6, c, sw=1.4))
    return svg(
        sky(), rainbow(400, 330, 300, 0.7), cloud(120, 70, 0.9), cloud(650, 60, 0.8),
        hills(300, "#a9cf9f", "#8fbf8a"),
        P(flood, "#c98a4a", sw=2.4),
        P("M0,360 C160,345 320,380 480,360 C620,344 720,370 800,352", stroke="#e8b47a", sw=3),
        P("M0,410 C160,398 320,428 480,410 C620,396 720,420 800,404", stroke="#e8b47a", sw=3),
        R(240, 395, 90, 14, "#8a5a2b", stroke=OUT, sw=2, rx=6), R(520, 360, 70, 12, "#8a5a2b", stroke=OUT, sw=2, rx=6),
        *bits,
        P("M0,470 C200,450 520,480 800,456 L800,500 L0,500 Z", SAND, stroke="none"),
        tree(720, 330, 1.0, 0), G(monkey(), x=700, y=262, s=0.9), G(monkey(pose="wave"), x=740, y=250, s=0.8),
        tree(70, 330, 0.9, 2), G(monkey(), x=70, y=250, s=0.8),
        defs=sky_defs("day"),
        title="மலைப் பொருள்களை எல்லாம் வாரிக்கொண்டு பெருகி வரும் சரயுவின் வெள்ளம்")


def p01_scene3():
    chans = ("M360,250 C380,300 300,320 300,360 C300,400 200,420 120,500 L170,500 C230,440 330,410 340,370 "
             "C350,330 420,300 400,250 Z")
    chan2 = "M330,350 C420,380 520,400 640,500 L690,500 C560,390 460,360 360,330 Z"
    return svg(
        sky(), sun(680, 90, 30), cloud(200, 70, 0.9),
        hills(260, "#b7d9b0", "#9cc99a"), field_band(300, 200, "#c7e29a"),
        paddy(20, 280, 340, 2), paddy(440, 790, 330, 2), paddy(420, 780, 420, 3, ripe=True), paddy(20, 120, 440, 3, ripe=True),
        P(chans, "url(#water)", sw=2.2), P(chan2, "url(#water)", sw=2.2),
        lotus(330, 420, 0.8), lotus(560, 440, 0.7),
        coconut(60, 330, 0.7, 6), coconut(760, 320, 0.75, -8),
        G(man(pose="raise", cloth="#f2efe6", skin="#b9784a", hair="turban", top=None), x=230, y=470, s=1.0),
        G(man(pose="wave", cloth="#f2efe6", skin="#a86a3e", hair="bun"), x=470, y=470, s=0.95),
        G(woman(pose="pot", cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, hold="pot"), x=600, y=470, s=0.95),
        G(bull(), x=720, y=480, s=0.7),
        defs=sky_defs("day"),
        title="ஐவகை நிலங்களிலும் பாய்ந்து வயல்களை நிறைக்கும் சரயு; மகிழ்ந்து ஆர்ப்பரிக்கும் உழவர்")


# ======================= 02 நாட்டுப் படலம் =======================
def p02_chapter():
    return svg(
        sky(), sun(120, 90, 30), cloud(330, 70, 0.9), cloud(620, 90, 1.0),
        hills(250, "#b7d9b0", "#9cc99a"),
        coconut(60, 300, 0.8, 6), coconut(150, 290, 0.65, -6), coconut(740, 300, 0.85, -8),
        art.hut(640, 300, 0.75), art.hut(540, 296, 0.55),
        field_band(300, 200, "#d6e9a8"),
        paddy(20, 790, 340, 2, ripe=True), paddy(20, 300, 420, 3, ripe=True), paddy(520, 790, 430, 3),
        P("M300,500 C330,440 400,400 520,380 L560,384 C440,410 380,450 360,500 Z", "url(#water)", sw=2),
        G(man(pose="raise", cloth="#f2efe6", skin="#b9784a", hair="turban"), x=200, y=470, s=0.95),
        G(woman(cloth=PURPLE_CLOTH, cloth_d=PURPLE_CLOTH_D, hold="basket", pose="down"), x=110, y=470, s=0.9),
        G(bull(), x=640, y=470, s=0.8),
        G(peacock(), x=450, y=360, s=0.75),
        sparkle(380, 150, 0.8), 
        defs=sky_defs("day"),
        title="கோசல நாட்டின் வளம்: விளைந்த வயல்கள், மகிழும் மக்கள்")


# ======================= 03 நகரப் படலம் =======================
def p03_chapter():
    return svg(
        sky(), cloud(130, 70, 0.9), cloud(560, 60, 0.8),
        palace(400, 250, 0.9), tower(170, 250, 1.0), tower(630, 250, 1.0),
        flag(140, 120, ROYAL_RED, 1.0), flag(600, 110, "#f2a33a", 1.0), flag(360, 80, GOLD, 0.9), flag(460, 84, ROYAL_RED, 0.9),
        city_wall(360, 0, 800, "#e8c98a", 110, gate_x=400),
        flag(330, 210, "#3f9a6b", 0.9), flag(470, 210, "#3f9a6b", 0.9),
        moat(372, 70),
        P("M370,372 L430,372 L436,442 L364,442 Z", "#c9a46a", sw=2),
        G(swan(), x=560, y=420, s=0.9), G(swan(), x=650, y=430, s=0.7),
        R(0, 442, 800, 58, SAND),
        G(elephant(howdah=False, umbrella=False, rider=man(cloth=ROYAL_RED, cloth_d=ROYAL_RED_D, hair="turban", top=GOLD)), x=150, y=494, s=0.55),
        G(woman(cloth=PINK_CLOTH, cloth_d=PINK_CLOTH_D, hold="pot", pose="pot"), x=600, y=496, s=0.75),
        G(man(cloth=MILK, hair="turban", hold=None, pose="walk"), x=700, y=496, s=0.75),
        defs=sky_defs("day"),
        title="அயோத்தி: பொன் மதில், அகழி, கொடிகள் அசையும் அரண்மனைகள்")


# ======================= 04 அரசியற் படலம் =======================
def p04_chapter():
    return svg(
        hall(380, "#f6e3c0"),
        R(300, 350, 200, 30, "#d8b77a", stroke=OUT, sw=2.2), R(280, 378, 240, 18, "#c9a46a", stroke=OUT, sw=2.2),
        G(throne(140), x=400, y=316, s=1.0),
        G(dasaratha("abhaya", sitting=True, eye="happy"), x=400, y=314, s=1.15),
        G(white_umbrella(), x=470, y=200, s=1.0),
        G(woman(cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, pose="namaste"), x=130, y=480, s=0.95),
        G(man(pose="namaste", cloth=MILK, hair="turban"), x=210, y=482, s=0.95),
        G(art.disciple("namaste", eye="happy"), x=600, y=482, s=1.0),
        G(man(pose="namaste", cloth="#f2efe6", skin="#a86a3e", hair="bun"), x=690, y=482, s=0.95),
        sparkle(250, 140, 0.8), sparkle(560, 130, 0.7),
        defs=indoor_defs(),
        title="தாயினும் அன்புடன் உலகைக் காத்த தயரதன்: வெண்கொற்றக் குடையின் கீழ் அறச் செங்கோல்")


# ======================= 05 திரு அவதாரப் படலம் =======================
def p05_chapter():
    pet = [(x, y, r) for x, y, r in [(120, 80, 20), (220, 140, 70), (330, 60, 10), (470, 110, 40), (600, 70, 80), (700, 150, 30),
                                       (160, 220, 60), (640, 230, 15), (380, 200, 100)]]
    return svg(
        hall(390, "#f7e6c6", curtain="#c9473d"),
        rays(400, 250, n=14, r1=40, r2=300, opacity=0.25),
        G(cradle(0, 0, 1.15), x=400, y=420),
        G(baby(RAMA_BLUE), x=400, y=410, s=1.3),
        G(woman(cloth=PINK_CLOTH, cloth_d=PINK_CLOTH_D, pose="namaste", queen=True, eye="happy"), x=230, y=480, s=1.1),
        G(dasaratha("raise", eye="happy"), x=570, y=482, s=1.12),
        G(vasishtha("bless", hold=None), x=700, y=482, s=1.0),
        G(woman(cloth=BLUE_CLOTH, cloth_d=BLUE_CLOTH_D, pose="offer", eye="happy"), x=110, y=482, s=0.9),
        petals(pet), stars([(300, 160, 0.8), (520, 170, 0.9), (420, 90, 0.7)], GOLD),
        defs=indoor_defs(),
        title="இராமன் அவதரித்தான்: தொட்டிலில் குழந்தை இராமன்; மகிழும் தயரதன், கோசலை, வசிட்டர்")


# ======================= 06 கையடைப் படலம் =======================
def p06_chapter():
    return svg(
        hall(380, "#f3e1c2"),
        R(560, 350, 200, 30, "#d8b77a", stroke=OUT, sw=2.2),
        G(throne(120), x=660, y=318, s=1.0),
        G(dasaratha("chest", sitting=True, eye="sad", mouth_kind="sad"), x=660, y=316, s=1.05),
        G(white_umbrella(), x=720, y=210, s=0.85),
        G(vasishtha("bless", hold=None), x=520, y=482, s=1.0),
        G(vishwamitra("abhaya"), x=120, y=482, s=1.15),
        G(rama("namaste", hold="bow", crown_kind="small"), x=260, y=482, s=1.0),
        G(lakshmana("namaste", hold="bow"), x=360, y=484, s=0.95),
        defs=indoor_defs(),
        title="தயரதன் மனம் கலங்க, இராம இலக்குவரை விசுவாமித்திரரிடம் அடைக்கலமாக ஒப்படைத்தல்")


# ======================= 07 தாடகை வதைப் படலம் =======================
def p07_chapter():
    cracks = "".join(P(f"M{x},{y} l14,8 l-6,12 l16,6", stroke="#b98a52", sw=2) for x, y in [(80, 420), (300, 460), (520, 430), (680, 470), (420, 480)])
    dead = "".join(G(P("M0,0 L0,-70 M0,-40 L-20,-60 M0,-50 L18,-74", stroke="#7a5a3a", sw=5), x=x, y=y, s=sc)
                   for x, y, sc in [(60, 370, 1.0), (740, 360, 0.9), (470, 350, 0.7)])
    return svg(
        sky(), sun(110, 90, 40), C(110, 90, 70, "#fff0c0", stroke="none", opacity=0.4),
        hills(330, "#e8c78f", "#dbb578"), R(0, 360, 800, 140, "#ecd29a"), cracks, dead,
        G(demon(pose="raise", hold=None, female=True, skin="#5f5384", cloth="#6b3a2a"), x=610, y=470, s=1.55),
        G(P("M0,40 L0,-120", stroke="#5d5d5d", sw=5) + P("M-16,-120 C-16,-98 16,-98 16,-120 M0,-130 L0,-100", stroke="#5d5d5d", sw=4.5),
          x=700, y=300, rot=18),
        G(rama("draw", hold=None, eye="stern", mouth_kind="flat"), x=230, y=470, s=1.15),
        G(lakshmana("namaste", hold="bow", eye="wonder"), x=110, y=470, s=0.85),
        G(vishwamitra("point", eye="open"), x=40, y=470, s=0.8),
        defs=desert_defs(),
        title="பாலை நிலத்தில் சீறி வந்த தாடகையை இராமன் ஒரே அம்பினால் வீழ்த்துதல்")


# ======================= 08 வேள்விப் படலம் =======================
def flying_demon(x, y, s=1.0, rot=0, hold="mace", skin=SKIN_DEMON):
    return G(demon(pose="raise", hold=None, skin=skin), x=x, y=y, s=s, rot=rot)


def p08_chapter():
    return svg(
        sky(), dark_cloud(560, 90, 1.6, "#5a5f7a"), dark_cloud(700, 140, 1.2, "#4f5470"), dark_cloud(420, 70, 1.0, "#5a5f7a"),
        flying_demon(560, 230, 0.75, -20), flying_demon(720, 170, 0.6, 40, skin="#4f7a5a"),
        P("M380,240 L520,200", stroke="#8a5a2b", sw=3), P("M520,196 L534,200 L520,206 Z", "#cfd6dc", sw=1.4),
        P("M760,140 q20,-20 40,-30", stroke="#ffffff", sw=2.4, stroke_dasharray="5 6"),
        hills(330, "#b7d9b0", "#9cc99a"), ground(360, "#cfe3a2"),
        tree(60, 370, 1.0, 0), art.hut(160, 372, 0.7),
        fire_altar(430, 460, 1.0),
        G(vishwamitra("lap", sitting=True, eye="closed", hold=None), x=560, y=462, s=1.05),
        G(rama("draw", hold=None, eye="stern", mouth_kind="flat"), x=280, y=476, s=1.0, rot=-12),
        G(lakshmana("down", hold="bow", eye="stern", mouth_kind="flat"), x=700, y=478, s=0.95),
        defs=sky_defs("evening"),
        title="விசுவாமித்திரரின் வேள்வியைக் காத்தல்: சுபாகு வீழ்ந்தான், மாரீசன் கடலில் எறியப்பட்டான்")


# ======================= 09 அகலிகைப் படலம் =======================
def p09_chapter():
    ahalya = woman(cloth=MILK, cloth_d=WHITE_CLOTH_D, top="#e9dfc8", pose="namaste", eye="happy", hair="bun")
    return svg(
        sky(), cloud(150, 80, 0.9), cloud(600, 60, 0.8),
        hills(290, "#a9cf9f", "#8fbf8a"), tree(40, 330, 1.1, 1), tree(140, 320, 0.8, 2), tree(760, 330, 1.0, 0),
        ground(330, "#cfe3a2"),
        P("M0,420 C200,400 480,430 800,410", stroke="#e6d6a6", sw=26), 
        rays(470, 360, n=14, r1=30, r2=260, opacity=0.35),
        stone(470, 470, 1.15, glow=True),
        G(ahalya, x=470, y=420, s=1.05),
        sparkle(400, 300, 0.9), sparkle(540, 290, 0.8), sparkle(470, 250, 0.7),
        G(rama("bless", hold="bow"), x=300, y=478, s=1.05),
        G(lakshmana("namaste", hold="bow", eye="wonder"), x=190, y=478, s=0.95),
        G(vishwamitra("speak", eye="happy", mouth_kind="open"), x=640, y=478, s=1.05),
        defs=sky_defs("dawn"),
        title="இராமனின் திருவடித் துகள் பட்டுக் கல்லாய்க் கிடந்த அகலிகை மீண்டும் உருப்பெறுதல்")


# ======================= 10 மிதிலைக் காட்சிப் படலம் =======================
def p10_chapter():
    return svg(
        sky(), cloud(120, 60, 0.8),
        R(430, 0, 370, 330, MARBLE, stroke=OUT, sw=2.4), R(430, 0, 370, 18, GOLD, stroke=OUT, sw=2),
        balcony(610, 210, 220, 130),
        G(sita("down", eye="happy"), x=575, y=210, s=0.95),
        G(woman(cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, pose="namaste", eye="happy"), x=665, y=210, s=0.8),
        flag(80, 210, ROYAL_RED, 1.1, 90, 6), flag(200, 180, "#f2a33a", 1.0, 80, -4), flag(320, 200, "#3f9a6b", 1.0, 80, 4),
        R(0, 330, 800, 170, "#e6d6b6"), P("M0,330 L800,330", stroke="#c9a46a", sw=2.2),
        P("M330,250 Q450,170 540,145", stroke=GOLD, sw=2.4, stroke_dasharray="4 7"),
        sparkle(440, 190, 0.8), sparkle(500, 160, 0.6),
        G(rama("down", hold="bow", eye="wonder"), x=300, y=474, s=1.2),
        G(lakshmana("down", hold="bow", eye="happy"), x=170, y=474, s=1.0),
        G(vishwamitra("walk"), x=70, y=476, s=0.95),
        defs=sky_defs("day"),
        title="“அண்ணலும் நோக்கினான்; அவளும் நோக்கினாள்” — கன்னிமாடத்தில் சீதையும் வீதியில் இராமனும்")


# ======================= 11 குலமுறை கிளத்து படலம் =======================
def p11_chapter():
    kings = "".join(G(person(skin=SKIN_KING, hair="none", moustache=BLACK_HAIR, outfit="robe", cloth=c, cloth_d=c, top=GOLD,
                             crown_kind="tall", jewels=True, eye="happy"), x=x, y=232, s=0.38)
                    for x, c in [(290, ROYAL_RED), (350, TEAL_CLOTH), (410, PURPLE_CLOTH), (470, BLUE_CLOTH), (530, SAFFRON)])
    return svg(
        hall(380, "#f3e1c2"),
        thought_bubble(410, 150, 380, 190, tail="left"),
        C(410, 92, 24, "#ffd34e", stroke=GOLD_D, sw=2), rays(410, 92, n=12, r1=10, r2=46, color="#ffcf4a", opacity=0.8),
        P("M410,118 L410,140 M290,140 L530,140 M290,140 L290,150 M350,140 L350,150 M410,140 L410,150 M470,140 L470,150 M530,140 L530,150",
          stroke=GOLD_D, sw=2.4),
        kings,
        R(560, 350, 200, 30, "#d8b77a", stroke=OUT, sw=2.2),
        G(throne(120), x=660, y=318, s=1.0),
        G(janaka("chest", sitting=True, eye="happy"), x=660, y=316, s=1.05),
        G(vishwamitra("speak", mouth_kind="open"), x=470, y=484, s=1.05),
        G(rama("namaste", sitting=True, hold=None, crown_kind="small"), x=170, y=470, s=0.95),
        G(lakshmana("namaste", sitting=True, hold=None), x=300, y=474, s=0.88),
        defs=indoor_defs(),
        title="விசுவாமித்திரர் சனகனுக்கு இராமனின் சூரிய குல மரபை எடுத்துரைத்தல்")


# ======================= 12 கார்முகப் படலம் =======================
def p12_chapter():
    bow_l = P("M392,250 C300,236 200,250 120,300", stroke="#7a4a21", sw=14)
    bow_r = P("M408,250 C500,236 600,250 680,300", stroke="#7a4a21", sw=14)
    bow_l2 = P("M392,250 C300,236 200,250 120,300", stroke="#a9733f", sw=8)
    bow_r2 = P("M408,250 C500,236 600,250 680,300", stroke="#a9733f", sw=8)
    return svg(
        hall(390, "#f3e1c2"),
        rays(400, 250, n=16, r1=30, r2=360, color="#fff1b0", opacity=0.55),
        bow_l, bow_l2, bow_r, bow_r2,
        C(400, 250, 30, "#ffffff", stroke="none", opacity=0.9), sparkle(400, 250, 2.2, "#ffd34e"),
        P("M340,200 l-20,-24 M460,200 l20,-24 M400,190 l0,-30", stroke="#f2a33a", sw=4),
        G(rama("raise", hold=None, eye="happy"), x=400, y=470, s=1.15),
        G(janaka("raise", eye="wonder", mouth_kind="open"), x=600, y=480, s=1.0),
        G(vishwamitra("bless", eye="happy", hold=None), x=700, y=482, s=1.0),
        G(lakshmana("raise", hold=None, eye="happy"), x=220, y=478, s=0.95),
        G(sita("garland", bride=False, eye="happy"), x=95, y=478, s=1.0),
        defs=indoor_defs(),
        title="சிவனின் பெருவில்லை இராமன் எடுத்தான்; வில் இற்ற ஓசை மூவுலகும் கேட்டது")


# ======================= 13 எழுச்சிப் படலம் =======================
def p13_chapter():
    dust = "".join(C(x, y, r, "#efe2c4", stroke="none", opacity=0.8) for x, y, r in [(60, 420, 40), (120, 400, 30), (700, 410, 36), (760, 430, 30)])
    return svg(
        sky(), cloud(150, 60, 0.8), cloud(620, 70, 0.9),
        hills(270, "#b7d9b0", "#9cc99a"),
        city_wall(300, 0, 260, "#e8c98a", 70), tower(80, 230, 0.6), flag(160, 190, ROYAL_RED, 0.8),
        R(0, 300, 800, 200, "#e8d7a8"), dust,
        G(elephant(howdah=True, umbrella=True, rider=dasaratha("bless", eye="happy")), x=430, y=470, s=0.95),
        G(horse(rider=man(cloth=ROYAL_RED, cloth_d=ROYAL_RED_D, hair="turban", top=GOLD, hold="sword")), x=680, y=480, s=0.85),
        G(chariot(rider=None), x=120, y=480, s=0.7),
        flag(250, 470, ROYAL_RED, 1.2, 110, 4), flag(560, 470, "#f2a33a", 1.2, 110, -4),
        G(drum(0, 0, 1.0), x=300, y=488), G(man(pose="raise", cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, hair="turban"), x=300, y=490, s=0.7),
        defs=sky_defs("day"),
        title="மணவிழாவுக்காகத் தயரதன் பெரும் படையுடனும் சுற்றத்துடனும் மிதிலைக்குப் புறப்படுதல்")


# ======================= 14 சந்திரசயிலப் படலம் =======================
def p14_chapter():
    smoke = "".join(C(x, y, r, "#e9edf2", stroke="none", opacity=0.75) for x, y, r in [(640, 300, 12), (650, 280, 15), (662, 256, 18), (676, 228, 21)])
    return svg(
        sky(), moon(620, 80, 34, crescent=True), stars([(120, 60, 0.8), (300, 100, 0.6), (480, 50, 0.7), (720, 160, 0.6), (200, 170, 0.5)]),
        mountain(330, 330, 1.45, color="#c9d3e6", snow="#ffffff"),
        hills(340, "#6f8f86", "#5d7d74"), R(0, 370, 800, 130, "#7a9a8a"),
        tent(120, 400, 0.9, "#f2e2b8", ROYAL_RED), tent(250, 390, 0.75, "#f6e7c4", "#3f9a6b"), tent(560, 395, 0.8, "#f2e2b8", "#f2a33a"),
        tent(700, 405, 0.95, "#f6e7c4", ROYAL_RED),
        R(630, 316, 26, 18, "#7a5a3a", stroke=OUT, sw=2), C(643, 314, 7, "#ffb02e", stroke="none"), smoke,
        lotus_pond(400, 450, 150, 32),
        G(elephant(deco=False, trunk="up"), x=430, y=470, s=0.55),
        G(woman(cloth=PURPLE_CLOTH, cloth_d=PURPLE_CLOTH_D, sitting=True, pose="lap", eye="closed"), x=110, y=470, s=0.8),
        G(man(cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, hair="turban", pose="wave"), x=690, y=490, s=0.8),
        defs=night_defs(),
        title="நிலவொளி படரும் சந்திரசயில மலைச்சாரலில் படை தங்குதல்")


# ======================= 15 வரைக் காட்சிப் படலம் =======================
def p15_chapter():
    return svg(
        sky(), sun(640, 150, 34), cloud(200, 80, 0.9),
        mountain(260, 360, 1.5, color="#9db7c9"), mountain(620, 380, 1.1, color="#a9c3d3"),
        waterfall(300, 330, 140, 30),
        hills(360, "#a9cf9f", "#8fbf8a"), ground(400, "#c7e29a"),
        lotus_pond(320, 420, 110, 20),
        tree(720, 410, 1.0, 1), tree(60, 410, 0.9, 0),
        G(peacock(), x=160, y=470, s=0.85), G(deer(), x=760, y=486, s=0.8),
        G(man(cloth=BLUE_CLOTH, cloth_d=BLUE_CLOTH_D, hair="bun", pose="point", top=GOLD), x=500, y=480, s=0.95),
        G(woman(cloth=PINK_CLOTH, cloth_d=PINK_CLOTH_D, pose="namaste", eye="happy"), x=590, y=480, s=0.9),
        defs=sky_defs("evening"),
        title="சந்திரசயில மலையின் அழகு: அருவி, மயில், மான்; மாலையில் மலைக் காட்சி காணும் மக்கள்")


# ======================= 16 பூக்கொய் படலம் =======================
def blossom_tree(x, y, s=1.0, flower="#f7a8c0"):
    pts = [(-40, -100), (-20, -128), (10, -136), (36, -110), (-30, -80), (20, -84), (0, -108), (44, -88), (-48, -118)]
    fl = "".join(C(px, py, 5, flower, sw=1.2) for px, py in pts)
    return G(tree(0, 0, 1.0, 2) + fl, x=x, y=y, s=s)


def p16_chapter():
    return svg(
        sky(), sun(120, 80, 28), cloud(420, 60, 0.8),
        hills(300, "#b7d9b0", "#9cc99a"), ground(330, "#cfe3a2"),
        blossom_tree(120, 380, 1.3), blossom_tree(400, 360, 1.1, "#ffffff"), blossom_tree(680, 380, 1.35, "#ffd34e"),
        bush(560, 420, 1.0, "#5aa060"), bush(260, 430, 0.9, "#4f9a5f"),
        "".join(C(x, y, 4, c, sw=1) for x, y, c in [(540, 400, "#f28aa6"), (575, 395, "#ffffff"), (250, 410, "#ffd34e"), (275, 404, "#f28aa6")]),
        G(woman(cloth=PINK_CLOTH, cloth_d=PINK_CLOTH_D, pose="wave", hold=None, eye="happy"), x=180, y=480, s=1.0),
        G(woman(cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, hold="basket", eye="happy"), x=330, y=480, s=0.95),
        G(woman(cloth=PURPLE_CLOTH, cloth_d=PURPLE_CLOTH_D, pose="garland", eye="happy"), x=470, y=480, s=0.95),
        G(peacock(), x=640, y=480, s=0.8),
        bee(200, 300), bee(230, 280, 0.9), bee(440, 270), bee(660, 300, 1.1), bee(700, 280),
        defs=sky_defs("day"),
        title="சோலையில் மகளிர் மலர் கொய்தல்; மொய்க்கும் வண்டுகள், ஆடும் மயில்")


# ======================= 17 நீர் விளையாட்டுப் படலம் =======================
def splash(x, y, s=1.0):
    return G("".join(C(dx, dy, r, "#dff4fa", stroke=WATER_D, sw=1.2) for dx, dy, r in
                     [(-14, -10, 4), (-6, -22, 3.4), (4, -16, 4.4), (12, -26, 3), (18, -12, 3.6)]), x=x, y=y, s=s)


def p17_chapter():
    def bather(c, cd, pose, x, eye="happy"):
        return G(woman(cloth=c, cloth_d=cd, pose=pose, eye=eye), x=x, y=430, s=0.9)
    return svg(
        sky(), sun(680, 90, 30), cloud(220, 70, 0.9),
        hills(260, "#a9cf9f", "#8fbf8a"), ground(290, "#cfe3a2"),
        tree(60, 300, 1.0, 0), tree(740, 300, 1.05, 2), blossom_tree(160, 300, 0.8),
        bather(PINK_CLOTH, PINK_CLOTH_D, "raise", 260), bather(TEAL_CLOTH, TEAL_CLOTH_D, "wave", 400),
        bather(PURPLE_CLOTH, PURPLE_CLOTH_D, "raise", 540),
        P("M0,360 C200,340 600,350 800,345 L800,500 L0,500 Z", "url(#water)", stroke="none"),
        "".join(P(f"M{x},{y} q12,-6 24,0 t24,0", stroke=WATER_L, sw=2.4) for x, y in [(60, 400), (300, 440), (520, 420), (660, 470), (180, 470)]),
        splash(330, 350, 1.4), splash(470, 345, 1.3), splash(610, 352, 1.2),
        G(swan(), x=120, y=430, s=1.0), G(swan(), x=700, y=420, s=0.9),
        lotus(80, 480, 0.9), lotus(400, 485, 0.8), lotus(760, 480, 0.9),
        fish("#f08a3a", 1.0) and G(fish("#f08a3a"), x=250, y=480), G(fish("#f2c14e", flip=True), x=580, y=470),
        defs=sky_defs("day"),
        title="தாமரைப் பொய்கையில் மகளிர் நீர் விளையாட்டு")


# ======================= 18 உண்டாட்டுப் படலம் =======================
def leaf_meal(x, y, s=1.0):
    return G(P("M-40,0 C-36,-14 30,-16 44,-4 C30,8 -30,10 -40,0 Z", "#5aa060", sw=2) + P("M-36,-2 L40,-4", stroke="#3f8049", sw=1.4) +
             C(-16, -4, 7, "#ffffff", sw=1.2) + C(0, -6, 5, "#f2c14e", sw=1.2) + C(12, -3, 5, "#e07a3a", sw=1.2) +
             C(26, -5, 4, "#f28aa6", sw=1.2), x=x, y=y, s=s)


def p18_chapter():
    return svg(
        sky(), moon(640, 90, 34, crescent=False), stars([(100, 60, 0.8), (260, 110, 0.6), (420, 50, 0.7), (520, 140, 0.5), (760, 180, 0.6)]),
        hills(300, "#4f6f78", "#3f5f68"), R(0, 330, 800, 170, "#6f8a7a"),
        palace(130, 330, 0.6, MARBLE, GOLD, 200), tent(720, 340, 0.8),
        R(160, 400, 480, 70, "#c9a46a", stroke=OUT, sw=2.2, rx=10),
        leaf_meal(230, 430, 1.0), leaf_meal(340, 436, 1.0), leaf_meal(460, 430, 1.0), leaf_meal(570, 436, 1.0),
        G(lamp(0.9), x=120, y=480), G(lamp(0.9), x=690, y=480),
        G(man(cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, hair="turban", sitting=True, pose="lap", eye="happy"), x=300, y=400, s=0.75),
        G(woman(cloth=PINK_CLOTH, cloth_d=PINK_CLOTH_D, sitting=True, pose="offer", eye="happy"), x=400, y=400, s=0.75),
        G(man(cloth=PURPLE_CLOTH, cloth_d=PURPLE_CLOTH_D, hair="bun", sitting=True, pose="raise", eye="happy"), x=500, y=400, s=0.75),
        G(woman(cloth=BLUE_CLOTH, cloth_d=BLUE_CLOTH_D, pose="raise", eye="happy"), x=620, y=400, s=0.8),
        G(drum(0, 0, 0.9), x=190, y=398),
        note(250, 300, 1.0, "#f2c14e"), note(560, 290, 0.9, "#f28aa6"),
        defs=night_defs(),
        title="நிலவொளியில் விருந்தும் இசையும் களியாட்டமும்")


# ======================= 19 எதிர்கொள் படலம் =======================
def p19_chapter():
    return svg(
        sky(), cloud(140, 60, 0.9), cloud(640, 70, 0.8),
        hills(290, "#b7d9b0", "#9cc99a"), R(0, 330, 800, 170, "#e8d7a8"),
        G(elephant(deco=True, umbrella=True), x=40, y=420, s=0.5, flip=False),
        G(elephant(deco=True, umbrella=True), x=770, y=420, s=0.5, flip=True),
        flag(250, 400, ROYAL_RED, 1.1, 100, 4), flag(560, 400, "#f2a33a", 1.1, 100, -4),
        G(dasaratha("hug", eye="happy"), x=360, y=470, s=1.1),
        G(janaka("hug", eye="happy"), x=450, y=470, s=1.1, flip=True),
        G(rama("namaste", hold="bow"), x=240, y=482, s=0.95),
        G(lakshmana("namaste", hold="bow"), x=150, y=486, s=0.85),
        G(man(cloth=ROYAL_RED, cloth_d=ROYAL_RED_D, hair="turban", top=GOLD, pose="raise"), x=600, y=486, s=0.85),
        petals([(320, 160, 10), (380, 120, 70), (440, 180, 30), (500, 130, 90), (400, 220, 50), (300, 230, 120)]),
        defs=sky_defs("day"),
        title="சனகன் எதிர்கொண்டு வந்து தயரதனைத் தழுவுதல்; தந்தையை வணங்கும் இராமன்")


# ======================= 20 உலாவியற் படலம் =======================
def window_lady(x, y, cloth, cloth_d, pose="namaste", eye="wonder"):
    return (balcony(x, y, 110, 80) + G(woman(cloth=cloth, cloth_d=cloth_d, pose=pose, eye=eye), x=x, y=y, s=0.6))


def p20_chapter():
    return svg(
        sky(), cloud(400, 50, 0.8),
        R(0, 40, 220, 300, MARBLE, stroke=OUT, sw=2.4), R(580, 40, 220, 300, MARBLE, stroke=OUT, sw=2.4),
        window_lady(110, 150, PINK_CLOTH, PINK_CLOTH_D), window_lady(690, 150, TEAL_CLOTH, TEAL_CLOTH_D, "raise"),
        window_lady(110, 290, PURPLE_CLOTH, PURPLE_CLOTH_D, "raise", "happy"), window_lady(690, 290, BLUE_CLOTH, BLUE_CLOTH_D),
        R(0, 340, 800, 160, "#e6d6b6"), P("M0,340 L800,340", stroke="#c9a46a", sw=2.2),
        G(chariot(rider=rama("bless", hold=None, eye="happy")), x=360, y=470, s=1.0),
        petals([(260, 120, 10), (330, 80, 60), (420, 150, 20), (480, 90, 80), (540, 170, 40), (300, 200, 100), (450, 230, 130)]),
        G(woman(cloth="#f2a33a", cloth_d=SAFFRON_D, pose="offer", eye="happy"), x=620, y=490, s=0.85),
        G(woman(cloth=GREEN_CLOTH, cloth_d=GREEN_CLOTH_D, pose="namaste", eye="wonder"), x=120, y=490, s=0.85),
        defs=sky_defs("day"),
        title="மிதிலை வீதிகளில் இராமன் உலா; அவன் அழகைக் கண்டு மயங்கும் மகளிர்")


# ======================= 21 கோலம் காண் படலம் =======================
def mirror(x, y, s=1.0):
    return G(E(0, -40, 22, 28, "#e8f4f8", stroke=GOLD_D, sw=4) + P("M-8,-56 l10,-8 M-4,-44 l16,-14", stroke="#ffffff", sw=2.4) +
             P("M0,-12 L0,10", stroke=GOLD_D, sw=5), x=x, y=y, s=s)


def p21_chapter():
    return svg(
        hall(380, "#f7e6c6", curtain="#8a3a6a"),
        R(300, 360, 200, 30, "#d8b77a", stroke=OUT, sw=2.2),
        G(seat(180, "#b5452f"), x=400, y=362),
        G(sita("lap", sitting=True, bride=True, eye="happy"), x=400, y=360, s=1.25),
        G(woman(cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, pose="garland", eye="happy"), x=250, y=480, s=1.0),
        G(woman(cloth=PURPLE_CLOTH, cloth_d=PURPLE_CLOTH_D, pose="chest", eye="happy"), x=560, y=480, s=1.0),
        G(mirror(0, 0, 1.0), x=620, y=400),
        G(lamp(1.0), x=120, y=480), G(lamp(1.0), x=690, y=480),
        R(140, 440, 40, 26, "#b5452f", stroke=OUT, sw=2, rx=4), C(152, 438, 4, GOLD, sw=1), C(166, 437, 4, JEWEL_RED, sw=1),
        stars([(300, 150, 0.9), (500, 140, 0.8), (400, 110, 1.0)], GOLD),
        defs=indoor_defs(),
        title="மணக்கோலம் பூணும் சீதை: அணிகலன் அணிவிக்கும் தோழியர்")


# ======================= 22 கடிமணப் படலம் =======================
def p22_chapter():
    return svg(
        R(0, 0, 800, 500, "#f6e3c0"), R(0, 400, 800, 100, "#e8cf9f"),
        banana(60, 400, 1.2), banana(740, 400, 1.2),
        mandapam(400, 400, 1.0, 420, 260),
        fire_altar(400, 440, 0.8),
        G(rama("garland", hold=None, groom=True, eye="happy"), x=290, y=470, s=1.05),
        G(sita("garland", bride=True, eye="happy"), x=500, y=470, s=1.05),
        G(janaka("pour", eye="happy"), x=630, y=480, s=0.95),
        G(vasishtha("bless", hold=None), x=160, y=482, s=0.95),
        petals([(260, 90, 10), (330, 60, 60), (420, 100, 20), (480, 70, 80), (540, 110, 40), (300, 140, 100), (380, 40, 130), (600, 60, 30)]),
        defs=indoor_defs(),
        title="திருமணம்: மணமேடையில் இராமனும் சீதையும்; சனகன் தாரை வார்த்துக் கொடுத்தல்")


# ======================= 23 பரசுராமப் படலம் =======================
def p23_chapter():
    bolt = P("M520,60 L500,110 L520,110 L496,160", stroke="#ffe27a", sw=5)
    return svg(
        sky(), dark_cloud(560, 70, 1.6, "#4f5470"), dark_cloud(380, 60, 1.2, "#5a5f7a"), dark_cloud(720, 100, 1.1, "#4f5470"), bolt,
        hills(320, "#8fa89a", "#7f988a"), R(0, 350, 800, 150, "#d9c69a"),
        G(chariot(rider=dasaratha("chest", eye="sad", mouth_kind="sad"), horses=False), x=110, y=440, s=0.75),
        G(parasurama("raise", hold=None, eye="stern", mouth_kind="open"), x=620, y=470, s=1.25),
        G(P("M0,50 L0,-90", stroke="#8a5a2b", sw=5) + P("M0,-88 C26,-98 34,-70 30,-56 C20,-64 8,-66 0,-68 Z", "#cfd6dc", sw=2.2),
          x=690, y=290, rot=20),
        G(rama("draw", hold=None, eye="stern", mouth_kind="flat"), x=330, y=476, s=1.15, rot=-8),
        G(lakshmana("down", hold="bow", eye="stern", mouth_kind="flat"), x=220, y=480, s=0.9),
        defs=sky_defs("evening"),
        title="திருமால் வில்லை வளைத்து நாணேற்றி, பரசுராமனின் செருக்கை அடக்கும் இராமன்")


PICS = {
    0: {"chapter": p00_chapter, "scene-1": p00_scene1, "scene-2": p00_scene2, "scene-3": p00_scene3},
    1: {"chapter": p01_chapter, "scene-1": p01_scene1, "scene-2": p01_scene2, "scene-3": p01_scene3},
    2: {"chapter": p02_chapter}, 3: {"chapter": p03_chapter}, 4: {"chapter": p04_chapter},
    5: {"chapter": p05_chapter}, 6: {"chapter": p06_chapter}, 7: {"chapter": p07_chapter},
    8: {"chapter": p08_chapter}, 9: {"chapter": p09_chapter}, 10: {"chapter": p10_chapter},
    11: {"chapter": p11_chapter}, 12: {"chapter": p12_chapter}, 13: {"chapter": p13_chapter},
    14: {"chapter": p14_chapter}, 15: {"chapter": p15_chapter}, 16: {"chapter": p16_chapter},
    17: {"chapter": p17_chapter}, 18: {"chapter": p18_chapter}, 19: {"chapter": p19_chapter},
    20: {"chapter": p20_chapter}, 21: {"chapter": p21_chapter}, 22: {"chapter": p22_chapter},
    23: {"chapter": p23_chapter},
}


def main():
    want = [int(a) for a in sys.argv[1:]] or sorted(PICS)
    n = 0
    for p in want:
        d = OUT / f"{p:02d}"
        d.mkdir(parents=True, exist_ok=True)
        for name, fn in PICS[p].items():
            (d / f"{name}.svg").write_text(fn(), encoding="utf-8")
            n += 1
    print("wrote", n, "pictures")


if __name__ == "__main__":
    main()
