"""Characters, animals and scenery for the Kamba Ramayanam pictures.

Builds on art.py (the drawing kit of the Valmiki Ramayanam site) so both sites share one
flat, friendly cartoon style. Every character is drawn with the feet at (0, 0) and "up" being
negative y; place it with G(rama(...), x=..., y=..., s=...).
"""
import math
from art import *  # noqa: F401,F403
from art import _arms, _a  # noqa: F401

# ---- palette for the Kamba pictures ------------------------------------------
RAMA_BLUE, RAMA_BLUE_D = "#6f93cf", "#557bb8"
SKIN_GOLD = "#e8b07c"
SKIN_KING = "#e0a878"
SKIN_WOMAN = "#efbd8c"
SKIN_DEMON, SKIN_DEMON_D = "#6d5a8f", "#57477a"
SAFFRON, SAFFRON_D = "#ef9a3a", "#cf7a22"
RUST, RUST_D = "#b9583a", "#97452c"
ROYAL_RED, ROYAL_RED_D = "#b83a3a", "#962c2c"
GREEN_CLOTH, GREEN_CLOTH_D = "#3f9a6b", "#2f7a53"
TEAL_CLOTH, TEAL_CLOTH_D = "#2f8a92", "#22707a"
PURPLE_CLOTH, PURPLE_CLOTH_D = "#8a5aa8", "#704489"
PINK_CLOTH, PINK_CLOTH_D = "#d2475e", "#b0364b"
BLUE_CLOTH, BLUE_CLOTH_D = "#4a78c0", "#3a62a3"
MILK = "#fbfaf4"
STONE, STONE_D = "#a9a39a", "#8a847b"
MARBLE, MARBLE_D = "#f4ecdc", "#e2d4b8"
JEWEL_RED = "#d23b3b"
JASMINE = "#ffffff"
GREY_HAIR = "#9a9a9a"


# ---- small parts ----------------------------------------------------------------
def gold_dot(x, y, r=2.2):
    return C(x, y, r, JEWEL_RED, stroke=GOLD_D, sw=1)


def necklace(y=-108, w=15, drop=12, color=GOLD):
    return (P(f"M{-w},{y} Q0,{y+drop*2} {w},{y}", stroke=GOLD_D, sw=4.6) +
            P(f"M{-w},{y} Q0,{y+drop*2} {w},{y}", stroke=color, sw=3) +
            C(0, y + drop + 1, 3.2, JEWEL_RED, stroke=GOLD_D, sw=1.2))


def namam(cx, cy, s=1.0):
    """Vaishnava tilak on the forehead."""
    return G(P("M-3.4,-1 L-2.4,-9 M3.4,-1 L2.4,-9 M-3.4,-1 Q0,2.4 3.4,-1", stroke="#ffffff", sw=1.9) +
             P("M0,0 L0,-9", stroke=JEWEL_RED, sw=1.7), x=cx, y=cy, s=s)


def bindi(cx, cy):
    return C(cx, cy, 1.9, JEWEL_RED, stroke="none")


def earrings(cx, cy, r, color=GOLD):
    return C(cx - r - 1, cy + 8, 2.8, color, stroke=GOLD_D, sw=1) + C(cx + r + 1, cy + 8, 2.8, color, stroke=GOLD_D, sw=1)


def crown(kind="tall", y=-141):
    """Gold crown sitting on a head whose top is near y-6."""
    if kind == "tall":       # kireedam
        return (P(f"M-16,{y} L-14,{y-26} Q0,{y-40} 14,{y-26} L16,{y} Z", GOLD, sw=2.2) +
                P(f"M-15,{y-9} L15,{y-9} M-14,{y-19} L14,{y-19}", stroke=GOLD_D, sw=2) +
                C(0, y - 38, 3.6, GOLD, sw=2) + gold_dot(0, y - 14, 3) + gold_dot(-8, y - 4, 1.9) + gold_dot(8, y - 4, 1.9) +
                R(-18, y - 2, 36, 6, GOLD, stroke=OUT, sw=2, rx=2))
    if kind == "small":      # prince / small crown
        return (P(f"M-15,{y} L-12,{y-18} L-6,{y-10} L0,{y-24} L6,{y-10} L12,{y-18} L15,{y} Z", GOLD, sw=2.2) +
                gold_dot(0, y - 13, 2.4) + R(-17, y - 2, 34, 6, GOLD, stroke=OUT, sw=2, rx=2))
    if kind == "tiara":      # queen / princess
        return (P(f"M-13,{y+1} Q0,{y-16} 13,{y+1}", GOLD, sw=2) + gold_dot(0, y - 6, 2.6) +
                gold_dot(-7, y - 3, 1.6) + gold_dot(7, y - 3, 1.6))
    return ""


# ---- the person ------------------------------------------------------------------
def person(skin=SKIN_YOUNG, hair="bun", hair_color=BLACK_HAIR, beard=None, moustache=None,
           outfit="dhoti", cloth=OCHRE, cloth_d=OCHRE_D, sash=None, top=None,
           pose="down", sitting=False, eye="open", mouth_kind="smile", tilak=None,
           jewels=False, crown_kind=None, female=False, quiver=False, thread=False,
           hold=None, flowers=False, old=False, big_head=1.0):
    """A standing or seated person.

    hair: bun | jata | long | braid | turban | wild | none     beard: None | colour (long beard)
    outfit: dhoti | robe | saree | bark       hold: None | bow | axe | trident | staff | pot | leaf |
                                               garland | lamp | kamandalu | mace | sword | baby | basket
    """
    parts = []
    w = 21 if not female else 18          # half-width of the torso
    sx, sy = (19, -108) if not female else (16, -101)
    head_y = -128 if not female else -121
    hr = (19 if not female else 17) * big_head
    if old:
        sx -= 1
    # --- things behind the body
    if quiver:
        parts.append(G(R(-6, -34, 12, 40, "#8a5a2b", stroke=OUT, sw=2, rx=4) +
                       P("M-3,-34 L-6,-46 M0,-34 L0,-48 M3,-34 L6,-46", stroke="#8a5a2b", sw=2) +
                       P("M-6,-46 l-4,-7 l6,1 Z M0,-48 l-3,-8 l6,0 Z M6,-46 l-2,-8 l6,2 Z", "#f6f0e0", sw=1.4),
                       x=-22, y=-80, rot=-22))
    if (hair == "braid" or hair == "long") and not sitting:
        hc = hair_color
        parts.append(P(f"M{-hr+2},{head_y} C{-hr-6},{head_y+40} {-hr},{head_y+70} {-hr+6},{head_y+90} "
                       f"L{-hr+14},{head_y+88} C{-hr+10},{head_y+60} {-hr+8},{head_y+30} {-hr+10},{head_y} Z", hc, sw=2.2))
        if flowers or hair == "braid":
            for k in range(4):
                parts.append(C(-hr - 1 + k * 1.6, head_y + 20 + k * 17, 3.4, JASMINE, sw=1.2))
    # --- legs / lower garment
    if sitting:
        parts += [P("M-42,-3 C-45,-24 -26,-36 0,-36 C26,-36 45,-24 42,-3 Z", cloth),
                  P("M-34,-12 Q-17,-19 0,-13 Q17,-19 34,-12", stroke=cloth_d, sw=1.8),
                  E(-21, -6, 9, 4.5, skin, sw=2), E(21, -6, 9, 4.5, skin, sw=2)]
        if outfit == "saree":
            parts.append(P("M-42,-4 L42,-4", stroke=GOLD, sw=3))
        dy = 34
    else:
        if outfit in ("robe", "bark"):
            parts += [E(-10, -3, 9, 4, skin, sw=2), E(10, -3, 9, 4, skin, sw=2),
                      P(f"M{-w-2},-72 C{-w-6},-50 {-w-10},-26 {-w-8},-7 L{w+8},-7 C{w+10},-26 {w+6},-50 {w+2},-72 Z", cloth)]
            if outfit == "bark":
                parts += [P("M-26,-52 Q-19,-55 -13,-52 T0,-52 T13,-52 T26,-52", stroke=cloth_d, sw=1.6),
                          P("M-28,-32 Q-21,-35 -14,-32 T0,-32 T14,-32 T28,-32", stroke=cloth_d, sw=1.6)]
            else:
                parts += [P(f"M{-w-8},-12 L{w+8},-12", stroke=GOLD, sw=3.4), P("M0,-70 L0,-14", stroke=cloth_d, sw=1.6)]
        elif outfit == "saree":
            parts += [E(-8, -3, 8, 3.6, skin, sw=2), E(8, -3, 8, 3.6, skin, sw=2),
                      P(f"M{-w},-66 C{-w-6},-44 {-w-10},-24 {-w-8},-7 L{w+8},-7 C{w+10},-24 {w+6},-44 {w},-66 Z", cloth),
                      P(f"M{-w-8},-11 L{w+8},-11", stroke=GOLD, sw=3.4),
                      P("M2,-62 L4,-12 M9,-60 L12,-12 M16,-56 L19,-12", stroke=cloth_d, sw=1.5)]
        else:  # dhoti: wrapped to the ankles, feet showing
            parts += [E(-10, -3, 9, 4, skin, sw=2), E(10, -3, 9, 4, skin, sw=2),
                      limb("M-9,-20 L-10,-6", skin, 8), limb("M9,-20 L10,-6", skin, 8),
                      P(f"M{-w},-72 C{-w-4},-50 {-w-6},-34 {-w-3},-18 L{w+3},-18 C{w+6},-34 {w+4},-50 {w},-72 Z", cloth),
                      P("M-2,-70 L-4,-20 M6,-68 L8,-20", stroke=cloth_d, sw=1.6),
                      P(f"M{-w-3},-19 L{w+3},-19", stroke=GOLD if jewels else cloth_d, sw=3)]
        dy = 0
    # --- upper body
    up = []
    if female:
        tw = 17
        up.append(P(f"M{-tw+1},{sy+4} C{-tw-3},{sy+18} {-tw-3},{sy+32} {-tw},-66 L{tw},-66 C{tw+3},{sy+32} {tw+3},{sy+18} {tw-1},{sy+4} Z", skin))
        bl = top or cloth_d
        up.append(P(f"M{-tw-1},{sy+8} C{-tw-2},{sy+16} {-tw-1},{sy+22} {-tw+1},{sy+25} L{tw-1},{sy+25} "
                    f"C{tw+1},{sy+22} {tw+2},{sy+16} {tw+1},{sy+8} Q0,{sy+14} {-tw-1},{sy+8} Z", bl, sw=2))
        # pallu across the chest from the left shoulder
        up.append(P(f"M{-tw+2},{sy+2} L{-tw+10},{sy+1} L{tw+2},-64 L{tw-6},-60 Z", cloth, sw=2.2))
        up.append(P(f"M{-tw+10},{sy+1} L{tw+2},-64", stroke=GOLD, sw=2.6))
        up.append(P(f"M{-tw-2},-67 L{tw+2},-67", stroke=GOLD, sw=2.4))
    else:
        top_y = sy - 5
        up.append(P(f"M{-w+1},{top_y} C{-w-4},{top_y+13} {-w-4},{top_y+29} {-w-2},-72 L{w+2},-72 C{w+4},{top_y+29} {w+4},{top_y+13} {w-1},{top_y} Z", skin))
        if outfit == "bark":
            up.append(P(f"M{-w+1},{top_y} L{-w+13},{top_y} L{w+2},-81 L{w+2},-72 L{w-9},-72 Z", BARK_L, sw=2.2))
        elif top:          # a shawl / upper cloth
            up.append(P(f"M{-w+1},{top_y} L{-w+13},{top_y} L{w+2},-84 L{w+2},-72 L{w-9},-72 Z", top, sw=2.2))
        if outfit == "robe" and not top:
            up.append(P(f"M{-w-2},{top_y+38} L{w+2},{top_y+38}", stroke=cloth_d, sw=2))
        if sash:
            up.append(P(f"M{-w},-80 Q0,-70 {w},-80", stroke=sash, sw=5))
        if thread:
            up.append(P(f"M{-w+6},{top_y+1} L{w-1},-74", stroke="#fff7e2", sw=2))
        up.append(P(f"M{-w-2},-74 L{w+2},-74", stroke=cloth_d, sw=3.4))
        if jewels:
            up.append(necklace(sy + 1, 14, 10))
            up.append(C(-w - 1, sy + 14, 3.6, GOLD, stroke=GOLD_D, sw=1.4) + C(w + 1, sy + 14, 3.6, GOLD, stroke=GOLD_D, sw=1.4))
    if female and jewels:
        up.append(necklace(sy + 2, 11, 7))
    # arms (behind-body arm first)
    if pose in EXTRA_POSES:
        la, ra = _arms_extra(pose, skin, sx, sy, 7.5 if not female else 6.6)
    else:
        la, ra = _arms(pose if pose in ("namaste", "lap", "down", "walk", "speak", "bless", "abhaya", "give", "point", "think", "pot")
                       else "down", skin, sx=sx, sy=sy, w=7.5 if not female else 6.6)
    up.append(la)
    # head
    up += [E(-hr, head_y, 3.6 * big_head, 5.4 * big_head, skin, sw=2), E(hr, head_y, 3.6 * big_head, 5.4 * big_head, skin, sw=2)]
    if hair == "long" and not female:   # locks falling behind the ears to the shoulders
        up.append(P(f"M{-hr+2},{head_y-6} C{-hr-7},{head_y+6} {-hr-8},{head_y+18} {-hr-3},{head_y+24} "
                    f"L{-hr+5},{head_y+16} Z", hair_color, sw=2))
        up.append(P(f"M{hr-2},{head_y-6} C{hr+7},{head_y+6} {hr+8},{head_y+18} {hr+3},{head_y+24} "
                    f"L{hr-5},{head_y+16} Z", hair_color, sw=2))
    up.append(C(0, head_y, hr, skin))
    # hair
    top_head = head_y - hr
    if hair in ("bun", "braid", "long", "jata"):
        hc = hair_color
        up.append(P(f"M{-hr},{head_y-2} C{-hr-1},{top_head-4} {hr+1},{top_head-4} {hr},{head_y-2} "
                    f"C{hr*0.6},{head_y-11} {-hr*0.6},{head_y-11} {-hr},{head_y-2} Z", hc, sw=2.1))
        if hair == "bun":
            up.append(C(0, top_head - 2, hr * 0.38, hc, sw=2))
        if hair == "jata":
            up.append(E(0, top_head - 6, hr * 0.55, hr * 0.62, hc, sw=2.1))
            up.append(P(f"M{-hr*0.45},{top_head-2} Q0,{top_head+1} {hr*0.45},{top_head-2}", stroke=BARK_D, sw=2.6))
        if female and hair in ("bun", "braid"):
            up.append(C(hr * 0.7, head_y - hr * 0.55, 2.6, JASMINE, sw=1) + C(hr * 0.85, head_y - hr * 0.3, 2.4, JASMINE, sw=1))
            if hair == "bun":
                up.append(C(0, top_head - 2, hr * 0.42, hc, sw=2))
                up.append(P(f"M{-hr*0.45},{top_head-4} Q0,{top_head-12} {hr*0.45},{top_head-4}", stroke=JASMINE, sw=3.2))
    elif hair == "turban":
        tc = hair_color
        up.append(P(f"M{-hr-2},{head_y-3} C{-hr-4},{top_head-10} {hr+4},{top_head-10} {hr+2},{head_y-3} "
                    f"C{hr*0.6},{head_y-9} {-hr*0.6},{head_y-9} {-hr-2},{head_y-3} Z", tc, sw=2.2))
        up.append(P(f"M{-hr},{head_y-8} Q0,{top_head-2} {hr},{head_y-12}", stroke="#00000022", sw=3))
        up.append(P(f"M{-hr+2},{head_y-5} Q0,{head_y-16} {hr-2},{head_y-9}", stroke="#ffffff66", sw=2))
    elif hair == "wild":
        hc = hair_color
        spikes = " ".join(f"L{(hr+8)*math.cos(a):.1f},{head_y+(hr+10)*math.sin(a):.1f} L{(hr+1)*math.cos(a+0.2):.1f},{head_y+(hr+1)*math.sin(a+0.2):.1f}"
                          for a in [math.pi + 0.15 + i * 0.36 for i in range(9)])
        up.append(P(f"M{-hr},{head_y} {spikes} L{hr},{head_y-2} C{hr*0.6},{head_y-10} {-hr*0.6},{head_y-10} {-hr},{head_y} Z", hc, sw=2))
    # face
    up.append(eyes(0, head_y, hr, eye))
    up.append(P(f"M0,{head_y+2} Q2.4,{head_y+6.5} -1,{head_y+8}", sw=1.5))
    if beard:
        up.append(P(f"M{-hr+1},{head_y+3} C{-hr},{head_y+22} {-hr*0.55},{head_y+36} 0,{head_y+40} "
                    f"C{hr*0.55},{head_y+36} {hr},{head_y+22} {hr-1},{head_y+3} C{hr*0.6},{head_y+11} {-hr*0.6},{head_y+11} {-hr+1},{head_y+3} Z",
                    beard, sw=2.1))
    else:
        up.append(blush(0, head_y, hr))
    if moustache or beard:
        mc = moustache or beard
        up.append(P(f"M-8,{head_y+12} Q-4,{head_y+8} 0,{head_y+11} Q4,{head_y+8} 8,{head_y+12} Q4,{head_y+15} 0,{head_y+13} Q-4,{head_y+15} -8,{head_y+12} Z",
                    mc, sw=1.5))
    if not beard:
        up.append(mouth(0, head_y + 15 if not female else head_y + 13, mouth_kind if mouth_kind != "calm" else "smile"))
    elif mouth_kind == "open":
        up.append(E(0, head_y + 18, 3.2, 2.8, "#7a2e2a", sw=1.3))
    if tilak == "namam":
        up.append(namam(0, head_y - hr * 0.45, 0.95))
    elif tilak == "bindi":
        up.append(bindi(0, head_y - hr * 0.42))
    elif tilak == "ash":
        up.append(P(f"M-8,{head_y-hr*0.5} L8,{head_y-hr*0.5} M-8,{head_y-hr*0.5+3.5} L8,{head_y-hr*0.5+3.5}", stroke="#ffffff", sw=1.6))
    if jewels:
        up.append(earrings(0, head_y, hr))
    if crown_kind:
        up.append(crown(crown_kind, y=int(top_head + 6)))
    # front arm and held things
    up.append(ra)
    if pose == "pot" and hold is None:
        hold = "pot"
    up.append(_held(hold, sx, sy, skin))
    parts.append(G(*up, y=dy))
    return "".join(parts)


EXTRA_POSES = ("draw", "raise", "pour", "garland", "chest", "offer", "hug", "wave")


def _arms_extra(pose, skin, sx, sy, w):
    hand = lambda x, y, r=4.8: C(x, y, r, skin, sw=2.2)
    L, Rt = "", ""
    if pose == "draw":           # archer: bow held out to the figure's left (viewer's right), string pulled to the chest
        L = limb(f"M{-sx},{sy} C{-sx+4},{sy+18} {-4},{sy+16} {6},{sy+8}", skin, w) + hand(7, sy + 8)
        bx, by = sx + 56, sy + 4
        Rt = (limb(f"M{sx},{sy} L{bx-4},{by}", skin, w) +
              P(f"M{bx},{by-66} Q{bx+30},{by} {bx},{by+66}", stroke="#6b4421", sw=5) +
              P(f"M{bx},{by-66} L{8},{sy+8} L{bx},{by+66}", stroke="#efe6cc", sw=1.4) +
              P(f"M{-4},{sy+8} L{bx+40},{sy+6}", stroke="#8a5a2b", sw=3) +
              P(f"M{bx+40},{sy+1} L{bx+54},{sy+6} L{bx+40},{sy+11} Z", "#cfd6dc", sw=1.6) +
              P(f"M{-4},{sy+8} l-8,-6 M{-4},{sy+8} l-8,6", stroke="#f6f0e0", sw=2.6) +
              hand(bx - 2, by))
    elif pose == "raise":        # both hands up in joy
        L = limb(f"M{-sx},{sy} C{-sx-12},{sy-8} {-sx-16},{sy-24} {-sx-14},{sy-40}", skin, w) + hand(-sx - 14, sy - 44)
        Rt = limb(f"M{sx},{sy} C{sx+12},{sy-8} {sx+16},{sy-24} {sx+14},{sy-40}", skin, w) + hand(sx + 14, sy - 44)
    elif pose == "wave":         # one hand up
        L = limb(f"M{-sx},{sy} C{-sx-8},{sy+12} {-sx-10},{sy+26} {-sx-8},{sy+36}", skin, w) + hand(-sx - 8, sy + 37)
        Rt = limb(f"M{sx},{sy} C{sx+12},{sy-8} {sx+16},{sy-24} {sx+14},{sy-40}", skin, w) + hand(sx + 14, sy - 44)
    elif pose == "pour":         # pouring water from a pot held forward
        L = limb(f"M{-sx},{sy} C{-sx+2},{sy+20} {6},{sy+26} {22},{sy+20}", skin, w) + hand(22, sy + 20)
        Rt = (limb(f"M{sx},{sy} C{sx+10},{sy+6} {sx+18},{sy+4} {sx+24},{sy}", skin, w) +
              G(kalasha(full=True), x=sx + 34, y=sy + 16, rot=-50, s=0.85) + hand(sx + 24, sy) +
              P(f"M{sx+52},{sy+2} C{sx+60},{sy+20} {sx+56},{sy+40} {sx+58},{sy+60}", stroke=WATER, sw=3.5))
    elif pose in ("garland", "offer"):   # holding a garland / a plate forward with both hands
        L = limb(f"M{-sx},{sy} C{-sx-4},{sy+18} {-10},{sy+30} {-8},{sy+30}", skin, w) + hand(-8, sy + 30)
        Rt = limb(f"M{sx},{sy} C{sx+4},{sy+18} {10},{sy+30} {8},{sy+30}", skin, w) + hand(8, sy + 30)
        if pose == "garland":
            Rt += garland(0, sy + 30, 0.9)
        else:
            Rt += G(E(0, 0, 22, 6, GOLD, sw=2) + C(-8, -6, 5, "#f28aa6", sw=1.2) + C(4, -7, 5, "#ffd34e", sw=1.2) +
                    C(12, -4, 4, "#ffffff", sw=1.2), x=0, y=sy + 32)
    elif pose == "chest":        # humble: hand on the chest
        L = limb(f"M{-sx},{sy} C{-sx-8},{sy+12} {-sx-10},{sy+26} {-sx-8},{sy+36}", skin, w) + hand(-sx - 8, sy + 37)
        Rt = limb(f"M{sx},{sy} C{sx+8},{sy+18} {6},{sy+20} {-2},{sy+14}", skin, w) + hand(-3, sy + 13)
    elif pose == "hug":          # arms reaching forward (to the viewer's right) to embrace
        L = limb(f"M{-sx},{sy} C{-sx+6},{sy+22} {10},{sy+22} {30},{sy+14}", skin, w) + hand(31, sy + 14)
        Rt = limb(f"M{sx},{sy} C{sx+10},{sy-2} {sx+22},{sy-4} {sx+30},{sy+2}", skin, w) + hand(sx + 31, sy + 2)
    return L, Rt


def garland(x, y, s=1.0, a="#f28aa6", b="#ffffff"):
    out = []
    for k in range(13):
        t = k / 12
        xx = -26 + 52 * t
        yy = 30 * math.sin(math.pi * t)
        out.append(C(xx, yy, 4.2, a if k % 2 else b, sw=1.1))
    return G(*out, x=x, y=y, s=s)


def _held(hold, sx, sy, skin):
    hx, hy = sx + 8, sy + 37        # right hand when the arm hangs down
    if hold == "bow":
        return G(bow(124), x=hx + 4, y=hy - 26)
    if hold == "staff":
        return P(f"M{hx},{hy-70} L{hx},{hy+66}", stroke="#8a5a2b", sw=4.5) + C(hx, hy, 5, skin, sw=2.2)
    if hold == "axe":
        return (P(f"M{hx},{hy-74} L{hx},{hy+40}", stroke="#8a5a2b", sw=5) +
                P(f"M{hx},{hy-72} C{hx+26},{hy-82} {hx+34},{hy-54} {hx+30},{hy-40} C{hx+20},{hy-48} {hx+8},{hy-50} {hx},{hy-52} Z",
                  "#cfd6dc", sw=2.2) + C(hx, hy, 5, skin, sw=2.2))
    if hold == "trident":
        return (P(f"M{hx},{hy-96} L{hx},{hy+60}", stroke="#5d5d5d", sw=4.5) +
                P(f"M{hx-14},{hy-112} C{hx-14},{hy-92} {hx+14},{hy-92} {hx+14},{hy-112} M{hx},{hy-118} L{hx},{hy-94}",
                  stroke="#5d5d5d", sw=4) + C(hx, hy, 5, skin, sw=2.2))
    if hold == "mace":
        return (P(f"M{hx},{hy+4} L{hx+4},{hy-52}", stroke="#8a5a2b", sw=5) + C(hx + 5, hy - 60, 12, GOLD, sw=2.2) +
                C(hx, hy, 5, skin, sw=2.2))
    if hold == "sword":
        return (P(f"M{hx},{hy} L{hx+6},{hy-66}", stroke="#cfd6dc", sw=6) + P(f"M{hx-8},{hy-4} L{hx+8},{hy+2}", stroke=GOLD_D, sw=4) +
                C(hx, hy, 5, skin, sw=2.2))
    if hold == "pot":
        return G(kalasha(full=True), x=hx + 8, y=hy + 14, s=0.82)
    if hold == "kamandalu":
        return G(E(0, 0, 9, 8, "#7a5230") + P("M-6,-6 Q0,-20 6,-6", stroke="#7a5230", sw=2.6) + P("M8,-2 L16,-8", stroke="#7a5230", sw=3),
                 x=hx, y=hy + 10)
    if hold == "leaf":
        return G(palm_leaf(), x=hx + 4, y=hy - 2, rot=-12, s=0.8)
    if hold == "lamp":
        return G(lamp(0.55), x=hx, y=hy + 4)
    if hold == "basket":
        return G(P("M-14,-6 L14,-6 L10,8 L-10,8 Z", "#c99a55", sw=2) + P("M-12,-6 Q0,-22 12,-6", stroke="#9b7032", sw=2.4) +
                 C(-6, -9, 3.4, "#ff7aa8", sw=1) + C(2, -10, 3.4, "#ffd34e", sw=1) + C(8, -8, 3, "#ffffff", sw=1), x=hx + 2, y=hy + 6)
    return ""


def palm_leaf():
    """An ola (palm-leaf manuscript) bundle."""
    return (R(-26, -6, 52, 12, "#e9cf8f", stroke=OUT, sw=2, rx=5) +
            P("M-20,-2 L20,-2 M-20,2 L14,2", stroke="#a88b4c", sw=1.2) + C(-14, 0, 1.6, OUT, stroke="none") +
            C(14, 0, 1.6, OUT, stroke="none"))


def lamp(s=1.0):
    """Brass oil lamp (kuthuvilakku) with flame; base at (0,0)."""
    l = (E(0, -3, 16, 4, "#d9a63a", sw=2) + P("M-3,-6 L-3,-48 L3,-48 L3,-6 Z", "#d9a63a", sw=2) +
         E(0, -50, 14, 4, "#d9a63a", sw=2) + P("M-10,-52 L0,-62 L10,-52", stroke="#b98622", sw=2) +
         E(-11, -57, 4.5, 6.5, "#ffcc4d", stroke="#f08a24", sw=1.6) + E(11, -57, 4.5, 6.5, "#ffcc4d", stroke="#f08a24", sw=1.6) +
         C(0, -70, 3, "#d9a63a", sw=1.6))
    return G(l, s=s)


# ---- named characters (keep these the same in every picture) ------------------------
def rama(pose="down", hold="bow", eye="open", mouth_kind="smile", sitting=False, crown_kind="tall", groom=False):
    return person(skin=RAMA_BLUE, hair="long", hair_color=BLACK_HAIR, outfit="dhoti", cloth=YELLOW_ROBE, cloth_d=OCHRE_D,
                  sash=JEWEL_RED, top=None, pose=pose, sitting=sitting, eye=eye, mouth_kind=mouth_kind, tilak="namam",
                  jewels=True, crown_kind=crown_kind, quiver=(hold == "bow"), hold=hold, thread=True)


def lakshmana(pose="down", hold="bow", eye="open", mouth_kind="smile", sitting=False, crown_kind="small"):
    return person(skin=SKIN_GOLD, hair="long", outfit="dhoti", cloth=SAFFRON, cloth_d=SAFFRON_D, sash=GREEN_CLOTH,
                  pose=pose, sitting=sitting, eye=eye, mouth_kind=mouth_kind, tilak="namam", jewels=True,
                  crown_kind=crown_kind, quiver=(hold == "bow"), hold=hold, thread=True)


def bharata(pose="down", hold=None, eye="happy", sitting=False):
    return person(skin=RAMA_BLUE_D, hair="long", outfit="dhoti", cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, sash=GOLD,
                  pose=pose, sitting=sitting, eye=eye, tilak="namam", jewels=True, crown_kind="small", hold=hold, thread=True)


def shatrughna(pose="down", hold=None, eye="happy", sitting=False):
    return person(skin="#eab98a", hair="long", outfit="dhoti", cloth=PURPLE_CLOTH, cloth_d=PURPLE_CLOTH_D, sash=GOLD,
                  pose=pose, sitting=sitting, eye=eye, tilak="namam", jewels=True, crown_kind="small", hold=hold, thread=True)


def dasaratha(pose="down", sitting=False, eye="happy", mouth_kind="smile", hold=None):
    return person(skin=SKIN_KING, hair="none", beard=None, moustache=WHITE_HAIR, outfit="robe", cloth=ROYAL_RED,
                  cloth_d=ROYAL_RED_D, top=GOLD, pose=pose, sitting=sitting, eye=eye, mouth_kind=mouth_kind,
                  tilak="namam", jewels=True, crown_kind="tall", hold=hold, old=True)


def janaka(pose="down", sitting=False, eye="happy", mouth_kind="smile", hold=None):
    return person(skin=SKIN_YOUNG, hair="none", beard=WHITE_HAIR, outfit="robe", cloth=SAFFRON, cloth_d=SAFFRON_D,
                  top=MILK, pose=pose, sitting=sitting, eye=eye, mouth_kind=mouth_kind, tilak="ash", jewels=True,
                  crown_kind="small", hold=hold, old=True)


def vasishtha(pose="down", sitting=False, eye="happy", mouth_kind="smile", hold="kamandalu"):
    return person(skin=SKIN_SAGE, hair="jata", hair_color=WHITE_HAIR, beard=WHITE_HAIR, outfit="robe", cloth=OCHRE,
                  cloth_d=OCHRE_D, top=MILK, pose=pose, sitting=sitting, eye=eye, mouth_kind=mouth_kind, tilak="ash",
                  hold=hold, old=True, thread=True)


def vishwamitra(pose="down", sitting=False, eye="open", mouth_kind="smile", hold="staff"):
    return person(skin="#c48450", hair="jata", hair_color=GREY_HAIR, beard=GREY_HAIR, outfit="robe", cloth=RUST,
                  cloth_d=RUST_D, top=BARK_L, pose=pose, sitting=sitting, eye=eye, mouth_kind=mouth_kind, tilak="ash",
                  hold=hold, old=True, thread=True)


def shatananda(pose="down", sitting=False, eye="happy", hold=None):
    return person(skin=SKIN_SAGE, hair="jata", hair_color=BLACK_HAIR, beard=BLACK_HAIR, outfit="robe", cloth=MILK,
                  cloth_d=WHITE_CLOTH_D, top=OCHRE, pose=pose, sitting=sitting, eye=eye, tilak="ash", hold=hold, thread=True)


def kamban(pose="down", sitting=False, eye="happy", mouth_kind="smile", hold="leaf"):
    return person(skin=SKIN_SAGE, hair="turban", hair_color=MILK, moustache=BLACK_HAIR, outfit="dhoti", cloth=MILK,
                  cloth_d=WHITE_CLOTH_D, top="#e9dfc8", pose=pose, sitting=sitting, eye=eye, mouth_kind=mouth_kind,
                  tilak="namam", hold=hold)


def patron(pose="down", sitting=False, eye="happy", hold="lamp"):
    """Sadaiyappa Vallal of Thiruvennainallur, Kamban's patron."""
    return person(skin="#c98b5a", hair="turban", hair_color=ROYAL_RED, moustache=BLACK_HAIR, outfit="dhoti", cloth=MILK,
                  cloth_d=WHITE_CLOTH_D, top=GOLD, pose=pose, sitting=sitting, eye=eye, tilak="ash", jewels=True, hold=hold)


def parasurama(pose="down", eye="stern", mouth_kind="open", hold="axe"):
    return person(skin="#c07a4a", hair="jata", hair_color=BLACK_HAIR, beard=BLACK_HAIR, outfit="dhoti", cloth=RUST,
                  cloth_d=RUST_D, pose=pose, eye=eye, mouth_kind=mouth_kind, tilak="ash", hold=hold, thread=True, quiver=True)


def sita(pose="down", eye="happy", mouth_kind="smile", sitting=False, bride=False, hold=None):
    return person(skin=SKIN_WOMAN, hair="braid", outfit="saree", cloth=PINK_CLOTH if bride else GREEN_CLOTH,
                  cloth_d=PINK_CLOTH_D if bride else GREEN_CLOTH_D, top=GOLD if bride else PINK_CLOTH,
                  pose=pose, sitting=sitting, eye=eye, mouth_kind=mouth_kind, tilak="bindi", jewels=True,
                  crown_kind="tiara", female=True, hold=hold, flowers=True)


def woman(cloth=TEAL_CLOTH, cloth_d=TEAL_CLOTH_D, top=None, skin=SKIN_WOMAN, pose="down", eye="happy", mouth_kind="smile",
          sitting=False, hold=None, hair="bun", queen=False):
    return person(skin=skin, hair=hair, outfit="saree", cloth=cloth, cloth_d=cloth_d, top=top or GOLD, pose=pose,
                  sitting=sitting, eye=eye, mouth_kind=mouth_kind, tilak="bindi", jewels=True, female=True, hold=hold,
                  crown_kind="tiara" if queen else None, flowers=True)


def man(cloth=MILK, cloth_d=WHITE_CLOTH_D, skin=SKIN_YOUNG, pose="down", eye="happy", mouth_kind="smile", hold=None,
        hair="bun", top=None, moustache=BLACK_HAIR, sitting=False):
    return person(skin=skin, hair=hair, hair_color=BLACK_HAIR, moustache=moustache, outfit="dhoti", cloth=cloth,
                  cloth_d=cloth_d, top=top, pose=pose, eye=eye, mouth_kind=mouth_kind, hold=hold, sitting=sitting)


def demon(pose="down", hold="mace", skin=SKIN_DEMON, eye="stern", mouth_kind="open", female=False, cloth="#3f3a52"):
    p = person(skin=skin, hair="wild", hair_color="#c2452d", outfit="dhoti" if not female else "saree", cloth=cloth,
               cloth_d="#2a2638", pose=pose, eye=eye, mouth_kind=mouth_kind, jewels=True, female=female, hold=hold)
    hy = -128 if not female else -121
    fangs = (P(f"M-6,{hy+12} L-4,{hy+20} L-2,{hy+12} Z", "#ffffff", sw=1.4) + P(f"M2,{hy+12} L4,{hy+20} L6,{hy+12} Z", "#ffffff", sw=1.4))
    return p + fangs


def baby(skin=RAMA_BLUE, glow=True):
    """A baby wrapped in cloth, centred at (0,0), about 50 wide."""
    out = []
    if glow:
        out.append(C(0, -6, 34, "#fff4c9", stroke="none", opacity=0.8))
    out += [E(4, 4, 24, 13, "#fffaf0", sw=2.2), P("M-14,0 Q4,10 26,2", stroke="#e6d8b8", sw=1.6),
            C(-16, -4, 12, skin, sw=2.2), P("M-24,-10 Q-16,-20 -8,-11", stroke=BLACK_HAIR, sw=3),
            eyes(-16, -4, 12, "happy"), mouth(-16, 3, "smile"), namam(-16, -9, 0.6)]
    return "".join(out)


# ---- animals ------------------------------------------------------------------------
def cat(pose="lap", color="#f0b46a", stripe="#d08a3c"):
    """A small cat seen from the side, facing right, feet at (0,0). pose: lap (tongue out) | sit."""
    out = [P("M-30,-14 C-46,-22 -50,-40 -40,-46", stroke=OUT, sw=7.5), P("M-30,-14 C-46,-22 -50,-40 -40,-46", stroke=color, sw=4.5),
           E(-8, -18, 26, 16, color),
           P("M-18,-30 l3,8 M-8,-33 l2,9 M2,-32 l1,9", stroke=stripe, sw=2.4),
           R(-26, -10, 8, 10, color, stroke=OUT, sw=2, rx=3), R(6, -10, 8, 10, color, stroke=OUT, sw=2, rx=3)]
    hx, hy = (22, -18) if pose == "lap" else (18, -38)
    out += [P(f"M{hx-10},{hy-10} L{hx-8},{hy-24} L{hx-1},{hy-14} Z", color, sw=2),
            P(f"M{hx+6},{hy-13} L{hx+11},{hy-25} L{hx+14},{hy-9} Z", color, sw=2),
            C(hx + 2, hy, 13, color),
            E(hx + 5, hy - 2, 1.8, 2.6, "#2a1c14", stroke="none"), E(hx + 11, hy - 2, 1.8, 2.6, "#2a1c14", stroke="none"),
            P(f"M{hx+9},{hy+3} l-1.5,1.5 l-1.5,-1.5 Z", "#e07a7a", sw=1),
            P(f"M{hx+14},{hy+4} l9,-2 M{hx+14},{hy+6} l9,2", stroke=OUT, sw=1)]
    if pose == "lap":
        out.append(P(f"M{hx+6},{hy+8} q4,8 9,4", "#f08aa0", sw=1.6))
    return "".join(out)


def elephant(howdah=False, umbrella=False, rider=None, trunk="down", deco=True):
    """Elephant seen from the side, facing right, feet at (0,0); about 190 wide, 150 tall."""
    g, gd = "#9aa3ad", "#7f8893"
    out = [R(-62, -48, 22, 48, gd, stroke=OUT, sw=2.4, rx=8), R(30, -48, 22, 48, gd, stroke=OUT, sw=2.4, rx=8),
           P("M-80,-60 C-84,-118 -30,-140 26,-128 C70,-118 86,-92 80,-56 C74,-36 50,-34 30,-40 L-50,-40 C-70,-40 -78,-46 -80,-60 Z", g, sw=2.6),
           R(-46, -48, 22, 48, g, stroke=OUT, sw=2.4, rx=8), R(46, -48, 22, 48, g, stroke=OUT, sw=2.4, rx=8),
           P("M-82,-78 C-96,-74 -100,-58 -92,-50", stroke=OUT, sw=3)]
    # head, ear, trunk
    out += [C(78, -104, 32, g, sw=2.6),
            P("M60,-120 C38,-128 30,-96 38,-80 C46,-70 62,-76 66,-90 Z", gd, sw=2.2)]
    if trunk == "up":
        out += [P("M100,-96 C118,-104 124,-128 116,-150", stroke=OUT, sw=17), P("M100,-96 C118,-104 124,-128 116,-150", stroke=g, sw=12.5)]
    else:
        out += [P("M102,-92 C114,-70 112,-40 118,-18", stroke=OUT, sw=17), P("M102,-92 C114,-70 112,-40 118,-18", stroke=g, sw=12.5)]
    out += [P("M92,-84 C106,-80 112,-74 116,-66", stroke=OUT, sw=7), P("M92,-84 C106,-80 112,-74 116,-66", stroke="#fffaf0", sw=4.5),
            E(88, -110, 3, 4, "#2a1c14", stroke="none"), C(89, -112, 1, "#ffffff", stroke="none")]
    if deco:
        out += [P("M54,-132 C72,-140 96,-136 104,-122 L96,-110 C86,-120 70,-122 58,-116 Z", ROYAL_RED, sw=2),
                P("M60,-126 L98,-120", stroke=GOLD, sw=2.4), C(100, -116, 4, GOLD, sw=1.4),
                P("M-44,-120 L40,-124 L44,-60 L-48,-56 Z", ROYAL_RED, sw=2.2),
                P("M-46,-64 L44,-68", stroke=GOLD, sw=4), P("M-44,-120 L40,-124", stroke=GOLD, sw=3)]
        for k in range(6):
            out.append(C(-38 + k * 15, -62, 3, GOLD, sw=1))
    if howdah:
        out += [R(-34, -168, 66, 44, GOLD, stroke=OUT, sw=2.4, rx=6), R(-28, -160, 54, 26, "#c9473d", stroke=OUT, sw=1.8, rx=4),
                P("M-38,-168 L36,-168", stroke=OUT, sw=3)]
    if rider is not None:
        out.append(G(rider, x=0, y=-128 if not howdah else -150, s=0.62))
    if umbrella:
        out.append(G(white_umbrella(), x=-2, y=-190, s=0.8))
    return "".join(out)


def horse(color="#c98b5a", mane="#5a3a22", rider=None, prance=False):
    """Horse seen from the side, facing right, hooves at (0,0); about 150 wide."""
    out = []
    legs = ["M-44,-56 L-50,-2", "M-30,-56 L-26,-2", "M30,-56 L36,-2", "M44,-56 L48,-2"] if not prance else \
           ["M-44,-56 L-52,-2", "M-30,-56 L-24,-2", "M30,-56 L48,-30 L56,-34", "M44,-56 L58,-40 L64,-46"]
    for i, d in enumerate(legs):
        out.append(P(d, stroke=OUT, sw=10.5))
        out.append(P(d, stroke=color if i % 2 else "#b47a4c", sw=7))
    out += [P("M-58,-70 C-58,-96 -30,-100 0,-98 C30,-96 52,-96 58,-80 C62,-64 50,-52 30,-52 L-40,-52 C-54,-52 -58,-60 -58,-70 Z", color, sw=2.6),
            P("M-58,-78 C-74,-74 -80,-56 -76,-40 C-70,-52 -64,-62 -58,-66", mane, sw=2),
            P("M40,-90 C50,-110 62,-126 76,-128 C88,-128 94,-118 90,-110 L70,-96 C64,-86 56,-78 50,-74 Z", color, sw=2.6),
            P("M44,-96 C52,-118 62,-132 72,-132 C66,-120 58,-104 54,-92 Z", mane, sw=2),
            P("M70,-128 L72,-140 L78,-128 Z", color, sw=2), E(80, -118, 2.4, 3, "#2a1c14", stroke="none"),
            P("M-50,-96 C-20,-104 20,-104 44,-96", stroke=ROYAL_RED, sw=6)]
    if rider is not None:
        out.append(G(rider, x=0, y=-92, s=0.62))
    return "".join(out)


def chariot(color=GOLD, flag=ROYAL_RED, rider=None, horses=True):
    """Chariot facing right with (optionally) one horse in front; wheels on the ground at y=0."""
    out = []
    if horses:
        out.append(G(horse("#f2efe6", "#c9c2b2", prance=False), x=110, y=0, s=0.92))
        out.append(P("M30,-66 L96,-74", stroke="#8a5a2b", sw=4))
    out += [P("M-60,-40 L40,-40 L50,-70 L-62,-70 Z", color, sw=2.4),
            P("M-56,-70 L-56,-150 M36,-70 L36,-150", stroke="#8a5a2b", sw=4),
            P("M-72,-150 Q-10,-178 48,-150 Z", ROYAL_RED, sw=2.2), P("M-70,-150 L46,-150", stroke=GOLD, sw=4),
            P("M-10,-170 L-10,-210", stroke="#8a5a2b", sw=3), P("M-10,-208 L18,-200 L-10,-192 Z", flag, sw=2)]
    if rider is not None:
        out.append(G(rider, x=-10, y=-60, s=0.75))
    out += [C(-30, -26, 26, "#8a5a2b", sw=2.6), C(-30, -26, 20, "none", stroke="#c9a46a", sw=3)]
    for k in range(8):
        a = k * math.pi / 4
        out.append(P(f"M-30,-26 L{-30 + 20*math.cos(a):.1f},{-26 + 20*math.sin(a):.1f}", stroke="#c9a46a", sw=2.4))
    out.append(C(-30, -26, 5, GOLD, sw=1.8))
    return "".join(out)


def peacock(dance=True, s=1.0):
    """Peacock facing right; feet at (0,0)."""
    out = []
    if dance:
        for k in range(13):
            a = math.pi + 0.25 + k * (math.pi - 0.5) / 12
            x2, y2 = 70 * math.cos(a), -46 + 70 * math.sin(a)
            out.append(P(f"M-6,-40 L{x2:.1f},{y2:.1f}", stroke="#2f8a6a", sw=3))
            out.append(E(x2, y2, 8, 10, "#2f9a7a", sw=1.6))
            out.append(C(x2, y2, 4.2, "#1f5fa0", stroke="none"))
            out.append(C(x2, y2, 1.8, "#f2c14e", stroke="none"))
    else:
        out.append(P("M-6,-34 C-40,-30 -70,-14 -84,-4 L-74,0 C-56,-6 -30,-14 -4,-20 Z", "#2f8a6a", sw=2))
    out += [P("M-2,-6 L-4,0 M6,-6 L8,0", stroke="#8a6a4a", sw=2.4),
            E(0, -28, 14, 20, "#1f63b0", sw=2.2),
            P("M6,-44 C10,-60 14,-72 12,-80", stroke=OUT, sw=8), P("M6,-44 C10,-60 14,-72 12,-80", stroke="#1f63b0", sw=5),
            C(13, -82, 7, "#1f63b0", sw=2), E(15, -83, 1.4, 1.8, "#ffffff", stroke="none"),
            P("M19,-82 L26,-80 L19,-78 Z", "#d9b06a", sw=1.2),
            P("M10,-89 L8,-100 M13,-89 L13,-101 M16,-89 L18,-100", stroke="#1f63b0", sw=1.6),
            C(8, -101, 2, "#1f63b0", stroke="none"), C(13, -102, 2, "#1f63b0", stroke="none"), C(18, -101, 2, "#1f63b0", stroke="none")]
    return G("".join(out), s=s)


def swan(s=1.0):
    """White swan on water, facing right; waterline at (0,0)."""
    out = [P("M-30,-4 C-34,-24 -10,-30 10,-24 C20,-20 26,-12 24,-4 Z", "#ffffff", sw=2.2),
           P("M-26,-10 C-14,-22 2,-22 10,-14", stroke="#d9dde2", sw=2),
           P("M16,-16 C14,-36 26,-46 32,-40", stroke=OUT, sw=7.5), P("M16,-16 C14,-36 26,-46 32,-40", stroke="#ffffff", sw=4.5),
           C(32, -41, 5, "#ffffff", sw=2), P("M36,-42 L44,-39 L36,-37 Z", "#f0a030", sw=1.2),
           C(33, -42, 1.1, "#2a1c14", stroke="none"),
           P("M-34,0 q8,-4 16,0 t16,0 t16,0 t16,0", stroke=WATER_L, sw=2)]
    return G("".join(out), s=s)


def monkey(s=1.0, pose="sit"):
    """A small monkey sitting, facing right; seat at (0,0)."""
    c, cl = "#a8743f", "#e6c39a"
    out = [P("M-14,-8 C-30,-6 -34,-30 -24,-40", stroke=OUT, sw=5.5), P("M-14,-8 C-30,-6 -34,-30 -24,-40", stroke=c, sw=3),
           E(0, -16, 15, 17, c), E(4, -12, 8, 10, cl, stroke="none"),
           E(-6, -2, 9, 5, c, sw=2), E(10, -2, 9, 5, c, sw=2),
           C(6, -40, 13, c), E(8, -38, 9, 8, cl, stroke="none"), C(-6, -44, 5, c, sw=2), C(18, -44, 4.5, c, sw=2),
           C(4, -41, 1.6, "#2a1c14", stroke="none"), C(11, -41, 1.6, "#2a1c14", stroke="none"),
           P("M5,-34 Q8,-31 11,-34", sw=1.4)]
    if pose == "wave":
        out.append(limb("M10,-24 C20,-30 24,-42 26,-52", c, 5))
    return G("".join(out), s=s)


def fish(color="#f08a3a", s=1.0, flip=False):
    return G(E(0, 0, 12, 6, color, sw=1.6) + P("M10,0 L18,-6 L18,6 Z", color, sw=1.6) + C(-6, -1, 1.2, "#2a1c14", stroke="none"),
             s=s, flip=flip)


def bee(x, y, s=1.0):
    return G(E(0, 0, 5, 3.4, "#f2c14e", sw=1.2) + P("M-1,-3 L-1,3 M2,-3 L2,3", stroke=OUT, sw=1.2) +
             E(-1, -5, 3.4, 2.4, "#ffffff", sw=1, opacity=0.9), x=x, y=y, s=s)


def deer(s=1.0):
    c = "#c98b4a"
    out = [P("M-20,-30 L-22,0 M-12,-30 L-10,0 M14,-30 L12,0 M22,-30 L26,0", stroke=OUT, sw=6), 
           P("M-20,-30 L-22,0 M-12,-30 L-10,0 M14,-30 L12,0 M22,-30 L26,0", stroke=c, sw=3.4),
           E(0, -36, 28, 13, c), C(-10, -38, 2, "#ffffff", stroke="none"), C(2, -40, 2, "#ffffff", stroke="none"),
           C(-4, -32, 2, "#ffffff", stroke="none"),
           P("M20,-44 L30,-62", stroke=OUT, sw=9), P("M20,-44 L30,-62", stroke=c, sw=6),
           E(36, -64, 9, 6.5, c, sw=2), P("M30,-70 L28,-84 M28,-78 L22,-84 M34,-70 L38,-84 M37,-78 L44,-82", stroke="#8a5a2b", sw=2.2),
           E(32, -71, 3, 5, c, sw=1.6), C(39, -65, 1.4, "#2a1c14", stroke="none")]
    return G("".join(out), s=s)


def bull(s=1.0, color="#ece6da"):
    out = [P("M-34,-30 L-36,0 M-22,-30 L-20,0 M22,-30 L20,0 M34,-30 L38,0", stroke=OUT, sw=8),
           P("M-34,-30 L-36,0 M-22,-30 L-20,0 M22,-30 L20,0 M34,-30 L38,0", stroke=color, sw=5),
           E(0, -40, 42, 18, color), P("M-10,-56 Q0,-70 10,-56", color, sw=2),
           E(46, -46, 13, 10, color, sw=2), P("M42,-56 L38,-68 M50,-56 L56,-66", stroke="#8a6a4a", sw=3),
           C(50, -48, 1.5, "#2a1c14", stroke="none"), P("M-42,-40 C-52,-36 -52,-24 -48,-18", stroke=OUT, sw=2)]
    return G("".join(out), s=s)


# ---- buildings and things ---------------------------------------------------------------
def white_umbrella():
    """The king's white umbrella (வெண்கொற்றக் குடை); shaft bottom at (0,0)."""
    return (P("M0,0 L0,-70", stroke=GOLD_D, sw=4) + P("M-46,-64 Q0,-110 46,-64 Z", MILK, sw=2.4) +
            P("M-46,-64 Q-34,-56 -23,-64 Q-12,-56 0,-64 Q12,-56 23,-64 Q34,-56 46,-64", MILK, sw=2.2) +
            C(0, -92, 4, GOLD, sw=1.6) + P("M-30,-70 Q0,-96 30,-70", stroke=GOLD, sw=2))


def throne(w=110, color=GOLD):
    """Seat top at y=0, legs to y=40; backrest rising behind."""
    return (P(f"M{-w/2+4},-6 L{-w/2},-96 Q0,-130 {w/2},-96 L{w/2-4},-6 Z", color, sw=2.4) +
            P(f"M{-w/2+12},-14 L{-w/2+10},-88 Q0,-114 {w/2-10},-88 L{w/2-12},-14 Z", ROYAL_RED, sw=2) +
            R(-w / 2 - 6, -6, w + 12, 14, color, stroke=OUT, sw=2.2, rx=4) +
            R(-w / 2, 8, 12, 30, color, stroke=OUT, sw=2) + R(w / 2 - 12, 8, 12, 30, color, stroke=OUT, sw=2) +
            C(0, -112, 6, JEWEL_RED, stroke=GOLD_D, sw=1.6))


def palace(x, y, s=1.0, color=MARBLE, roof=GOLD, w=220):
    """South-Indian style palace hall: base at (x, y)."""
    h = []
    h.append(R(-w / 2, -16, w, 16, "#d8c7a6", stroke=OUT, sw=2.2))
    cols = 6
    for k in range(cols):
        cx = -w / 2 + 14 + k * (w - 28) / (cols - 1)
        h.append(R(cx - 6, -96, 12, 80, color, stroke=OUT, sw=2))
    h.append(R(-w / 2 + 8, -96, w - 16, 80, "#00000010"))
    h.append(R(-w / 2 - 6, -110, w + 12, 16, color, stroke=OUT, sw=2.2))
    h.append(P(f"M{-w/2-14},-110 L{-w/2+20},-150 L{w/2-20},-150 L{w/2+14},-110 Z", roof, sw=2.4))
    h.append(P(f"M{-w/2+20},-150 L{-w/2+40},-176 L{w/2-40},-176 L{w/2-20},-150 Z", roof, sw=2.4))
    for k in range(5):
        h.append(G(P("M-5,0 Q0,-14 5,0 Z", GOLD_D, sw=1.6) + C(0, -16, 3, GOLD, sw=1.4), x=-w / 2 + 50 + k * (w - 100) / 4, y=-176))
    h.append(P(f"M{-w/2-6},-118 L{w/2+6},-118", stroke=JEWEL_RED, sw=2.4))
    return G(*h, x=x, y=y, s=s)


def tower(x, y, s=1.0, color=MARBLE, roof=GOLD):
    t = [R(-26, -120, 52, 120, color, stroke=OUT, sw=2.2),
         R(-10, -100, 20, 26, "#5a3a22", stroke=OUT, sw=2, rx=10), R(-10, -56, 20, 26, "#5a3a22", stroke=OUT, sw=2, rx=10),
         P("M-34,-120 L0,-170 L34,-120 Z", roof, sw=2.2), C(0, -176, 5, GOLD, sw=1.6)]
    return G(*t, x=x, y=y, s=s)


def flag(x, y, color=ROYAL_RED, s=1.0, pole=60, wave=0):
    return G(P(f"M0,0 L0,{-pole}", stroke="#8a5a2b", sw=3) +
             P(f"M0,{-pole} C14,{-pole-6+wave} 26,{-pole+4} 40,{-pole-2} L36,{-pole+18} C24,{-pole+22} 12,{-pole+12} 0,{-pole+20} Z", color, sw=2),
             x=x, y=y, s=s)


def city_wall(y=360, x0=0, x1=800, color="#e3c48a", h=90, gate_x=None):
    out = [R(x0, y - h, x1 - x0, h, color, stroke=OUT, sw=2.4)]
    for xx in range(int(x0), int(x1), 28):
        out.append(R(xx + 4, y - h - 16, 18, 18, color, stroke=OUT, sw=2))
    for yy in range(int(y - h + 18), int(y), 22):
        out.append(P(f"M{x0},{yy} L{x1},{yy}", stroke="#c9a46a", sw=1.2, opacity=0.6))
    if gate_x is not None:
        out += [R(gate_x - 52, y - h - 40, 104, h + 40, color, stroke=OUT, sw=2.4),
                P(f"M{gate_x-30},{y} L{gate_x-30},{y-70} Q{gate_x},{y-104} {gate_x+30},{y-70} L{gate_x+30},{y} Z", "#6b4a2e", sw=2.4),
                P(f"M{gate_x},{y-90} L{gate_x},{y}", stroke="#4a3220", sw=2),
                P(f"M{gate_x-60},{y-h-40} L{gate_x},{y-h-82} L{gate_x+60},{y-h-40} Z", GOLD, sw=2.4)]
    return "".join(out)


def moat(y=380, h=40, x0=0, x1=800):
    out = [R(x0, y, x1 - x0, h, "url(#water)", stroke="none"), P(f"M{x0},{y} L{x1},{y}", stroke="#ffffff", sw=2.4, opacity=0.6)]
    for k in range(int(x0) + 30, int(x1), 120):
        out.append(lotus(k, y + h * 0.55, 0.7))
    return "".join(out)


def lotus(x, y, s=1.0, color="#f28aa6"):
    pad = E(-14, 6, 18, 6, "#5aa060", sw=1.8)
    fl = (P("M0,0 C-10,-6 -12,-18 -4,-24 C-2,-14 0,-8 0,0 Z", color, sw=1.6) +
          P("M0,0 C10,-6 12,-18 4,-24 C2,-14 0,-8 0,0 Z", color, sw=1.6) +
          P("M0,0 C-4,-10 -3,-22 0,-28 C3,-22 4,-10 0,0 Z", "#f6a8bd", sw=1.6) +
          P("M-2,0 C-14,-2 -20,-10 -18,-14 C-10,-12 -4,-6 -2,0 Z M2,0 C14,-2 20,-10 18,-14 C10,-12 4,-6 2,0 Z", color, sw=1.4))
    return G(pad + fl, x=x, y=y, s=s)


def lotus_pond(cx, cy, rx=200, ry=46):
    out = [E(cx, cy, rx, ry, "url(#water)", stroke=OUT, sw=2.4),
           E(cx, cy, rx - 8, ry - 6, "none", stroke=WATER_L, sw=2, opacity=0.7)]
    for k, (dx, dy) in enumerate([(-0.6, 0.1), (-0.25, -0.2), (0.15, 0.25), (0.5, -0.1), (0.75, 0.2)]):
        out.append(lotus(cx + dx * rx, cy + dy * ry, 0.8, "#f28aa6" if k % 2 else "#f7d0dc"))
    return "".join(out)


def mountain(x, y, s=1.0, color="#9db7c9", snow="#ffffff", gold=False):
    c = "#e8c25a" if gold else color
    d = "#cfa23a" if gold else "#86a2b6"
    m = (P("M-150,0 L-40,-170 L0,-120 L40,-180 L160,0 Z", c, sw=2.6) +
         P("M40,-180 L60,-140 L30,-150 L10,-130 L0,-120 Z", d, stroke="none", opacity=0.6) +
         P("M-40,-170 L-18,-136 L-36,-142 L-54,-130 Z", snow, sw=1.8) +
         P("M40,-180 L64,-140 L44,-146 L28,-134 L20,-150 Z", snow, sw=1.8))
    return G(m, x=x, y=y, s=s)


def waterfall(x, y, h=150, w=34):
    out = [R(x - w / 2, y - h, w, h, "#bfe6f3", stroke=OUT, sw=2)]
    for k in range(4):
        out.append(P(f"M{x - w/2 + 6 + k*8},{y-h+6} L{x - w/2 + 6 + k*8},{y-6}", stroke="#ffffff", sw=2.4, opacity=0.9))
    out.append(E(x, y, w + 14, 10, "#dff4fa", sw=2))
    return "".join(out)


def coconut(x, y, s=1.0, lean=6):
    t = [P(f"M0,0 C{lean*0.5},-60 {lean},-120 {lean*1.4},-170", stroke=OUT, sw=11), P(f"M0,0 C{lean*0.5},-60 {lean},-120 {lean*1.4},-170", stroke="#a9733f", sw=7.5)]
    top = (lean * 1.4, -170)
    for a in (-160, -125, -90, -55, -20, 15, 200):
        r = math.radians(a)
        ex, ey = top[0] + 64 * math.cos(r), top[1] + 30 * math.sin(r) + 14
        t.append(P(f"M{top[0]},{top[1]} Q{(top[0]+ex)/2},{top[1]-26} {ex:.1f},{ey:.1f}", stroke=OUT, sw=8.5))
        t.append(P(f"M{top[0]},{top[1]} Q{(top[0]+ex)/2},{top[1]-26} {ex:.1f},{ey:.1f}", stroke=LEAF, sw=5.5))
    t += [C(top[0] - 5, top[1] + 6, 6, "#7a5a2a", sw=1.6), C(top[0] + 6, top[1] + 7, 6, "#7a5a2a", sw=1.6)]
    return G(*t, x=x, y=y, s=s)


def banana(x, y, s=1.0):
    t = [P("M-6,0 L-5,-90 L5,-90 L6,0 Z", "#8fbf5a", sw=2.2)]
    for ang, ln in ((-150, 70), (-120, 80), (-60, 80), (-30, 70), (-95, 60)):
        r = math.radians(ang)
        ex, ey = ln * math.cos(r), -90 + ln * math.sin(r)
        t.append(P(f"M0,-90 Q{ex*0.5 - 10},{-90 + (ey+90)*0.5 - 18} {ex:.1f},{ey:.1f} Q{ex*0.5 + 6},{-90 + (ey+90)*0.5 + 4} 0,-88 Z", LEAF_L, sw=2))
    t.append(P("M2,-70 C14,-66 18,-50 12,-40", stroke="#7a5a2a", sw=3))
    t.append(E(14, -36, 7, 10, "#e8d24a", sw=1.6))
    return G(*t, x=x, y=y, s=s)


def paddy(x0, x1, y, rows=3, color="#9acb5a", ripe=False):
    out = []
    c = "#e2c254" if ripe else color
    for r in range(rows):
        yy = y + r * 16
        for xx in range(int(x0) + (r % 2) * 9, int(x1), 18):
            out.append(P(f"M{xx},{yy} L{xx-5},{yy-18} M{xx},{yy} L{xx},{yy-22} M{xx},{yy} L{xx+5},{yy-18}", stroke=c, sw=2.4))
            if ripe:
                out.append(P(f"M{xx},{yy-22} q4,-2 6,4", stroke="#c9a23a", sw=2))
    return "".join(out)


def field_band(y, h, color="#c7e29a", water=False):
    out = [R(0, y, W, h, color, stroke="none")]
    if water:
        for xx in range(30, W, 110):
            out.append(P(f"M{xx},{y + h/2} q10,-4 20,0", stroke="#ffffff", sw=2, opacity=0.6))
    out.append(P(f"M0,{y} L{W},{y}", stroke="#8fb86a", sw=2))
    return "".join(out)


def tent(x, y, s=1.0, color="#f2e2b8", stripe=ROYAL_RED):
    t = [P("M-60,0 L0,-80 L60,0 Z", color, sw=2.4), P("M-20,0 L0,-80 L20,0", stroke=stripe, sw=3),
         P("M-12,0 L0,-30 L12,0 Z", "#7a5a3a", sw=2), P("M0,-80 L0,-104", stroke="#8a5a2b", sw=2.6),
         P("M0,-104 L18,-98 L0,-92 Z", stripe, sw=1.6)]
    return G(*t, x=x, y=y, s=s)


def fire_altar(x, y, s=1.0):
    """Homa / yagna fire on a square brick altar; base at (x,y)."""
    f = [R(-50, -26, 100, 26, "#c9673d", stroke=OUT, sw=2.4), R(-40, -40, 80, 16, "#d97d4f", stroke=OUT, sw=2.2),
         P("M-50,-13 L50,-13 M-20,-26 L-20,0 M20,-26 L20,0", stroke="#a04a28", sw=1.4),
         P("M-26,-40 C-30,-62 -14,-70 -12,-88 C-2,-74 2,-80 0,-104 C14,-86 22,-74 14,-58 C24,-62 28,-50 26,-40 Z", "#ffb02e", sw=2.2),
         P("M-12,-40 C-14,-56 -4,-60 0,-76 C8,-62 14,-54 10,-40 Z", "#ffe27a", sw=1.6)]
    return G(*f, x=x, y=y, s=s)


def mandapam(x, y, s=1.0, w=300, h=200, color="#f6e7c4"):
    """Wedding pavilion with four pillars, a canopy and mango-leaf garlands; floor at (x,y)."""
    out = [R(-w / 2 - 10, -14, w + 20, 14, "#d8c7a6", stroke=OUT, sw=2.2)]
    for k in (-w / 2, -w / 6, w / 6, w / 2):
        out.append(R(k - 8, -h, 16, h - 14, color, stroke=OUT, sw=2.2))
        out.append(P(f"M{k-8},{-h+30} L{k+8},{-h+30} M{k-8},{-60} L{k+8},{-60}", stroke=GOLD_D, sw=2))
    out.append(P(f"M{-w/2-24},{-h} L{-w/2+10},{-h-50} L{w/2-10},{-h-50} L{w/2+24},{-h} Z", ROYAL_RED, sw=2.4))
    out.append(P(f"M{-w/2-24},{-h} L{w/2+24},{-h}", stroke=GOLD, sw=5))
    for k in range(int(-w / 2), int(w / 2) + 1, 22):
        out.append(P(f"M{k},{-h+2} l6,16 l6,-16", "#5aa060", sw=1.6))
    for k in (-w / 3, 0, w / 3):
        out.append(P(f"M{k-40},{-h+20} Q{k},{-h+52} {k+40},{-h+20}", stroke="#ffffff", sw=4))
        out.append(P(f"M{k-40},{-h+20} Q{k},{-h+52} {k+40},{-h+20}", stroke="#f28aa6", sw=4, stroke_dasharray="3 6"))
    return G(*out, x=x, y=y, s=s)


def balcony(x, y, w=180, h=120, color=MARBLE):
    """A palace window/balcony; the floor of the window at (x, y)."""
    return G(R(-w / 2, -h, w, h, "#7a5a3a", stroke=OUT, sw=2.4, rx=4) +
             R(-w / 2 + 10, -h + 10, w - 20, h - 10, "#f3d9a8", stroke=OUT, sw=1.8) +
             P(f"M{-w/2-14},{-h} L{-w/2},{-h-34} L{w/2},{-h-34} L{w/2+14},{-h} Z", GOLD, sw=2.2) +
             R(-w / 2 - 14, 0, w + 28, 14, color, stroke=OUT, sw=2.2) +
             "".join(R(-w / 2 - 8 + k * 22, 14, 8, 26, color, stroke=OUT, sw=1.8) for k in range(int((w + 16) / 22) + 1)) +
             R(-w / 2 - 14, 40, w + 28, 10, color, stroke=OUT, sw=2.2),
             x=x, y=y)


def stone(x, y, s=1.0, glow=False):
    out = []
    if glow:
        out.append(E(0, -30, 70, 50, "url(#glow)", stroke="none"))
    out += [P("M-50,0 C-56,-30 -40,-58 -6,-60 C30,-62 52,-40 50,-10 L46,0 Z", STONE, sw=2.4),
            P("M-30,-40 C-20,-48 -6,-50 6,-46", stroke="#c7c1b8", sw=3), P("M10,-20 l12,-6 M-20,-14 l8,4", stroke=STONE_D, sw=2)]
    return G(*out, x=x, y=y, s=s)


def milk_sea(y_top=320, y_bot=500):
    out = [P(f"M0,{y_top} C200,{y_top-10} 420,{y_top+10} 800,{y_top-4} L800,{y_bot} L0,{y_bot} Z", "#fbfaf2", stroke="none")]
    for i, yy in enumerate(range(y_top + 16, y_bot, 24)):
        off = (i * 83) % 150
        for xx in range(30 + off, 800, 190):
            out.append(P(f"M{xx},{yy} q14,-8 28,0 t28,0", stroke="#d9dccd", sw=2.4))
    out.append(P(f"M0,{y_top} C200,{y_top-10} 420,{y_top+10} 800,{y_top-4}", stroke="#e6e2cf", sw=3))
    return "".join(out)


def sea(y_top=330, y_bot=500):
    return river(y_top, y_bot) if False else (
        P(f"M0,{y_top} C200,{y_top-8} 420,{y_top+8} 800,{y_top-4} L800,{y_bot} L0,{y_bot} Z", "url(#water)", stroke="none") +
        "".join(P(f"M{xx},{yy} q12,-6 24,0 t24,0", stroke=WATER_L, sw=2.4, opacity=0.9)
                for i, yy in enumerate(range(y_top + 18, y_bot, 22)) for xx in range(40 + (i * 97) % 160, 800, 210)))


def rainbow(cx, cy, r=220, opacity=0.75):
    cols = ["#e0524a", "#f2994a", "#f2d24a", "#6cc06a", "#4aa0e0", "#7a6ad0"]
    return "".join(P(f"M{cx-r+i*9},{cy} A{r-i*9},{r-i*9} 0 0 1 {cx+r-i*9},{cy}", stroke=c, sw=9, opacity=opacity)
                   for i, c in enumerate(cols))


def dark_cloud(x, y, s=1.0, color="#6e7f99"):
    c = (E(0, 0, 46, 18, color, stroke="none") + C(-18, -10, 18, color, stroke="none") +
         C(10, -16, 22, color, stroke="none") + C(32, -6, 14, color, stroke="none"))
    return G(c, x=x, y=y, s=s)


def rain(x0, x1, y0, y1, color="#e6f2ff", step=16):
    out = []
    for i, xx in enumerate(range(int(x0), int(x1), step)):
        off = (i * 37) % 30
        out.append(P(f"M{xx},{y0 + off} L{xx-6},{y1 - (i*13) % 40}", stroke=color, sw=2.2, opacity=0.9))
    return "".join(out)


def cradle(x, y, s=1.0):
    c = [P("M-60,-30 Q0,10 60,-30", "#c98b4a", sw=2.4), P("M-60,-30 L-70,-110 M60,-30 L70,-110", stroke="#8a5a2b", sw=4),
         P("M-70,-110 L70,-110", stroke="#8a5a2b", sw=4), P("M-50,-104 L-50,-36 M50,-104 L50,-36", stroke="#c9a46a", sw=1.6),
         P("M-60,-30 L60,-30", stroke=GOLD, sw=3)]
    return G(*c, x=x, y=y, s=s)


def drum(x, y, s=1.0):
    return G(E(0, -20, 18, 22, "#b5452f", sw=2.2) + E(0, -42, 18, 5, "#f3e3c3", sw=2) +
             P("M-16,-38 L16,-6 M16,-38 L-16,-6", stroke="#f3e3c3", sw=1.4), x=x, y=y, s=s)


def petals(points, color="#f28aa6"):
    return "".join(G(E(0, 0, 4, 2.6, color, stroke="none"), x=x, y=y, rot=r) for x, y, r in points)


def stars(points, color="#fff6c8"):
    return "".join(sparkle(x, y, s, color) for x, y, s in points)


def moon(x, y, r=26, crescent=True):
    if crescent:
        return C(x, y, r, "#fff6c8", stroke="none") + C(x + r * 0.45, y - r * 0.25, r * 0.9, "url(#sky)", stroke="none")
    return C(x, y, r * 1.6, "#fffbe6", stroke="none", opacity=0.35) + C(x, y, r, "#fff6c8", stroke="none")


def night_defs():
    return ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d2b52"/>'
            '<stop offset="0.6" stop-color="#34497a"/><stop offset="1" stop-color="#5b6f9e"/></linearGradient>'
            f'<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4b6fa0"/><stop offset="1" stop-color="#36557f"/></linearGradient>'
            '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fffbe6" stop-opacity="1"/>'
            '<stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>')


def desert_defs():
    return ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7c77a"/>'
            '<stop offset="0.6" stop-color="#fbe2b0"/><stop offset="1" stop-color="#fdf0d5"/></linearGradient>'
            f'<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WATER}"/><stop offset="1" stop-color="{WATER_D}"/></linearGradient>'
            '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fffbe6" stop-opacity="1"/>'
            '<stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>')


def indoor_defs():
    return ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6e3c0"/>'
            '<stop offset="1" stop-color="#f9ecd6"/></linearGradient>'
            f'<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WATER}"/><stop offset="1" stop-color="{WATER_D}"/></linearGradient>'
            '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fffbe6" stop-opacity="1"/>'
            '<stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>')


def hall(floor=400, wall="#f6e3c0", pillar=MARBLE, n=5, curtain=ROYAL_RED):
    """Inside a palace hall: back wall, pillars, a patterned floor."""
    out = [R(0, 0, W, floor, wall), R(0, floor, W, H - floor, "#e8cf9f"),
           P(f"M0,{floor} L{W},{floor}", stroke="#c9a46a", sw=2.4)]
    for i in range(0, W, 40):
        out.append(P(f"M{i},{floor} L{i - 60},{H}", stroke="#d9bb85", sw=1.4))
    for k in range(n):
        x = 40 + k * (W - 80) / (n - 1)
        out += [R(x - 14, 40, 28, floor - 40, pillar, stroke=OUT, sw=2.2), R(x - 20, 30, 40, 14, GOLD, stroke=OUT, sw=2),
                R(x - 20, floor - 12, 40, 12, GOLD, stroke=OUT, sw=2)]
    out.append(P(f"M0,30 L{W},30", stroke=OUT, sw=2.4))
    out.append(R(0, 0, W, 30, curtain))
    for k in range(0, W, 50):
        out.append(P(f"M{k},30 Q{k+25},62 {k+50},30", curtain, sw=2))
    return "".join(out)


def speech_bubble(x, y, w, h, tail=(0, 40)):
    return G(R(-w / 2, -h / 2, w, h, "#ffffff", stroke=OUT, sw=2.2, rx=18) +
             P(f"M-12,{h/2-1} L{tail[0]},{h/2 + tail[1]} L12,{h/2-1}", "#ffffff", sw=2.2) +
             P(f"M-11,{h/2-1} L11,{h/2-1}", stroke="#ffffff", sw=3), x=x, y=y)
