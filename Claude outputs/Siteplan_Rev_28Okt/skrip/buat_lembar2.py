import sys, os
sys.path.insert(0, '..')
from matplotlib.patches import PathPatch
from pdfmerge import new_overlay, merge
from render_preview import draw_scene, draw_kop, poly_path
from geo2 import pt
import scene2 as scene, kop
import geopandas as gpd
SRC = '/home/user/RancangKota/Claude outputs/Siteplan_Rev_24Okt/SitePlan_Kroya_Smart_Unified_Market_Rev_24Okt_SitePlan_%s.pdf'
OUT = '../out3'
os.makedirs(OUT, exist_ok=True)
S, D, a, b, hapus = scene.build_all()
import pickle; pickle.dump((S, [h.wkt for h in hapus]), open('../scene2_final.pkl', 'wb'))
luas = {'A': a['batas'].area, 'B': b['batas'].area, 'trotoar': sum(D[k][e].area for k in scene.DJ.CL for e in ('trotoar', 'pedsep') if e in D[k])}
dl = gpd.read_file('/home/user/RancangKota/Delineasi Tapak D3.2 Baru/Delineasi Tapak D3.2 Baru.shp').to_crs(32749).geometry.iloc[0]
polos = [p for p in S if p['layer'] not in ('D32_NOMOR', 'D32_POTONGAN', 'D32_NOMOR_TUTUP')]
# 1) A0 + kop
fig, ax = new_overlay(); draw_scene(ax, S, 'A0'); draw_kop(ax, kop.items(luas))
merge(SRC % 'A0', fig, OUT + '/SitePlan_Kroya_Smart_Unified_Market_Rev28Okt_SitePlan_A0.pdf')
# 2) tanpa kop
fig, ax = new_overlay(); draw_scene(ax, polos, 'TanpaKop')
merge(SRC % 'TanpaKop_A0', fig, OUT + '/SitePlan_Kroya_Smart_Unified_Market_Rev28Okt_SitePlan_TanpaKop_A0.pdf')
# 3) delineasi (dipotong garis delineasi)
fig, ax = new_overlay()
clip = PathPatch(poly_path(dl, lambda x, y: pt(x, y, 'Delineasi')), transform=ax.transData, fc='none', ec='none')
ax.add_patch(clip)
draw_scene(ax, [p for p in polos if p['layer'] != 'D32_DELINEASI_ATAS'], 'Delineasi', clip=clip)
draw_scene(ax, [p for p in polos if p['layer'] == 'D32_DELINEASI_ATAS'], 'Delineasi')
merge(SRC % 'Delineasi_A0', fig, OUT + '/SitePlan_Kroya_Smart_Unified_Market_Rev28Okt_SitePlan_Delineasi_A0.pdf')
print(luas)
