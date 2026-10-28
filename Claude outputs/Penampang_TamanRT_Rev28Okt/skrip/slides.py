import sys, os, textwrap
sys.path.insert(0, '..')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon as MPoly, Circle
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
from geo import px
from penampang import ROADS, ops_for, dim_ops, COL
from render import draw_ops
import konten as K, ruas, taman as T
from shapely.geometry import Point

BG = '#fdf8e7'; OL = '#4c5928'; OL2 = '#7d8a3c'; TX = '#2f3318'; MUTE = '#5b5e44'
plt.rcParams['font.family'] = 'Inter'
W, H = 11.69, 8.27
OUT = '../out/slide'
os.makedirs(OUT, exist_ok=True)
SITE = Image.open('../img/r24full.png').convert('RGB')

def new_slide(title):
    fig = plt.figure(figsize=(W, H)); fig.patch.set_facecolor(BG)
    fig.text(0.045, 0.952, 'Departemen', fontsize=9, color=OL, va='center')
    fig.text(0.045, 0.930, 'Perencanaan Wilayah dan Kota', fontsize=11, color=OL, va='center', fontweight='bold')
    fig.text(0.86, 0.958, 'Perancangan Kota', fontsize=8, color=OL, ha='right', va='center', family='DejaVu Serif', fontweight='bold')
    fig.text(0.86, 0.941, 'Kecamatan Kroya', fontsize=10.5, color=OL, ha='right', va='center', fontweight='bold')
    fig.text(0.86, 0.924, 'Kabupaten Cilacap', fontsize=8, color=OL, ha='right', va='center', family='DejaVu Serif', fontweight='bold')
    fig.text(0.955, 0.941, 'D3.2', fontsize=30, color=OL, ha='right', va='center', family='DejaVu Serif', fontweight='bold')
    fig.add_artist(plt.Line2D([0.045, 0.955], [0.905, 0.905], color=OL, lw=1.2))
    fig.text(0.5, 0.872, title, fontsize=21, color='#5b5e2a', ha='center', va='center', family='DejaVu Serif', fontweight='bold')
    return fig

def box(fig, x, y, w, h, label, lx=None, pw=0.19):
    ax = fig.add_axes([x, y, w, h]); ax.axis('off'); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(FancyBboxPatch((0.004, 0.006), 0.992, 0.975, boxstyle='round,pad=0,rounding_size=0.03',
                                fc='none', ec=OL, lw=2.0, ls=(0, (6, 3)), transform=ax.transAxes, mutation_aspect=w / h * W / H))
    lx = 0.72 if lx is None else lx
    fig.patches.append(FancyBboxPatch((x + w * lx - w * pw / 2, y + h - 0.017), w * pw, 0.034, boxstyle='round,pad=0,rounding_size=0.016',
                                      fc=OL2, ec=OL, lw=1.0, transform=fig.transFigure, figure=fig, mutation_aspect=W / H))
    fig.text(x + w * lx, y + h, label, fontsize=13, color='white', ha='center', va='center', fontweight='bold')
    return ax

def bullets(fig, x, y, w, h, lines, fs=9.2, gap=0.35):
    """tulis bullet di area figure (x,y,w,h); lines '**' = tebal; '• ' = sub-butir."""
    chars = int(w * W * 72 / (fs * 0.53))
    yy = y + h
    lh = fs / 72 / H * 1.22
    for ln in lines:
        bold = ln.startswith('**'); t = ln.lstrip('*')
        sub = t.startswith('• ')
        if sub: t = t[2:]
        indent = 0.022 if sub else 0.012
        wrapped = textwrap.wrap(t, chars - (6 if sub else 3))
        fig.text(x + (0.010 if sub else 0.0), yy, '–' if sub else '•', fontsize=fs, color=OL, va='top', fontweight='bold')
        for i, wl in enumerate(wrapped):
            fig.text(x + indent, yy - i * lh, wl, fontsize=fs, color=TX, va='top', fontweight='bold' if bold else 'normal')
        yy -= lh * (len(wrapped) + gap)
    return yy

def section_axes(fig, rect, key, which, title=None, txt=1.0, ymin=-5.3, ymax=7.6):
    els = ROADS[key][which]
    ops, dims, total = ops_for(els)
    ops += dim_ops(dims, total_label='Ruang milik jalan' if which == 'ren' else 'Ruang milik jalan eksisting')
    x0, y0, w, h = rect
    th = 0.055 * (h / 0.335) ** 0.3          # ruang judul (fraksi figure)
    ax = fig.add_axes([x0, y0, w, h - th]); ax.axis('off')
    wi, hi = w * W, (h - th) * H
    xr = (-0.4, total + 0.4)
    if (xr[1] - xr[0]) / (ymax - ymin) > wi / hi:      # dibatasi lebar
        span = (xr[1] - xr[0]) * hi / wi; ax.set_xlim(*xr); ax.set_ylim(ymin, ymin + span)
        ppm = wi * 72 / (xr[1] - xr[0])
    else:
        span = (ymax - ymin) * wi / hi; cx = total / 2
        ax.set_xlim(cx - span / 2, cx + span / 2); ax.set_ylim(ymin, ymax)
        ppm = hi * 72 / (ymax - ymin)
    ax.set_aspect('equal')
    draw_ops(ax, ops, scale_txt=txt, pt_per_m=ppm)
    r = ROADS[key]
    t = title or ('%s — %s' % (r['nama'], 'Eksisting' if which == 'eks' else 'Rencana'))
    cxf = x0 + w / 2
    fig.text(cxf, y0 + h, t, ha='center', va='top', fontsize=11.5, fontweight='bold', color=TX)
    fig.text(cxf, y0 + h - 0.024, '(%s)' % r['ket'], ha='center', va='top', fontsize=7.8, color=MUTE)
    xl0 = ax.transData.transform((-0.3, 0))[0] / fig.bbox.width
    xl1 = ax.transData.transform((total + 0.3, 0))[0] / fig.bbox.width
    yl = y0 + h - th + 0.002
    fig.text(xl0, yl, r['kiri'], ha='left', va='bottom', fontsize=7.2, color=MUTE, style='italic')
    fig.text(xl1, yl, r['kanan'], ha='right', va='bottom', fontsize=7.2, color=MUTE, style='italic')
    return ax

def site_crop(bb, lines=(), polys=(), cuts=(), scale=1.0, labels=()):
    e0, n1, e1, n0 = bb
    x0, y0 = px(e0, n1); x1, y1 = px(e1, n0)
    c = SITE.crop((int(x0), int(y0), int(x1), int(y1))).convert('RGBA')
    if scale != 1.0:
        c = c.resize((int(c.size[0] * scale), int(c.size[1] * scale)), Image.LANCZOS)
    def P(E, N):
        X, Y = px(E, N); return ((X - int(x0)) * scale, (Y - int(y0)) * scale)
    ov = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for pl, col, wd in lines:
        d.line([P(*p) for p in pl], fill=col, width=wd, joint='curve')
    for g, fill, out, wd in polys:
        for p in getattr(g, 'geoms', [g]):
            d.polygon([P(*xy) for xy in p.exterior.coords], fill=fill, outline=out, width=wd)
    c = Image.alpha_composite(c, ov)
    return c, P

def put_img(fig, rect, img, border=True):
    ax = fig.add_axes(rect); ax.imshow(img); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(OL if border else BG); s.set_linewidth(1.2)
    return ax

def cut_marker(ax, P, a, b, lab, col='#c0392b', fs=10):
    (xa, ya), (xb, yb) = P(*a), P(*b)
    ax.plot([xa, xb], [ya, yb], color=col, lw=2.2, ls=(0, (4, 2)))
    for (x, y), t in (((xa, ya), lab), ((xb, yb), lab + "'")):
        ax.add_patch(Circle((x, y), 14 * fs / 10, fc=col, ec='white', lw=1.2, zorder=5))
        ax.text(x, y, t, color='white', fontsize=fs * 0.8, ha='center', va='center', fontweight='bold', zorder=6)

def table(fig, x, ytop, w, rows, fs=8.0):
    rh = 0.028
    cw = [0.30, 0.30, 0.40]
    for i, row in enumerate(rows):
        y = ytop - (i + 1) * rh
        fc = OL2 if i == 0 else ('#f3edd2' if i % 2 else BG)
        fig.patches.append(FancyBboxPatch((x, y), w, rh, boxstyle='square,pad=0', fc=fc, ec='#d8d0b0', lw=0.6, transform=fig.transFigure, figure=fig))
        xx = x
        for j, cell in enumerate(row):
            fig.text(xx + 0.006, y + rh / 2, cell, fontsize=fs, va='center', color='white' if i == 0 else TX,
                     fontweight='bold' if (i == 0 or j == 0) else 'normal')
            xx += w * cw[j]

# ----------------------------------------------------------------- slide builder
def slide_DA(key, sec_key, kont, name, keyplan):
    r = ROADS[sec_key]
    fig = new_slide('Penampang Jalan — %s' % r['nama'])
    box(fig, 0.045, 0.385, 0.91, 0.43, 'Data')
    section_axes(fig, [0.052, 0.395, 0.45, 0.405], sec_key, 'eks', txt=1.15)
    bullets(fig, 0.515, 0.40, 0.425, 0.385, kont['data'], fs=8.8)
    box(fig, 0.045, 0.03, 0.91, 0.32, 'Analisis')
    img, P, cuts = keyplan
    iw, ih = img.size
    aw = 0.42; ah = min(0.235, aw * W / H * ih / iw); aw = ah * H / W * iw / ih
    fig.text(0.06, 0.06 + ah + 0.012, 'Lokasi ruas & garis potong (site plan Rev 24 Okt)', fontsize=8.5, color=OL, fontweight='bold', va='bottom')
    ax = put_img(fig, [0.06, 0.06, aw, ah], img)
    for a, b, lab in cuts: cut_marker(ax, P, a, b, lab)
    bullets(fig, 0.515, 0.04, 0.425, 0.285, kont['analisis'], fs=8.5, gap=0.25)
    fig.savefig(f'{OUT}/{name}.png', dpi=160, facecolor=BG); plt.close(fig); print('saved', name)

def slide_R(sec_keys, kont, name, title, note=None):
    fig = new_slide(title)
    box(fig, 0.045, 0.035, 0.91, 0.78, 'Respon', lx=0.75)
    n = len(sec_keys)
    if n == 1:
        section_axes(fig, [0.055, 0.06, 0.48, 0.72], sec_keys[0], 'ren', txt=1.0)
        yy = bullets(fig, 0.555, 0.06, 0.385, 0.72, kont['respon'], fs=8.9)
        if kont.get('tabel'):
            table(fig, 0.555, yy - 0.01, 0.385, kont['tabel'])
    else:
        for i, k in enumerate(sec_keys):
            t = {'cendrawasih_b1': 'Tipe B1 — Segmen Permukiman', 'cendrawasih_b2': 'Tipe B2 — Segmen Tepi Rel'}.get(k)
            section_axes(fig, [0.055 + i * 0.45, 0.385, 0.44, 0.40], k, 'ren', title=t, txt=1.1)
        bullets(fig, 0.06, 0.06, 0.50, 0.30, kont['respon'], fs=8.2, gap=0.2)
        if kont.get('tabel'):
            table(fig, 0.585, 0.335, 0.355, kont['tabel'], fs=7.8)
    if note:
        fig.text(0.585, 0.06, note, fontsize=7.2, color=MUTE, style='italic', va='bottom', wrap=True)
    fig.savefig(f'{OUT}/{name}.png', dpi=160, facecolor=BG); plt.close(fig); print('saved', name)

RED = (200, 40, 40, 255); BLUE = (40, 70, 200, 255); ORG = (230, 120, 0, 255); PUR = (140, 30, 140, 255); GRN = (30, 130, 30, 255)

def keyplan_full():
    bb = (305990, 9156610, 307080, 9156140)
    img, P = site_crop(bb, lines=[(ruas.BETET, RED, 9), (ruas.LETKOL, BLUE, 9), (ruas.CENDRAWASIH_B1, ORG, 9), (ruas.CENDRAWASIH_B2, PUR, 9)],
                       polys=[(T.A, (40, 160, 40, 150), GRN, 6), (T.B, (40, 160, 40, 150), GRN, 6)], scale=0.45)
    return img, P

def main():
    # --- lokasi (overview)
    img, P = keyplan_full()
    fig = new_slide('Lokasi Penampang Jalan & Taman RT')
    box(fig, 0.045, 0.035, 0.91, 0.78, 'Lokasi', lx=0.5)
    ax = put_img(fig, [0.06, 0.135, 0.88, 0.635], img)
    for k, lab in (('A', 'A'), ('B1', 'B1'), ('B2', 'B2'), ('C', 'C')):
        cut_marker(ax, P, *ruas.POTONG[k], lab, fs=9)
    for g, t in ((T.A, 'Taman RT A'), (T.B, 'Taman RT B')):
        cx, cy = P(g.centroid.x, g.centroid.y)
        ax.annotate(t, (cx, cy), (cx + 60, cy - 70), color='#1e6b1e', fontsize=9, fontweight='bold',
                    arrowprops=dict(arrowstyle='-', color='#1e6b1e', lw=1.2), bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#1e6b1e', lw=0.8))
    leg = [('#c82828', 'A–A\'  Jl. Betet'), ('#e67800', 'B1  Jl. Cendrawasih (segmen permukiman)'),
           ('#8c1e8c', 'B2  Jl. Cendrawasih (segmen tepi rel)'), ('#2846c8', 'C–C\'  Jl. Letkol Sudarso'), ('#1e821e', 'Taman RT baru')]
    for i, (c, t) in enumerate(leg):
        xx = 0.07 + (i % 3) * 0.29; yy = 0.095 - (i // 3) * 0.03
        fig.add_artist(plt.Line2D([xx, xx + 0.025], [yy, yy], color=c, lw=4))
        fig.text(xx + 0.03, yy, t, fontsize=8.5, va='center', color=TX)
    fig.text(0.94, 0.785, 'Dasar: Site Plan Rev 24 Okt 2026 (UTM 49S) · Jl. A. Yani tidak diubah (sudah didesain)', fontsize=7.5, color=MUTE, ha='right')
    fig.savefig(f'{OUT}/00_Lokasi_Penampang_TamanRT.png', dpi=160, facecolor=BG); plt.close(fig); print('saved lokasi')

    # --- key plan per ruas
    def kp(bb, lines, cutkeys, polys=(), scale=0.9):
        img, P = site_crop(bb, lines=lines, polys=polys, scale=scale)
        return img, P, [(*ruas.POTONG[k], k) for k in cutkeys]
    kp_betet = kp((305995, 9156640, 306920, 9156300), [(ruas.BETET, RED, 10)], ['A'],
                  polys=[(T.A, (40, 160, 40, 140), GRN, 4), (T.B, (40, 160, 40, 140), GRN, 4)], scale=0.42)
    kp_cend = kp((305995, 9156600, 306920, 9156200), [(ruas.CENDRAWASIH_B1, ORG, 10), (ruas.CENDRAWASIH_B2, PUR, 10)], ['B1', 'B2'],
                 polys=[(T.A, (40, 160, 40, 140), GRN, 4)], scale=0.42)
    kp_letkol = kp((306700, 9156560, 307075, 9156290), [(ruas.LETKOL, BLUE, 10)], ['C'], scale=0.75)

    slide_DA('betet', 'betet', K.BETET, '01_Betet_Data_Analisis', kp_betet)
    slide_R(['betet'], K.BETET, '02_Betet_Respon', 'Penampang Jalan — Jl. Betet (Rencana)')
    slide_DA('cendrawasih', 'cendrawasih_b1', K.CENDRAWASIH, '03_Cendrawasih_Data_Analisis', kp_cend)
    slide_R(['cendrawasih_b1', 'cendrawasih_b2'], K.CENDRAWASIH, '04_Cendrawasih_Respon', 'Penampang Jalan — Jl. Cendrawasih (Rencana)',
            note='B2: jalur pejalan & sepeda tetap di dalam ruang milik jalan (tidak memakai lahan KAI).')
    slide_DA('letkol', 'letkol', K.LETKOL, '05_LetkolSudarso_Data_Analisis', kp_letkol)
    slide_R(['letkol'], K.LETKOL, '06_LetkolSudarso_Respon', 'Penampang Jalan — Jl. Letkol Sudarso (Rencana)')

def taman_plan(ax, which):
    from matplotlib.patches import Polygon as MP
    if which == 'A':
        bb = (306040, 9156528, 306122, 9156476); geom = T.A
        parts = [(T.A, '#cfe6b0', 'Rumput'), (T.A_pagar, '#4f8a3a', None), (T.A_jalur, '#e3d3ae', None),
                 (T.A_main, '#f2c46d', None), (T.A_lap, '#b6dc8e', None), (T.A_gazebo, '#9a5b2c', None)]
        trees, benches, ent = T.A_pohon, T.A_bangku, T.A_masuk
        callouts = [(T.A_pagar.centroid, 'Pagar hijau\nperedam (sisi rel)', (-30, -14)), (T.A_main.centroid, 'Area bermain', (0, 8)),
                    (T.A_lap.centroid, 'Lapangan rumput', (6, 6)), (T.A_gazebo.centroid, 'Gazebo', (16, -3)),
                    (T.A_rumah.centroid, 'Rumah eksisting\n(tetap)', (0, -12))]
    else:
        bb = (306314, 9156505, 306394, 9156458); geom = T.B
        parts = [(T.B, '#cfe6b0', None), (T.B_plaza.intersection(T.B), '#e3d3ae', None), (T.B_main, '#f2c46d', None),
                 (T.B_gazebo, '#9a5b2c', None), (T.B_zebra, '#ffffff', None)]
        trees, benches, ent = T.B_pohon, T.B_bangku, T.B_masuk
        callouts = [(T.B_plaza.centroid, 'Plaza bazar /\npameran tempe', (-2, 2)), (T.B_main.centroid, 'Area bermain', (0, 11)),
                    (T.B_gazebo.centroid, 'Gazebo', (8, -4)), (T.BALAI.centroid, 'BALAI\nPELATIHAN\nUMKM', (14, -14)),
                    (T.B_zebra.centroid, 'Zebra cross', (10, 14)), (T.B_rumah.centroid, 'Rumah\neksisting', (0, -2))]
    e0, n1, e1, n0 = bb
    x0, y0 = px(e0, n1); x1, y1 = px(e1, n0)
    img = SITE.crop((int(x0), int(y0), int(x1), int(y1)))
    ax.imshow(img, extent=(e0, e1, n0, n1), alpha=0.55)
    for g, col, _ in parts:
        for p in getattr(g, 'geoms', [g]):
            if p.is_empty: continue
            ax.add_patch(MP(list(p.exterior.coords), closed=True, fc=col, ec='#3d6b2a' if g is geom else '#7a6a4a', lw=1.6 if g is geom else 0.5, zorder=3))
    if which == 'B':
        zb = T.B_zebra.bounds
        for k in range(6):
            yy = zb[1] + 0.3 + k * 0.55
            ax.plot([zb[0] + 0.3, zb[2] - 0.3], [yy, yy], color='#333333', lw=2.2, zorder=4)
    for t in trees:
        ax.add_patch(Circle((t.x, t.y), 1.9, fc='#5e9c43', ec='#2e5e1f', lw=0.8, alpha=0.9, zorder=5))
    for b in benches:
        ax.add_patch(MP([(b[0] - 0.9, b[1] - 0.3), (b[0] + 0.9, b[1] - 0.3), (b[0] + 0.9, b[1] + 0.3), (b[0] - 0.9, b[1] + 0.3)], closed=True, fc='#7a5230', ec='none', zorder=5))
    for (xy, t) in ent:
        ax.annotate('', xy, (xy[0], xy[1] - 6) if 'selatan' in t.lower() else (xy[0] - 7, xy[1]),
                    arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=2), zorder=6)
    for c, t, off in callouts:
        tx, ty = (off[0], off[1]) if len(off) == 3 else (c.x + off[0], c.y + off[1])
        ax.annotate(t, (c.x, c.y), (tx, ty), fontsize=6.6, ha='center', va='center', color=TX, zorder=7,
                    bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='#999999', lw=0.4, alpha=0.9),
                    arrowprops=dict(arrowstyle='-', color='#666666', lw=0.6))
    ax.set_xlim(e0, e1); ax.set_ylim(n0, n1); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(OL); s.set_linewidth(1.2)
    # skala
    ax.plot([e0 + 3, e0 + 13], [n0 + 2.5, n0 + 2.5], color='black', lw=3, zorder=8)
    ax.text(e0 + 8, n0 + 3.3, '10 m', fontsize=6.5, ha='center', va='bottom', zorder=8)
    ax.annotate('U', (e1 - 4, n1 - 3), (e1 - 4, n1 - 10), ha='center', fontsize=8, fontweight='bold', arrowprops=dict(arrowstyle='-|>', color='black', lw=1.2), zorder=8)

def slide_taman():
    fig = new_slide('Respon — Taman RT di Permukiman')
    box(fig, 0.045, 0.035, 0.91, 0.78, 'Data · Analisis · Respon', lx=0.62, pw=0.30)
    axA = fig.add_axes([0.06, 0.365, 0.43, 0.40]); taman_plan(axA, 'A')
    fig.text(0.06, 0.772, 'Taman RT A — simpang Jl. Betet–Jl. Cendrawasih, tepi rel (±%d m²)' % round(T.A.area, -1), fontsize=9, fontweight='bold', color=OL)
    axB = fig.add_axes([0.51, 0.365, 0.43, 0.40]); taman_plan(axB, 'B')
    fig.text(0.51, 0.772, 'Taman RT B — sebelah balai tempe, Jl. Ampas Waras (±%d m²)' % round(T.B.area, -1), fontsize=9, fontweight='bold', color=OL)
    fig.text(0.06, 0.325, 'Data & Analisis', fontsize=9.5, fontweight='bold', color=OL)
    bullets(fig, 0.06, 0.05, 0.40, 0.26, K.TAMAN['data'] + [
        '**Kedua lahan berada di dalam permukiman eksisting dan berdekatan dengan dua titik yang dituju warga/pengunjung (rel–Jl. Betet dan balai tempe), sehingga cocok menjadi ruang komunal tanpa mengubah massa bangunan.'], fs=8.2, gap=0.25)
    fig.text(0.51, 0.325, 'Respon', fontsize=9.5, fontweight='bold', color=OL)
    bullets(fig, 0.51, 0.05, 0.43, 0.26, K.TAMAN['respon'], fs=8.2, gap=0.25)
    fig.savefig(f'{OUT}/07_TamanRT_Respon.png', dpi=160, facecolor=BG); plt.close(fig); print('saved taman')

if __name__ == '__main__':
    main()
    slide_taman()
