# Revisi Penampang Jalan Permukiman & Taman RT (Rev 28 Okt 2026)

Revisi slide **Penampang Jalan** (Data, Analisis, Respon) untuk jalan permukiman selain Jl. Jend. A. Yani, ditambah **dua Taman RT**: satu di dekat rel dan satu di sebelah balai tempe.
Dasar gambar: **Site Plan Rev 24 Okt** (`Claude outputs/Siteplan_Rev_24Okt/…_Rev_24Okt_final.dwg` / `…_SitePlan_A0.pdf`, UTM 49S). Jl. A. Yani **tidak diubah** karena sudah didesain.

## Isi folder

| File | Kegunaan |
|---|---|
| `slide/00…07_*.png` | 8 slide siap pakai (rasio A3 seperti deck Canva, 1870×1323 px). Bisa langsung di-upload ke Canva sebagai halaman/gambar. |
| `Penampang_TamanRT_Rev28Okt_slides.pdf` | 8 slide yang sama dalam satu PDF. |
| `penampang_png/*_eks.png`, `*_ren.png` | Gambar penampang terpisah (latar transparan) kalau ingin menyusun ulang di Canva. |
| `dxf/TamanRT_PotonganJalan_Rev28Okt_UTM49S.dxf` | Taman RT A & B + garis potong A–A', B1, B2, C–C' dalam **koordinat UTM 49S** (sama dengan model space DWG Rev 24 Okt). |
| `dxf/Penampang_Jalan_Permukiman_Rev28Okt.dxf` | 8 penampang (eksisting & rencana) dalam meter, layer `D32_PNP_*`. Untuk plot skala 1:100. |
| `SitePlan_Rev24Okt_+TamanRT_preview.png`, `…_zoomBarat.png` | Pratinjau site plan Rev 24 Okt dengan kedua taman. |
| `skrip/` | Skrip Python pembuat semua gambar/DXF (geometri taman di `taman.py`, ukuran penampang di `penampang.py`, teks slide di `konten.py`). |

## Cara memasukkan ke DWG Site Plan Rev 24 Okt

DWG tidak bisa ditulis langsung dari lingkungan ini, jadi hasilnya berupa DXF. Cara memasukkannya di AutoCAD:
1. Buka `SitePlan_Kroya_Smart_Unified_Market_Rev_24Okt_final.dwg`.
2. `INSERT` → pilih `TamanRT_PotonganJalan_Rev28Okt_UTM49S.dxf` → Insertion point **0,0,0**, Scale **1**, Rotation **0**, centang **Explode**.
   (Alternatif: buka DXF → pilih semua → `COPYBASE` dengan titik dasar 0,0 → di DWG site plan `PASTECLIP` di 0,0.)
3. Semua objek masuk ke layer `D32_TAMAN_RT_*` dan `D32_POTONGAN_*`, sehingga mudah diganti warna/hatch sesuai legenda.
4. Tambahkan ke legenda site plan: **Taman RT (rencana)**.
5. Penampang: buka `Penampang_Jalan_Permukiman_Rev28Okt.dxf`, lalu copy ke layout/sheet penampang (1 unit = 1 m).

## Ringkasan desain

- **Prinsip (sesuai Asistensi 4):** ruang milik jalan eksisting tidak diubah dan tidak ada rumah yang dibongkar. Lebar jalan diperoleh dengan menutup saluran terbuka dan memperkeras bahu tanah. Respon ditulis per lokasi/segmen, bukan generik.
- **Jl. Betet (A–A')**: badan jalan 3,2 → 4,0 m; trotoar 1,5 m di sisi klaster tempe di atas saluran tertutup; jalur hijau 0,5 m. Menjadi rute pejalan kaki/wisata tempe A. Yani → klaster → Taman RT A.
- **Jl. Cendrawasih**: dibuat **dua tipe** karena konteksnya berbeda.
    - **B1 (segmen permukiman)**: trotoar 1,5 m satu sisi.
    - **B2 (segmen tepi rel)**: pagar hijau perdu sebagai pembatas rel + jalur pejalan & sepeda 1,5 m.
- **Jl. Letkol Sudarso (C–C')**: jalan berbagi 3,5 m, Zona Selamat Sekolah (ZoSS) 20 km/jam, trotoar 1,5 m di sisi zona pendidikan, larangan truk/bongkar-muat karena <100 m dari simpang.
- **Taman RT A** (±1090 m²): lahan kosong di simpang Jl. Betet–Jl. Cendrawasih, tepi rel (lokasi yang dilingkari di Google Maps).
- **Taman RT B** (±1260 m²): lahan kosong di barat Jl. Ampas Waras, berseberangan dengan Balai Pelatihan UMKM (balai tempe). Dilengkapi penghubung 3,5 m dan zebra cross ke balai.

## Catatan yang perlu dicek saat survei

1. **Batas lahan taman** diambil dari lahan kosong pada site plan Rev 24 Okt dan jejak bangunan BIG. Cek kepemilikan/batas persil di lapangan. Pada Taman A ada satu rumah eksisting yang sengaja dikecualikan dari taman.
2. **Sisi kiri/kanan penampang eksisting** diasumsikan: kiri = selatan (Betet, Letkol) dan kiri = utara (Cendrawasih segmen permukiman). Kalau saat survei arah pandangnya berbeda, cukup tukar label di `penampang.py`.
3. **Jl. Betet**: data lama menulis "badan jalan 4 m" tetapi gambarnya 3,2 m, dan bahu kiri 1,15 m tidak cocok dengan total 1,9 m. Di revisi ini dipakai 3,2 m (hasil ukur kelompok) dan bahu kiri 1,05 m. Andalalin 2023 mencatat perkerasan 4,0 m; total ruang milik jalan keduanya tetap ±7 m.
4. **Jl. Letkol Sudarso**: badan jalan 2,5 m (kelompok) vs perkerasan 4,0 m (Andalalin), selisihnya besar. **Perlu diukur ulang.**
5. Kebutuhan taman RT memakai SNI 03-1733-2004 (250 jiwa/taman, ≥250 m²) dan penduduk tapak 2.348 jiwa dari slide Infrastruktur Air Bersih.

## Teks slide (untuk di-copy ke Canva)

### Jl. Betet
**Data**
- Jalan kabupaten, fungsi lokal primer (Andalalin 2023); kapasitas 1.462 smp/jam.
- Ruas ±870 m dari Simpang 4 Jl. A. Yani–Jl. Letkol Sudarso ke barat hingga Jl. Cendrawasih (tepi rel); menjadi batas utara delineasi.
- Ruang milik jalan ±7 m. Badan jalan (aspal) 3,2 m = 2 lajur @1,6 m.
- Sisi selatan: furnitur 0,45 m, drainase terbuka 0,4 m, bahu tanah 1,05 m. Sisi utara: bahu tanah 1,15 m, drainase terbuka 0,35 m, furnitur 0,35 m.
- Tidak ada trotoar. Andalalin mencatat perkerasan 4,0 m + bahu 1,6 m di kedua sisi (±7,2 m), sama-sama ±7 m.
- Tepi jalan: klaster sentra produksi tempe (T1 Keripik Tempe Mirasa), rumah warga, sawah/LSD, lahan kosong di simpang Betet–Cendrawasih.

**Analisis**
- Fungsi ganda: jalan kabupaten sekaligus akses utama klaster tempe. Dilalui motor warga, pick-up pemasok kedelai/pengambil produk, dan calon pengunjung wisata edukasi tempe dari Jl. A. Yani.
- Badan jalan 3,2 m < 2 × 2,0 m: mobil dan motor yang berpapasan harus turun ke bahu tanah yang becek saat hujan.
- Bahu tanah 1,05–1,15 m dipakai parkir motor dan tumpukan barang produksi, sehingga pejalan kaki (warga, siswa, pengunjung) berjalan di badan jalan.
- Drainase terbuka 0,35–0,4 m menerima limbah cair rebusan/rendaman kedelai: bau, sedimen, mudah tersumbat.
- Ruang milik jalan ±7 m sebenarnya cukup untuk 2 lajur + 1 trotoar bila bahu dan saluran ditata, tanpa membongkar rumah (permukiman tetap, sesuai Asistensi 4).
- Belum ada titik singgah/ruang terbuka di sepanjang ruas; lahan kosong di ujung barat (tepi rel) belum dimanfaatkan.

**Respon**
- Penampang rencana, ruang milik jalan tetap ±7 m:
    - Sisi selatan (sisi klaster): jalur hijau 0,5 m (ketapang kencana, PJU, papan arah "Sentra Tempe") + trotoar 1,5 m (+15 cm) di atas drainase tertutup 0,5 m.
    - Badan jalan 4,0 m (2 × 2,0 m), aspal, marka tengah putus-putus, kecepatan 30 km/jam.
    - Sisi utara: drainase tertutup 0,5 m + bahu diperkeras 0,5 m (tiang listrik eksisting tetap).
- Trotoar sisi selatan menyambung Jl. A. Yani → klaster tempe → Taman RT A sebagai rute pejalan kaki/wisata edukasi tempe.
- Limbah cair tempe tidak dibuang ke saluran jalan: dialirkan ke biofilter komunal di balai. Saluran jalan khusus air hujan; dimensi naik dari 0,35–0,4 m menjadi 0,5 m.
- Bongkar-muat pick-up di halaman rumah produksi/balai, bukan di badan jalan. Zebra cross + pita penggaduh di depan T1 dan Taman RT A.
- Pelebaran perkerasan diambil dari bahu tanah dan saluran terbuka yang ditutup, tanpa pembebasan lahan.

| Elemen | Eksisting | Rencana |
|---|---|---|
| Badan jalan | 3,2 m | 4,0 m (2 × 2,0) |
| Trotoar | tidak ada | 1,5 m (selatan) |
| Drainase | terbuka 0,35–0,4 m | tertutup 0,5 m |
| Bahu tanah | 1,05 + 1,15 m | – (diperkeras 0,5 m) |
| Jalur hijau/PJU | tiang saja | 0,5 m + pohon |
| Ruang milik jalan | ±7 m | ±7 m (tetap) |

### Jl. Cendrawasih
**Data**
- Jalan kabupaten, fungsi lokal primer (Andalalin 2023); kapasitas 1.543 smp/jam.
- Ruas dari Simpang 3 Jl. A. Yani (±145 m utara perlintasan KA, dekat pasar & stasiun) ke barat membelah permukiman, lalu berbelok menyusuri sisi dalam rel hingga Jl. Betet.
- Ruang milik jalan ±6,5 m. Badan jalan 3,2 m = 2 lajur @1,6 m.
- Tiap sisi: bahu tanah 0,9 m, furnitur 0,4 m (tiang PJU/listrik), drainase terbuka 0,35 m.
- Tidak ada trotoar. Andalalin: perkerasan 4,0 m, bahu 1,0 m dan 2,0 m (±7 m).
- Segmen tengah: rumah di kedua sisi. Segmen tepi rel: sisi barat sempadan rel (147 perjalanan KA/hari), sisi timur lahan kosong (rencana Taman RT A).

**Analisis**
- Penghubung bagian barat kawasan (klaster tempe, permukiman) ke Jl. A. Yani dekat pasar & stasiun, sehingga dipakai warga ke pasar/stasiun dan jalan pintas kendaraan.
- Badan jalan 3,2 m tanpa trotoar: pejalan kaki & sepeda berbagi badan jalan; dekat simpang A. Yani arus naik (antrean perlintasan KA merembet).
- Segmen tengah: rumah menempel ke ruang milik jalan, sehingga trotoar hanya mungkin di satu sisi bila saluran ditutup.
- Segmen tepi rel: sisi rel terbuka tanpa pembatas: bising, tidak aman bagi anak, dan berkesan "belakang kawasan" (lihat analisis View).
- Drainase terbuka 0,35 m kecil; kontur menurun ke arah rel sehingga terjadi genangan (analisis drainase).
- Konteks kedua segmen berbeda, jadi penampangnya tidak bisa disamaratakan: dibuat 2 tipe.

**Respon**
- Tipe B1, segmen permukiman (ruang milik jalan 6,5 m tetap):
    - Trotoar 1,5 m satu sisi (sisi utara, menerus ke Jl. A. Yani) di atas drainase tertutup 0,5 m.
    - Badan jalan 4,0 m (2 × 2,0 m); sisi selatan drainase tertutup 0,5 m + bahu diperkeras 0,5 m untuk tiang PJU.
- Tipe B2, segmen tepi rel (depan Taman RT A):
    - Pagar hijau perdu 0,5 m (bambu pagar/teh-tehan) sebagai pembatas rel; tidak memakai pohon besar agar ruang bebas KA tetap aman.
    - Jalur pejalan kaki & sepeda 1,5 m di atas drainase tertutup 0,5 m; badan jalan 4,0 m; drainase tertutup 0,5 m di sisi taman.
- Simpang Cendrawasih–A. Yani: zebra cross dan larangan parkir ±50 m dari simpang. Pejalan dari kawasan diarahkan ke trotoar A. Yani (sudah didesain) menuju pasar/stasiun.
- Simpang Betet–Cendrawasih menjadi gerbang barat kawasan dan titik masuk Taman RT A.

| Elemen | Eksisting | Rencana B1 / B2 |
|---|---|---|
| Badan jalan | 3,2 m | 4,0 m / 4,0 m |
| Trotoar | tidak ada | 1,5 m / 1,5 m (+sepeda) |
| Drainase | terbuka 0,35 m | tertutup 0,5 m |
| Pembatas rel | tidak ada | – / pagar hijau 0,5 m |
| Ruang milik jalan | ±6,5 m | ±6,5 m (tetap) |

### Jl. Letkol Sudarso
**Data**
- Jalan kabupaten, fungsi lokal primer (Andalalin 2023); kapasitas 1.462 smp/jam.
- Kaki timur Simpang 4 Jl. A. Yani–Jl. Betet–Jl. Letkol Sudarso (lanjutan Jl. Betet ke timur hingga Jl. Jeruk Manis); berbatasan dengan zona pendidikan di utara Pasar Induk.
- Ruang milik jalan ±5,7 m. Badan jalan 2,5 m = 2 lajur @1,25 m.
- Tiap sisi: bahu tanah 0,9 m, furnitur 0,4 m, drainase terbuka 0,3 m.
- Tidak ada trotoar. Andalalin mencatat perkerasan 4,0 m dengan bahu 0,3 m dan 1,3 m (±5,6 m); lebar perkerasan perlu diukur ulang.

**Analisis**
- Badan jalan 2,5 m hanya muat satu mobil; kendaraan yang berpapasan menunggu di bahu atau di mulut simpang.
- Mulut ruas tepat di Simpang 4 Jl. A. Yani yang sudah padat oleh aktivitas pasar dan antrean perlintasan KA.
- Dilalui siswa zona pendidikan pada jam masuk/pulang yang bersamaan dengan jam pasar pagi (06.00–07.00), sehingga berisiko bagi keselamatan.
- Tidak layak menjadi akses barang/bongkar-muat pasar: lebar sempit dan berjarak < 100 m dari simpang (arahan Asistensi 4: in-out ≥ 100 m dari simpang).
- Ruang milik jalan ±5,7 m hanya cukup untuk 1 lajur kendaraan dua arah terbatas + 1 trotoar.

**Respon**
- Penampang rencana, ruang milik jalan tetap ±5,7 m (jalan berbagi kecepatan rendah):
    - Sisi selatan (zona pendidikan): trotoar 1,5 m di atas drainase tertutup 0,4 m.
    - Badan jalan 3,5 m untuk dua arah terbatas (berpapasan pelan), marka merah Zona Selamat Sekolah (ZoSS), batas 20 km/jam.
    - Sisi utara: drainase tertutup 0,4 m + bahu diperkeras 0,3 m (tiang PJU).
- Zebra cross ditinggikan di depan sekolah; ±30 m pertama dari simpang diberi marka dilarang berhenti/parkir.
- Rambu larangan truk dan larangan bongkar-muat: kendaraan barang pasar hanya lewat pintu barang yang ditetapkan di site plan.
- Lebar ruang milik jalan tidak diubah; rumah dan pagar sekolah tetap.

| Elemen | Eksisting | Rencana |
|---|---|---|
| Badan jalan | 2,5 m | 3,5 m (berbagi) |
| Trotoar | tidak ada | 1,5 m (sisi sekolah) |
| Drainase | terbuka 0,3 m | tertutup 0,4 m |
| Kecepatan | – | 20 km/jam (ZoSS) |
| Ruang milik jalan | ±5,7 m | ±5,7 m (tetap) |

### Taman RT
**Data**
- Analisis vegetasi: tidak ada RTH untuk rekreasi masyarakat di kawasan; lahan terbangun 70,2%.
- Penduduk tapak ±2.348 jiwa (2025). SNI 03-1733-2004: 1 taman RT per 250 jiwa, luas ≥ 250 m², radius ±100 m, sehingga dibutuhkan ±9 taman RT.
- Ada dua lahan kosong di dalam permukiman: simpang Betet–Cendrawasih (tepi rel) dan sisi barat Jl. Ampas Waras di seberang balai tempe.

**Respon**
- Taman RT A, tepi rel (±1.090 m²): pagar hijau peredam di sisi Jl. Cendrawasih/rel, area bermain anak, lapangan rumput serbaguna, gazebo, jalur keliling 1,5 m, bangku & lampu taman, pohon peneduh. Juga menjadi titik singgah rute wisata tempe dari Jl. Betet.
- Taman RT B, sebelah balai tempe (±1.260 m²): plaza berpori untuk bazar/pameran tempe akhir pekan dan pelatihan luar ruang, area bermain, gazebo, pohon peneduh. Ada penghubung 3,5 m + zebra cross langsung ke balai.
- Hanya memakai lahan kosong; rumah warga di sekitarnya tetap (rumah di tengah Taman A dikecualikan).

