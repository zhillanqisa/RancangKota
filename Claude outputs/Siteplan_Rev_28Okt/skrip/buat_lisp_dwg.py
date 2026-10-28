"""Membuat D32_Rev28Okt.lsp: perintah AutoCAD D32REV28 yang menyisipkan revisi 28 Okt
(jalan, Taman RT, garis potong, kop, layout penampang) ke DWG Rev 24 Okt final lalu SAVEAS DWG 2018.
Poligon hapus = jejak bangunan dihapus (SHP) + buffer 2 m, koordinat UTM 49S (= koordinat model DWG)."""
import os
import pyogrio
from shapely.geometry import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
gdf = pyogrio.read_dataframe(os.path.join(ROOT, 'dxf', 'Bangunan_Dihapus_Rev28Okt.shp'))

polys = []
for g in gdf.geometry:
    b = g.buffer(2.0, join_style='mitre').simplify(0.25)
    if b.geom_type != 'Polygon':
        b = max(b.geoms, key=lambda q: q.area)
    polys.append(list(b.exterior.coords)[:-1])

data = '\n'.join('  (' + ' '.join('(%.2f %.2f)' % (x, y) for x, y in p) + ')' for p in polys)
tpl = open(os.path.join(HERE, 'D32_Rev28Okt_template.lsp'), encoding='utf-8').read()
out = tpl.replace(';;@@POLIGON_HAPUS@@', data)
fn = os.path.join(ROOT, 'D32_Rev28Okt.lsp')
open(fn, 'w', encoding='utf-8', newline='\r\n').write(out)

# cek keseimbangan kurung (di luar string dan komentar)
depth = 0; s = False; i = 0
while i < len(out):
    c = out[i]
    if s:
        if c == '\\': i += 1
        elif c == '"': s = False
    elif c == '"': s = True
    elif c == ';':
        while i < len(out) and out[i] != '\n': i += 1
    elif c == '(': depth += 1
    elif c == ')':
        depth -= 1
        assert depth >= 0, 'kurung tutup berlebih dekat karakter %d' % i
    i += 1
assert depth == 0 and not s, 'kurung/string tidak seimbang: %d' % depth
print(fn, len(polys), 'poligon hapus')
