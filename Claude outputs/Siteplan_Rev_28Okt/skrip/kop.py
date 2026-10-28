"""Tambahan kop (koordinat halaman PDF dalam pt, origin kiri-atas, lembar A0 3370 x 2384 pt).
Kertas DWG (mm): x_mm = x * 25.4/72 ; y_mm = (2384 - y) * 25.4/72."""
from scene import C, SP

def K(k, **kw):
    d = dict(k=k); d.update(kw); return d

def items(luas):
    out = []
    X0, X1, TX = 2286.7, 2307.0, 2312.7
    rows = [
        ('aspal', 'Jalan permukiman ditata (aspal 3,5-4 m)'),
        ('trotoar', 'Trotoar permukiman 1,5 m (saluran di bawah)'),
        ('pedsep', 'Jalur pejalan & sepeda 1,5 m (tepi rel)'),
        ('hijau', 'Jalur hijau 0,5 m / pagar perdu'),
        ('saluran', 'Saluran tertutup 0,4-0,5 m'),
        ('zebra', 'Zebra cross / ZoSS 20 km/jam'),
        ('taman', 'Taman RT (rencana)'),
        ('fasil', 'Area bermain | plaza | lawn taman RT'),
        ('tabebuya', 'Pohon berbunga (tabebuya) taman RT'),
        ('pju', 'Lampu jalan / taman (PJU)'),
        ('potong', 'Garis potong penampang (A, B1, B2, C)'),
    ]
    y = 2018.0
    for key, txt in rows:
        y0, y1 = y - 0.5, y + 9.8
        cy = (y0 + y1) / 2
        if key in ('aspal', 'trotoar', 'pedsep', 'hijau', 'saluran', 'taman'):
            col = {'aspal': C['aspal'], 'trotoar': C['trotoar'], 'pedsep': C['pedsep'], 'hijau': C['hijau'], 'saluran': C['saluran'], 'taman': C['taman_bg']}[key]
            out.append(K('rect', x0=X0, y0=y0, x1=X1, y1=y1, fill=col, edge=(40, 40, 40), lw=0.4))
            if key == 'aspal':
                out.append(K('line', pts=[(X0 + 3, cy), (X0 + 8, cy)], color=(255, 255, 255), lw=1.0))
                out.append(K('line', pts=[(X0 + 12, cy), (X1 - 3, cy)], color=(255, 255, 255), lw=1.0))
            if key == 'saluran':
                out.append(K('line', pts=[(X0 + 2, cy), (X1 - 2, cy)], color=(90, 90, 90), lw=0.6, dash=(2, 1.5)))
            if key == 'taman':
                out.append(K('circle', c=(X0 + 13.5, cy), r=3.6, fill=SP['trembesi'][0], edge=(30, 70, 30), lw=0.4))
        elif key == 'zebra':
            out.append(K('rect', x0=X0, y0=y0, x1=(X0 + X1) / 2, y1=y1, fill=C['aspal'], edge=(40, 40, 40), lw=0.4))
            for i in range(3):
                xx = X0 + 1.5 + i * 3.2
                out.append(K('rect', x0=xx, y0=y0 + 1, x1=xx + 1.6, y1=y1 - 1, fill=(255, 255, 255), edge=None, lw=0))
            out.append(K('rect', x0=(X0 + X1) / 2, y0=y0, x1=X1, y1=y1, fill=C['zoss'], edge=(40, 40, 40), lw=0.4))
        elif key == 'fasil':
            w = (X1 - X0) / 3
            for i, col in enumerate([C['bermain'], C['plaza'], C['lawn']]):
                out.append(K('rect', x0=X0 + i * w, y0=y0, x1=X0 + (i + 1) * w, y1=y1, fill=col, edge=(40, 40, 40), lw=0.4))
        elif key == 'tabebuya':
            out.append(K('circle', c=((X0 + X1) / 2, cy), r=4.6, fill=SP['tabebuya'][0], edge=(150, 70, 110), lw=0.4))
            out.append(K('circle', c=((X0 + X1) / 2 - 1.2, cy - 1.2), r=2.4, fill=SP['tabebuya'][1], edge=None, lw=0))
        elif key == 'pju':
            out.append(K('circle', c=((X0 + X1) / 2, cy), r=2.6, fill=(250, 220, 90), edge=(60, 60, 60), lw=0.4))
            out.append(K('line', pts=[((X0 + X1) / 2 - 2.6, cy), ((X0 + X1) / 2 + 2.6, cy)], color=(60, 60, 60), lw=0.4))
            out.append(K('line', pts=[((X0 + X1) / 2, cy - 2.6), ((X0 + X1) / 2, cy + 2.6)], color=(60, 60, 60), lw=0.4))
        elif key == 'potong':
            out.append(K('line', pts=[(X0, cy), (X1, cy)], color=C['potong'], lw=1.2, dash=(3, 1.5)))
            out.append(K('circle', c=(X0 + 2.5, cy), r=3.2, fill=C['potong'], edge=(255, 255, 255), lw=0.3))
        out.append(K('text', xy=(TX, y + 7.9), s=txt, size=9.3, color=(0, 0, 0)))
        y += 15.85
    # keterangan 34, 35 (kolom kanan)
    for cx, n, txt in [(2959.3, '34', 'Taman RT A & B (rencana)'), (3121.0, '35', 'Penataan jalan permukiman (pot. A-C)')]:
        yy = 2059.6
        out.append(K('circle', c=(cx, yy + 4.4), r=5.2, fill=(255, 255, 255), edge=(0, 0, 0), lw=0.7))
        out.append(K('text', xy=(cx, yy + 6.9), s=n, size=6.4, color=(0, 0, 0), ha='center'))
        out.append(K('text', xy=(cx + 11.7, yy + 7.6), s=txt, size=8.4, color=(0, 0, 0)))
    # luas elemen (kolom kanan)
    for i, txt in enumerate(['Taman RT A / B: %s / %s m2' % (fmt(luas['A']), fmt(luas['B'])),
                             'Trotoar + jalur sepeda permukiman: %s m2' % fmt(luas['trotoar'])]):
        yy = 2166.8 + i * 12.5
        out.append(K('text', xy=(2950.0, yy + 7.4), s=txt, size=8.6, color=(0, 0, 0)))
    return out

def fmt(v):
    return '{:,.0f}'.format(v).replace(',', '.')
