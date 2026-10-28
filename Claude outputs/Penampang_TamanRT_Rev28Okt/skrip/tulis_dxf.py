"""Tulis DXF (AutoCAD 2018):
1) TamanRT_PotonganJalan_Rev28Okt_UTM49S.dxf : taman RT + garis potong, koordinat UTM 49S
   (sama dengan model space Site Plan Rev 24 Okt) -> tempel dengan base point 0,0.
2) Penampang_Jalan_Permukiman_Rev28Okt.dxf    : penampang eksisting & rencana (satuan meter)."""
import os
import ezdxf
from ezdxf.colors import rgb2int
from ezdxf.enums import TextEntityAlignment, MTextEntityAlignment
from shapely.geometry import Polygon, MultiPolygon
from penampang import ROADS, ops_for, dim_ops
import taman as T, ruas

OUT = '../out/dxf'
os.makedirs(OUT, exist_ok=True)

def hex2rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def ensure_layer(doc, name, aci=7):
    if name not in doc.layers:
        doc.layers.add(name, color=aci)

def add_poly(msp, pts, layer, fill=None, outline=True, lw=None):
    if fill and fill != 'none':
        h = msp.add_hatch(dxfattribs={'layer': layer})
        h.set_solid_fill(rgb=hex2rgb(fill) if isinstance(fill, str) else fill)
        h.paths.add_polyline_path([(x, y) for x, y in pts], is_closed=True)
    if outline:
        msp.add_lwpolyline([(x, y) for x, y in pts], close=True, dxfattribs={'layer': layer})

def add_geom(msp, g, layer, fill=None):
    for p in (g.geoms if isinstance(g, MultiPolygon) else [g]):
        if p.is_empty: continue
        ext = list(p.exterior.coords)[:-1]
        if fill:
            h = msp.add_hatch(dxfattribs={'layer': layer})
            h.set_solid_fill(rgb=hex2rgb(fill))
            h.paths.add_polyline_path(ext, is_closed=True, flags=1)
            for it in p.interiors:
                h.paths.add_polyline_path(list(it.coords)[:-1], is_closed=True, flags=16)
        msp.add_lwpolyline(ext, close=True, dxfattribs={'layer': layer})
        for it in p.interiors:
            msp.add_lwpolyline(list(it.coords)[:-1], close=True, dxfattribs={'layer': layer})

ATT = {('left', 'top'): MTextEntityAlignment.TOP_LEFT, ('center', 'top'): MTextEntityAlignment.TOP_CENTER, ('right', 'top'): MTextEntityAlignment.TOP_RIGHT,
       ('left', 'center'): MTextEntityAlignment.MIDDLE_LEFT, ('center', 'center'): MTextEntityAlignment.MIDDLE_CENTER, ('right', 'center'): MTextEntityAlignment.MIDDLE_RIGHT,
       ('left', 'bottom'): MTextEntityAlignment.BOTTOM_LEFT, ('center', 'bottom'): MTextEntityAlignment.BOTTOM_CENTER, ('right', 'bottom'): MTextEntityAlignment.BOTTOM_RIGHT}

def add_text(msp, xy, s, h, layer, ha='center', va='center', rot=0, bold=False):
    t = s.replace('\n', '\\P')
    if bold: t = '\\fArial|b1;' + t
    m = msp.add_mtext(t, dxfattribs={'layer': layer, 'char_height': h, 'style': 'D32'})
    m.set_location(xy, rotation=rot, attachment_point=ATT[(ha, va)])
    return m

def new_doc():
    doc = ezdxf.new('R2018', setup=True)
    doc.units = ezdxf.units.M
    doc.header['$INSUNITS'] = 6
    if 'D32' not in doc.styles:
        doc.styles.add('D32', font='arial.ttf')
    return doc

# ------------------------------------------------------------------ 1) taman RT (UTM)
def tulis_taman():
    doc = new_doc(); msp = doc.modelspace()
    L = {'D32_TAMAN_RT_BATAS': 3, 'D32_TAMAN_RT_RUMPUT': 3, 'D32_TAMAN_RT_JALUR': 33, 'D32_TAMAN_RT_PLAZA': 33,
         'D32_TAMAN_RT_BERMAIN': 40, 'D32_TAMAN_RT_LAPANGAN': 82, 'D32_TAMAN_RT_GAZEBO': 22, 'D32_TAMAN_RT_PAGAR_HIJAU': 94,
         'D32_TAMAN_RT_POHON': 94, 'D32_TAMAN_RT_BANGKU': 32, 'D32_TAMAN_RT_ZEBRA': 7, 'D32_TAMAN_RT_TEKS': 7,
         'D32_TAMAN_RT_AKSES': 1, 'D32_POTONGAN_JALAN': 1, 'D32_POTONGAN_TEKS': 1}
    for k, v in L.items(): ensure_layer(doc, k, v)

    def taman(geom, parts, trees, benches, entries, name, luas):
        add_geom(msp, geom, 'D32_TAMAN_RT_RUMPUT', '#cfe6b0')
        for g, lay, col in parts:
            add_geom(msp, g, lay, col)
        add_geom(msp, geom, 'D32_TAMAN_RT_BATAS')
        for t in trees:
            c = msp.add_circle((t.x, t.y), 1.9, dxfattribs={'layer': 'D32_TAMAN_RT_POHON'})
            h = msp.add_hatch(dxfattribs={'layer': 'D32_TAMAN_RT_POHON'}); h.set_solid_fill(rgb=hex2rgb('#5e9c43'))
            ep = h.paths.add_edge_path(); ep.add_arc((t.x, t.y), 1.9, 0, 360)
        for b in benches:
            add_poly(msp, [(b[0] - 0.9, b[1] - 0.3), (b[0] + 0.9, b[1] - 0.3), (b[0] + 0.9, b[1] + 0.3), (b[0] - 0.9, b[1] + 0.3)], 'D32_TAMAN_RT_BANGKU', '#7a5230')
        for (x, y), t in entries:
            vert = 'selatan' in t.lower()
            p0 = (x, y - 6) if vert else (x - 7, y)
            msp.add_line(p0, (x, y), dxfattribs={'layer': 'D32_TAMAN_RT_AKSES'})
            ah = [(x, y), (x - 0.7, y - 1.4), (x + 0.7, y - 1.4)] if vert else [(x, y), (x - 1.4, y - 0.7), (x - 1.4, y + 0.7)]
            add_poly(msp, ah, 'D32_TAMAN_RT_AKSES', (192, 57, 43))
        c = geom.centroid
        add_text(msp, (c.x, c.y), '%s\nRENCANA ±%d m²' % (name, round(luas, -1)), 1.6, 'D32_TAMAN_RT_TEKS', bold=True)

    taman(T.A, [(T.A_pagar, 'D32_TAMAN_RT_PAGAR_HIJAU', '#4f8a3a'), (T.A_jalur, 'D32_TAMAN_RT_JALUR', '#e3d3ae'),
                (T.A_main, 'D32_TAMAN_RT_BERMAIN', '#f2c46d'), (T.A_lap, 'D32_TAMAN_RT_LAPANGAN', '#b6dc8e'),
                (T.A_gazebo, 'D32_TAMAN_RT_GAZEBO', '#9a5b2c')],
          T.A_pohon, T.A_bangku, T.A_masuk, 'TAMAN RT A', T.A.area)
    taman(T.B, [(T.B_plaza.intersection(T.B), 'D32_TAMAN_RT_PLAZA', '#e3d3ae'), (T.B_main, 'D32_TAMAN_RT_BERMAIN', '#f2c46d'),
                (T.B_gazebo, 'D32_TAMAN_RT_GAZEBO', '#9a5b2c')],
          T.B_pohon, T.B_bangku, T.B_masuk, 'TAMAN RT B', T.B.area)
    zb = T.B_zebra.bounds
    for k in range(6):
        y = zb[1] + 0.3 + k * 0.55
        add_poly(msp, [(zb[0] + 0.3, y - 0.15), (zb[2] - 0.3, y - 0.15), (zb[2] - 0.3, y + 0.15), (zb[0] + 0.3, y + 0.15)], 'D32_TAMAN_RT_ZEBRA', (255, 255, 255))
    # garis potong penampang
    for k, (a, b) in ruas.POTONG.items():
        msp.add_line(a, b, dxfattribs={'layer': 'D32_POTONGAN_JALAN', 'linetype': 'DASHED', 'lineweight': 50})
        for p, lab in ((a, k), (b, k + "'")):
            msp.add_circle(p, 2.2, dxfattribs={'layer': 'D32_POTONGAN_JALAN'})
            add_text(msp, p, lab, 2.0, 'D32_POTONGAN_TEKS', bold=True)
    add_text(msp, (306030.0, 9156610.0),
             'D3.2 Rev 28 Okt 2026: Taman RT A/B + garis potong penampang jalan.\nKoordinat UTM 49S (WGS84), satuan meter. Tempel ke Site Plan Rev 24 Okt dengan titik dasar 0,0,0.',
             1.8, 'D32_TAMAN_RT_TEKS', ha='left', va='bottom')
    fn = f'{OUT}/TamanRT_PotonganJalan_Rev28Okt_UTM49S.dxf'
    doc.saveas(fn); print('saved', fn)

# ------------------------------------------------------------------ 2) penampang
def tulis_penampang():
    doc = new_doc(); msp = doc.modelspace()
    order = [('betet', 'A–A\' JL. BETET'), ('cendrawasih_b1', 'B1 JL. CENDRAWASIH (SEGMEN PERMUKIMAN)'),
             ('cendrawasih_b2', 'B2 JL. CENDRAWASIH (SEGMEN TEPI REL)'), ('letkol', 'C–C\' JL. LETKOL SUDARSO')]
    lay_col = {}
    for row, (key, title) in enumerate(order):
        for col, which in enumerate(('eks', 'ren')):
            ops, dims, total = ops_for(ROADS[key][which])
            ops += dim_ops(dims, total_label='Ruang milik jalan' if which == 'ren' else 'Ruang milik jalan eksisting')
            ox, oy = col * 22.0, -row * 20.0
            for o in ops:
                lay = 'D32_PNP_' + o['layer']
                if lay not in lay_col:
                    ensure_layer(doc, lay, 7); lay_col[lay] = 1
                if o['k'] == 'poly':
                    pts = [(x + ox, y + oy) for x, y in o['pts']]
                    add_poly(msp, pts, lay, o['fill'] if o['fill'] != '#ffffff' else (255, 255, 255))
                elif o['k'] == 'line':
                    msp.add_lwpolyline([(x + ox, y + oy) for x, y in o['pts']], dxfattribs={'layer': lay, 'true_color': rgb2int(hex2rgb(o['color']))})
                elif o['k'] == 'circle':
                    cx, cy = o['c']
                    msp.add_circle((cx + ox, cy + oy), o['r'], dxfattribs={'layer': lay})
                    if o['fill'] != 'none':
                        h = msp.add_hatch(dxfattribs={'layer': lay}); h.set_solid_fill(rgb=hex2rgb(o['fill']))
                        ep = h.paths.add_edge_path(); ep.add_arc((cx + ox, cy + oy), o['r'], 0, 360)
                elif o['k'] == 'text':
                    x, y = o['xy']
                    add_text(msp, (x + ox, y + oy), o['s'], o['size'] * 0.12, lay, ha=o['ha'], va=o['va'], rot=o['rot'], bold=o['weight'] == 'bold')
            ensure_layer(doc, 'D32_PNP_JUDUL', 7)
            add_text(msp, (ox + total / 2, oy + 9.2), '%s — %s' % (title, 'EKSISTING' if which == 'eks' else 'RENCANA'), 0.45, 'D32_PNP_JUDUL', va='bottom', bold=True)
            add_text(msp, (ox + total / 2, oy + 8.9), '(%s)  |  kiri: %s, kanan: %s  |  skala 1:100' % (ROADS[key]['ket'], ROADS[key]['kiri'], ROADS[key]['kanan']),
                     0.22, 'D32_PNP_JUDUL', va='top')
    fn = f'{OUT}/Penampang_Jalan_Permukiman_Rev28Okt.dxf'
    doc.saveas(fn); print('saved', fn)

if __name__ == '__main__':
    tulis_taman(); tulis_penampang()
