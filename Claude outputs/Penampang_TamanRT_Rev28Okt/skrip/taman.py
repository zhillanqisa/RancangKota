"""Geometri Taman RT A (simpang Jl. Betet - Jl. Cendrawasih, tepi rel) dan
Taman RT B (sebelah barat Balai Pelatihan UMKM / balai tempe, Jl. Ampas Waras).
Koordinat UTM 49S (m), sama dengan model space DWG Site Plan Rev 24 Okt."""
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union

# ---------------- Taman RT A ----------------
# batas: timur Jl. Cendrawasih (sisi rel), utara deret rumah Jl. Betet,
# timur RTH eksisting, selatan jalan lingkungan; rumah eksisting di tengah dikecualikan.
A = Polygon([
    (306057.5, 9156518.0), (306090.0, 9156518.0), (306090.0, 9156508.0),
    (306110.5, 9156507.0), (306110.0, 9156485.5), (306089.0, 9156485.0),
    (306089.0, 9156503.0), (306071.0, 9156503.0), (306071.0, 9156485.5),
    (306064.0, 9156485.5),
])
A_rumah = box(306073.0, 9156484.0, 306087.0, 9156501.0)   # rumah eksisting (tetap)

A_pagar = A.intersection(LineString([(306057.5, 9156518.0), (306064.0, 9156485.5)]).buffer(1.6, cap_style=2))
A_ring_out = A.buffer(-2.2, join_style=2)
A_jalur = A_ring_out.difference(A_ring_out.buffer(-1.5, join_style=2))
A_main = box(306064.0, 9156506.5, 306080.0, 9156515.0).intersection(A.buffer(-3.9, join_style=2))
A_lap = box(306093.5, 9156488.5, 306106.5, 9156503.5)
A_gazebo = box(306064.6, 9156490.0, 306068.4, 9156494.0)
A_masuk = [((306059.6, 9156507.5), 'Masuk dari\nJl. Cendrawasih'), ((306100.0, 9156485.3), 'Masuk dari jalan\nlingkungan selatan')]
A_pohon = []
for seg_pts in [[(306060.5, 9156516.0), (306088.0, 9156516.0)], [(306092.0, 9156506.0), (306108.5, 9156505.5)],
                [(306108.5, 9156503.0), (306108.0, 9156488.0)], [(306091.0, 9156487.0), (306106.0, 9156487.0)]]:
    ls = LineString(seg_pts)
    n = max(2, int(ls.length // 6) + 1)
    A_pohon += [ls.interpolate(i / (n - 1), normalized=True) for i in range(n)]
A_bangku = [(306083.0, 9156511.0), (306083.0, 9156507.5), (306091.5, 9156496.0), (306069.5, 9156497.5)]

# ---------------- Taman RT B ----------------
# lahan kosong di barat Jl. Ampas Waras, berseberangan dengan balai tempe.
B = Polygon([
    (306321.0, 9156499.0), (306353.0, 9156499.0), (306353.0, 9156488.5),
    (306371.0, 9156488.5), (306371.0, 9156485.0), (306354.5, 9156485.0),
    (306354.5, 9156469.5), (306371.5, 9156469.5), (306371.5, 9156465.0),
    (306321.0, 9156465.0),
])
B_rumah = box(306356.0, 9156470.5, 306369.0, 9156484.0)    # rumah eksisting (tetap)
B_plaza = unary_union([box(306337.0, 9156467.5, 306353.0, 9156496.5),
                       box(306353.0, 9156485.0, 306371.0, 9156488.5),
                       box(306354.5, 9156465.0, 306371.5, 9156469.5)])
B_main = box(306323.5, 9156486.0, 306334.0, 9156496.5)
B_gazebo = box(306325.0, 9156470.0, 306330.0, 9156475.0)
B_zebra = box(306371.0, 9156485.0, 306378.0, 9156488.5)   # zebra cross ke balai
B_pohon = []
for seg_pts in [[(306323.0, 9156497.5), (306351.0, 9156497.5)], [(306322.5, 9156484.0), (306322.5, 9156467.0)],
                [(306336.0, 9156478.0), (306336.0, 9156478.1)]]:
    ls = LineString(seg_pts)
    n = max(1, int(ls.length // 6) + 1)
    B_pohon += [ls.interpolate(i / max(n - 1, 1), normalized=True) for i in range(n)]
B_bangku = [(306340.0, 9156494.0), (306348.0, 9156494.0), (306340.0, 9156470.5), (306348.0, 9156470.5)]
B_masuk = [((306366.0, 9156486.8), 'Penghubung 3,5 m\nke balai'), ((306363.0, 9156467.2), 'Masuk selatan')]

BALAI = box(306379.0, 9156471.0, 306389.0, 9156482.0)

if __name__ == '__main__':
    print('Taman A luas %.0f m2' % A.area, ' jalur %.0f, main %.0f, lapangan %.0f' % (A_jalur.area, A_main.area, A_lap.area))
    print('Taman B luas %.0f m2' % B.area, ' plaza %.0f, main %.0f' % (B_plaza.intersection(B).area, B_main.area))
    print('A overlaps rumah?', A.intersects(A_rumah.buffer(-0.5)), 'B overlaps rumah?', B.intersects(B_rumah.buffer(-0.5)))
