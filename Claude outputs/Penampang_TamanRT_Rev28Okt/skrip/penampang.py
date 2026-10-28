"""Penampang jalan permukiman (eksisting & rencana) sebagai daftar elemen kiri->kanan.
Satuan meter. Dipakai bersama oleh render slide (matplotlib) dan DXF (ezdxf)."""

# tipe elemen: persil, rel, bahu, bahu_keras, drain_o, drain_c, furn, jalan, trotoar,
#              hijau, pagar, pedsep
# Elemen dengan 'dim': False tidak diberi ukuran (di luar ruang milik jalan).

def E(t, w, label=None, **kw):
    d = dict(t=t, w=w, label=label); d.update(kw); return d

ROADS = {
'betet': dict(
    nama='Jl. Betet', ket='Dari Jl. Jend. A. Yani ke Jl. Cendrawasih', kiri='Selatan (klaster tempe)', kanan='Utara',
    eks=[E('persil', 2.8, dim=False), E('furn', 0.45, 'Furnitur', pole='listrik'), E('drain_o', 0.40, 'Drainase'),
         E('bahu', 1.05, 'Bahu tanah', parkir=True), E('jalan', 3.20, 'Badan jalan', lanes=2, walker=True, veh=(None, 'pickup')), E('bahu', 1.15, 'Bahu tanah'),
         E('drain_o', 0.35, 'Drainase'), E('furn', 0.35, 'Furnitur', pole='pju'), E('persil', 2.8, dim=False)],
    ren=[E('persil', 2.8, dim=False), E('hijau', 0.50, 'Jalur hijau', tree='kecil', lamp=True),
         E('trotoar', 1.50, 'Trotoar', drain=0.5, person=True), E('jalan', 4.00, 'Badan jalan', lanes=2, veh=('motor', 'pickup')),
         E('drain_c', 0.50, 'Drainase tertutup'), E('bahu_keras', 0.50, 'Bahu', pole='listrik'), E('persil', 2.8, dim=False)],
),
'cendrawasih_b1': dict(
    nama='Jl. Cendrawasih', ket='Segmen permukiman (Jl. Jend. A. Yani - belokan tepi rel)', kiri='Utara', kanan='Selatan',
    eks=[E('persil', 2.8, dim=False), E('drain_o', 0.35, 'Drainase'), E('furn', 0.40, 'Furnitur', pole='pju'),
         E('bahu', 0.90, 'Bahu tanah', parkir=True), E('jalan', 3.20, 'Badan jalan', lanes=2, walker=True, veh=(None, 'mobil')), E('bahu', 0.90, 'Bahu tanah'),
         E('furn', 0.40, 'Furnitur', pole='pju'), E('drain_o', 0.35, 'Drainase'), E('persil', 2.8, dim=False)],
    ren=[E('persil', 2.8, dim=False), E('trotoar', 1.50, 'Trotoar', drain=0.5, person=True),
         E('jalan', 4.00, 'Badan jalan', lanes=2, veh=('motor', 'mobil')), E('drain_c', 0.50, 'Drainase tertutup'),
         E('bahu_keras', 0.50, 'Bahu', pole='pju'), E('persil', 2.8, dim=False)],
),
'cendrawasih_b2': dict(
    nama='Jl. Cendrawasih', ket='Segmen tepi rel (belokan - Jl. Betet, depan Taman RT A)', kiri='Barat (rel KA)', kanan='Timur',
    eks=[E('rel', 4.2, dim=False), E('drain_o', 0.35, 'Drainase'), E('furn', 0.40, 'Furnitur', pole='pju'),
         E('bahu', 0.90, 'Bahu tanah'), E('jalan', 3.20, 'Badan jalan', lanes=2, walker=True, veh=(None, 'motor')), E('bahu', 0.90, 'Bahu tanah'),
         E('furn', 0.40, 'Furnitur', pole='listrik'), E('drain_o', 0.35, 'Drainase'), E('persil', 2.8, dim=False, kind='lahan')],
    ren=[E('rel', 4.2, dim=False), E('pagar', 0.50, 'Pagar hijau'),
         E('pedsep', 1.50, 'Jalur pejalan\n& sepeda', drain=0.5, person=True),
         E('jalan', 4.00, 'Badan jalan', lanes=2, veh=('motor', 'mobil')), E('drain_c', 0.50, 'Drainase tertutup', pole='pju'),
         E('persil', 2.8, dim=False, kind='taman')],
),
'letkol': dict(
    nama='Jl. Letkol Sudarso', ket='Dari Jl. Jeruk Manis ke Jl. Betet (Simpang 4 A. Yani)', kiri='Selatan (zona pendidikan)', kanan='Utara',
    eks=[E('persil', 2.8, dim=False), E('drain_o', 0.30, 'Drainase'), E('furn', 0.40, 'Furnitur', pole='pju'),
         E('bahu', 0.90, 'Bahu tanah'), E('jalan', 2.50, 'Badan jalan', lanes=2, walker=True, child=True, veh=(None, 'mobil')), E('bahu', 0.90, 'Bahu tanah', parkir=True),
         E('furn', 0.40, 'Furnitur', pole='listrik'), E('drain_o', 0.30, 'Drainase'), E('persil', 2.8, dim=False)],
    ren=[E('persil', 2.8, dim=False, kind='sekolah'), E('trotoar', 1.50, 'Trotoar ZoSS', drain=0.4, person=True, child=True),
         E('jalan', 3.50, 'Badan jalan (berbagi)', lanes=1, veh=('motor', 'mobil'), zoss=True),
         E('drain_c', 0.40, 'Drainase\ntertutup'), E('bahu_keras', 0.30, 'Bahu', pole='pju'), E('persil', 2.8, dim=False)],
),
}

def row_width(els):
    return sum(e['w'] for e in els if e.get('dim', True))


# ---------------------------------------------------------------- drawing ops
# op: dict(k='poly'|'line'|'circle'|'text', layer=..., ...)
COL = dict(aspal='#5b5b5b', tanah='#b59468', paving='#d9c7a3', beton='#bdbdbd', hijau='#7fae5a', rumput='#a9cf7f',
           daun='#4f8a3a', daun2='#6aa84f', air='#7fb7d9', dinding='#efe6d2', atap='#c4643c', garis='#2f3318',
           rel='#8a8a8a', kayu='#7a5230', merah='#c0392b', putih='#ffffff', pedsep='#c9d7a0')

def ops_for(els, with_people=True):
    ops = []
    def poly(pts, fill, layer, ec=COL['garis'], lw=0.6, z=2):
        ops.append(dict(k='poly', pts=pts, fill=fill, layer=layer, ec=ec, lw=lw, z=z))
    def line(pts, layer, color=COL['garis'], lw=0.8, ls='-', z=3):
        ops.append(dict(k='line', pts=pts, layer=layer, color=color, lw=lw, ls=ls, z=z))
    def circle(c, r, fill, layer, ec=None, z=4):
        ops.append(dict(k='circle', c=c, r=r, fill=fill, layer=layer, ec=ec or fill, z=z))
    def text(xy, s, size, layer, ha='center', va='center', color=COL['garis'], weight='normal', rot=0):
        ops.append(dict(k='text', xy=xy, s=s, size=size, layer=layer, ha=ha, va=va, color=color, weight=weight, rot=rot))

    def tree(x, base, h=4.6, r=1.4, small=False):
        if small: h, r = 3.6, 1.0
        poly([(x - 0.12, base), (x + 0.12, base), (x + 0.12, base + h - r), (x - 0.12, base + h - r)], COL['kayu'], 'VEGETASI')
        circle((x, base + h - r * 0.4), r, COL['daun'], 'VEGETASI')
        circle((x - r * 0.55, base + h - r * 0.9), r * 0.7, COL['daun2'], 'VEGETASI')
        circle((x + r * 0.55, base + h - r * 0.8), r * 0.7, COL['daun2'], 'VEGETASI')
    def shrub(x0, x1, base, h=1.3):
        n = max(2, int((x1 - x0) / 0.35))
        for i in range(n):
            cx = x0 + (i + 0.5) * (x1 - x0) / n
            circle((cx, base + h * 0.55), (x1 - x0) / n * 0.75 + 0.12, COL['daun2'], 'VEGETASI')
    def pole(x, base, kind):
        if kind == 'listrik':
            poly([(x - 0.08, base), (x + 0.08, base), (x + 0.06, base + 7.2), (x - 0.06, base + 7.2)], COL['beton'], 'UTILITAS')
            line([(x - 0.7, base + 6.8), (x + 0.7, base + 6.8)], 'UTILITAS', lw=1.2)
            line([(x - 0.5, base + 6.4), (x + 0.5, base + 6.4)], 'UTILITAS', lw=1.0)
        else:
            poly([(x - 0.06, base), (x + 0.06, base), (x + 0.05, base + 5.6), (x - 0.05, base + 5.6)], COL['beton'], 'UTILITAS')
            line([(x, base + 5.6), (x + 0.4, base + 6.0), (x + 1.2, base + 6.0)], 'UTILITAS', lw=1.2)
            poly([(x + 0.9, base + 5.85), (x + 1.4, base + 5.85), (x + 1.3, base + 6.0), (x + 1.0, base + 6.0)], '#f4d03f', 'UTILITAS')
    def person(x, base, h=1.65, child=False):
        if child: h = 1.25
        r = h * 0.08
        circle((x, base + h - r), r, '#3a3a3a', 'ORANG')
        poly([(x - h * 0.1, base + h * 0.45), (x + h * 0.1, base + h * 0.45), (x + h * 0.09, base + h - 2 * r), (x - h * 0.09, base + h - 2 * r)], '#c0392b' if child else '#34495e', 'ORANG')
        line([(x - h * 0.05, base + h * 0.45), (x - h * 0.08, base)], 'ORANG', color='#3a3a3a', lw=1.4)
        line([(x + h * 0.05, base + h * 0.45), (x + h * 0.08, base)], 'ORANG', color='#3a3a3a', lw=1.4)
    def cyclist(x, base):
        circle((x - 0.35, base + 0.33), 0.33, 'none', 'ORANG', ec='#3a3a3a')
        circle((x + 0.35, base + 0.33), 0.33, 'none', 'ORANG', ec='#3a3a3a')
        line([(x - 0.35, base + 0.33), (x, base + 0.75), (x + 0.35, base + 0.33)], 'ORANG', color='#3a3a3a', lw=1.2)
        person(x - 0.05, base + 0.75, h=0.95)
    def vehicle(x, base, kind):
        if kind == 'motor':
            poly([(x - 0.2, base + 0.25), (x + 0.2, base + 0.25), (x + 0.28, base + 0.8), (x - 0.28, base + 0.8)], '#2c3e50', 'KENDARAAN')
            circle((x, base + 0.15), 0.15, '#222222', 'KENDARAAN')
            line([(x - 0.42, base + 1.05), (x + 0.42, base + 1.05)], 'KENDARAAN', color='#222222', lw=1.4)
            person(x, base + 0.62, h=1.05)
        else:
            w = 1.7 if kind == 'mobil' else 1.75
            h = 1.5 if kind == 'mobil' else 1.85
            poly([(x - w / 2, base + 0.3), (x + w / 2, base + 0.3), (x + w / 2, base + h * 0.6), (x + w * 0.38, base + h), (x - w * 0.38, base + h), (x - w / 2, base + h * 0.6)],
                 '#d0d3d4' if kind == 'mobil' else '#e5e8e8', 'KENDARAAN')
            poly([(x - w * 0.36, base + h * 0.65), (x + w * 0.36, base + h * 0.65), (x + w * 0.3, base + h * 0.93), (x - w * 0.3, base + h * 0.93)], '#85929e', 'KENDARAAN')
            for dx in (-w * 0.35, w * 0.35):
                poly([(x + dx - 0.12, base), (x + dx + 0.12, base), (x + dx + 0.12, base + 0.32), (x + dx - 0.12, base + 0.32)], '#222222', 'KENDARAAN')

    x = 0.0
    dims = []
    n = len(els)
    for i, e in enumerate(els):
        t, w = e['t'], e['w']; x0, x1 = x, x + w
        if t == 'persil':
            kind = e.get('kind', 'rumah')
            left = (i == 0)
            if kind == 'lahan':
                poly([(x0, -0.3), (x1, -0.3), (x1, 0), (x0, 0)], COL['rumput'], 'TANAH', lw=0.3)
                shrub(x0 + 0.5, x0 + 1.5, 0, 0.8); text(((x0 + x1) / 2, 2.2), 'Lahan kosong\n(rencana Taman RT A)', 2.0, 'TEKS')
            elif kind == 'taman':
                poly([(x0, -0.3), (x1, -0.3), (x1, 0.15), (x0, 0.15)], COL['rumput'], 'TANAH', lw=0.3)
                tree(x0 + 1.2, 0.15); person(x0 + 2.8, 0.15, child=True)
                text(((x0 + x1) / 2, -0.85), 'Taman RT A', 2.0, 'TEKS', weight='bold')
            else:
                poly([(x0, -0.3), (x1, -0.3), (x1, 0), (x0, 0)], COL['tanah'], 'TANAH', lw=0.3)
                wx0, wx1 = (x0, x1 - 0.6) if left else (x0 + 0.6, x1)
                poly([(wx0, 0), (wx1, 0), (wx1, 3.4), (wx0, 3.4)], COL['dinding'], 'BANGUNAN')
                ex = wx1 if left else wx0
                poly([(wx0 - (0.3 if not left else 0), 3.4), (wx1 + (0.3 if left else 0), 3.4), ((wx0 + wx1) / 2, 5.2)], COL['atap'], 'BANGUNAN')
                line([(ex, 0), (ex, 3.4)], 'BANGUNAN', lw=1.2)
                lbl = {'rumah': 'Rumah warga\n(tidak diubah)', 'sekolah': 'Zona\npendidikan'}[kind]
                text(((wx0 + wx1) / 2, 1.7), lbl, 1.45, 'TEKS')
            x = x1; continue
        if t == 'rel':
            poly([(x0, -0.3), (x1, -0.3), (x1, 0), (x0, 0)], COL['tanah'], 'TANAH', lw=0.3)
            poly([(x0 + 0.5, 0), (x1 - 0.8, 0), (x1 - 1.4, 0.5), (x0 + 1.1, 0.5)], COL['rel'], 'REL')
            for rx in (x0 + 1.8, x0 + 3.3):
                poly([(rx - 0.08, 0.5), (rx + 0.08, 0.5), (rx + 0.08, 0.68), (rx - 0.08, 0.68)], '#333333', 'REL')
            text(((x0 + x1) / 2 - 0.3, 2.0), 'Rel KA', 2.0, 'TEKS', weight='bold')
            x = x1; continue
        if t == 'jalan':
            poly([(x0, -0.25), (x1, -0.25), (x1, 0), (x0, 0)], COL['aspal'], 'JALAN')
            if e.get('lanes', 2) == 2:
                line([((x0 + x1) / 2, 0.01), ((x0 + x1) / 2, 0.01)], 'JALAN')
                poly([((x0 + x1) / 2 - 0.06, -0.02), ((x0 + x1) / 2 + 0.06, -0.02), ((x0 + x1) / 2 + 0.06, 0.02), ((x0 + x1) / 2 - 0.06, 0.02)], COL['putih'], 'MARKA', ec=COL['putih'])
            if e.get('zoss'):
                poly([(x0 + 0.05, -0.03), (x1 - 0.05, -0.03), (x1 - 0.05, 0.0), (x0 + 0.05, 0.0)], COL['merah'], 'MARKA', ec=COL['merah'])
            veh = e.get('veh')
            if veh and with_people:
                if veh[0]: vehicle(x0 + w * 0.27, 0, veh[0])
                if veh[1]: vehicle(x0 + w * 0.70, 0, veh[1])
            if e.get('walker') and with_people:
                person(x0 + 0.35, 0)
                if e.get('child'): person(x0 + 0.75, 0, child=True)
        elif t in ('bahu', 'bahu_keras'):
            poly([(x0, -0.2), (x1, -0.2), (x1, 0), (x0, 0)], COL['tanah'] if t == 'bahu' else COL['beton'], 'BAHU')
            if e.get('parkir') and with_people:
                poly([(x0 + w / 2 - 0.3, 0.25), (x0 + w / 2 + 0.3, 0.25), (x0 + w / 2 + 0.25, 0.85), (x0 + w / 2 - 0.25, 0.85)], '#7b241c', 'KENDARAAN')
                circle((x0 + w / 2, 0.15), 0.15, '#222222', 'KENDARAAN')
        elif t == 'drain_o':
            poly([(x0, -0.6), (x1, -0.6), (x1, 0), (x0, 0)], COL['beton'], 'DRAINASE')
            poly([(x0 + 0.06, -0.52), (x1 - 0.06, -0.52), (x1 - 0.06, 0), (x0 + 0.06, 0)], '#ffffff', 'DRAINASE')
            poly([(x0 + 0.06, -0.52), (x1 - 0.06, -0.52), (x1 - 0.06, -0.35), (x0 + 0.06, -0.35)], COL['air'], 'DRAINASE', lw=0.2)
        elif t == 'drain_c':
            poly([(x0, -0.7), (x1, -0.7), (x1, 0), (x0, 0)], COL['beton'], 'DRAINASE')
            poly([(x0 + 0.07, -0.62), (x1 - 0.07, -0.62), (x1 - 0.07, -0.08), (x0 + 0.07, -0.08)], '#ffffff', 'DRAINASE')
            poly([(x0 + 0.07, -0.62), (x1 - 0.07, -0.62), (x1 - 0.07, -0.45), (x0 + 0.07, -0.45)], COL['air'], 'DRAINASE', lw=0.2)
            for k in range(5):
                gx = x0 + 0.08 + k * (w - 0.16) / 4
                line([(gx, -0.08), (gx, 0)], 'DRAINASE', lw=0.6)
        elif t == 'furn':
            poly([(x0, -0.2), (x1, -0.2), (x1, 0), (x0, 0)], COL['tanah'], 'FURNITUR')
        elif t in ('trotoar', 'pedsep'):
            dr = e.get('drain', 0)
            road_side_right = (i + 1 < n and els[i + 1]['t'] == 'jalan')
            fill = COL['paving'] if t == 'trotoar' else COL['pedsep']
            poly([(x0, -0.1), (x1, -0.1), (x1, 0.15), (x0, 0.15)], fill, 'TROTOAR')
            if dr:
                dx0, dx1 = (x1 - dr, x1) if road_side_right else (x0, x0 + dr)
                poly([(dx0, -0.75), (dx1, -0.75), (dx1, -0.1), (dx0, -0.1)], COL['beton'], 'DRAINASE')
                poly([(dx0 + 0.06, -0.68), (dx1 - 0.06, -0.68), (dx1 - 0.06, -0.12), (dx0 + 0.06, -0.12)], '#ffffff', 'DRAINASE')
                poly([(dx0 + 0.06, -0.68), (dx1 - 0.06, -0.68), (dx1 - 0.06, -0.5), (dx0 + 0.06, -0.5)], COL['air'], 'DRAINASE', lw=0.2)
                text(((dx0 + dx1) / 2, -0.92), 'saluran\ntertutup %s' % ('%.2f' % dr).rstrip('0').rstrip('.').replace('.', ','), 1.2, 'TEKS')
            kx = x1 if road_side_right else x0
            line([(kx, -0.25), (kx, 0.15)], 'TROTOAR', lw=1.4)
            if with_people and e.get('person'):
                if t == 'pedsep':
                    cyclist(x0 + w * 0.35, 0.15)
                else:
                    person(x0 + w * 0.4, 0.15, child=False)
                    if e.get('child'): person(x0 + w * 0.68, 0.15, child=True)
        elif t == 'hijau':
            poly([(x0, -0.2), (x1, -0.2), (x1, 0.2), (x0, 0.2)], COL['hijau'], 'JALUR_HIJAU')
            tree((x0 + x1) / 2 + 0.05, 0.2, small=e.get('tree') == 'kecil')
        elif t == 'pagar':
            poly([(x0, -0.2), (x1, -0.2), (x1, 0.2), (x0, 0.2)], COL['hijau'], 'JALUR_HIJAU')
            shrub(x0, x1, 0.2, 1.5)
        if e.get('pole') or (t == 'hijau' and e.get('lamp')):
            kind = e.get('pole', 'pju')
            pole((x0 + 0.1) if t == 'hijau' else (x0 + x1) / 2, 0.2 if t == 'hijau' else 0, kind)
        if e.get('dim', True):
            dims.append((x0, x1, e.get('label') or ''))
        x = x1
    return ops, dims, x

def dim_ops(dims, y=-1.75, ytot=-4.35, total_label='Ruang milik jalan'):
    ops = []
    def line(pts, lw=0.6): ops.append(dict(k='line', pts=pts, layer='DIMENSI', color=COL['garis'], lw=lw, ls='-', z=5))
    def text(xy, s, size, weight='normal', va='bottom'):
        ops.append(dict(k='text', xy=xy, s=s, size=size, layer='DIMENSI', ha='center', va=va, color=COL['garis'], weight=weight, rot=0))
    for x0, x1, lab in dims:
        line([(x0, y), (x1, y)]); line([(x0, y - 0.15), (x0, y + 0.15)]); line([(x1, y - 0.15), (x1, y + 0.15)])
        line([(x0 - 0.1, y - 0.1), (x0 + 0.1, y + 0.1)], 1.0); line([(x1 - 0.1, y - 0.1), (x1 + 0.1, y + 0.1)], 1.0)
        w = x1 - x0
        v = ('%.2f' % w).rstrip('0').rstrip('.').replace('.', ',')
        if w < 0.6:
            ops.append(dict(k='text', xy=((x0 + x1) / 2, y + 0.1), s=v, size=1.35, layer='DIMENSI', ha='center', va='bottom', color=COL['garis'], weight='bold', rot=90))
        else:
            text(((x0 + x1) / 2, y + 0.08), v, 1.4, 'bold')
        if w < 1.3:
            ops.append(dict(k='text', xy=((x0 + x1) / 2, y - 0.15), s=lab.replace('\n', ' '), size=1.25, layer='DIMENSI', ha='center', va='top', color=COL['garis'], weight='normal', rot=90))
        else:
            text(((x0 + x1) / 2, y - 0.2), lab, 1.3, va='top')
    xa, xb = dims[0][0], dims[-1][1]
    line([(xa, ytot), (xb, ytot)]); line([(xa, ytot - 0.15), (xa, -0.3)], 0.4); line([(xb, ytot - 0.15), (xb, -0.3)], 0.4)
    v = ('%.2f' % (xb - xa)).rstrip('0').rstrip('.').replace('.', ',')
    text(((xa + xb) / 2, ytot - 0.15), '%s ±%s m (ukuran dalam meter)' % (total_label, v), 1.55, 'bold', va='top')
    return ops

if __name__ == '__main__':
    for k, r in ROADS.items():
        print(k, 'eks ROW', round(row_width(r['eks']), 2), 'ren ROW', round(row_width(r['ren']), 2))
