"""Desain denah jalan permukiman (UTM 49S) sesuai penampang rencana Rev 28 Okt.
Offset positif = kiri arah gambar as jalan."""
import json, pickle, os
import numpy as np
from shapely.geometry import LineString, Point, Polygon, MultiPolygon, box
from shapely.ops import unary_union, substring
import pyogrio

HERE = os.path.dirname(os.path.abspath(__file__))
CL = {k: LineString(v) for k, v in json.load(open(os.path.join(HERE, 'ruas_cl.json'))).items()}
ROADS = pickle.load(open(os.path.join(HERE, 'roads_union.pkl'), 'rb'))
_B = pyogrio.read_dataframe('/home/user/RancangKota/GIS_Stuff/Rancang_Kota/Rancang_Kota.gdb', layer='Building_Clip').to_crs(32749)
BUILD = unary_union([g.buffer(0) for g in _B.geometry])

# (nama elemen, offset1, offset2)  -- offset dalam meter dari as eksisting
BANDS = {
    'BETET': [('aspal', -1.5, 2.5), ('trotoar', -3.0, -1.5), ('hijau', -3.5, -3.0), ('saluran', 2.5, 3.0), ('bahu', 3.0, 3.5),
              ('saluran_bawah', -2.0, -1.5)],
    'CENDRAWASIH_B1': [('aspal', -1.75, 2.25), ('trotoar', -3.25, -1.75), ('saluran', 2.25, 2.75), ('bahu', 2.75, 3.25),
                       ('saluran_bawah', -2.25, -1.75)],
    'CENDRAWASIH_B2': [('aspal', -2.75, 1.25), ('pedsep', 1.25, 2.75), ('pagar', 2.75, 3.25), ('saluran', -3.25, -2.75),
                       ('saluran_bawah', 1.25, 1.75)],
    'LETKOL': [('aspal', -1.35, 2.15), ('trotoar', -2.85, -1.35), ('saluran', 2.15, 2.55), ('bahu', 2.55, 2.85),
               ('saluran_bawah', -1.75, -1.35)],
}
AS_ASPAL = {'BETET': 0.5, 'CENDRAWASIH_B1': 0.25, 'CENDRAWASIH_B2': -0.75, 'LETKOL': 0.4}
DUA_LAJUR = {'BETET': True, 'CENDRAWASIH_B1': True, 'CENDRAWASIH_B2': True, 'LETKOL': False}

def side(line, d):
    if d == 0: return Polygon()
    return line.buffer(abs(d), single_sided=True, cap_style='flat') if d > 0 else line.buffer(-abs(d), single_sided=True, cap_style='flat')

def band(line, a, b):
    a, b = min(a, b), max(a, b)
    if a >= 0: return side(line, b).difference(side(line, a)).buffer(0)
    if b <= 0: return side(line, a).difference(side(line, b)).buffer(0)
    return unary_union([side(line, b), side(line, a)]).buffer(0)

def offset_line(line, d):
    o = line.offset_curve(d)
    return o if o.geom_type == 'LineString' else max(o.geoms, key=lambda g: g.length)

def side_streets(name):
    """mulut jalan lain yang memotong ruas ini (untuk celah trotoar & penyeberangan)."""
    own = CL[name].buffer(4.5, cap_style='flat')
    others = ROADS.difference(own)
    zone = CL[name].buffer(9, cap_style='flat')
    parts = [g for g in getattr(others.intersection(zone), 'geoms', [others.intersection(zone)]) if g.area > 3]
    return unary_union(parts) if parts else Polygon()

def build():
    out = {}
    for nm, line in CL.items():
        ss = side_streets(nm).buffer(1.2)
        res = {'cl': line}
        for el, a, b in BANDS[nm]:
            g = band(line, a, b)
            if el in ('trotoar', 'hijau', 'pedsep', 'pagar'):
                g = g.difference(ss)
            if el not in ('aspal',):
                g = g.difference(BUILD)
            res[el] = g
        # marka as
        if DUA_LAJUR[nm]:
            m = offset_line(line, AS_ASPAL[nm])
            dashes = []
            L = m.length; d = 6.0
            while d + 3 < L - 6:
                seg = substring(m, d, d + 3)
                if not seg.buffer(0.2).intersects(ss.buffer(4)):
                    dashes.append(seg)
                d += 8
            res['marka'] = dashes
        # pohon & PJU
        trees, lamps = [], []
        if nm == 'BETET':
            tl = offset_line(line, -3.25)
            for d in np.arange(5, tl.length - 4, 9.0):
                p = tl.interpolate(d)
                if not p.buffer(1.0).intersects(ss) and not p.buffer(0.8).intersects(BUILD):
                    trees.append(p)
            for d in np.arange(9.5, tl.length - 4, 36.0):
                p = tl.interpolate(d)
                if not p.buffer(0.5).intersects(ss): lamps.append(p)
        else:
            off = {'CENDRAWASIH_B1': 3.0, 'CENDRAWASIH_B2': -3.0, 'LETKOL': 2.7}[nm]
            ll = offset_line(line, off)
            for d in np.arange(8, ll.length - 4, 30.0):
                p = ll.interpolate(d)
                if not p.buffer(0.5).intersects(ss) and not p.buffer(0.3).intersects(BUILD): lamps.append(p)
        if nm == 'CENDRAWASIH_B2':
            sl = offset_line(line, 3.0)
            res['perdu'] = [sl.interpolate(d) for d in np.arange(1.0, sl.length - 1, 1.6)
                            if not sl.interpolate(d).buffer(0.6).intersects(ss)]
            # simbol sepeda tiap 35 m
            pl = offset_line(line, 2.0)
            res['sepeda'] = [(pl.interpolate(d), pl.interpolate(d + 1)) for d in np.arange(12, pl.length - 6, 35.0)]
        res['pohon'] = trees; res['pju'] = lamps
        res['simpang'] = ss
        out[nm] = res
    return out

def zebra(line, at_d, aspal_a, aspal_b, width=3.0, stripe=0.5):
    """zebra cross melintang badan jalan pada jarak at_d dari awal as."""
    p = line.interpolate(at_d); q = line.interpolate(min(at_d + 1, line.length))
    tx, ty = q.x - p.x, q.y - p.y; L = (tx * tx + ty * ty) ** .5; tx, ty = tx / L, ty / L; nx, ny = -ty, tx
    strips = []
    k = -width / 2
    while k + stripe <= width / 2 + 1e-6:
        c0, c1 = k, k + stripe
        strips.append(Polygon([(p.x + tx * c0 + nx * aspal_a, p.y + ty * c0 + ny * aspal_a), (p.x + tx * c1 + nx * aspal_a, p.y + ty * c1 + ny * aspal_a),
                               (p.x + tx * c1 + nx * aspal_b, p.y + ty * c1 + ny * aspal_b), (p.x + tx * c0 + nx * aspal_b, p.y + ty * c0 + ny * aspal_b)]))
        k += stripe * 2
    return strips

def zebras():
    """lokasi penyeberangan (sesuai respon penampang)."""
    z = {}
    b = CL['BETET']
    z['Betet - depan klaster tempe'] = zebra(b, b.project(Point(306205, 9156560)), -1.5, 2.5)
    z['Betet - simpang Jl. Ampas Waras (ke balai & Taman RT B)'] = zebra(b, b.project(Point(306395, 9156542)), -1.5, 2.5)
    c2 = CL['CENDRAWASIH_B2']
    z['Cendrawasih - pintu Taman RT A'] = zebra(c2, c2.project(Point(306057.5, 9156510.5)), -2.75, 1.25)
    c1 = CL['CENDRAWASIH_B1']
    z['Cendrawasih - dekat simpang A. Yani'] = zebra(c1, 16.0, -1.75, 2.25)
    lk = CL['LETKOL']
    z['Letkol Sudarso - depan sekolah (ditinggikan)'] = zebra(lk, lk.project(Point(306960, 9156455)), -1.35, 2.15, width=4.0)
    return z

def zoss():
    lk = CL['LETKOL']
    d0 = lk.project(Point(306930, 9156458)); d1 = lk.project(Point(306995, 9156452))
    seg = substring(lk, d0, d1)
    return band(seg, -1.35, 2.15)

if __name__ == '__main__':
    D = build()
    for nm, r in D.items():
        print(nm, 'aspal %.0f m2' % r['aspal'].area, 'trotoar %.0f' % r.get('trotoar', Polygon()).area,
              'pedsep %.0f' % r.get('pedsep', Polygon()).area, 'pohon', len(r['pohon']), 'pju', len(r['pju']))
        # konflik bangunan pada lebar rencana
        full = band(r['cl'], min(a for _, a, _ in BANDS[nm]), max(b for _, _, b in BANDS[nm]))
        conf = full.intersection(BUILD).area
        print('   overlap bangunan dalam ruang milik jalan rencana: %.1f m2' % conf)
    print({k: len(v) for k, v in zebras().items()}, 'zoss %.0f m2' % zoss().area)
