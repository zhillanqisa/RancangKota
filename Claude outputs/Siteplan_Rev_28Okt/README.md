# Site Plan Rev 28 Okt 2026 — Penataan Jalan Permukiman & Taman RT

Lanjutan dari Site Plan **Rev 24 Okt** (revisi kedua 28 Okt: jalan menyambung + fillet, Jl. Ampas Waras ditata, bangunan penghalang dihapus, Taman RT A/B diperbaiki) (Cowork). Format lembar, kop, skala, dan koordinat tetap sama (A0, skala 1:1.000, UTM 49S). Hanya bagian berikut yang ditambahkan:

1. **Jalan permukiman digambar sesuai penampang rencana** (no. 35 di keterangan):
   - **Jl. Betet**: aspal 4 m dengan marka putus-putus, trotoar 1,5 m di sisi klaster tempe (saluran tertutup di bawahnya), jalur hijau 0,5 m berisi ketapang kencana dan PJU.
   - **Jl. Cendrawasih segmen permukiman (B1)**: trotoar 1,5 m di satu sisi.
   - **Jl. Cendrawasih segmen tepi rel (B2)**: jalur pejalan kaki & sepeda 1,5 m dan pagar perdu pembatas rel.
   - **Jl. Letkol Sudarso**: lajur berbagi 3,5 m, ZoSS merah, trotoar 1,5 m di sisi sekolah.
   - **Jl. Ampas Waras (depan balai)**: lajur berbagi 3,5 m, trotoar 1,5 m di sisi Taman RT B, saluran tertutup di sisi balai.
   - **Semua ruas menyambung**: setiap pertemuan jalan, termasuk mulut gang dan A. Yani, diberi fillet R 3 m. Marka dan trotoar diputus di simpang.
   - **Zebra cross** di 6 titik: depan klaster tempe, simpang Ampas Waras, pintu Taman RT A, dekat simpang A. Yani, depan sekolah, dan Taman RT B ke balai.
   - **Bangunan yang tertabrak ruang jalan rencana dihapus**: 29 bangunan. Daftarnya ada di `dxf/Bangunan_Dihapus_Rev28Okt.shp`. Bangunan besar dengan singgungan kecil dipertahankan, dan trotoar diputus di depannya.
   - Jl. A. Yani tidak diubah.
2. **Taman RT detail** (no. 34):
   - **Taman RT A** (±1.694 m², tepi rel): bangunan di tengah lahan dihapus karena di lapangan memang kosong. Lahan diperluas mengikuti batas jalan dan bangunan.
     - Isinya: plaza pertemuan bundar dengan pohon tengah, jalur lengkung dari pintu barat, area bermain, gazebo, loop joging mengelilingi lapangan rumput, pagar perdu peredam di sisi rel, dan pohon berlapis.
     - Pintu masuk/keluar: **barat** dari Jl. Cendrawasih (dengan zebra cross) dan **selatan** dari jalan lingkungan. Keduanya diberi pilar gerbang, papan nama, dan tersambung ke tepi jalan.
   - **Taman RT B** (±1.542 m², depan balai tempe): sumbu taman sejajar deretan rumah sehingga tidak miring lagi.
     - Isinya: plaza bazar/pameran dengan 8 pohon ber-grate, lawn dengan seat wall lengkung, area bermain, gazebo, dan parkir sepeda.
     - Pintu masuk/keluar ada 3: **timur** lewat koridor lurus dari trotoar Jl. Ampas Waras ke zebra cross depan balai, **selatan** dari jalan lingkungan, dan **tenggara** lewat plaza di sudut simpang. Semua tersambung ke jalan dengan fillet.
3. **Garis potong A–A', B1, B2, C–C', D–D'** di site plan, terhubung ke lembar penampang.
4. **Kop** diperbarui: 11 baris legenda baru, keterangan no. 34 dan 35, serta luas Taman RT A/B dan luas trotoar.

## File

| File | Isi |
|---|---|
| `SitePlan_Kroya_Smart_Unified_Market_Rev28Okt_SitePlan_A0.pdf` / `SitePlan_Rev28Okt_A0.png` | Site plan lengkap dengan kop (A0, 1:1.000) |
| `…_SitePlan_TanpaKop_A0.pdf` / `SitePlan_Rev28Okt_TanpaKop_A0.png` | Gambar saja, tanpa kop, tanpa nomor |
| `…_SitePlan_Delineasi_A0.pdf` / `SitePlan_Rev28Okt_Delineasi_A0.png` | Hanya isi di dalam delineasi |
| `D32_Penampang_Jalan_Permukiman_Rev28Okt_A3.pdf`, `penampang_png/` | 5 lembar gambar teknik penampang (A3, 1:100, termasuk D–D' Jl. Ampas Waras). Isi tiap lembar: eksisting & rencana, dimensi lajur/elemen/ruang milik jalan, arsir material, nomor keterangan material, denah ruas 1:200, key plan, dan kop |
| `dxf/D32_Penampang_Jalan_Permukiman_Rev28Okt.dxf` | **Sumber CAD penampang**: model space (meter) + 5 layout A3 (`PNP_A_BETET`, `PNP_B1_…`, `PNP_B2_…`, `PNP_C_…`, `PNP_D_AMPAS_WARAS`). Bisa dibuka di AutoCAD lalu *Save As* .dwg |
| `dxf/D32_Overlay_Model_Rev28Okt_UTM49S.dxf` | Jalan, taman, pohon (block), dan garis potong dalam **UTM 49S (meter)** |
| `dxf/D32_Overlay_KopA0_Rev28Okt_mm.dxf` | Tambahan legenda/keterangan kop dalam **mm kertas A0** |
| `D32_Rev28Okt.lsp` | **Perintah AutoCAD `D32REV28`**: menerapkan revisi ke DWG Rev 24 Okt final dan menyimpan DWG Rev 28 Okt |
| `skrip/` | Skrip pembuat (geometri jalan `desain_jalan.py`, taman `desain_taman.py`, gambar `scene.py`, penampang `penampang_teknik.py`) |

## Jadikan DWG langsung (otomatis, 1 perintah)

`D32_Rev28Okt.lsp` menerapkan semua revisi ke DWG Rev 24 Okt final di AutoCAD dan menyimpannya sebagai DWG baru. Isi layout tetap: Model, `SITEPLAN_A0_1-1000`, `ALUR_…`, `SITEPLAN_MURNI_…`, dan `SITEPLAN_DELINEASI_…`.

0. Kalau folder ini belum ada di komputermu, unduh `D32_Rev28Okt_DWG_Kit.zip` (isi: LISP + 3 DXF) lalu ekstrak, sebaiknya ke `Claude outputs\` sehingga terbentuk `Claude outputs\Siteplan_Rev_28Okt\`.
1. Buka `Claude outputs/Siteplan_Rev_24Okt/SitePlan_Kroya_Smart_Unified_Market_Rev_24Okt_final.dwg`.
2. Seret `D32_Rev28Okt.lsp` ke jendela AutoCAD, atau muat lewat `APPLOAD`. Ketik **`D32REV28`**, lalu Enter.
3. Perintah ini otomatis:
   - menyisipkan overlay jalan + Taman RT ke model space di 0,0 skala 1. Model DWG memakai UTM 49S, sehingga posisinya langsung tepat;
   - **menghapus bangunan yang tertabrak jalan dan bangunan di lahan Taman RT A dari DWG**. Yang dihapus adalah objek di layer `*BANGU*` / `*BAYANG*` yang seluruhnya berada dalam jejak bangunan + 2 m. Sudah dicek: tidak ada bangunan lain yang ikut terhapus;
   - menaruh revisi di atas gambar lama (DRAWORDER);
   - menambah legenda/keterangan kop di layout `SITEPLAN_A0_1-1000`. Posisinya disesuaikan otomatis terhadap teks "LEGENDA";
   - menambah 5 layout penampang `PNP_A_BETET` … `PNP_D_AMPAS_WARAS` (A3, 1:100);
   - menyimpan hasilnya sebagai **`Claude outputs/Siteplan_Rev_28Okt/SitePlan_Kroya_Smart_Unified_Market_Rev28Okt.dwg`** (DWG 2018). File Rev 24 Okt tidak diubah.
4. Di akhir muncul ringkasan, misalnya jumlah objek yang dihapus dan pergeseran kop. Kalau ada langkah yang gagal, kotak pesan menyebutkan langkahnya.

File DXF di `dxf/` dicari otomatis di folder `..\Siteplan_Rev_28Okt\dxf\` relatif terhadap DWG. Kalau tidak ketemu, AutoCAD meminta kamu memilih file pertama (`D32_Overlay_Model_…dxf` di folder `dxf`). File berikutnya otomatis dicari di folder yang sama. Kalau versi AutoCAD-mu menolak menyisipkan DXF, buka DXF itu dan *Save As* DWG dengan nama yang sama di folder yang sama, lalu jalankan `D32REV28` lagi (file .dwg diutamakan).

Langkah manual lama (INSERT satu per satu) tidak diperlukan lagi.

## Catatan

- Jalan rencana mengikuti as jalan eksisting di site plan Rev 24 Okt.
- Lebar ruang milik jalan rencana sama dengan eksisting. Namun di beberapa titik, rumah eksisting (data BIG) mepet ke tepi jalan, sehingga trotoar/saluran **diputus di depan rumah tersebut** dan rumah tidak dibongkar. Ini sesuai Asistensi 4: permukiman tetap.
- Trotoar juga diputus di mulut gang/jalan lain.
- Luas trotoar dan jalur sepeda yang tergambar: ±2.876 m².
