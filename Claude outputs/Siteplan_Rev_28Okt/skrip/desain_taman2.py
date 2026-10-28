"""Taman RT A & B Rev 28 Okt (b): batas mengikuti tepi jalan & bangunan (tidak miring),
pintu masuk/keluar jelas dan tersambung ke jalan dengan fillet. Koordinat UTM 49S."""
import math, pickle, os
import numpy as np
from shapely.geometry import Polygon, Point, LineString, box, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity
import desain_jalan2 as DJ

HERE = os.path.dirname(os.path.abspath(__file__))
H = pickle.load(open(os.path.join(HERE, 'hijau_eks.pkl'), 'rb'))
KEBUN, SAWAH = H['(176, 208, 142)'], H['(206, 226, 150)']

def spline(pts, n=16, closed=False):
    P = list(pts)
    P = ([P[-1]] + P + [P[0], P[1]]) if closed else ([P[0]] + P + [P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = map(np.array, (P[i - 1], P[i], P[i + 1], P[i + 2]))
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)))
    if not closed: out.append(tuple(P[-2]))
    return out

class Frame:
    def __init__(self, o, deg): self.o = o; self.a = math.radians(deg)
    def p(self, u, v):
        c, s = math.cos(self.a), math.sin(self.a); return (self.o[0] + u * c - v * s, self.o[1] + u * s + v * c)
    def poly(self, pts): return Polygon([self.p(*q) for q in pts])
    def rect(self, u0, v0, u1, v1): return self.poly([(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
    def ell(self, u, v, ru, rv, n=48): return self.poly([(u + ru * math.cos(t), v + rv * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n, endpoint=False)])
    def line(self, pts): return LineString([self.p(*q) for q in pts])
    def curve(self, pts, n=12): return LineString([self.p(*q) for q in spline(pts, n)])
    def blob(self, pts, n=10): return Polygon([self.p(*q) for q in spline(pts, n, closed=True)])

def fillet_join(*gs, r=1.5):
    U = unary_union(gs)
    return U.buffer(r, join_style='round').buffer(-r, join_style='round').difference(U).buffer(0)

def trees_along(ring_line, step, skip, kinds, r=2.0, start=2.0):
    out = []; i = 0
    for d in np.arange(start, ring_line.length - 1, step):
        p = ring_line.interpolate(d)
        if skip.contains(p): continue
        out.append((p.x, p.y, r * (1.15 if kinds[i % len(kinds)] == 'trembesi' else 1.0), kinds[i % len(kinds)])); i += 1
    return out

def base_lot(region, seed, hapus, bld_buf=1.0):
    D = DJ.build()
    keep = [g for g in DJ.BLD if g.intersects(region.buffer(5)) and not any(g.equals(h) for h in hapus)]
    r = region.difference(D['row_all'].buffer(0.05)).difference(D['aspal_all'].buffer(0.05)).difference(DJ.ROADS.buffer(0.3))
    r = r.difference(KEBUN.buffer(0.05)).difference(SAWAH.buffer(0.05)).difference(unary_union(keep).buffer(bld_buf))
    c = [g for g in getattr(r, 'geoms', [r]) if g.contains(Point(*seed))][0]
    return Polygon(c.exterior).buffer(-0.2, join_style='mitre').buffer(0.2, join_style='mitre'), D

# ------------------------------------------------------------------ TAMAN A (tepi rel)
def taman_A():
    D0 = DJ.build()
    dihapus = [g for g in DJ.BLD if g.contains(Point(306077, 9156495))]
    hapus = D0['hapus_jalan'] + dihapus
    F = Frame((306084.0, 9156501.0), -5.0)
    region = F.poly([(-40, -22), (40, -22), (40, 18.0), (6.5, 18.0), (6.5, 16.6), (-40, 16.6)])
    lot, D = base_lot(region, (306084, 9156501), hapus, 1.0)
    g = {'batas': lot, 'dihapus': dihapus, 'frame': F}
    # pintu: barat (utama, dari Jl. Cendrawasih) & selatan (dari jalan lingkungan)
    pw = F.p(-24.5, 3.0); ps = F.p(9.0, -15.8)
    c2 = DJ.CL['CENDRAWASIH_B2']
    dW = c2.project(Point(pw)); q = c2.interpolate(dW)
    entW = LineString([q, Point(pw)]); entW = LineString([entW.interpolate(1.2), entW.interpolate(entW.length + 3.5)])
    southR = DJ.ROADS
    entS = LineString([ps, F.p(9.0, -11.5)])
    apronW = entW.buffer(1.5, cap_style='flat')
    cutA = F.line([(9.0, -11.0), (9.0, -40.0)]).intersection(DJ.ROADS)
    segA = [q for q in getattr(cutA, 'geoms', [cutA]) if q.length > 0]
    eA = min(segA, key=lambda q: q.distance(Point(F.p(9.0, -11.0))))
    pA = min([Point(eA.coords[0]), Point(eA.coords[-1])], key=lambda q: q.distance(Point(F.p(9.0, -11.0))))
    c_, s2 = math.cos(F.a), math.sin(F.a); vA = -(pA.x - F.o[0]) * s2 + (pA.y - F.o[1]) * c_
    apronS = F.rect(7.5, vA - 0.6, 10.5, -11.5)
    plazaW = F.ell(-20.5, 3.0, 4.2, 4.2).intersection(lot)
    # jalur utama (lengkung) barat -> plaza tengah -> selatan, & loop joging timur
    mainW = F.curve([(-21, 3.0), (-15, 4.5), (-8, 3.2), (-2.5, 0.5)]).buffer(1.25)
    plazaC = F.ell(-1.0, -0.5, 5.2, 5.2)
    mainS = F.curve([(1.5, -4.5), (5.5, -9.0), (9.0, -12.0)]).buffer(1.25)
    loop = F.curve([(3.8, 2.5), (9, 7.5), (17, 9.5), (23, 6), (24, -2), (20, -8.5), (12, -9.5), (6.5, -6.5)], n=14).buffer(0.9)
    jalur = unary_union([mainW, plazaC, mainS, loop, apronS.intersection(lot), plazaW]).intersection(lot.buffer(-0.6).union(apronS).union(plazaW))
    g['jalur'] = jalur.buffer(0)
    g['plaza'] = plazaC.difference(F.ell(-1.0, -0.5, 1.6, 1.6))
    g['plaza_pusat'] = F.ell(-1.0, -0.5, 1.6, 1.6)      # bedeng pohon tengah
    g['bermain'] = F.blob([(-17, 8.5), (-11, 12.5), (-4.5, 12.0), (-3.5, 8.0), (-8, 6.0), (-14, 6.2)]).intersection(lot.buffer(-1.8)).difference(jalur.buffer(0.4))
    g['lawn'] = F.blob([(6.5, 0.5), (10, 6.0), (17, 7.2), (21.5, 4.0), (21.5, -3.5), (17, -7.0), (10, -6.8), (6.5, -4.0)]).difference(jalur.buffer(0.3))
    g['gazebo'] = F.rect(-17.0, -9.5, -13.0, -5.5); g['gazebo_lantai'] = F.rect(-17.6, -10.1, -12.4, -4.9)
    g['setapak_gazebo'] = F.curve([(-12.4, -7.2), (-8.5, -5.0), (-4.8, -3.2)]).buffer(0.7)
    g['bunga'] = unary_union([F.ell(-9.0, -1.5, 2.6, 1.4), F.ell(4.5, 5.5, 1.6, 1.2), F.ell(13.5, -12.5, 2.0, 1.2), F.ell(-14.5, 0.0, 1.8, 1.1)]).intersection(lot.buffer(-1.0)).difference(jalur.buffer(0.3))
    edge = lot.difference(lot.buffer(-1.4))
    peredam = lot.intersection(LineString([F.p(-34, -20), F.p(-22, 18)]).buffer(6.0)).difference(lot.buffer(-2.6).difference(LineString([F.p(-34, -20), F.p(-22, 18)]).buffer(1.0)))
    gaps = unary_union([apronW.buffer(1.0), apronS.buffer(1.0), plazaW.buffer(0.6)])
    g['perdu_peredam'] = lot.difference(lot.buffer(-2.4)).intersection(F.rect(-40, -25, -20, 25)).difference(gaps).difference(jalur.buffer(0.3))
    g['perdu_tepi'] = edge.difference(g['perdu_peredam'].buffer(0.1)).difference(gaps).difference(jalur.buffer(0.3))
    ring = lot.buffer(-2.6).exterior
    skip = unary_union([gaps.buffer(1.5), jalur.buffer(1.4), g['bermain'].buffer(1.0), g['gazebo_lantai'].buffer(1.5)])
    pohon = trees_along(ring, 7.0, skip, ['trembesi', 'ketapang', 'tabebuya', 'ketapang'], r=2.1)
    pohon += [(*F.p(-1.0, -0.5), 1.6, 'tabebuya'), (*F.p(-24.5, 8.5), 2.0, 'tabebuya'), (*F.p(-24.0, -2.8), 2.0, 'tabebuya'),
              (*F.p(4.0, -12.5), 1.8, 'tabebuya'), (*F.p(14.0, -12.8), 1.8, 'tabebuya'), (*F.p(13.0, 1.0), 2.4, 'trembesi')]
    g['pohon'] = [t for t in pohon if lot.buffer(0.5).contains(Point(t[0], t[1]))]
    g['bangku'] = [(F.p(*q), a - 5) for q, a in [((-1.0, 5.4), 0), ((-6.4, -0.5), 90), ((-1.0, -6.4), 0), ((4.4, -0.5), 90),
                                                   ((16.0, 10.6), 0), ((25.4, 1.5), 90), ((-12.0, 6.3), 10)]]
    g['lampu'] = [F.p(*q) for q in [(-19, 6.2), (-11.0, 5.6), (-5.6, 3.8), (3.0, -6.5), (7.5, -10.2), (12.0, 9.8), (22.8, 6.4), (22.8, -6.0), (12.0, -10.4)]]
    g['tong_sampah'] = [F.p(*q) for q in [(-21.0, -1.0), (11.2, -14.0), (5.6, 5.0)]]
    g['main_alat'] = [(F.p(-13.0, 9.5), 'ayunan'), (F.p(-7.5, 9.8), 'perosotan'), (F.p(-10.0, 7.2), 'jungkat')]
    g['papan'] = [(F.p(-21.8, 6.6), -5), (F.p(11.6, -14.6), -5)]
    # gerbang: pilar di kiri-kanan pintu
    g['pilar'] = [F.rect(u - 0.35, v - 0.35, u + 0.35, v + 0.35) for u, v in [(-24.2, 5.8), (-24.8, 0.2), (6.4, -15.6), (11.6, -15.6)]]
    # akses ke jalan: pelat lintas saluran + fillet ke aspal/trotoar
    aspal = D['aspal_all']
    lintasW = apronW.difference(lot).difference(aspal).buffer(0)
    lintasS = apronS.difference(lot).difference(aspal).buffer(0)
    g['akses'] = unary_union([lintasW, lintasS])
    g['akses_fillet'] = unary_union([fillet_join(aspal.intersection(apronW.buffer(5)), lintasW, plazaW, r=1.5),
                                     fillet_join(aspal.intersection(apronS.buffer(5)), lintasS, g['jalur'].intersection(apronS.buffer(3)), r=1.5)]).difference(lot.buffer(-0.01).difference(g['jalur'])).buffer(0)
    g['pintu'] = [(F.p(-26.5, 3.0), F.p(-21.5, 3.0), 'MASUK / KELUAR'), (F.p(9.0, vA + 0.4), F.p(9.0, vA + 5.0), 'MASUK / KELUAR')]
    return g

# ------------------------------------------------------------------ TAMAN B (depan balai tempe)
def taman_B():
    D0 = DJ.build()
    F = Frame((306336.0, 9156484.0), -8.7)
    region = F.poly([(-30, -25), (40, -25), (40, 30), (-30, 30)])
    lot0, D = base_lot(region, (306336, 9156484), D0['hapus_jalan'], 0.6)
    # inti taman di barat deretan rumah + koridor timur (celah rumah) + plaza tenggara (depan simpang)
    core = F.poly([(-30, -30), (15.2, -30), (15.2, 30), (-30, 30)])
    koridor = F.rect(15.0, 4.0, 40, 6.8)
    se = F.rect(15.0, -40, 40, -11.4)
    lot = lot0.intersection(unary_union([core, koridor, se])).intersection(F.rect(-60, -60, 60, 19.5)).buffer(0)
    lot = max(getattr(lot, 'geoms', [lot]), key=lambda q: q.area)
    g = {'batas': lot, 'dihapus': [], 'frame': F}
    aw = D['AMPAS_WARAS']
    trot = aw['trotoar']
    # pintu timur (utama, menghadap balai): koridor lurus 2,4 m
    pathE = F.rect(4.0, 4.2, 40, 6.6).intersection(lot.union(trot.buffer(0.2)))
    # plaza tenggara (depan simpang Ampas Waras - jalan lingkungan)
    plazaSE = F.rect(8.0, -30, 40, -12.6).intersection(lot)
    # pintu selatan (dari jalan lingkungan) ke plaza tengah
    pathS = F.rect(-9.5, -30, -7.1, -9.0).intersection(lot)
    plaza = F.rect(-4.0, -12.6, 13.0, 9.5).intersection(lot)
    g['plaza'] = unary_union([plaza, plazaSE, pathE.intersection(lot)]).buffer(0)
    g['jalur'] = unary_union([pathS, F.curve([(-8.3, -9.2), (-6.5, -6.0), (-4.0, -4.5)]).buffer(1.2).intersection(lot),
                              F.curve([(-4.0, 6.0), (-9.0, 9.5), (-12.0, 10.5)]).buffer(0.8).intersection(lot)]).difference(g['plaza']).buffer(0)
    g['lawn'] = F.ell(-12.5, -1.5, 6.0, 6.8).intersection(lot.buffer(-1.6)).difference(g['jalur'].buffer(0.3))
    arc = [F.p(-12.5 + 7.0 * math.cos(t), -1.5 + 7.6 * math.sin(t)) for t in np.linspace(-1.05, 1.05, 30)]
    g['seat_wall'] = LineString(arc).buffer(0.25)
    g['bermain'] = F.blob([(-17, 11.5), (-11, 15.5), (-5.5, 15.0), (-5.0, 11.5), (-10, 9.8)]).intersection(lot.buffer(-1.6)).difference(g['jalur'].buffer(0.4))
    g['gazebo'] = F.rect(-17.5, -16.5, -13.5, -12.5); g['gazebo_lantai'] = F.rect(-18.1, -17.1, -12.9, -11.9)
    g['setapak_gazebo'] = F.curve([(-12.9, -14.0), (-10.5, -13.0), (-9.5, -12.0)]).buffer(0.6)
    g['bunga'] = unary_union([F.ell(19.5, -17.0, 2.0, 1.2), F.ell(-1.0, 12.0, 1.8, 1.1)]).intersection(lot.buffer(-0.8)).difference(g['jalur'].buffer(0.2))
    edge = lot.difference(lot.buffer(-1.2))
    gaps = unary_union([pathE.buffer(0.8), pathS.buffer(0.8), plazaSE.buffer(0.3)])
    g['perdu_tepi'] = edge.difference(gaps).difference(g['plaza'].buffer(0.2)).intersection(F.rect(-40, -40, 14.0, 40))
    g['perdu_peredam'] = Polygon()
    # pohon: 2 baris dalam grate di plaza + tepi barat/utara + aksen
    pohon = []
    for u in (0.5, 8.5):
        for v in (-9.5, -3.5, 2.5, 8.0):
            pohon.append((*F.p(u, v), 1.9, 'ketapang' if (v in (-9.5, 2.5)) else 'tabebuya'))
    for u, v in [(14.5, -15.5), (24.0, -15.0), (31.0, -14.5)]:
        pohon.append((*F.p(u, v), 1.8, 'tabebuya'))
    ring = lot.buffer(-2.2).exterior
    skip = unary_union([g['plaza'].buffer(0.8), gaps.buffer(1.0), g['jalur'].buffer(1.2), g['bermain'].buffer(0.8), g['gazebo_lantai'].buffer(1.2)])
    pohon += trees_along(ring, 6.5, skip, ['trembesi', 'ketapang', 'tabebuya'], r=2.0)
    g['pohon'] = [t for t in pohon if lot.buffer(0.3).contains(Point(t[0], t[1]))]
    g['grate'] = [(t[0], t[1]) for t in pohon[:8]]
    g['bangku'] = [(F.p(*q), a - 8.7) for q, a in [((4.5, -6.5), 90), ((4.5, 5.0), 90), ((12.2, -1.0), 90), ((20.0, -12.9), 0), ((-6.0, 12.5), 20)]]
    g['lampu'] = [F.p(*q) for q in [(-3.3, -11.8), (12.3, -11.8), (12.3, 8.8), (-3.3, 8.8), (20.0, 7.2), (28.0, -13.0), (-8.3, -14.0)]]
    g['tong_sampah'] = [F.p(*q) for q in [(14.0, 7.3), (26.0, -13.2), (-10.5, -17.0)]]
    g['main_alat'] = [(F.p(-14.0, 13.0), 'ayunan'), (F.p(-8.5, 13.0), 'perosotan')]
    g['parkir_sepeda'] = F.rect(21.0, -19.8, 27.5, -18.4).intersection(lot)
    g['papan'] = [(F.p(16.5, 7.3), -8.7), (F.p(-6.2, -16.0), -8.7), (F.p(30.0, -12.2), -8.7)]
    g['pilar'] = [F.rect(u - 0.35, v - 0.35, u + 0.35, v + 0.35) for u, v in [(15.6, 3.6), (15.6, 7.2), (-10.3, -17.6), (-6.3, -17.6)]]
    aspal = D['aspal_all']
    # sambungan ke trotoar & aspal (fillet)
    fil = [fillet_join(trot.intersection(pathE.buffer(4)), pathE, r=1.5),
           fillet_join(aspal.intersection(pathS.buffer(6)), pathS, r=1.5),
           fillet_join(aspal.intersection(plazaSE.buffer(6)), plazaSE, trot.intersection(plazaSE.buffer(6)), r=1.5)]
    cut = F.line([(-8.3, -15.0), (-8.3, -45.0)]).intersection(DJ.ROADS)
    segs = [q for q in getattr(cut, 'geoms', [cut]) if q.length > 0]
    edge = min(segs, key=lambda q: q.distance(Point(F.p(-8.3, -15.0))))
    p0 = Point(edge.coords[0]) if Point(edge.coords[0]).distance(Point(F.p(-8.3, -15))) < Point(edge.coords[-1]).distance(Point(F.p(-8.3, -15))) else Point(edge.coords[-1])
    c, s_ = math.cos(F.a), math.sin(F.a); dx, dy = p0.x - F.o[0], p0.y - F.o[1]; v_edge = -dx * s_ + dy * c
    lintasS = F.rect(-9.5, v_edge - 0.6, -7.1, -14.0).difference(lot).difference(aspal)
    g['akses'] = lintasS.buffer(0)
    g['akses_fillet'] = unary_union(fil).difference(lot.buffer(-0.01).difference(g['plaza']).difference(g['jalur'])).buffer(0)
    g['pintu'] = [(F.p(22.0, 5.4), F.p(14.5, 5.4), 'MASUK / KELUAR (dari balai)'), (F.p(-8.3, v_edge + 0.4), F.p(-8.3, v_edge + 5.0), 'MASUK / KELUAR'),
                  (F.p(33.0, -16.5), F.p(26.0, -16.5), 'MASUK / KELUAR')]
    return g

if __name__ == '__main__':
    a = taman_A(); b = taman_B()
    for n, t in (('A', a), ('B', b)):
        print(n, 'luas %.0f' % t['batas'].area, {k: round(v.area) for k, v in t.items() if hasattr(v, 'area') and not isinstance(v, (list, tuple))}, 'pohon', len(t['pohon']))
