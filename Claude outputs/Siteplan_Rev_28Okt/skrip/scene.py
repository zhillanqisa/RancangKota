"""Primitif gambar overlay Rev 28 Okt (UTM 49S) dipakai bersama oleh pratinjau (matplotlib)
dan penulis DXF. Setiap primitif: dict(k=..., layer=..., ...)."""
import math, random
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, LineString, Point, box
from shapely.ops import unary_union
from shapely import affinity
import desain_jalan as DJ
import desain_taman as DT

C = dict(aspal=(122, 124, 120), trotoar=(222, 206, 172), hijau=(140, 190, 104), saluran=(196, 198, 194), bahu=(206, 206, 200),
         pedsep=(196, 214, 150), marka=(255, 255, 255), zoss=(196, 58, 46), kanstin=(110, 104, 92),
         lawn=(184, 218, 140), lawn_d=(150, 192, 108), jalur=(226, 210, 176), bermain=(232, 148, 98), plaza=(232, 220, 196),
         gazebo=(140, 92, 60), gazebo_l=(216, 198, 162), bunga=(236, 150, 186), perdu=(86, 140, 70), perdu2=(112, 166, 86),
         taman_bg=(198, 226, 160), seat=(176, 176, 170), shadow=(60, 60, 60), garis=(60, 60, 50), potong=(192, 40, 40))
SP = {'trembesi': ((70, 128, 58), (112, 170, 84)), 'ketapang': ((92, 152, 70), (146, 196, 104)), 'tabebuya': ((214, 120, 168), (240, 176, 206))}

def P(k, layer, **kw):
    d = dict(k=k, layer=layer); d.update(kw); return d

def polys(g):
    if g is None or g.is_empty: return []
    if isinstance(g, Polygon): return [g]
    return [p for p in getattr(g, 'geoms', []) if isinstance(p, Polygon) and not p.is_empty]

def fill(g, col, layer, edge=None, lw=0.0, alpha=1.0, z=1):
    return [P('poly', layer, poly=p, fill=col, edge=edge, lw=lw, alpha=alpha, z=z) for p in polys(g) if p.area > 0.05]

def lobed(cx, cy, r, n=9, amp=0.09, rot=0.0, seg=72):
    pts = []
    for i in range(seg):
        t = 2 * math.pi * i / seg
        rr = r * (1 + amp * math.sin(n * t + rot))
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    return Polygon(pts)

TREE_LOG = []
def tree(x, y, r, jenis, layer='D32_RT_POHON', z=20):
    TREE_LOG.append((x, y, r, jenis, layer))
    dk, lt = SP[jenis]
    out = []
    out.append(P('poly', layer + '_BAYANGAN', poly=lobed(x + 0.35 * r, y - 0.35 * r, r * 0.98, rot=0.4), fill=C['shadow'], edge=None, lw=0, alpha=0.28, z=z))
    out.append(P('poly', layer, poly=lobed(x, y, r, rot=hash((round(x), round(y))) % 7), fill=dk, edge=tuple(int(v * 0.7) for v in dk), lw=0.5, alpha=1, z=z + 1))
    out.append(P('poly', layer, poly=lobed(x - 0.22 * r, y + 0.22 * r, r * 0.62, n=7, amp=0.12, rot=1.3), fill=lt, edge=None, lw=0, alpha=0.75, z=z + 2))
    br = []
    for i in range(6):
        a = 2 * math.pi * i / 6 + 0.3
        br.append([(x, y), (x + 0.62 * r * math.cos(a), y + 0.62 * r * math.sin(a))])
    out.append(P('lines', layer, lines=br, color=tuple(int(v * 0.55) for v in dk), lw=0.35, z=z + 3))
    out.append(P('circle', layer, c=(x, y), r=max(0.12, 0.07 * r), fill=(92, 64, 40), z=z + 4))
    return out

def shrubs(g, layer, step=1.1, rmin=0.45, rmax=0.75, seed=1):
    rnd = random.Random(seed); out = []
    for p in polys(g):
        minx, miny, maxx, maxy = p.bounds
        y = miny + step / 2
        row = 0
        while y < maxy:
            x = minx + step / 2 + (step / 2 if row % 2 else 0)
            while x < maxx:
                q = Point(x + rnd.uniform(-0.2, 0.2), y + rnd.uniform(-0.2, 0.2))
                if p.buffer(-0.25).contains(q):
                    r = rnd.uniform(rmin, rmax)
                    col = C['perdu'] if rnd.random() < 0.6 else C['perdu2']
                    out.append(P('poly', layer, poly=lobed(q.x, q.y, r, n=6, amp=0.12, rot=rnd.random() * 6, seg=36), fill=col,
                                 edge=(60, 100, 50), lw=0.3, alpha=1, z=12))
                x += step
            y += step * 0.87; row += 1
    return out

def grid_lines(g, spacing, angle_deg, layer, color, lw=0.25, z=6):
    out = []
    for p in polys(g):
        c = p.centroid; R = max(p.bounds[2] - p.bounds[0], p.bounds[3] - p.bounds[1])
        lines = []
        for ang in (angle_deg, angle_deg + 90):
            a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
            k = -R
            while k <= R:
                L = LineString([(c.x + nx * k - dx * R, c.y + ny * k - dy * R), (c.x + nx * k + dx * R, c.y + ny * k + dy * R)]).intersection(p)
                for seg in getattr(L, 'geoms', [L]):
                    if seg.geom_type == 'LineString' and seg.length > 0.1: lines.append(list(seg.coords))
                k += spacing
        out.append(P('lines', layer, lines=lines, color=color, lw=lw, z=z))
    return out

def stipple(g, layer, dens=0.6, seed=3, color=(120, 168, 90)):
    rnd = random.Random(seed); pts = []
    for p in polys(g):
        n = int(p.area * dens)
        minx, miny, maxx, maxy = p.bounds
        while n > 0:
            q = Point(rnd.uniform(minx, maxx), rnd.uniform(miny, maxy))
            if p.contains(q): pts.append((q.x, q.y)); n -= 1
    return [P('dots', layer, pts=pts, color=color, r=0.06, z=4)]

def bench(xy, ang, layer):
    x, y = xy; b = affinity.rotate(box(x - 0.9, y - 0.25, x + 0.9, y + 0.25), ang, origin=(x, y))
    return [P('poly', layer, poly=b, fill=(150, 104, 66), edge=(80, 54, 34), lw=0.4, alpha=1, z=15)]

def lamp(xy, layer):
    x, y = xy
    return [P('circle', layer, c=(x, y), r=0.35, fill=(250, 220, 90), edge=(60, 60, 60), z=16),
            P('lines', layer, lines=[[(x - 0.35, y), (x + 0.35, y)], [(x, y - 0.35), (x, y + 0.35)]], color=(60, 60, 60), lw=0.3, z=17)]

def bins(xy, layer):
    x, y = xy; out = []
    for i, col in enumerate([(70, 150, 70), (230, 190, 40), (130, 130, 130)]):
        out.append(P('circle', layer, c=(x - 0.45 + i * 0.45, y), r=0.2, fill=col, edge=(40, 40, 40), z=16))
    return out

def gazebo(g, lantai, layer):
    out = fill(lantai, C['gazebo_l'], layer, edge=(120, 100, 70), lw=0.4, z=13)
    out += fill(g, C['gazebo'], layer, edge=(70, 44, 28), lw=0.6, z=14)
    (x0, y0, x1, y1) = g.bounds; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    out.append(P('lines', layer, lines=[[(x0, y0), (cx, cy)], [(x1, y0), (cx, cy)], [(x1, y1), (cx, cy)], [(x0, y1), (cx, cy)]], color=(70, 44, 28), lw=0.5, z=15))
    return out

def play_icon(xy, kind, layer):
    x, y = xy; col = (60, 60, 70)
    if kind == 'ayunan':
        L = [[(x - 1.2, y - 0.6), (x + 1.2, y - 0.6)], [(x - 1.2, y + 0.6), (x + 1.2, y + 0.6)], [(x - 1.2, y - 0.6), (x - 1.2, y + 0.6)], [(x + 1.2, y - 0.6), (x + 1.2, y + 0.6)],
             [(x - 0.5, y - 0.2), (x - 0.5, y + 0.2)], [(x + 0.5, y - 0.2), (x + 0.5, y + 0.2)]]
    elif kind == 'perosotan':
        L = [[(x - 0.4, y - 1.2), (x + 0.4, y - 1.2)], [(x - 0.4, y - 1.2), (x - 0.4, y + 1.2)], [(x + 0.4, y - 1.2), (x + 0.4, y + 1.2)], [(x - 0.4, y + 1.2), (x + 0.4, y + 1.2)],
             [(x - 0.4, y + 0.4), (x + 0.4, y + 0.4)]]
    else:
        L = [[(x - 1.0, y), (x + 1.0, y)]]
    out = [P('lines', layer, lines=L, color=col, lw=0.6, z=16)]
    if kind == 'jungkat':
        out += [P('circle', layer, c=(x - 1.0, y), r=0.2, fill=(240, 200, 60), edge=col, z=17), P('circle', layer, c=(x + 1.0, y), r=0.2, fill=(240, 200, 60), edge=col, z=17)]
    return out

# ============================================================== JALAN
def scene_jalan():
    D = DJ.build(); out = []
    for nm, r in D.items():
        L = 'D32_JLN_'
        out += fill(r['aspal'].difference(DJ.BUILD.buffer(0.15)), C['aspal'], L + 'ASPAL', edge=(80, 80, 78), lw=0.35, z=2)
        if 'trotoar' in r: out += fill(r['trotoar'], C['trotoar'], L + 'TROTOAR', edge=C['kanstin'], lw=0.4, z=3)
        if 'pedsep' in r: out += fill(r['pedsep'], C['pedsep'], L + 'JALUR_SEPEDA', edge=C['kanstin'], lw=0.4, z=3)
        if 'hijau' in r: out += fill(r['hijau'], C['hijau'], L + 'JALUR_HIJAU', edge=(90, 140, 70), lw=0.3, z=3)
        if 'pagar' in r: out += fill(r['pagar'], (120, 170, 96), L + 'PAGAR_HIJAU', z=3)
        out += fill(r['saluran'], C['saluran'], L + 'SALURAN_TERTUTUP', edge=(120, 120, 118), lw=0.3, z=3)
        if 'bahu' in r: out += fill(r['bahu'], C['bahu'], L + 'BAHU', z=3)
        # garis saluran (grill) putus-putus
        for g in polys(r['saluran']) + polys(r['saluran_bawah']):
            out.append(P('dash', L + 'SALURAN_TERTUTUP', line=list(g.exterior.coords), color=(110, 110, 108), lw=0.25, dash=(0.8, 0.6), z=4))
        for seg in r.get('marka', []):
            out.append(P('thick', L + 'MARKA', line=list(seg.coords), color=C['marka'], w=0.12, z=5))
        for p in r['pohon']:
            out += tree(p.x, p.y, 1.7, 'ketapang', layer='D32_JLN_POHON', z=20)
        for p in r['pju']:
            out += lamp((p.x, p.y), 'D32_JLN_PJU')
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
    return out, D

# ============================================================== TAMAN
def scene_taman():
    out = []
    a = DT.taman_A(); L = 'D32_RT_'
    out += fill(a['batas'].difference(a['rumah'].buffer(0.3)), C['taman_bg'], L + 'LATAR', edge=(46, 110, 30), lw=0.9, z=1)
    out += fill(a['lawn'], C['lawn'], L + 'RUMPUT', edge=C['lawn_d'], lw=0.4, z=3)
    out += stipple(a['lawn'], L + 'RUMPUT')
    out += fill(a['jalur'], C['jalur'], L + 'JALUR', edge=(170, 150, 110), lw=0.4, z=5)
    out += fill(a['bermain'], C['bermain'], L + 'BERMAIN', edge=(170, 90, 50), lw=0.5, z=6)
    for xy, kind in a['main_alat']: out += play_icon(xy, kind, L + 'BERMAIN')
    out += fill(a['bunga'], C['bunga'], L + 'BUNGA', edge=(190, 100, 140), lw=0.3, z=7)
    out += shrubs(a['perdu_peredam'], L + 'PERDU', step=1.0, seed=2)
    out += shrubs(a['perdu_tepi'], L + 'PERDU', step=1.2, rmin=0.4, rmax=0.6, seed=5)
    out += gazebo(a['gazebo'], a['gazebo_lantai'], L + 'GAZEBO')
    for xy, ang in a['bangku']: out += bench(xy, ang, L + 'PERABOT')
    for xy in a['lampu']: out += lamp(xy, L + 'PERABOT')
    for xy in a['tong_sampah']: out += bins(xy, L + 'PERABOT')
    for x, y, r, j in a['pohon']: out += tree(x, y, r * 1.25, j, layer='D32_RT_POHON')
    b = DT.taman_B()
    out += fill(b['batas'].difference(b['rumah'].buffer(0.3)), C['taman_bg'], L + 'LATAR', edge=(46, 110, 30), lw=0.9, z=1)
    out += fill(b['plaza'], C['plaza'], L + 'PLAZA', edge=(170, 150, 120), lw=0.4, z=3)
    out += grid_lines(b['plaza'], 1.2, 7.0, L + 'PLAZA', (200, 184, 156))
    out += fill(b['lawn'], C['lawn'], L + 'RUMPUT', edge=C['lawn_d'], lw=0.5, z=3)
    out += stipple(b['lawn'], L + 'RUMPUT', seed=9)
    out += fill(b['setapak'], C['jalur'], L + 'JALUR', edge=(170, 150, 110), lw=0.3, z=5)
    out += fill(b['seat_wall'], C['seat'], L + 'PERABOT', edge=(110, 110, 104), lw=0.4, z=8)
    out += fill(b['bermain'], C['bermain'], L + 'BERMAIN', edge=(170, 90, 50), lw=0.5, z=6)
    for xy, kind in b['main_alat']: out += play_icon(xy, kind, L + 'BERMAIN')
    out += shrubs(b['perdu_tepi'], L + 'PERDU', step=1.1, rmin=0.4, rmax=0.6, seed=7)
    out += gazebo(b['gazebo'], b['gazebo_lantai'], L + 'GAZEBO')
    for x, y in b['grate']:
        out.append(P('poly', L + 'PERABOT', poly=box(x - 0.75, y - 0.75, x + 0.75, y + 0.75), fill=(170, 170, 164), edge=(100, 100, 96), lw=0.3, alpha=1, z=9))
    out += fill(b['parkir_sepeda'], (190, 190, 186), L + 'PERABOT', edge=(90, 90, 90), lw=0.3, z=9)
    for zb in b['zebra']: out += fill(zb, (255, 255, 255), L + 'ZEBRA', edge=(140, 140, 140), lw=0.2, z=9)
    for xy, ang in b['bangku']: out += bench(xy, ang, L + 'PERABOT')
    for xy in b['lampu']: out += lamp(xy, L + 'PERABOT')
    for xy in b['tong_sampah']: out += bins(xy, L + 'PERABOT')
    for x, y, r, j in b['pohon']: out += tree(x, y, r * 1.15, j, layer='D32_RT_POHON')
    return out, a, b

# ============================================================== simbol: potongan & nomor
def bubble(xy, s, layer, r=2.2, h=1.9):
    x, y = xy
    return [P('circle', layer, c=(x, y), r=r, fill=(255, 255, 255), edge=(0, 0, 0), z=40, lw=0.5),
            P('text', layer, xy=(x, y), s=s, h=h, color=(0, 0, 0), rot=0, ha='center', va='center', bold=False, z=41)]

POTONG = {   # (a, b) ujung garis potong; label
    'A': ((306250.0, 9156571.0), (306246.0, 9156540.0)),
    'B1': ((306562.0, 9156342.0), (306557.0, 9156306.0)),
    'B2': ((306034.0, 9156494.0), (306074.0, 9156503.0)),
    'C': ((306962.0, 9156472.0), (306960.0, 9156436.0)),
}

def scene_simbol():
    out = []
    for k, (a, b) in POTONG.items():
        out.append(P('dash', 'D32_POTONGAN', line=[a, b], color=C['potong'], lw=0.9, dash=(3.0, 1.2), z=42))
        for p, lab in ((a, k), (b, k + "'")):
            out.append(P('circle', 'D32_POTONGAN', c=p, r=2.6, fill=C['potong'], edge=(255, 255, 255), z=43, lw=0.4))
            out.append(P('text', 'D32_POTONGAN', xy=p, s=lab, h=2.0, color=(255, 255, 255), rot=0, ha='center', va='center', bold=True, z=44))
    out += bubble((306086.0, 9156497.0), '34', 'D32_NOMOR')
    out += bubble((306344.0, 9156480.0), '34', 'D32_NOMOR')
    for xy in [(306290.0, 9156537.0), (306470.0, 9156328.0), (306086.0, 9156430.0), (307015.0, 9156437.0)]:
        out += bubble(xy, '35', 'D32_NOMOR')
    # nomor 17 eksisting (balai) digambar ulang di atas zebra
    out.append(P('circle', 'D32_JLN_ASPAL', c=(306371.9, 9156489.1), r=2.5, fill=(168, 168, 166), edge=None, z=8))
    out += bubble((306373.5, 9156497.5), '17', 'D32_NOMOR', r=2.2, h=1.9)
    # batas delineasi digambar ulang di atas perkerasan baru
    import geopandas as gpd
    dl = gpd.read_file('/home/user/RancangKota/Delineasi Tapak D3.2 Baru/Delineasi Tapak D3.2 Baru.shp').to_crs(32749).geometry.iloc[0]
    for g in getattr(dl, 'geoms', [dl]):
        out.append(P('lines', 'D32_DELINEASI_ATAS', lines=[list(g.exterior.coords)], color=(200, 0, 200), lw=1.0, z=39))
    return out

def build_all():
    TREE_LOG.clear()
    sj, D = scene_jalan()
    st, a, b = scene_taman()
    return sj + st + scene_simbol(), D, a, b

if __name__ == '__main__':
    S, D, a, b = build_all()
    from collections import Counter
    print(len(S), Counter(p['k'] for p in S))
