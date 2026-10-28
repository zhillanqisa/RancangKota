"""Tulis overlay DXF: (1) model UTM 49S meter, (2) kop tambahan A0 dalam mm (paper space)."""
import math, random
import ezdxf
from ezdxf.enums import MTextEntityAlignment
from ezdxf.colors import rgb2int
import scene, kop

ATT = {('left', 'baseline'): MTextEntityAlignment.BOTTOM_LEFT, ('center', 'baseline'): MTextEntityAlignment.BOTTOM_CENTER,
       ('center', 'center'): MTextEntityAlignment.MIDDLE_CENTER, ('left', 'center'): MTextEntityAlignment.MIDDLE_LEFT}

def new_doc():
    doc = ezdxf.new('R2018', setup=True)
    doc.header['$INSUNITS'] = 0          # tanpa satuan -> tidak diskalakan saat INSERT
    doc.header['$MEASUREMENT'] = 1
    if 'D32_ARIAL' not in doc.styles: doc.styles.add('D32_ARIAL', font='arial.ttf')
    return doc

def lay(doc, name, aci=7):
    if name not in doc.layers: doc.layers.add(name, color=aci)
    return name

def lw_of(mm):
    # lineweight enum (1/100 mm) terdekat
    std = [0, 5, 9, 13, 15, 18, 20, 25, 30, 35, 40, 50, 53, 60, 70, 80, 90, 100]
    v = int(round(mm * 100)); return min(std, key=lambda s: abs(s - v))

def hatch_poly(msp, poly, layer, col, alpha=1.0):
    h = msp.add_hatch(dxfattribs={'layer': layer})
    h.set_solid_fill(rgb=col)
    h.paths.add_polyline_path(list(poly.exterior.coords)[:-1], is_closed=True, flags=1)
    for it in poly.interiors:
        h.paths.add_polyline_path(list(it.coords)[:-1], is_closed=True, flags=16)
    if alpha < 1: h.transparency = 1 - alpha
    return h

def outline(msp, coords, layer, col, lw_mm, closed=True, **extra):
    a = {'layer': layer, 'true_color': rgb2int(col), 'lineweight': lw_of(lw_mm)}; a.update(extra)
    return msp.add_lwpolyline(coords, close=closed, dxfattribs=a)

def tree_blocks(doc):
    for jenis, (dk, lt) in scene.SP.items():
        name = 'D32_POHON_' + jenis.upper()
        if name in doc.blocks: continue
        b = doc.blocks.new(name)
        prims = scene.tree(0.0, 0.0, 1.0, jenis, layer='0')
        scene.TREE_LOG.pop()
        for p in prims:
            if p['k'] == 'poly':
                hatch_poly(b, p['poly'], '0', p['fill'], p.get('alpha', 1))
                if p.get('edge'): outline(b, list(p['poly'].exterior.coords)[:-1], '0', p['edge'], 0.13)
            elif p['k'] == 'lines':
                for ln in p['lines']: outline(b, ln, '0', p['color'], 0.09, closed=False)
            elif p['k'] == 'circle':
                b.add_circle(p['c'], p['r'], dxfattribs={'layer': '0', 'true_color': rgb2int(p['fill'])})
                h = b.add_hatch(dxfattribs={'layer': '0'}); h.set_solid_fill(rgb=p['fill'])
                h.paths.add_edge_path().add_arc(p['c'], p['r'], 0, 360)

def write_model(S, fn):
    doc = new_doc(); msp = doc.modelspace()
    tree_blocks(doc)
    for p in sorted(S, key=lambda q: q.get('z', 0)):
        L = p['layer']
        if L.endswith('POHON') or L.endswith('_BAYANGAN'): continue
        lay(doc, L)
        k = p['k']
        if k == 'poly':
            hatch_poly(msp, p['poly'], L, p['fill'], p.get('alpha', 1))
            if p.get('edge'):
                outline(msp, list(p['poly'].exterior.coords)[:-1], L, p['edge'], max(0.05, p.get('lw', 0.3) * 0.35))
                for it in p['poly'].interiors: outline(msp, list(it.coords)[:-1], L, p['edge'], max(0.05, p.get('lw', 0.3) * 0.35))
        elif k == 'lines':
            for ln in p['lines']: outline(msp, ln, L, p['color'], p['lw'] * 0.35, closed=False)
        elif k == 'dash':
            on, off = p['dash']
            outline(msp, p['line'], L, p['color'], p['lw'] * 0.35, closed=False, linetype='DASHED', ltscale=(on + off) / 0.75)
        elif k == 'thick':
            pl = msp.add_lwpolyline(p['line'], dxfattribs={'layer': L, 'true_color': rgb2int(p['color'])}); pl.dxf.const_width = p['w']
        elif k == 'circle':
            if p.get('fill'):
                h = msp.add_hatch(dxfattribs={'layer': L}); h.set_solid_fill(rgb=p['fill']); h.paths.add_edge_path().add_arc(p['c'], p['r'], 0, 360)
            msp.add_circle(p['c'], p['r'], dxfattribs={'layer': L, 'true_color': rgb2int(p.get('edge') or p.get('fill') or (0, 0, 0))})
        elif k == 'dots':
            for x, y in p['pts']: msp.add_circle((x, y), p['r'], dxfattribs={'layer': L, 'true_color': rgb2int(p['color'])})
        elif k == 'text':
            t = ('\\fArial|b1;' if p.get('bold') else '') + p['s']
            m = msp.add_mtext(t, dxfattribs={'layer': L, 'char_height': p['h'], 'style': 'D32_ARIAL', 'true_color': rgb2int(p['color'])})
            m.set_location(p['xy'], rotation=p.get('rot', 0), attachment_point=ATT.get((p.get('ha', 'left'), p.get('va', 'baseline')), MTextEntityAlignment.MIDDLE_CENTER))
        elif k == 'bike':
            (ax, ay), (bx, by) = p['a'], p['b']
            dx, dy = bx - ax, by - ay; Lg = math.hypot(dx, dy); dx, dy = dx / Lg, dy / Lg; nx, ny = -dy, dx
            for off in (-0.35, 0.35): msp.add_circle((ax + dx * off, ay + dy * off), 0.22, dxfattribs={'layer': L, 'true_color': rgb2int(p['color'])})
            outline(msp, [(ax + dx * u + nx * v, ay + dy * u + ny * v) for u, v in ((-0.35, 0), (0, 0.3), (0.35, 0))], L, p['color'], 0.13, closed=False)
    rnd = random.Random(11)
    for x, y, r, jenis, L in scene.TREE_LOG:
        lay(doc, L, 3)
        msp.add_blockref('D32_POHON_' + jenis.upper(), (x, y), dxfattribs={'layer': L, 'xscale': r, 'yscale': r, 'rotation': rnd.uniform(0, 360)})
    doc.saveas(fn)
    return doc

def write_kop(K, fn):
    doc = new_doc(); msp = doc.modelspace()
    L = lay(doc, 'D32_KOP_TAMBAHAN')
    f = 25.4 / 72
    T = lambda x, y: (x * f, (2384 - y) * f)
    for p in K:
        if p['k'] == 'rect':
            pts = [T(p['x0'], p['y0']), T(p['x1'], p['y0']), T(p['x1'], p['y1']), T(p['x0'], p['y1'])]
            h = msp.add_hatch(dxfattribs={'layer': L}); h.set_solid_fill(rgb=p['fill']); h.paths.add_polyline_path(pts, is_closed=True)
            if p.get('edge'): outline(msp, pts, L, p['edge'], 0.13)
        elif p['k'] == 'line':
            ex = dict(linetype='DASHED', ltscale=(p['dash'][0] + p['dash'][1]) * f / 0.75) if p.get('dash') else {}
            outline(msp, [T(*q) for q in p['pts']], L, p['color'], max(0.13, p['lw'] * f), closed=False, **ex)
        elif p['k'] == 'circle':
            c = T(*p['c']); r = p['r'] * f
            h = msp.add_hatch(dxfattribs={'layer': L}); h.set_solid_fill(rgb=p['fill']); h.paths.add_edge_path().add_arc(c, r, 0, 360)
            if p.get('edge'): msp.add_circle(c, r, dxfattribs={'layer': L, 'true_color': rgb2int(p['edge'])})
        elif p['k'] == 'text':
            t = msp.add_text(p['s'], dxfattribs={'layer': L, 'height': p['size'] * f * 0.716, 'style': 'D32_ARIAL', 'true_color': rgb2int(p['color'])})
            if p.get('ha') == 'center': t.set_placement(T(*p['xy']), align=ezdxf.enums.TextEntityAlignment.BOTTOM_CENTER)
            else: t.set_placement(T(*p['xy']))
    doc.saveas(fn)
    return doc
