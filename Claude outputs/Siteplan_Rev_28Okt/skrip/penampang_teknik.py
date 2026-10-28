"""Penampang jalan permukiman sebagai GAMBAR TEKNIK (DXF R2018, satuan meter, cetak 1:100 di layout A3).
Sumber ukuran: penampang Rev 28 Okt (gen/penampang.py)."""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'gen'))
import ezdxf
from ezdxf.enums import TextEntityAlignment, MTextEntityAlignment
from penampang import ROADS

ARIAL = 'D32_ARIAL'
TH = 0.25            # tinggi teks 2,5 mm @1:100
LAY = {  # nama: (ACI, lineweight 1/100 mm, linetype)
    'D32_PNP_POTONGAN': (7, 50, 'Continuous'), 'D32_PNP_KONSTRUKSI': (7, 25, 'Continuous'), 'D32_PNP_TAMPAK': (8, 18, 'Continuous'),
    'D32_PNP_ARSIR': (8, 9, 'Continuous'), 'D32_PNP_ARSIR_TANAH': (33, 9, 'Continuous'), 'D32_PNP_VEGETASI': (94, 18, 'Continuous'),
    'D32_PNP_FIGUR': (251, 13, 'Continuous'), 'D32_PNP_DIMENSI': (7, 13, 'Continuous'), 'D32_PNP_TEKS': (7, 18, 'Continuous'),
    'D32_PNP_BATAS_RMJ': (1, 25, 'PHANTOM'), 'D32_PNP_AS': (1, 13, 'CENTER'), 'D32_PNP_AIR': (5, 13, 'Continuous'),
    'D32_KOP': (7, 35, 'Continuous'), 'D32_KOP_TIPIS': (7, 18, 'Continuous'), 'D32_VIEWPORT': (8, 9, 'Continuous'),
}

def setup(doc):
    doc.header['$INSUNITS'] = 6; doc.header['$MEASUREMENT'] = 1; doc.header['$LTSCALE'] = 1.0
    doc.header['$PSLTSCALE'] = 1
    if ARIAL not in doc.styles: doc.styles.add(ARIAL, font='arial.ttf')
    if 'D32_TIMES' not in doc.styles: doc.styles.add('D32_TIMES', font='times.ttf')
    for n, (c, lw, lt) in LAY.items():
        if n not in doc.layers: doc.layers.add(n, color=c, lineweight=lw, linetype=lt)
    ds = doc.dimstyles.new('D32_1-100')
    for k, v in dict(dimtxt=TH * 0.9, dimasz=0.12, dimblk='ARCHTICK', dimblk1='ARCHTICK', dimblk2='ARCHTICK', dimexe=0.08, dimexo=0.06,
                     dimgap=0.04, dimdec=2, dimzin=8, dimdsep=ord(','), dimtad=1, dimtxsty=ARIAL, dimlunit=2, dimclrd=7, dimclre=7,
                     dimclrt=7, dimtih=0, dimtoh=0, dimtix=0, dimtmove=2, dimlwd=13, dimlwe=13).items():
        try: ds.dxf.set(k, v)
        except Exception: pass

# ------------------------------------------------------------- primitif
class Pen:
    def __init__(self, msp, ox, oy):
        self.m = msp; self.ox = ox; self.oy = oy
    def P(self, x, y): return (x + self.ox, y + self.oy)
    def pl(self, pts, layer, closed=False, **kw):
        a = {'layer': layer}; a.update(kw)
        return self.m.add_lwpolyline([self.P(*p) for p in pts], close=closed, dxfattribs=a)
    def line(self, a, b, layer, **kw): return self.pl([a, b], layer, **kw)
    def rect(self, x0, y0, x1, y1, layer, hatch=None, scale=0.02, angle=0, hlayer='D32_PNP_ARSIR'):
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        if hatch: self.hatch(pts, hatch, scale, angle, hlayer)
        return self.pl(pts, layer, closed=True)
    def hatch(self, pts, pat, scale=0.02, angle=0, layer='D32_PNP_ARSIR'):
        h = self.m.add_hatch(dxfattribs={'layer': layer})
        if pat == 'SOLID': h.set_solid_fill(color=8)
        else: h.set_pattern_fill(pat, scale=scale, angle=angle)
        h.paths.add_polyline_path([self.P(*p) for p in pts], is_closed=True)
        return h
    def circle(self, c, r, layer): return self.m.add_circle(self.P(*c), r, dxfattribs={'layer': layer})
    def arc(self, c, r, a0, a1, layer): return self.m.add_arc(self.P(*c), r, a0, a1, dxfattribs={'layer': layer})
    def text(self, xy, s, h=TH, layer='D32_PNP_TEKS', align='MIDDLE_CENTER', rot=0):
        t = self.m.add_text(s, dxfattribs={'layer': layer, 'height': h, 'style': ARIAL, 'rotation': rot})
        t.set_placement(self.P(*xy), align=TextEntityAlignment[align]); return t
    def mtext(self, xy, s, h=TH, layer='D32_PNP_TEKS', att=MTextEntityAlignment.BOTTOM_LEFT, width=None):
        m = self.m.add_mtext(s.replace('\n', '\\P'), dxfattribs={'layer': layer, 'char_height': h, 'style': ARIAL})
        m.set_location(self.P(*xy), attachment_point=att)
        if width: m.dxf.width = width
        return m
    def leader(self, p_obj, p_txt, s, h=TH * 0.85, right=True):
        x0, y0 = p_obj; x1, y1 = p_txt
        x2 = x1 + (1.0 if right else -1.0)
        self.pl([(x0, y0), (x1, y1), (x2, y1)], 'D32_PNP_DIMENSI')
        self.m.add_circle(self.P(x0, y0), 0.04, dxfattribs={'layer': 'D32_PNP_DIMENSI'})
        h_ = self.m.add_hatch(dxfattribs={'layer': 'D32_PNP_DIMENSI'}); h_.set_solid_fill(color=7)
        h_.paths.add_edge_path().add_arc(self.P(x0, y0), 0.04, 0, 360)
        att = MTextEntityAlignment.MIDDLE_LEFT if right else MTextEntityAlignment.MIDDLE_RIGHT
        self.mtext((x2 + (0.08 if right else -0.08), y1), s, h=h, att=att)
    def dim(self, x0, x1, y, ydim, text=None, loc=None):
        d = self.m.add_linear_dim(base=self.P((x0 + x1) / 2, ydim), p1=self.P(x0, y), p2=self.P(x1, y), dimstyle='D32_1-100',
                                  text=text if text else '<>', location=self.P(*loc) if loc else None, dxfattribs={'layer': 'D32_PNP_DIMENSI'})
        d.render()
    def dimline(self, x0, x1, y, ydim):
        L = 'D32_PNP_DIMENSI'
        self.line((x0, y - 0.06), (x0, ydim - 0.08), L); self.line((x1, y - 0.06), (x1, ydim - 0.08), L)
        self.line((x0 - 0.06, ydim), (x1 + 0.06, ydim), L)
        for xx in (x0, x1): self.line((xx - 0.06, ydim - 0.06), (xx + 0.06, ydim + 0.06), L)
    def elev(self, x, y, s):
        self.pl([(x - 0.12, y + 0.2), (x + 0.12, y + 0.2), (x, y), (x - 0.12, y + 0.2)], 'D32_PNP_DIMENSI', closed=True)
        self.line((x - 0.12, y + 0.2), (x + 0.9, y + 0.2), 'D32_PNP_DIMENSI')
        self.text((x + 0.05, y + 0.25), s, h=TH * 0.8, align='BOTTOM_LEFT')

# ------------------------------------------------------------- simbol tampak
def cloud(pen, cx, cy, rx, ry, layer='D32_PNP_VEGETASI', n=11):
    pts = []
    for i in range(n * 6 + 1):
        t = 2 * math.pi * i / (n * 6)
        bump = 1 + 0.07 * abs(math.sin(n * t / 2))
        pts.append((cx + rx * bump * math.cos(t), cy + ry * bump * math.sin(t)))
    pen.pl(pts, layer)

def pohon(pen, x, base, h=4.6, r=1.4):
    pen.pl([(x - 0.11, base), (x - 0.09, base + h - 1.6 * r), (x - 0.5, base + h - 1.0 * r)], 'D32_PNP_VEGETASI')
    pen.pl([(x + 0.11, base), (x + 0.09, base + h - 1.6 * r), (x + 0.45, base + h - 0.9 * r)], 'D32_PNP_VEGETASI')
    pen.line((x, base + h - 1.5 * r), (x + 0.1, base + h - 0.6 * r), 'D32_PNP_VEGETASI')
    cloud(pen, x, base + h - r * 0.75, r, r * 0.8)
    cloud(pen, x - r * 0.45, base + h - r * 1.05, r * 0.55, r * 0.45, n=7)
    cloud(pen, x + r * 0.5, base + h - r * 1.0, r * 0.55, r * 0.45, n=7)

def perdu(pen, x0, x1, base, h=1.4):
    n = max(2, int((x1 - x0) / 0.3)); w = (x1 - x0) / n
    for i in range(n):
        cloud(pen, x0 + w * (i + 0.5), base + h * 0.55, w * 0.75, h * 0.48, n=5)

def tiang(pen, x, base, jenis, arah=1):
    """arah = +1 lengan ke kanan, -1 ke kiri (menghadap badan jalan)."""
    L = 'D32_PNP_TAMPAK'
    if jenis == 'listrik':
        H = 8.6
        pen.pl([(x - 0.14, base), (x - 0.08, base + H), (x + 0.08, base + H), (x + 0.14, base)], L, closed=True)
        pen.rect(x - 0.22, base - 0.02, x + 0.22, base + 0.06, L)
        for yy, w in ((H - 0.45, 0.85), (H - 1.05, 0.65)):
            pen.rect(x - w, base + yy - 0.05, x + w, base + yy + 0.05, L)
            for k in (-w + 0.1, 0.0, w - 0.1):
                if abs(k) < 0.05 and yy < H - 0.5: continue
                pen.rect(x + k - 0.035, base + yy + 0.05, x + k + 0.035, base + yy + 0.2, L)
        pen.pl([(x - 0.08, base + H - 0.45), (x - 0.5, base + H - 0.9)], L); pen.pl([(x + 0.08, base + H - 0.45), (x + 0.5, base + H - 0.9)], L)
        for yy in [2.4 + 0.42 * i for i in range(10)]:
            pen.line((x + 0.11, base + yy), (x + 0.3, base + yy), L)
        ax0 = x + arah * 0.1; ay = base + 6.3
        pen.pl([(ax0, ay), (ax0 + arah * 0.5, ay + 0.35), (ax0 + arah * 1.1, ay + 0.48), (ax0 + arah * 1.6, ay + 0.45)], L)
        pen.pl([(ax0, ay - 0.35), (ax0 + arah * 0.55, ay + 0.15)], L)
        hx = ax0 + arah * 1.6
        pen.pl([(hx - arah * 0.05, ay + 0.5), (hx + arah * 0.45, ay + 0.5), (hx + arah * 0.4, ay + 0.36), (hx, ay + 0.36)], L, closed=True)
    else:
        H = 6.5
        pen.pl([(x - 0.09, base), (x - 0.05, base + H), (x + 0.05, base + H), (x + 0.09, base)], L, closed=True)
        pen.rect(x - 0.2, base - 0.02, x + 0.2, base + 0.05, L)
        pen.rect(x - 0.12, base + 0.05, x + 0.12, base + 0.85, L)
        pen.arc((x + arah * 0.9, base + H - 0.15), 0.9, 90 if arah > 0 else 0, 180 if arah > 0 else 90, L)
        tip = (x + arah * 0.9, base + H + 0.75)
        pen.pl([tip, (tip[0] + arah * 0.75, tip[1] + 0.05)], L)
        hx = tip[0] + arah * 0.75
        pen.pl([(hx - arah * 0.1, tip[1] + 0.12), (hx + arah * 0.55, tip[1] + 0.12), (hx + arah * 0.5, tip[1] - 0.04), (hx, tip[1] - 0.04)], L, closed=True)

def orang(pen, x, base, h=1.65):
    s = h / 1.65
    pen.circle((x, base + 1.53 * s), 0.11 * s, 'D32_PNP_FIGUR')
    pen.pl([(x - 0.08 * s, base), (x - 0.11 * s, base + 0.8 * s), (x - 0.2 * s, base + 1.38 * s), (x + 0.2 * s, base + 1.38 * s),
            (x + 0.11 * s, base + 0.8 * s), (x + 0.08 * s, base)], 'D32_PNP_FIGUR')
    pen.line((x, base + 0.05 * s), (x, base + 0.8 * s), 'D32_PNP_FIGUR')

def mobil(pen, x, base):
    w, h = 1.7, 1.5
    pen.pl([(x - w / 2, base + 0.35), (x - w / 2, base + 0.9), (x - w * 0.38, base + h), (x + w * 0.38, base + h), (x + w / 2, base + 0.9), (x + w / 2, base + 0.35)], 'D32_PNP_FIGUR', closed=True)
    pen.pl([(x - w * 0.33, base + 0.95), (x - w * 0.27, base + h - 0.08), (x + w * 0.27, base + h - 0.08), (x + w * 0.33, base + 0.95)], 'D32_PNP_FIGUR', closed=True)
    for dx in (-w * 0.33, w * 0.33): pen.rect(x + dx - 0.12, base, x + dx + 0.12, base + 0.35, 'D32_PNP_FIGUR')

def motor(pen, x, base):
    pen.pl([(x - 0.12, base), (x - 0.18, base + 0.75), (x + 0.18, base + 0.75), (x + 0.12, base)], 'D32_PNP_FIGUR', closed=True)
    pen.line((x - 0.4, base + 1.0), (x + 0.4, base + 1.0), 'D32_PNP_FIGUR')
    orang(pen, x, base + 0.55, h=1.15)

def sepeda(pen, x, base):
    for dx in (-0.35, 0.35): pen.circle((x + dx, base + 0.33), 0.33, 'D32_PNP_FIGUR')
    pen.pl([(x - 0.35, base + 0.33), (x, base + 0.75), (x + 0.35, base + 0.33)], 'D32_PNP_FIGUR')
    orang(pen, x, base + 0.7, h=1.0)

def rumah(pen, x0, x1, left, label):
    pen.pl([(x0, 0.05), (x1, 0.05)], 'D32_PNP_TAMPAK')
    wx0, wx1 = (x0, x1 - 0.5) if left else (x0 + 0.5, x1)
    pen.pl([(wx0, 0.05), (wx0, 3.4), (wx1, 3.4), (wx1, 0.05)], 'D32_PNP_TAMPAK')
    pen.pl([(wx0 - 0.3, 3.4), ((wx0 + wx1) / 2, 5.0), (wx1 + 0.3, 3.4)], 'D32_PNP_TAMPAK')
    dx = (wx0 + wx1) / 2
    pen.rect(dx - 0.45, 0.05, dx + 0.45, 2.15, 'D32_PNP_TAMPAK')
    pen.text(((wx0 + wx1) / 2, 2.75), label, h=TH * 0.8)

# ------------------------------------------------------------- konstruksi per elemen
def tanah_dasar(pen, x0, x1, top=-0.25, bot=-0.85):
    pen.hatch([(x0, bot), (x1, bot), (x1, top), (x0, top)], 'EARTH', 0.035, 45, 'D32_PNP_ARSIR_TANAH')

def u_ditch(pen, x0, x1, top, depth=0.6, wall=0.07, cover=False, label=None):
    pen.pl([(x0, top), (x0, top - depth), (x1, top - depth), (x1, top)], 'D32_PNP_POTONGAN')
    pen.pl([(x0 + wall, top), (x0 + wall, top - depth + wall), (x1 - wall, top - depth + wall), (x1 - wall, top)], 'D32_PNP_POTONGAN')
    for pts in ([(x0, top - depth), (x0 + wall, top - depth), (x0 + wall, top), (x0, top)],
                [(x1 - wall, top - depth), (x1, top - depth), (x1, top), (x1 - wall, top)],
                [(x0 + wall, top - depth), (x1 - wall, top - depth), (x1 - wall, top - depth + wall), (x0 + wall, top - depth + wall)]):
        pen.hatch(pts, 'AR-CONC', 0.003)
    wl = top - depth + wall + 0.15
    pen.line((x0 + wall + 0.02, wl), (x1 - wall - 0.02, wl), 'D32_PNP_AIR')
    pen.line((x0 + wall + 0.08, wl - 0.05), (x1 - wall - 0.08, wl - 0.05), 'D32_PNP_AIR')
    if cover:
        pen.rect(x0, top - 0.04, x1, top, 'D32_PNP_POTONGAN', hatch='STEEL', scale=0.01)
    tanah_dasar(pen, x0 - 0.15, x1 + 0.15, top - depth, top - depth - 0.2)

def build_section(msp, ox, oy, key, which):
    pen = Pen(msp, ox, oy)
    els = ROADS[key][which]
    x = 0.0
    spans = []
    n = len(els)
    _x = 0.0; road_mid = 0.0
    for e_ in els:
        if e_['t'] == 'jalan': road_mid = _x + e_['w'] / 2
        _x += e_['w']
    for i, e in enumerate(els):
        t, w = e['t'], e['w']; x0, x1 = x, x + w
        ren = (which == 'ren')
        if t == 'persil':
            kind = e.get('kind', 'rumah')
            if kind in ('lahan', 'taman'):
                pen.pl([(x0, 0.05), (x1, 0.05)], 'D32_PNP_POTONGAN')
                tanah_dasar(pen, x0, x1, 0.05, -0.6)
                if kind == 'taman':
                    pohon(pen, x0 + 1.5, 0.05, 4.6, 1.3)
                    pen.text(((x0 + x1) / 2, -1.0), 'TAMAN RT A', h=TH, align='MIDDLE_CENTER')
                else:
                    perdu(pen, x0 + 0.4, x0 + 1.6, 0.05, 0.8)
                    pen.text(((x0 + x1) / 2, 2.0), 'Lahan kosong', h=TH * 0.8)
                    pen.text(((x0 + x1) / 2, 1.65), '(rencana Taman RT A)', h=TH * 0.8)
            else:
                pen.pl([(x0, 0.05), (x1, 0.05)], 'D32_PNP_POTONGAN')
                tanah_dasar(pen, x0, x1, 0.05, -0.6)
                lbl = {'rumah': 'PERSIL WARGA', 'sekolah': 'ZONA PENDIDIKAN'}[kind]
                pen.text(((x0 + x1) / 2, 0.55), lbl, h=TH * 0.8)
                pen.text(((x0 + x1) / 2, 0.22), '(tidak diubah)', h=TH * 0.7)
            x = x1; continue
        if t == 'rel':
            pen.pl([(x0 + 0.4, 0.05), (x1 - 0.8, 0.05), (x1 - 1.4, 0.6), (x0 + 1.0, 0.6)], 'D32_PNP_POTONGAN', closed=True)
            pen.hatch([(x0 + 0.4, 0.05), (x1 - 0.8, 0.05), (x1 - 1.4, 0.6), (x0 + 1.0, 0.6)], 'GRAVEL', 0.02)
            for rx in (x0 + 1.6, x0 + 3.0):
                pen.rect(rx - 0.07, 0.6, rx + 0.07, 0.78, 'D32_PNP_POTONGAN', hatch='SOLID')
            pen.rect(x0 + 1.2, 0.48, x0 + 3.4, 0.6, 'D32_PNP_POTONGAN', hatch='AR-CONC', scale=0.003)
            pen.text(((x0 + x1) / 2 - 0.3, 1.4), 'REL KA', h=TH)
            tanah_dasar(pen, x0, x1, 0.05, -0.6)
            pen.pl([(x0, 0.05), (x0 + 0.4, 0.05)], 'D32_PNP_POTONGAN'); pen.pl([(x1 - 0.8, 0.05), (x1, 0.05)], 'D32_PNP_POTONGAN')
            x = x1; continue
        spans.append((x0, x1, e))
        if t == 'jalan':
            pen.rect(x0, -0.05, x1, 0.0, 'D32_PNP_POTONGAN', hatch='AR-SAND', scale=0.002)
            pen.rect(x0, -0.25, x1, -0.05, 'D32_PNP_KONSTRUKSI', hatch='GRAVEL', scale=0.012)
            tanah_dasar(pen, x0, x1, -0.25, -0.75)
            if e.get('lanes', 2) == 2:
                pen.line(((x0 + x1) / 2, -0.3), ((x0 + x1) / 2, 7.4), 'D32_PNP_AS')
            veh = e.get('veh') or (None, None)
        elif t in ('bahu', 'furn'):
            pen.pl([(x0, -0.02), (x1, -0.02)], 'D32_PNP_POTONGAN')
            tanah_dasar(pen, x0, x1, -0.02, -0.75)
        elif t == 'bahu_keras':
            pen.rect(x0, -0.10, x1, 0.0, 'D32_PNP_POTONGAN', hatch='AR-CONC', scale=0.003)
            tanah_dasar(pen, x0, x1, -0.10, -0.75)
        elif t == 'drain_o':
            u_ditch(pen, x0, x1, 0.0, depth=0.55, wall=0.06)
        elif t == 'drain_c':
            u_ditch(pen, x0, x1, 0.0, depth=0.6, wall=0.07, cover=True)
        elif t in ('trotoar', 'pedsep'):
            dr = e.get('drain', 0)
            road_right = (i + 1 < n and els[i + 1]['t'] == 'jalan')
            kx0, kx1 = (x1 - 0.15, x1) if road_right else (x0, x0 + 0.15)
            pen.rect(kx0, -0.25, kx1, 0.15, 'D32_PNP_POTONGAN', hatch='AR-CONC', scale=0.003)
            sx0, sx1 = (x0, kx0) if road_right else (kx1, x1)
            pen.rect(sx0, 0.09, sx1, 0.15, 'D32_PNP_POTONGAN', hatch='AR-HBONE' if t == 'trotoar' else 'AR-B816', scale=0.006)
            pen.rect(sx0, 0.04, sx1, 0.09, 'D32_PNP_KONSTRUKSI', hatch='AR-SAND', scale=0.002)
            if dr:
                dx0, dx1 = (kx0 - dr, kx0) if road_right else (kx1, kx1 + dr)
                u_ditch(pen, dx0, dx1, 0.04, depth=0.6, wall=0.07, cover=False)
                rest = (sx0, dx0) if road_right else (dx1, sx1)
            else:
                rest = (sx0, sx1)
            if rest[1] - rest[0] > 0.05:
                pen.hatch([(rest[0], -0.6), (rest[1], -0.6), (rest[1], 0.04), (rest[0], 0.04)], 'EARTH', 0.035, 45, 'D32_PNP_ARSIR_TANAH')
            if t == 'pedsep':
                pen.text((x0 + w * 0.5, 0.45), 'JALUR SEPEDA', h=TH * 0.6)
        elif t in ('hijau', 'pagar'):
            pen.rect(x0, -0.25, x0 + 0.08, 0.2, 'D32_PNP_POTONGAN', hatch='AR-CONC', scale=0.003)
            pen.rect(x1 - 0.08, -0.25, x1, 0.2, 'D32_PNP_POTONGAN', hatch='AR-CONC', scale=0.003)
            pen.pl([(x0 + 0.08, 0.15), (x1 - 0.08, 0.15)], 'D32_PNP_POTONGAN')
            pen.hatch([(x0 + 0.08, -0.6), (x1 - 0.08, -0.6), (x1 - 0.08, 0.15), (x0 + 0.08, 0.15)], 'GRASS', 0.01, 0, 'D32_PNP_ARSIR_TANAH')
            if t == 'hijau': pohon(pen, (x0 + x1) / 2 + 0.05, 0.15, 3.8, 1.0)
            else: perdu(pen, x0, x1, 0.2, 1.5)
        if e.get('pole') or (t == 'hijau' and e.get('lamp')):
            px_ = (x0 + 0.1) if t == 'hijau' else (x0 + x1) / 2
            tiang(pen, px_, 0.2 if t == 'hijau' else 0, e.get('pole', 'pju'), arah=1 if px_ < road_mid else -1)
        x = x1
    total = x
    a, b = spans[0][0], spans[-1][1]
    # batas ruang milik jalan
    for xx in (a, b): pen.line((xx, -1.0), (xx, 6.0), 'D32_PNP_BATAS_RMJ')
    # dimensi bertingkat: lajur (atas), elemen + nama (bawah), ruang milik jalan
    NAMA = {'jalan': 'Badan Jalan', 'trotoar': 'Trotoar', 'pedsep': 'Jalur Pejalan & Sepeda', 'drain_o': 'Drainase', 'drain_c': 'Saluran Tertutup',
            'bahu': 'Bahu Tanah', 'bahu_keras': 'Bahu', 'furn': 'Furnitur', 'hijau': 'Jalur Hijau', 'pagar': 'Pagar Hijau'}
    jl = [s_ for s_ in spans if s_[2]['t'] == 'jalan'][0]
    nl = jl[2].get('lanes', 2)
    if nl == 2:
        m = (jl[0] + jl[1]) / 2
        for a_, b_ in ((jl[0], m), (m, jl[1])):
            pen.dim(a_, b_, 0.0, 1.15)
            pen.text(((a_ + b_) / 2, 1.02), 'Lebar Lajur' if (b_ - a_) >= 1.5 else 'Lajur', h=TH * 0.7, align='TOP_CENTER')
    else:
        pen.dim(jl[0], jl[1], 0.0, 1.15); pen.text(((jl[0] + jl[1]) / 2, 1.02), 'Lajur Berbagi (2 arah)', h=TH * 0.7, align='TOP_CENTER')
    lvl = 0
    for idx, (x0, x1, e) in enumerate(spans):
        w = x1 - x0; nm_ = NAMA.get(e['t'], '')
        yb = -0.9 if e['t'] not in ('drain_o', 'drain_c') else -0.62
        if w >= 0.95:
            pen.dim(x0, x1, yb, -1.35)
            pen.text(((x0 + x1) / 2, -1.48), nm_, h=TH * 0.72, align='TOP_CENTER')
        else:
            pen.dimline(x0, x1, yb, -1.35)
            lvl_y = -1.98 - 0.42 * (lvl % 3); lvl += 1
            cxm = (x0 + x1) / 2
            pen.line((cxm, -1.38), (cxm, lvl_y + 0.05), 'D32_PNP_DIMENSI')
            v = ('%.2f' % w).rstrip('0').rstrip('.').replace('.', ',')
            pen.text((cxm + 0.05, lvl_y), '%s m  %s' % (v, nm_), h=TH * 0.62, align='MIDDLE_LEFT' if cxm < total / 2 else 'MIDDLE_RIGHT')
    a, b = spans[0][0], spans[-1][1]
    for xx in (a, b): pen.line((xx, -1.0), (xx, 5.0), 'D32_PNP_BATAS_RMJ')
    pen.dim(a, b, -0.9, -3.35, text='<> m')
    pen.text(((a + b) / 2, -3.48), 'Ruang Milik Jalan', h=TH * 0.75, align='TOP_CENTER')
    # elevasi
    jl = [s for s in spans if s[2]['t'] == 'jalan'][0]
    pen.elev(jl[1] - 1.05, 0.0, '±0,00')
    tr = [s for s in spans if s[2]['t'] in ('trotoar', 'pedsep')]
    if tr: pen.elev(tr[0][0] + 0.25, 0.15, '+0,15')
    # leader material
    notes = {
        'jalan': ('Perkerasan aspal AC-WC t=5 cm\nLapis pondasi agregat kelas A t=20 cm' if which == 'ren' else 'Perkerasan aspal eksisting'),
        'trotoar': 'Paving block t=6 cm + pasir t=5 cm\nKanstin beton 15x40 cm (+0,15)',
        'pedsep': 'Jalur pejalan & sepeda: paving t=6 cm\nmarka sepeda, kanstin beton 15x40 cm',
        'drain_c': 'Saluran U-ditch beton + tutup grill baja',
        'drain_o': 'Saluran terbuka eksisting',
        'bahu': 'Bahu tanah eksisting', 'bahu_keras': 'Bahu beton t=10 cm',
        'hijau': 'Jalur hijau: ketapang kencana + PJU',
        'pagar': 'Pagar hijau perdu h=1,5 m (bambu pagar / teh-tehan)',
        'furn': 'Tiang PJU / listrik eksisting',
    }
    calls = []; used = set()
    for x0, x1, e in spans:
        t = e['t']
        if t in used or t not in notes: continue
        used.add(t); calls.append(((x0 + x1) / 2, t))
    calls.sort()
    bx = []
    for cx_, t in calls:
        b = cx_ if not bx else max(cx_, bx[-1] + 0.62)
        bx.append(b)
    shift = max(0.0, bx[-1] - (total - 0.3)) if bx else 0
    bx = [b - shift for b in bx]
    for i, ((cx_, t), b) in enumerate(zip(calls, bx)):
        pen.pl([(cx_, -0.25), (cx_, -0.6)], 'D32_PNP_DIMENSI'); pen.text((cx_, -0.68), str(i + 1), h=0.16, align='TOP_CENTER')
        pen.circle((b, -4.25), 0.22, 'D32_PNP_DIMENSI')
        pen.text((b, -4.25), str(i + 1), h=0.19)
        lines = notes[t].split('\n')
        pen.text((0.0, -4.85 - i * 0.4), '%d.  %s' % (i + 1, '; '.join(lines)), h=0.19, align='MIDDLE_LEFT')
    k = len(calls)
    # label sisi
    r = ROADS[key]
    pen.text((0.0, 7.6), r['kiri'].upper(), h=TH * 0.7, align='BOTTOM_LEFT')
    pen.text((total, 7.6), r['kanan'].upper(), h=TH * 0.7, align='BOTTOM_RIGHT')
    return total, -4.85 - 0.4 * k

SECTIONS = [('betet', 'A', "POTONGAN A-A'", 'JL. BETET'),
            ('cendrawasih_b1', 'B1', "POTONGAN B1-B1'", 'JL. CENDRAWASIH - SEGMEN PERMUKIMAN'),
            ('cendrawasih_b2', 'B2', "POTONGAN B2-B2'", 'JL. CENDRAWASIH - SEGMEN TEPI REL'),
            ('letkol', 'C', "POTONGAN C-C'", 'JL. LETKOL SUDARSO')]

def denah(msp, ox, oy, cut_key, half_len=24.0, half_w=7.5):
    sys.path.insert(0, HERE)
    import desain_jalan as DJ, scene
    from shapely.geometry import Point, Polygon, box
    from shapely import affinity
    nm = {'A': 'BETET', 'B1': 'CENDRAWASIH_B1', 'B2': 'CENDRAWASIH_B2', 'C': 'LETKOL'}[cut_key]
    D = DJ.build(); r = D[nm]; L = DJ.CL[nm]
    a, b = scene.POTONG[cut_key]
    mid = Point((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    d0 = L.project(mid); p = L.interpolate(d0); q = L.interpolate(min(L.length, d0 + 1)); q0 = L.interpolate(max(0, d0 - 1))
    ang = math.degrees(math.atan2(q.y - q0.y, q.x - q0.x))
    win = affinity.rotate(box(p.x - half_len, p.y - half_w, p.x + half_len, p.y + half_w), ang, origin=p)
    def tr(g):
        g = affinity.rotate(g, -ang, origin=p); return affinity.translate(g, ox - p.x, oy - p.y)
    def draw(g, layer, pat=None, sc=0.02, ang_=0):
        g = g.intersection(win)
        for pg in getattr(g, 'geoms', [g]):
            if pg.is_empty or pg.geom_type != 'Polygon' or pg.area < 0.05: continue
            pg = tr(pg)
            if pat:
                h = msp.add_hatch(dxfattribs={'layer': 'D32_PNP_ARSIR'})
                if pat == 'SOLID': h.set_solid_fill(color=252)
                else: h.set_pattern_fill(pat, scale=sc, angle=ang_)
                h.paths.add_polyline_path(list(pg.exterior.coords)[:-1], is_closed=True)
            msp.add_lwpolyline(list(pg.exterior.coords)[:-1], close=True, dxfattribs={'layer': layer})
    draw(DJ.ROADS, 'D32_PNP_TAMPAK')
    draw(DJ.BUILD, 'D32_PNP_TAMPAK', 'ANSI31', 2.5, 0)
    draw(r['aspal'].difference(DJ.BUILD.buffer(0.15)), 'D32_PNP_POTONGAN', 'AR-SAND', 0.09)
    for k, pat, sc in (('trotoar', 'AR-HBONE', 0.025), ('pedsep', 'AR-B816', 0.025), ('hijau', 'GRASS', 0.04), ('pagar', 'GRASS', 0.04),
                       ('saluran', 'AR-CONC', 0.01), ('bahu', 'AR-CONC', 0.01)):
        if k in r: draw(r[k], 'D32_PNP_KONSTRUKSI', pat, sc)
    for t in r['pohon'] + []:
        if win.contains(t):
            c = tr(t); msp.add_circle((c.x, c.y), 1.7, dxfattribs={'layer': 'D32_PNP_VEGETASI'})
            cloud(Pen(msp, 0, 0), c.x, c.y, 1.6, 1.6, n=9)
            msp.add_line((c.x - 0.3, c.y), (c.x + 0.3, c.y), dxfattribs={'layer': 'D32_PNP_VEGETASI'})
            msp.add_line((c.x, c.y - 0.3), (c.x, c.y + 0.3), dxfattribs={'layer': 'D32_PNP_VEGETASI'})
    for t in r['pju']:
        if win.contains(t):
            c = tr(t); msp.add_circle((c.x, c.y), 0.3, dxfattribs={'layer': 'D32_PNP_TAMPAK'})
            msp.add_line((c.x - 0.45, c.y - 0.45), (c.x + 0.45, c.y + 0.45), dxfattribs={'layer': 'D32_PNP_TAMPAK'})
    for seg in r.get('marka', []):
        g = seg.intersection(win)
        if not g.is_empty and g.geom_type == 'LineString':
            msp.add_lwpolyline(list(tr(g).coords), dxfattribs={'layer': 'D32_PNP_TAMPAK', 'const_width': 0.12})
    for zname, strips in DJ.zebras().items():
        for s_ in strips:
            if win.intersects(s_): draw(s_, 'D32_PNP_TAMPAK', 'SOLID')
    # garis potong
    from shapely.geometry import LineString as _LS
    cut = _LS([a, b])
    dx_, dy_ = b[0] - a[0], b[1] - a[1]; ln_ = math.hypot(dx_, dy_); ux, uy = dx_ / ln_, dy_ / ln_
    cut = _LS([(p.x - ux * (half_w - 1.2), p.y - uy * (half_w - 1.2)), (p.x + ux * (half_w - 1.2), p.y + uy * (half_w - 1.2))])
    ca, cb = tr(Point(cut.coords[0])), tr(Point(cut.coords[1]))
    msp.add_lwpolyline([(ca.x, ca.y), (cb.x, cb.y)], dxfattribs={'layer': 'D32_PNP_BATAS_RMJ', 'color': 1, 'const_width': 0.06, 'ltscale': 1.5})
    for c, lab in ((ca, cut_key), (cb, cut_key + "'")):
        msp.add_circle((c.x, c.y), 0.8, dxfattribs={'layer': 'D32_PNP_TEKS', 'color': 1})
        t = msp.add_text(lab, dxfattribs={'height': 0.7, 'style': ARIAL, 'color': 1}); t.set_placement((c.x, c.y), align=TextEntityAlignment.MIDDLE_CENTER)
    wb = tr(win).bounds
    msp.add_lwpolyline([(wb[0], wb[1]), (wb[2], wb[1]), (wb[2], wb[3]), (wb[0], wb[3])], close=True, dxfattribs={'layer': 'D32_PNP_TEKS'})
    t = msp.add_text('DENAH RUAS SEKITAR POTONGAN %s  |  SKALA 1:200' % cut_key, dxfattribs={'height': 0.6, 'style': ARIAL, 'layer': 'D32_PNP_TEKS'})
    t.set_placement((wb[0], wb[3] + 0.5), align=TextEntityAlignment.BOTTOM_LEFT)
    # panah utara (rotasi mengikuti denah)
    nx, ny = wb[2] - 2.5, wb[3] - 3.2
    th = math.radians(90 - ang)
    tip = (nx + 1.6 * math.cos(th), ny + 1.6 * math.sin(th)); tail = (nx - 1.0 * math.cos(th), ny - 1.0 * math.sin(th))
    msp.add_line(tail, tip, dxfattribs={'layer': 'D32_PNP_TEKS'})
    left = (tip[0] - 0.6 * math.cos(th) + 0.35 * math.sin(th), tip[1] - 0.6 * math.sin(th) - 0.35 * math.cos(th))
    right = (tip[0] - 0.6 * math.cos(th) - 0.35 * math.sin(th), tip[1] - 0.6 * math.sin(th) + 0.35 * math.cos(th))
    msp.add_lwpolyline([tip, left, right], close=True, dxfattribs={'layer': 'D32_PNP_TEKS'})
    t = msp.add_text('U', dxfattribs={'height': 0.8, 'style': ARIAL}); t.set_placement((tip[0] + 0.9 * math.cos(th), tip[1] + 0.9 * math.sin(th)), align=TextEntityAlignment.MIDDLE_CENTER)
    return wb

def keyplan(lay, x0, y0, w, h, cut_key):
    import geopandas as gpd
    sys.path.insert(0, HERE)
    import scene
    dl = gpd.read_file('/home/user/RancangKota/Delineasi Tapak D3.2 Baru/Delineasi Tapak D3.2 Baru.shp').to_crs(32749).geometry.iloc[0]
    cl = json.load(open(os.path.join(HERE, 'ruas_cl.json')))
    bx0, by0, bx1, by1 = dl.bounds
    s = min(w / (bx1 - bx0), h / (by1 - by0)) * 0.92
    T = lambda X, Y: (x0 + (w - (bx1 - bx0) * s) / 2 + (X - bx0) * s, y0 + (h - (by1 - by0) * s) / 2 + (Y - by0) * s)
    lay.add_lwpolyline([T(*q) for q in dl.exterior.coords], close=True, dxfattribs={'layer': 'D32_KOP_TIPIS', 'color': 6})
    hi = {'A': ['BETET'], 'B1': ['CENDRAWASIH_B1'], 'B2': ['CENDRAWASIH_B2'], 'C': ['LETKOL']}[cut_key]
    for nm, pts in cl.items():
        lay.add_lwpolyline([T(*q) for q in pts], dxfattribs={'layer': 'D32_KOP_TIPIS', 'color': 1 if nm in hi else 8,
                                                              'const_width': 1.0 if nm in hi else 0.35})
    a, b = scene.POTONG[cut_key]
    lay.add_line(T(*a), T(*b), dxfattribs={'layer': 'D32_KOP', 'color': 1})
    for p, lab in ((a, cut_key), (b, cut_key + "'")):
        c = T(*p); lay.add_circle(c, 2.2, dxfattribs={'layer': 'D32_KOP', 'color': 1})
        t = lay.add_text(lab, dxfattribs={'height': 1.8, 'style': ARIAL, 'color': 1}); t.set_placement(c, align=TextEntityAlignment.MIDDLE_CENTER)

def kop(lay, cut_key, title, sub, sheet_no):
    X0, Y0, X1, Y1 = 10, 10, 410, 287
    lay.add_lwpolyline([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)], close=True, dxfattribs={'layer': 'D32_KOP', 'lineweight': 70})
    KX = 305
    lay.add_line((KX, Y0), (KX, Y1), dxfattribs={'layer': 'D32_KOP'})
    def T(x, y, s, h, al='TOP_LEFT', bold=False):
        t = lay.add_text(s, dxfattribs={'height': h, 'style': ARIAL, 'layer': 'D32_KOP_TIPIS'}); t.set_placement((x, y), align=TextEntityAlignment[al]); return t
    def hl(y): lay.add_line((KX, y), (X1, y), dxfattribs={'layer': 'D32_KOP'})
    cx = (KX + X1) / 2
    T(cx, 282, 'PENAMPANG JALAN', 5.0, 'TOP_CENTER'); T(cx, 274.5, 'PERMUKIMAN', 5.0, 'TOP_CENTER')
    T(cx, 266, 'KAWASAN PASAR INDUK KROYA', 2.8, 'TOP_CENTER')
    T(cx, 261.5, '"KROYA SMART UNIFIED MARKET"', 2.4, 'TOP_CENTER')
    T(cx, 257.5, 'KEC. KROYA, KAB. CILACAP, JAWA TENGAH', 2.0, 'TOP_CENTER')
    hl(252)
    T(cx, 248, title, 4.0, 'TOP_CENTER'); T(cx, 241.5, sub, 2.4, 'TOP_CENTER')
    T(cx, 236.5, 'EKSISTING (KIRI) & RENCANA (KANAN)', 2.0, 'TOP_CENTER')
    hl(231)
    T(KX + 4, 227, 'KEY PLAN', 2.4)
    keyplan(lay, KX + 4, 180, X1 - KX - 8, 44, cut_key)
    hl(176)
    T(KX + 4, 172, 'LEGENDA ARSIR', 2.4)
    leg = [('AR-SAND', 0.05, 'Aspal AC-WC'), ('GRAVEL', 0.3, 'Agregat kelas A'), ('AR-CONC', 0.08, 'Beton (kanstin, U-ditch)'),
           ('AR-HBONE', 0.15, 'Paving block trotoar'), ('AR-B816', 0.15, 'Paving jalur sepeda'), ('EARTH', 0.3, 'Tanah dasar / urug'),
           ('GRASS', 0.25, 'Tanah taman / jalur hijau'), ('STEEL', 0.25, 'Tutup grill baja')]
    for i, (pat, sc, s) in enumerate(leg):
        y = 166 - i * 6.2
        pts = [(KX + 4, y - 4), (KX + 16, y - 4), (KX + 16, y), (KX + 4, y)]
        h = lay.add_hatch(dxfattribs={'layer': 'D32_KOP_TIPIS'}); h.set_pattern_fill(pat, scale=sc); h.paths.add_polyline_path(pts, is_closed=True)
        lay.add_lwpolyline(pts, close=True, dxfattribs={'layer': 'D32_KOP_TIPIS'})
        T(KX + 19, y - 0.6, s, 2.0)
    yy = 166 - len(leg) * 6.2 - 1
    for lt, s, col in [('PHANTOM', 'Batas ruang milik jalan / persil', 1), ('CENTER', 'As jalan', 1)]:
        lay.add_line((KX + 4, yy - 2), (KX + 16, yy - 2), dxfattribs={'layer': 'D32_KOP_TIPIS', 'linetype': lt, 'color': col, 'ltscale': 0.3})
        T(KX + 19, yy - 0.6, s, 2.0); yy -= 6.2
    hl(yy - 1)
    T(KX + 4, yy - 4, 'CATATAN', 2.4)
    notes = ['1. Ukuran dalam meter; elevasi relatif terhadap', '    muka aspal (±0,00).',
             '2. Ruang milik jalan eksisting dipertahankan;', '    rumah warga tidak dibongkar (Asistensi 4).',
             '3. Ukuran eksisting: survei kelompok D3.2 &', '    Andalalin 2023.', '4. Skala 1:100 pada kertas A3.']
    for i, s in enumerate(notes): T(KX + 4, yy - 9 - i * 3.6, s, 1.9)
    yb = 42
    hl(yb)
    T(KX + 4, yb - 3, 'STUDIO PERANCANGAN KOTA - KELOMPOK D3.2', 2.2)
    T(KX + 4, yb - 7.5, 'Departemen Perencanaan Wilayah dan Kota', 1.9)
    T(KX + 4, yb - 11, 'Dosen Pengampu: Novia Sari Ristianti, S.T., M.T.', 1.9)
    hl(yb - 15)
    T(KX + 4, yb - 18.5, 'SKALA', 1.9); T(KX + 4, yb - 22.5, '1 : 100 (A3)', 3.2)
    T(KX + 52, yb - 18.5, 'TANGGAL', 1.9); T(KX + 52, yb - 22.5, '28 Okt 2026', 2.6)
    lay.add_line((KX + 48, yb - 15), (KX + 48, Y0), dxfattribs={'layer': 'D32_KOP'})
    T(KX + 80, yb - 18.5, 'LEMBAR', 1.9); T(KX + 80, yb - 22.5, '%d / 4' % sheet_no, 3.2)
    lay.add_line((KX + 76, yb - 15), (KX + 76, Y0), dxfattribs={'layer': 'D32_KOP'})

def main(fn):
    doc = ezdxf.new('R2018', setup=True); setup(doc)
    msp = doc.modelspace()
    # hapus layout bawaan "Layout1"
    try: doc.layouts.delete('Layout1')
    except Exception: pass
    meta = []
    for row, (key, ck, title, sub) in enumerate(SECTIONS):
        oy = -row * 30.0
        for col, which in enumerate(('eks', 'ren')):
            ox = col * 22.0
            pen = Pen(msp, ox, oy)
            total, ybot = build_section(msp, ox, oy, key, which)
            jn = {'betet': 'Jl. Betet', 'cendrawasih_b1': 'Jl. Cendrawasih', 'cendrawasih_b2': 'Jl. Cendrawasih', 'letkol': 'Jl. Letkol Sudarso'}[key]
            t_ = msp.add_text(jn, dxfattribs={'height': 0.55, 'style': 'D32_TIMES', 'layer': 'D32_PNP_TEKS'})
            t_.set_placement((ox + total / 2, oy + 9.3), align=TextEntityAlignment.BOTTOM_CENTER)
            lab = '%s  -  %s' % (title, 'EKSISTING' if which == 'eks' else 'RENCANA')
            pen.text((total / 2, 8.85), lab, h=0.26, align='BOTTOM_CENTER')
            pen.line((total / 2 - len(lab) * 0.105, 8.78), (total / 2 + len(lab) * 0.105, 8.78), 'D32_PNP_TEKS')
            pen.text((total / 2, 8.45), '%s   |   SKALA 1:100' % sub, h=0.2, align='BOTTOM_CENTER')
            meta.append((key, ck, which, ox, oy, total, ybot))
        wb = denah(msp, 70.0 + 30.0, oy - 2.0, ck)
        meta.append((key, ck, 'denah', wb, None, None, None))
    # layout A3 per potongan
    for i, (key, ck, title, sub) in enumerate(SECTIONS):
        lay = doc.layouts.new('PNP_%s_%s' % (ck, sub.split(' - ')[0].replace('JL. ', '').replace(' ', '_')))
        lay.page_setup(size=(420, 297), margins=(0, 0, 0, 0), units='mm', scale=(1, 1))
        kop(lay, ck, title, sub, i + 1)
        for j, which in enumerate(('eks', 'ren')):
            _, _, _, ox, oy, total, ybot = [m for m in meta if m[0] == key and m[2] == which][0]
            vh = 17.6; vw = 14.5
            cy = oy + (10.0 + ybot) / 2
            v = lay.add_viewport(center=(85.0 + j * 147.5, 194.5), size=(vw * 10, vh * 10),
                                 view_center_point=(ox + total / 2, cy), view_height=vh)
            v.dxf.layer = 'D32_VIEWPORT'
        wb = [m for m in meta if m[0] == key and m[2] == 'denah'][0][3]
        if True:
            pw, ph = 290.0, 92.0
            v = lay.add_viewport(center=(157.5, 59.0), size=(pw, ph), view_center_point=((wb[0] + wb[2]) / 2, (wb[1] + wb[3]) / 2 + 0.4),
                                 view_height=ph / 5.0)
            v.dxf.layer = 'D32_VIEWPORT'
    doc.layouts.set_active_layout('PNP_A_BETET')
    try: doc.layouts.delete('Layout1')
    except Exception as ex: print('Layout1:', ex)
    doc.saveas(fn)
    return doc

if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, '..', 'out2', 'dxf'), exist_ok=True)
    main(os.path.join(HERE, '..', 'out2', 'dxf', 'D32_Penampang_Jalan_Permukiman_Rev28Okt.dxf'))
    print('ok')
