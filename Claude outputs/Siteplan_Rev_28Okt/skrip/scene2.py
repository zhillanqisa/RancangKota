"""Scene overlay Rev 28 Okt (b)."""
import math, os, sys
import numpy as np
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import unary_union
from shapely import affinity
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from scene import P, fill, polys, lobed, tree, shrubs, grid_lines, stipple, bench, lamp, bins, gazebo, play_icon, bubble, C, SP, TREE_LOG
import desain_jalan2 as DJ
import desain_taman2 as DT
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from geo2 import px

_IM = None
def base_color(g):
    H = DT.H
    for key in H:
        if H[key].buffer(0.5).contains(g.centroid): return tuple(int(v) for v in key.strip('()').split(','))
    return (224, 222, 217)

def _base_color_raster(g):
    global _IM
    if _IM is None: _IM = Image.open(os.path.join(HERE, '..', 'img', 'r24full.png')).convert('RGB')
    ring = g.buffer(3.5).difference(g.buffer(1.8)).difference(unary_union([b for b in DJ.BLD if b.intersects(g.buffer(5))]).buffer(1.6)).difference(DJ.ROADS.buffer(0.5))
    cols = []
    minx, miny, maxx, maxy = g.buffer(3.5).bounds
    for x in np.linspace(minx, maxx, 14):
        for y in np.linspace(miny, maxy, 14):
            if ring.contains(Point(x, y)):
                X, Y = px(x, y); cols.append(_IM.getpixel((int(X), int(Y))))
    if not cols: return (224, 222, 217)
    a = np.array(cols); return tuple(int(v) for v in np.median(a, axis=0))

def scene_hapus(gs, keep):
    out = []
    K = unary_union(keep).buffer(0.05) if keep else Polygon()
    for g in gs:
        cov = unary_union([g, affinity.translate(g, 1.15, -1.15)]).convex_hull.buffer(0.35).difference(K)
        out += fill(cov, base_color(g), 'D32_BANGUNAN_DIHAPUS_TUTUP', z=0)
        out.append(P('lines', 'D32_BANGUNAN_DIHAPUS', lines=[list(q.exterior.coords) for q in polys(g)], color=(200, 40, 40), lw=0.0, z=-1))
    return out

def arrow2(a, b, layer, color=(192, 40, 40), w=0.18, head=0.9):
    """panah dua arah (masuk/keluar)."""
    (ax, ay), (bx, by) = a, b; dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    out = [P('thick', layer, line=[(ax + ux * head, ay + uy * head), (bx - ux * head, by - uy * head)], color=color, w=w, z=30)]
    for (px_, py_), s in (((bx, by), 1), ((ax, ay), -1)):
        tip = (px_, py_); base = (px_ - s * ux * head, py_ - s * uy * head)
        out.append(P('poly', layer, poly=Polygon([tip, (base[0] + nx * head * 0.45, base[1] + ny * head * 0.45), (base[0] - nx * head * 0.45, base[1] - ny * head * 0.45)]),
                     fill=color, edge=None, lw=0, alpha=1, z=30))
    return out

def scene_jalan(D):
    out = []
    L = 'D32_JLN_'
    out += fill(D['aspal_all'], C['aspal'], L + 'ASPAL', edge=(80, 80, 78), lw=0.35, z=2)
    for nm in DJ.CL:
        r = D[nm]
        if 'trotoar' in r: out += fill(r['trotoar'], C['trotoar'], L + 'TROTOAR', edge=C['kanstin'], lw=0.4, z=3)
        if 'pedsep' in r: out += fill(r['pedsep'], C['pedsep'], L + 'JALUR_SEPEDA', edge=C['kanstin'], lw=0.4, z=3)
        if 'hijau' in r: out += fill(r['hijau'], C['hijau'], L + 'JALUR_HIJAU', edge=(90, 140, 70), lw=0.3, z=3)
        if 'pagar' in r: out += fill(r['pagar'], (120, 170, 96), L + 'PAGAR_HIJAU', z=3)
        out += fill(r['saluran'], C['saluran'], L + 'SALURAN_TERTUTUP', edge=(120, 120, 118), lw=0.3, z=3)
        if 'bahu' in r: out += fill(r['bahu'], C['bahu'], L + 'BAHU', z=3)
        for g in polys(r['saluran']) + polys(r['saluran_bawah']):
            out.append(P('dash', L + 'SALURAN_TERTUTUP', line=list(g.exterior.coords), color=(110, 110, 108), lw=0.25, dash=(0.8, 0.6), z=4))
        for seg in r.get('marka', []):
            out.append(P('thick', L + 'MARKA', line=list(seg.coords), color=C['marka'], w=0.12, z=5))
        for p in r['pohon']: out += tree(p.x, p.y, 1.7, 'ketapang', layer='D32_JLN_POHON', z=20)
        for p in r['pju']: out += lamp((p.x, p.y), 'D32_JLN_PJU')
        for p in r.get('perdu', []):
            out.append(P('poly', 'D32_JLN_PAGAR_HIJAU', poly=lobed(p.x, p.y, 0.45, n=6, amp=0.12, seg=30), fill=C['perdu'], edge=(60, 100, 50), lw=0.25, alpha=1, z=12))
        for a, b in r.get('sepeda', []):
            out.append(P('bike', 'D32_JLN_MARKA', a=(a.x, a.y), b=(b.x, b.y), color=(255, 255, 255), z=6))
    for nm, strips in DJ.zebras().items():
        for s in strips: out += fill(s, (255, 255, 255), 'D32_JLN_ZEBRA', edge=(150, 150, 150), lw=0.2, z=6)
    z = DJ.zoss()
    out += fill(z, C['zoss'], 'D32_JLN_ZOSS', alpha=0.85, z=4)
    lk = DJ.CL['LETKOL']; c = DJ.offset_line(lk, 0.4).interpolate(lk.project(Point(306978, 9156453)))
    out.append(P('text', 'D32_JLN_ZOSS', xy=(c.x, c.y), s='ZoSS', h=1.1, color=(255, 255, 255), rot=-4, ha='center', va='center', bold=True, z=7))
    return out

def scene_taman(t):
    out = []; L = 'D32_RT_'
    out += fill(t['batas'], C['taman_bg'], L + 'LATAR', edge=(46, 110, 30), lw=0.9, z=1)
    out += fill(t['akses'], C['jalur'], L + 'AKSES', edge=(150, 130, 100), lw=0.4, z=7)
    out += fill(t['akses_fillet'], C['jalur'], L + 'AKSES', z=7)
    if 'lawn' in t:
        out += fill(t['lawn'], C['lawn'], L + 'RUMPUT', edge=C['lawn_d'], lw=0.4, z=3); out += stipple(t['lawn'], L + 'RUMPUT')
    if 'plaza' in t and not t['plaza'].is_empty:
        out += fill(t['plaza'], C['plaza'], L + 'PLAZA', edge=(170, 150, 120), lw=0.4, z=4)
        out += grid_lines(t['plaza'], 1.2, math.degrees(t['frame'].a), L + 'PLAZA', (200, 184, 156))
    out += fill(t['jalur'], C['jalur'], L + 'JALUR', edge=(170, 150, 110), lw=0.4, z=5)
    if 'plaza_pusat' in t: out += fill(t['plaza_pusat'], C['lawn_d'], L + 'BUNGA', edge=(120, 100, 80), lw=0.4, z=6)
    if 'setapak_gazebo' in t: out += fill(t['setapak_gazebo'], C['jalur'], L + 'JALUR', edge=(170, 150, 110), lw=0.3, z=5)
    if 'seat_wall' in t: out += fill(t['seat_wall'], C['seat'], L + 'PERABOT', edge=(110, 110, 104), lw=0.4, z=8)
    out += fill(t['bermain'], C['bermain'], L + 'BERMAIN', edge=(170, 90, 50), lw=0.5, z=6)
    for xy, kind in t['main_alat']: out += play_icon(xy, kind, L + 'BERMAIN')
    out += fill(t['bunga'], C['bunga'], L + 'BUNGA', edge=(190, 100, 140), lw=0.3, z=7)
    out += shrubs(t['perdu_peredam'], L + 'PERDU', step=1.0, seed=2)
    out += shrubs(t['perdu_tepi'], L + 'PERDU', step=1.15, rmin=0.4, rmax=0.62, seed=5)
    out += gazebo(t['gazebo'], t['gazebo_lantai'], L + 'GAZEBO')
    for x, y in t.get('grate', []):
        out.append(P('poly', L + 'PERABOT', poly=affinity.rotate(box(x - 0.75, y - 0.75, x + 0.75, y + 0.75), math.degrees(t['frame'].a), origin=(x, y)),
                     fill=(170, 170, 164), edge=(100, 100, 96), lw=0.3, alpha=1, z=9))
    if 'parkir_sepeda' in t: out += fill(t['parkir_sepeda'], (190, 190, 186), L + 'PERABOT', edge=(90, 90, 90), lw=0.3, z=9)
    for pl in t['pilar']: out += fill(pl, (70, 70, 64), L + 'GERBANG', z=16)
    for xy, ang in t['papan']:
        out.append(P('poly', L + 'GERBANG', poly=affinity.rotate(box(xy[0] - 0.9, xy[1] - 0.18, xy[0] + 0.9, xy[1] + 0.18), ang, origin=xy), fill=(40, 90, 50), edge=(20, 40, 20), lw=0.3, alpha=1, z=16))
    for xy, ang in t['bangku']: out += bench(xy, ang, L + 'PERABOT')
    for xy in t['lampu']: out += lamp(xy, L + 'PERABOT')
    for xy in t['tong_sampah']: out += bins(xy, L + 'PERABOT')
    for x, y, r, j in t['pohon']: out += tree(x, y, r, j, layer='D32_RT_POHON')
    for a, b, lab in t['pintu']: out += arrow2(a, b, 'D32_RT_PINTU')
    return out

POTONG = {
    'A': ((306250.0, 9156571.0), (306246.0, 9156540.0)),
    'B1': ((306562.0, 9156342.0), (306557.0, 9156306.0)),
    'B2': ((306030.0, 9156484.0), (306064.0, 9156491.5)),
    'C': ((306962.0, 9156472.0), (306960.0, 9156436.0)),
    'D': ((306349.0, 9156472.0), (306393.0, 9156465.5)),
}

def scene_simbol(a, b):
    out = []
    for k, (p, q) in POTONG.items():
        out.append(P('dash', 'D32_POTONGAN', line=[p, q], color=C['potong'], lw=0.9, dash=(3.0, 1.2), z=42))
        for pt_, lab in ((p, k), (q, k + "'")):
            out.append(P('circle', 'D32_POTONGAN', c=pt_, r=2.6, fill=C['potong'], edge=(255, 255, 255), z=43, lw=0.4))
            out.append(P('text', 'D32_POTONGAN', xy=pt_, s=lab, h=2.0, color=(255, 255, 255), rot=0, ha='center', va='center', bold=True, z=44))
    return out

def free_spot(want, obst, taken, r=2.6, maxd=16.0):
    from shapely.geometry import Point as _P
    best = None
    for d in np.arange(0, maxd, 0.8):
        for ang in np.linspace(0, 2 * math.pi, max(8, int(d * 3)), endpoint=False):
            q = _P(want[0] + d * math.cos(ang), want[1] + d * math.sin(ang))
            c = q.buffer(r)
            if c.intersects(obst) or any(c.intersects(t.buffer(r)) for t in taken): continue
            return (q.x, q.y)
    return want

def scene_bubbles(D, a, b, keep, covers):
    import json
    out = []
    design = unary_union([D['row_all'], D['aspal_all'], a['batas'], b['batas']])
    overlay = unary_union([design, covers])
    obst = unary_union([design] + keep)
    base = json.load(open(os.path.join(HERE, 'base_bubbles.json')))
    taken = [Point(x, y) for t, x, y, h in base]
    jalan_label = {'27', '28', '29', '32', '26', '31'}
    R = 2.6
    for t, x, y, hgt in base:
        c = Point(x, y).buffer(2.7)
        if not c.intersects(overlay): continue
        if t in jalan_label or not c.intersects(design):
            out += bubble((x, y), t, 'D32_NOMOR', r=R, h=2.1); continue
        out.append(P('circle', 'D32_NOMOR_TUTUP', c=(x - 0.6, y + 0.3), r=3.6, fill=base_color(c), edge=None, z=-2))
        q = (306393.0, 9156471.0) if t == '17' else free_spot((x, y), obst, [p for p in taken if not (abs(p.x - x) < 0.01 and abs(p.y - y) < 0.01)], r=R + 0.3)
        taken.append(Point(q)); out += bubble(q, t, 'D32_NOMOR', r=R, h=2.1)
    for want in [a['frame'].p(15.0, 2.0), b['frame'].p(-12.5, 4.5)]:
        out += bubble(want, '34', 'D32_NOMOR', r=R, h=2.1)
    for want in [(306290.0, 9156528.0), (306470.0, 9156336.0), (306086.0, 9156430.0), (307015.0, 9156430.0), (306392.0, 9156398.0)]:
        q = free_spot(want, obst, taken, r=R + 0.6); taken.append(Point(q)); out += bubble(q, '35', 'D32_NOMOR', r=R, h=2.1)
    return out

def _delineasi():
    out = []
    import geopandas as gpd
    dl = gpd.read_file('/home/user/RancangKota/Delineasi Tapak D3.2 Baru/Delineasi Tapak D3.2 Baru.shp').to_crs(32749).geometry.iloc[0]
    out.append(P('lines', 'D32_DELINEASI_ATAS', lines=[list(dl.exterior.coords)], color=(200, 0, 200), lw=1.0, z=39))
    return out

def build_all():
    TREE_LOG.clear()
    D = DJ.build()
    a = DT.taman_A(); b = DT.taman_B()
    hapus = D['hapus_jalan'] + a['dihapus']
    keep = [g for g in DJ.BLD if not any(g.equals(h) for h in hapus)]
    S = scene_hapus(hapus, [k for k in keep if any(k.intersects(h.buffer(3)) for h in hapus)])
    covers = unary_union([p['poly'] for p in S if p['k'] == 'poly'])
    S += scene_jalan(D) + scene_taman(a) + scene_taman(b) + scene_simbol(a, b) + scene_bubbles(D, a, b, keep, covers) + _delineasi()
    return S, D, a, b, hapus

if __name__ == '__main__':
    S, D, a, b, h = build_all()
    from collections import Counter
    print(len(S), Counter(p['k'] for p in S), 'hapus', len(h))
