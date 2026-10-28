"""Desain detail Taman RT A & B (UTM 49S, koordinat benar).
Gaya: denah lanskap organik (jalur lengkung, lawn, area bermain, gazebo, pohon berlapis)."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gen'))
import numpy as np
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import unary_union
from shapely import affinity
from geo2 import fix_old
import taman as OLD
from desain_jalan import BUILD

def fx(poly):
    return Polygon([fix_old(x, y) for x, y in poly.exterior.coords])

def smooth_curve(pts, n=24, closed=False):
    """Catmull-Rom spline."""
    P = list(pts)
    if closed: P = [P[-1]] + P + [P[0], P[1]]
    else: P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = map(np.array, (P[i - 1], P[i], P[i + 1], P[i + 2]))
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)))
    if not closed: out.append(tuple(P[-2]))
    return out

# ======================================================================= TAMAN A
A = fx(OLD.A)
A_RUMAH = fx(OLD.A_rumah).buffer(0)
A_bersih = A.difference(BUILD.buffer(0.5))

def taman_A():
    g = {}
    P = A_bersih
    c = P.centroid
    # pagar hijau peredam sisi Jl. Cendrawasih/rel (barat) + tepi lain
    west = LineString([fix_old(306057.5, 9156518.0), fix_old(306064.0, 9156485.5)])
    g['perdu_peredam'] = P.intersection(west.buffer(2.2, cap_style='flat'))
    g['perdu_tepi'] = P.difference(P.buffer(-1.2)).difference(g['perdu_peredam'].buffer(0.1))
    # jalur keliling lengkung (1,5 m)
    loop_pts = [fix_old(*q) for q in [(306066.5, 9156514.5), (306080.0, 9156514.8), (306087.5, 9156511.0), (306094.0, 9156505.0),
                                     (306104.0, 9156504.0), (306107.0, 9156496.0), (306103.5, 9156488.5), (306094.5, 9156488.8),
                                     (306092.5, 9156497.0), (306086.0, 9156505.0), (306076.0, 9156506.0), (306068.0, 9156504.0),
                                     (306066.5, 9156494.0), (306067.5, 9156488.5)]]
    curve = smooth_curve(loop_pts, n=14)
    jalur = LineString(curve).buffer(0.75, cap_style='round', join_style='round')
    # penghubung ke pintu barat (Jl. Cendrawasih) & selatan
    pin_w = LineString([fix_old(306061.0, 9156507.0), fix_old(306067.0, 9156507.5)]).buffer(1.0, cap_style='flat')
    pin_s = LineString([fix_old(306100.0, 9156484.5), fix_old(306100.0, 9156489.5)]).buffer(1.0, cap_style='flat')
    pin_sw = LineString([fix_old(306067.5, 9156484.5), fix_old(306067.5, 9156489.5)]).buffer(0.9, cap_style='flat')
    g['jalur'] = unary_union([jalur, pin_w, pin_s, pin_sw]).intersection(P)
    # area bermain (lantai karet) - oval utara
    pc = Point(fix_old(306073.5, 9156510.5))
    g['bermain'] = affinity.scale(pc.buffer(1), 6.0, 3.6).difference(g['jalur'].buffer(0.3)).intersection(P.buffer(-1.4))
    # lapangan rumput serbaguna - timur, di dalam lengkung
    lc = Point(fix_old(306100.0, 9156496.5))
    g['lawn'] = affinity.scale(lc.buffer(1), 4.6, 6.0).difference(g['jalur'].buffer(0.4)).intersection(P.buffer(-1.6))
    # gazebo 4x4 (atap perisai) sisi barat-daya
    gc = fix_old(306066.3, 9156496.5)
    g['gazebo'] = box(gc[0] - 2.0, gc[1] - 2.0, gc[0] + 2.0, gc[1] + 2.0)
    g['gazebo_lantai'] = g['gazebo'].buffer(0.6, join_style='mitre')
    # bedeng bunga (aksen)
    g['bunga'] = unary_union([Point(fix_old(306095.5, 9156493.0)).buffer(1.2), Point(fix_old(306086.5, 9156512.0)).buffer(1.0)]).difference(g['jalur'].buffer(0.2)).intersection(P.buffer(-1.0))
    # pohon: tepi + aksen (x, y, r, jenis)
    pohon = []
    for q, r, j in [((306060.5, 9156515.5), 2.6, 'trembesi'), ((306062.5, 9156505.5), 2.0, 'tabebuya'), ((306064.5, 9156491.0), 2.2, 'ketapang'),
                    ((306066.0, 9156486.8), 1.9, 'tabebuya'), ((306071.0, 9156516.0), 2.3, 'ketapang'), ((306081.0, 9156516.2), 2.4, 'trembesi'),
                    ((306088.2, 9156516.0), 1.8, 'tabebuya'), ((306096.0, 9156506.3), 2.1, 'ketapang'), ((306103.0, 9156506.0), 2.3, 'trembesi'),
                    ((306108.8, 9156500.0), 2.0, 'tabebuya'), ((306108.5, 9156490.5), 2.4, 'ketapang'), ((306092.0, 9156486.8), 2.0, 'tabebuya'),
                    ((306079.5, 9156509.8), 1.7, 'tabebuya')]:
        x, y = fix_old(*q); pohon.append((x, y, r, j))
    g['pohon'] = pohon
    g['bangku'] = [(fix_old(*q), ang) for q, ang in [((306079.5, 9156512.8), 0), ((306072.0, 9156507.6), 0), ((306094.0, 9156493.0), 90),
                                                     ((306103.0, 9156486.6), 0), ((306069.5, 9156499.0), 90)]]
    g['lampu'] = [fix_old(*q) for q in [(306068.8, 9156512.3), (306084.0, 9156508.6), (306097.5, 9156503.0), (306105.0, 9156490.0), (306069.8, 9156490.5)]]
    g['tong_sampah'] = [fix_old(*q) for q in [(306064.5, 9156508.8), (306098.5, 9156487.2)]]
    g['main_alat'] = [(fix_old(306070.8, 9156510.8), 'ayunan'), (fix_old(306075.8, 9156510.0), 'perosotan'), (fix_old(306073.3, 9156512.5), 'jungkat')]
    g['batas'] = A
    g['rumah'] = A_RUMAH
    g['pintu'] = [(fix_old(306059.6, 9156507.3), 'W'), (fix_old(306100.0, 9156485.0), 'S'), (fix_old(306067.5, 9156485.0), 'S')]
    return g

# ======================================================================= TAMAN B
B = fx(OLD.B)
B_RUMAH = fx(OLD.B_rumah)
BALAI = fx(OLD.BALAI)
B_bersih = B.difference(BUILD.buffer(0.5))

def taman_B():
    g = {}
    P = B_bersih
    g['perdu_tepi'] = P.difference(P.buffer(-1.0)).intersection(unary_union([
        LineString([fix_old(306321, 9156499), fix_old(306353, 9156499)]).buffer(1.2),
        LineString([fix_old(306321, 9156499), fix_old(306321, 9156465)]).buffer(1.2)]))
    plaza = unary_union([box(*fix_old(306336.5, 9156466.5), *fix_old(306353.5, 9156497.0)),
                         box(*fix_old(306353.0, 9156485.0), *fix_old(306371.0, 9156488.5)),
                         box(*fix_old(306354.5, 9156465.0), *fix_old(306371.5, 9156469.5))])
    g['plaza'] = plaza.intersection(P)
    lc = Point(fix_old(306328.0, 9156481.5))
    g['lawn'] = lc.buffer(5.6).intersection(P.buffer(-1.0)).difference(plaza.buffer(0.4))
    # dinding duduk lengkung (seat wall) di tepi timur lawn
    arc = [(lc.x + 6.3 * math.cos(a), lc.y + 6.3 * math.sin(a)) for a in np.linspace(-1.1, 1.1, 30)]
    g['seat_wall'] = LineString(arc).buffer(0.25, cap_style='round')
    g['bermain'] = affinity.scale(Point(fix_old(306329.0, 9156493.5)).buffer(1), 5.2, 3.0).intersection(P.buffer(-1.2)).difference(g['lawn'].buffer(0.5))
    gc = fix_old(306327.0, 9156470.0)
    g['gazebo'] = box(gc[0] - 2.0, gc[1] - 2.0, gc[0] + 2.0, gc[1] + 2.0)
    g['gazebo_lantai'] = g['gazebo'].buffer(0.6, join_style='mitre')
    # jalan setapak lawn -> plaza
    g['setapak'] = unary_union([LineString(smooth_curve([fix_old(306330.0, 9156472.5), fix_old(306333.5, 9156475.0), fix_old(306337.0, 9156476.0)], 8)).buffer(0.6),
                                LineString(smooth_curve([fix_old(306333.0, 9156491.5), fix_old(306335.5, 9156489.5), fix_old(306337.0, 9156489.0)], 8)).buffer(0.6)]).intersection(P)
    pohon = []
    # pohon dalam lubang (tree grate) di plaza: 2 baris
    for qx in (306340.5, 306349.5):
        for qy in (9156471.0, 9156478.5, 9156486.0, 9156493.5):
            x, y = fix_old(qx, qy); pohon.append((x, y, 2.0, 'ketapang' if qy in (9156471.0, 9156486.0) else 'tabebuya'))
    for q, r, j in [((306323.0, 9156497.0), 2.2, 'trembesi'), ((306323.0, 9156486.5), 1.9, 'tabebuya'), ((306323.0, 9156476.5), 2.0, 'ketapang'),
                    ((306333.5, 9156497.0), 2.0, 'ketapang'), ((306366.0, 9156467.0), 1.6, 'tabebuya')]:
        x, y = fix_old(*q); pohon.append((x, y, r, j))
    g['pohon'] = pohon
    g['grate'] = [(x, y) for x, y, r, j in pohon[:8]]
    g['bangku'] = [(fix_old(*q), ang) for q, ang in [((306345.0, 9156474.8), 90), ((306345.0, 9156489.8), 90), ((306361.0, 9156487.4), 0), ((306330.5, 9156466.6), 0)]]
    g['lampu'] = [fix_old(*q) for q in [(306338.0, 9156482.0), (306352.0, 9156482.0), (306362.0, 9156486.0), (306330.0, 9156488.0)]]
    g['tong_sampah'] = [fix_old(*q) for q in [(306353.5, 9156489.5), (306355.5, 9156468.2)]]
    g['main_alat'] = [(fix_old(306326.5, 9156493.5), 'ayunan'), (fix_old(306331.5, 9156493.5), 'perosotan')]
    g['parkir_sepeda'] = box(*fix_old(306364.0, 9156465.6), *fix_old(306370.5, 9156467.0))
    from desain_jalan import ROADS
    y0 = fix_old(306371.0, 9156486.8)[1]; x0 = fix_old(306371.0, 9156486.8)[0]
    cross = LineString([(x0 - 2, y0), (x0 + 12, y0)]).intersection(ROADS)
    seg = max(getattr(cross, 'geoms', [cross]), key=lambda q: q.length)
    xa, xb = seg.bounds[0], seg.bounds[2]
    g['zebra'] = [box(xa + 0.2, y0 - 1.6 + k * 0.6, xb - 0.2, y0 - 1.3 + k * 0.6) for k in range(6)]
    g['batas'] = B
    g['rumah'] = B_RUMAH
    g['balai'] = BALAI
    g['pintu'] = [(fix_old(306371.0, 9156486.8), 'E'), (fix_old(306363.0, 9156465.0), 'S')]
    return g

if __name__ == '__main__':
    a, b = taman_A(), taman_B()
    print('A luas %.0f (bersih %.0f), jalur %.0f, bermain %.0f, lawn %.0f, pohon %d' % (A.area, A_bersih.area, a['jalur'].area, a['bermain'].area, a['lawn'].area, len(a['pohon'])))
    print('B luas %.0f (bersih %.0f), plaza %.0f, lawn %.0f, bermain %.0f, pohon %d' % (B.area, B_bersih.area, b['plaza'].area, b['lawn'].area, b['bermain'].area, len(b['pohon'])))
