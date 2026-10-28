"""Desain jalan permukiman Rev 28 Okt (b): jalan menyambung + fillet di setiap mulut simpang,
Jl. Ampas Waras (depan balai) ikut ditata, bangunan yang tertabrak ruang jalan dihapus.
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
BLD_ALL = [g.buffer(0) for g in _B.geometry]

def _drawn_filter(gs):
    """hanya bangunan yang benar-benar tergambar di site plan Rev 24 Okt (cek warna raster)."""
    cache = os.path.join(HERE, 'bld_drawn.pkl')
    if os.path.exists(cache): return pickle.load(open(cache, 'rb'))
    import sys; sys.path.insert(0, os.path.join(HERE, '..'))
    from PIL import Image; Image.MAX_IMAGE_PIXELS = None
    from geo2 import px
    im = np.asarray(Image.open(os.path.join(HERE, '..', 'img', 'r24full.png')).convert('RGB')).astype(int)
    out = []
    for g in gs:
        inner = g.buffer(-0.6)
        if inner.is_empty: inner = g
        minx, miny, maxx, maxy = inner.bounds; n = tot = 0
        for x in np.arange(minx, maxx, 0.8):
            for y in np.arange(miny, maxy, 0.8):
                if not inner.contains(Point(x, y)): continue
                X, Y = px(x, y); r, gg, b = im[int(Y), int(X)]; tot += 1
                neutral = abs(r - gg) < 12 and abs(gg - b) < 14
                if not neutral or r < 140: n += 1
        if tot and n / tot > 0.55: out.append(g)
    pickle.dump(out, open(cache, 'wb'))
    return out

BLD = _drawn_filter(BLD_ALL)

R_FILLET = 3.0
BANDS = {
    'BETET': [('aspal', -1.5, 2.5), ('trotoar', -3.0, -1.5), ('hijau', -3.5, -3.0), ('saluran', 2.5, 3.0), ('bahu', 3.0, 3.5),
              ('saluran_bawah', -2.0, -1.5)],
    'CENDRAWASIH_B1': [('aspal', -1.75, 2.25), ('trotoar', -3.25, -1.75), ('saluran', 2.25, 2.75), ('bahu', 2.75, 3.25),
                       ('saluran_bawah', -2.25, -1.75)],
    'CENDRAWASIH_B2': [('aspal', -2.75, 1.25), ('pedsep', 1.25, 2.75), ('pagar', 2.75, 3.25), ('saluran', -3.25, -2.75),
                       ('saluran_bawah', 1.25, 1.75)],
    'LETKOL': [('aspal', -1.35, 2.15), ('trotoar', -2.85, -1.35), ('saluran', 2.15, 2.55), ('bahu', 2.55, 2.85),
               ('saluran_bawah', -1.75, -1.35)],
    # arah gambar utara -> selatan: kiri = timur (balai), kanan = barat (Taman RT B)
    'AMPAS_WARAS': [('aspal', -1.75, 1.75), ('trotoar', -3.25, -1.75), ('saluran', 1.75, 2.15), ('bahu', 2.15, 2.45),
                    ('saluran_bawah', -2.25, -1.75)],
}
AS_ASPAL = {'BETET': 0.5, 'CENDRAWASIH_B1': 0.25, 'CENDRAWASIH_B2': -0.75, 'LETKOL': 0.4, 'AMPAS_WARAS': 0.0}
DUA_LAJUR = {'BETET': True, 'CENDRAWASIH_B1': True, 'CENDRAWASIH_B2': True, 'LETKOL': False, 'AMPAS_WARAS': False}

def side(line, d):
    if d == 0: return Polygon()
    return line.buffer(d, single_sided=True, cap_style='flat')

def band(line, a, b):
    a, b = min(a, b), max(a, b)
    if a >= 0: return side(line, b).difference(side(line, a)).buffer(0)
    if b <= 0: return side(line, a).difference(side(line, b)).buffer(0)
    return unary_union([side(line, b), side(line, a)]).buffer(0)

def offset_line(line, d):
    o = line.offset_curve(d)
    return o if o.geom_type == 'LineString' else max(o.geoms, key=lambda g: g.length)

def ext(line, e=2.5):
    """perpanjang ujung as agar menyatu ke jalan yang ditemui."""
    c = list(line.coords)
    def push(p, q):
        dx, dy = p[0] - q[0], p[1] - q[1]; L = (dx * dx + dy * dy) ** .5
        return (p[0] + dx / L * e, p[1] + dy / L * e)
    return LineString([push(c[0], c[1])] + c[1:-1] + [push(c[-1], c[-2])])

def row_of(nm):
    return min(a for _, a, _ in BANDS[nm]), max(b for _, _, b in BANDS[nm])

def build():
    L = {nm: ext(CL[nm]) for nm in CL}
    ROW = {nm: band(L[nm], *row_of(nm)) for nm in L}
    ROW_ALL = unary_union(list(ROW.values()))
    ASPAL = unary_union([band(L[nm], *[(a, b) for e, a, b in BANDS[nm] if e == 'aspal'][0]) for nm in L])
    # mulut jalan lain (termasuk A. Yani & jalan servis) yang memotong ruang jalan
    zone = ROW_ALL.buffer(4.0)
    mouths = ROADS.intersection(zone).difference(ASPAL.buffer(0.05))
    mouths = unary_union([g for g in getattr(mouths, 'geoms', [mouths]) if g.area > 1.5])
    paved = unary_union([ASPAL, mouths])
    filleted = paved.buffer(R_FILLET, join_style='round').buffer(-R_FILLET, join_style='round')
    filleted = filleted.intersection(ROW_ALL.buffer(3.0)).buffer(0)
    # aspal yang digambar = perkerasan berfillet di dalam ruang jalan + sampai 3 m ke mulut simpang
    out = {'aspal_all': filleted, 'row_all': ROW_ALL}
    # bangunan yang tertabrak ruang jalan rencana (di luar perkerasan berfillet juga dihitung)
    # aturan: rumah (< 450 m2) yang terpotong ruang jalan rencana > 2 m2 dihapus;
    # bangunan besar / singgungan kecil dipertahankan dan elemen jalan diputus di depannya.
    core = ROW_ALL.difference(mouths.difference(ASPAL.buffer(0.5)))
    hapus, tetap = [], []
    for g in BLD:
        ov = g.intersection(core).area
        if ov <= 0.05: continue
        (hapus if (ov > 5.0 and g.area < 450) else tetap).append(g)
    out['hapus_jalan'] = hapus
    KEEP = unary_union(tetap).buffer(0.15) if tetap else Polygon()
    filleted = filleted.difference(KEEP)
    out['aspal_all'] = filleted
    for nm, line in L.items():
        r = {'cl': CL[nm]}
        for el, a, b in BANDS[nm]:
            g = band(line, a, b)
            if el != 'aspal':
                g = g.difference(filleted.buffer(0.02))
            g = g.difference(KEEP)
            if el in ('saluran_bawah',):
                g = g.difference(filleted.buffer(0.02))
            r[el] = g.buffer(0)
        r['aspal'] = filleted.intersection(band(line, *row_of(nm)).buffer(3.0)).buffer(0)
        ss = mouths.buffer(1.0)
        if DUA_LAJUR[nm]:
            m = offset_line(CL[nm], AS_ASPAL[nm]); dashes = []; d = 6.0
            while d + 3 < m.length - 6:
                seg = substring(m, d, d + 3)
                if not seg.buffer(0.3).intersects(ss.buffer(3)): dashes.append(seg)
                d += 8
            r['marka'] = dashes
        trees, lamps = [], []
        if nm == 'BETET':
            tl = offset_line(CL[nm], -3.25)
            for d in np.arange(5, tl.length - 4, 9.0):
                p = tl.interpolate(d)
                if not p.buffer(1.2).intersects(filleted): trees.append(p)
            for d in np.arange(9.5, tl.length - 4, 36.0):
                p = tl.interpolate(d)
                if not p.buffer(0.5).intersects(filleted): lamps.append(p)
        else:
            off = {'CENDRAWASIH_B1': 3.0, 'CENDRAWASIH_B2': -3.0, 'LETKOL': 2.7, 'AMPAS_WARAS': 2.3}[nm]
            ll = offset_line(CL[nm], off)
            for d in np.arange(8, ll.length - 4, 30.0):
                p = ll.interpolate(d)
                if not p.buffer(0.5).intersects(filleted): lamps.append(p)
        if nm == 'CENDRAWASIH_B2':
            sl = offset_line(CL[nm], 3.0)
            r['perdu'] = [sl.interpolate(d) for d in np.arange(1.0, sl.length - 1, 1.6) if not sl.interpolate(d).buffer(0.6).intersects(filleted)]
            pl = offset_line(CL[nm], 2.0)
            r['sepeda'] = [(pl.interpolate(d), pl.interpolate(d + 1)) for d in np.arange(12, pl.length - 6, 35.0)]
        r['pohon'] = trees; r['pju'] = lamps; r['simpang'] = mouths
        out[nm] = r
    return out

def zebra(line, at_d, a, b, width=3.0, stripe=0.5):
    p = line.interpolate(at_d); q = line.interpolate(min(at_d + 1, line.length))
    tx, ty = q.x - p.x, q.y - p.y; L = (tx * tx + ty * ty) ** .5; tx, ty = tx / L, ty / L; nx, ny = -ty, tx
    strips = []; k = -width / 2
    while k + stripe <= width / 2 + 1e-6:
        c0, c1 = k, k + stripe
        strips.append(Polygon([(p.x + tx * c0 + nx * a, p.y + ty * c0 + ny * a), (p.x + tx * c1 + nx * a, p.y + ty * c1 + ny * a),
                               (p.x + tx * c1 + nx * b, p.y + ty * c1 + ny * b), (p.x + tx * c0 + nx * b, p.y + ty * c0 + ny * b)]))
        k += stripe * 2
    return strips

def zebras():
    z = {}
    b = CL['BETET']
    z['Betet - depan klaster tempe'] = zebra(b, b.project(Point(306205, 9156560)), -1.5, 2.5)
    z['Betet - simpang Ampas Waras'] = zebra(b, b.project(Point(306372, 9156542)), -1.5, 2.5)
    c2 = CL['CENDRAWASIH_B2']
    z['Cendrawasih - pintu Taman RT A'] = zebra(c2, c2.project(Point(306059.85, 9156506.12)), -2.75, 1.25)
    c1 = CL['CENDRAWASIH_B1']
    z['Cendrawasih - dekat simpang A. Yani'] = zebra(c1, 16.0, -1.75, 2.25)
    lk = CL['LETKOL']
    z['Letkol Sudarso - depan sekolah'] = zebra(lk, lk.project(Point(306960, 9156455)), -1.35, 2.15, width=4.0)
    aw = CL['AMPAS_WARAS']
    z['Ampas Waras - Taman RT B ke balai'] = zebra(aw, aw.project(Point(306372.58, 9156485.08)), -1.75, 1.75, width=2.8)
    return z

def zoss():
    lk = CL['LETKOL']
    d0 = lk.project(Point(306930, 9156458)); d1 = lk.project(Point(306995, 9156452))
    return band(substring(lk, d0, d1), -1.35, 2.15)

if __name__ == '__main__':
    D = build()
    print('bangunan dihapus (jalan):', len(D['hapus_jalan']), 'total luas %.0f m2' % sum(g.area for g in D['hapus_jalan']))
    for nm in CL:
        r = D[nm]; print(nm, {k: round(v.area) for k, v in r.items() if hasattr(v, 'area') and k not in ('cl',)})
