# Data Eksisting untuk Kriteria Terukur — 4 Kelompok Aktivitas Kawasan Kroya
**Studio Rancang Kota D3.2, Kecamatan Kroya, Kabupaten Cilacap**
*Disusun 26 Oktober 2026. Seluruh angka di bawah adalah **kondisi eksisting** (belum ada rencana/site plan). Data rencana (zoning revisi, siteplan Rev 23/24 Okt, Asistensi 4, amplop bangunan, DED pasar) **tidak dipakai** sebagai angka.*

Kawasan dibagi menjadi 4 aktivitas utama: **Pasar, UMKM, Pertokoan, Permukiman**. Untuk masing-masing dicari tiga hal: **luas lahan, lantai, dan trotoar**, lalu dihitung **rata-ratanya**.

---

## 1. Ringkasan (angka utama)

| Kelompok | Jumlah bangunan | Rata-rata luas lahan / persil (m²) | Rata-rata luas lantai dasar / tapak (m²) | Rata-rata jumlah lantai | Rata-rata luas lantai total (m²) | Lebar trotoar eksisting |
|---|---|---|---|---|---|---|
| **Pasar** | 16 | **13.978** (1 bidang HPL, Andalalin) | 564,1 | **1,69 lt** (≈ 2 lt) | 1.271,4 | **0 m** (tidak ada; hanya bahu jalan rata-rata 1,85 m) |
| **UMKM** (sentra tempe) | 73 | ± **409** *(estimasi)* | 126,7 | **1,34 lt** (≈ 1 lt) | 167,0 | **0 m** (jalan lingkungan tanpa trotoar) |
| **Pertokoan** (muka Jl. A. Yani) | 21 | ± **801** *(estimasi)* | 432,3 | **1,90 lt** (≈ 2 lt) | 1.033,1 | **0 m** (tidak ada; hanya bahu jalan rata-rata 1,85 m) |
| **Permukiman** | 475 | ± **377** *(estimasi)* | 145,2 | **1,58 lt** (≈ 2 lt) | 242,8 | **0 m** (jalan lingkungan tanpa trotoar) |
| *Seluruh kawasan (615 bangunan)* | *615* | *± 434 (estimasi)* | *171,8* | *1,58 lt* | *306,3* | — |

Catatan cepat:
- **Luas lahan pasar** adalah data resmi (Sertifikat HPL No. 5). Luas lahan kelompok lain adalah **estimasi** karena peta persil/bidang tanah BPN tidak ada di folder proyek (metode di bagian 3.1).
- **Jumlah lantai** dibulatkan ke atas hanya untuk keterangan; untuk tabel kriteria terukur pakai angka desimalnya.
- **Trotoar**: di seluruh kawasan **tidak ada trotoar eksisting**. Yang ada hanya bahu jalan dan saluran drainase (detail di bagian 4).

---

## 2. Detail per kelompok

### 2.1 Pasar (Pasar Induk Kroya)

| Komponen | Nilai eksisting | Sumber |
|---|---|---|
| Luas lahan | **13.978 m²** (1 bidang, Sertifikat HPL No. 5) | Andalalin 2023, hlm. II-1 & VI-1 |
| Jumlah massa bangunan | 16 | Building_Clip BIG, atribut TOPONIM = "Pasar" |
| Luas lantai dasar total | 9.025,9 m² | dihitung GIS |
| Rata-rata luas lantai dasar per bangunan | **564,1 m²** (median 261,7; min 89,6; maks 3.465,1) | dihitung GIS |
| Jumlah lantai | 1 lt: 6 bangunan, 2 lt: 9 bangunan, ≥3 lt: 1 bangunan | peta kelas tinggi bangunan |
| **Rata-rata jumlah lantai** | **1,69 lantai** | dihitung |
| Luas lantai total | 20.342,6 m² (rata-rata 1.271,4 m² per bangunan) | tapak × lantai |
| KDB eksisting (terhadap HPL) | 9.025,9 / 13.978 = **64,6 %** | dihitung |
| KLB eksisting (terhadap HPL) | 20.342,6 / 13.978 = **1,46** | dihitung |
| Trotoar muka pasar (Jl. A. Yani) | **Tidak ada** — bahu jalan 1,7 m & 2,0 m (rata-rata **1,85 m**), drainase 1,7 m & 1,3 m | Andalalin 2023, Gbr. III.19 & Tabel III.7 |

> Perhatian: angka "bangunan 3 lantai, 15.107,4 m²" di Andalalin (hlm. III-7) adalah **rencana** renovasi, bukan eksisting, jadi tidak dipakai. Data jejak bangunan BIG berasal dari citra Pleiades 2020 + survei lapangan 2021, sehingga menggambarkan bangunan pasar lama (sebelum/sekitar kebakaran 23 Des 2021).

### 2.2 UMKM (sentra produksi tempe)

| Komponen | Nilai eksisting | Sumber |
|---|---|---|
| Jumlah bangunan | 73 | Building_Clip BIG di dalam klaster titik produsen tempe hasil survei |
| Luas lantai dasar total | 9.251,1 m² | dihitung GIS |
| Rata-rata luas lantai dasar | **126,7 m²** (median 95,9; min 14,4; maks 560,3) | dihitung GIS |
| Estimasi luas lahan / persil | rata-rata **409,3 m²** (median 350,3); total ± 29.875 m² | tessellation (bagian 3.1) |
| Jumlah lantai | 1 lt: 48 bangunan, 2 lt: 25 bangunan, ≥3 lt: 0 | peta kelas tinggi bangunan |
| **Rata-rata jumlah lantai** | **1,34 lantai** | dihitung |
| Luas lantai total | 12.189,3 m² (rata-rata 167,0 m² per bangunan) | tapak × lantai |
| KDB eksisting (estimasi) | **31,0 %** | tapak ÷ estimasi persil |
| KLB eksisting (estimasi) | **0,41** | luas lantai ÷ estimasi persil |
| Trotoar | **Tidak ada**; jalan lokal/lingkungan sempit (maks. dilalui 2 mobil) | Laporan kelompok `_Cangkot D3.2.pdf` hlm. 23 |

> UMKM eksisting di kawasan berupa **industri rumahan tempe** (rumah sekaligus tempat produksi), sehingga karakter bangunannya mirip permukiman tetapi lebih rendah (dominan 1 lantai). Data lapak PKL di Jl. A. Yani **belum ada** (survei PKL belum dilakukan), jadi PKL tidak masuk perhitungan.

### 2.3 Pertokoan (deret toko/ruko muka Jl. Jend. Ahmad Yani)

| Komponen | Nilai eksisting | Sumber |
|---|---|---|
| Jumlah massa bangunan | 21 | Building_Clip BIG, bangunan yang muka depannya ≤ 20 m dari as Jl. A. Yani |
| Luas lantai dasar total | 9.079,2 m² | dihitung GIS |
| Rata-rata luas lantai dasar | **432,3 m²** (median 205,3; min 45,0; maks 3.861,4) | dihitung GIS |
| Estimasi luas lahan / persil | rata-rata **801,4 m²** (median 406,7); total ± 16.829 m² | tessellation (bagian 3.1) |
| Jumlah lantai | 1 lt: 3 bangunan, 2 lt: 17 bangunan, ≥3 lt: 1 bangunan | peta kelas tinggi bangunan |
| **Rata-rata jumlah lantai** | **1,90 lantai** | dihitung |
| Luas lantai total | 21.694,2 m² (rata-rata 1.033,1 m² per bangunan) | tapak × lantai |
| KDB eksisting (estimasi) | **54,0 %** | tapak ÷ estimasi persil |
| KLB eksisting (estimasi) | **1,29** | luas lantai ÷ estimasi persil |
| Trotoar | **Tidak ada** — bahu jalan rata-rata **1,85 m** (dipakai PKL & parkir) | Andalalin 2023, Gbr. III.19 & Tabel III.7 |

> Rata-rata luas tapak pertokoan tertarik ke atas oleh satu bangunan besar 3.861 m² (3 lt). Untuk gambaran "satu toko tipikal" lebih aman memakai **median 205 m²**. Pada peta BIG, deret ruko yang menempel sering tergabung menjadi satu poligon, sehingga 21 massa bangunan ≠ 21 unit toko.

### 2.4 Permukiman

| Komponen | Nilai eksisting | Sumber |
|---|---|---|
| Jumlah bangunan | 475 | Building_Clip BIG (kode 1201, di luar pasar, pertokoan, UMKM, fasilitas umum) |
| Luas lantai dasar total | 68.959,8 m² | dihitung GIS |
| Rata-rata luas lantai dasar | **145,2 m²** (median 114,3; min 7,6; maks 962,6) | dihitung GIS |
| Estimasi luas lahan / persil | rata-rata **377,3 m²** (median 321,3); total ± 179.218 m² | tessellation (bagian 3.1) |
| Jumlah lantai | 1 lt: 208 bangunan, 2 lt: 258 bangunan, ≥3 lt: 9 bangunan | peta kelas tinggi bangunan |
| **Rata-rata jumlah lantai** | **1,58 lantai** | dihitung |
| Luas lantai total | 115.327,9 m² (rata-rata 242,8 m² per bangunan) | tapak × lantai |
| KDB eksisting (estimasi) | **38,5 %** | tapak ÷ estimasi persil |
| KLB eksisting (estimasi) | **0,64** | luas lantai ÷ estimasi persil |
| Trotoar | **Tidak ada**; jalan lokal/lingkungan sempit (maks. dilalui 2 mobil) | Laporan kelompok `_Cangkot D3.2.pdf` hlm. 23 |

---

## 3. Metode perhitungan

Data dasar (semua eksisting):

| Data | File | Isi |
|---|---|---|
| Delineasi kawasan | `Delineasi Tapak D3.2 Baru/` | 33,35 ha |
| Jejak bangunan | `GIS_Stuff/Rancang_Kota/Rancang_Kota.gdb` → `Building_Clip` | 615 bangunan di dalam delineasi; sumber BIG: interpretasi citra 2017, dimutakhirkan Pleiades 2020 (+ survei lapangan 2021 untuk 11 bangunan) |
| Tinggi bangunan | `Rancang_Kota.gdb` → `Bangunan_Kroya_Classifi_Clip` | peta kelas tinggi kelompok: kelas 1 = 0–4 m (1 lt), kelas 2 = 4–8 m (2 lt), kelas 3 = > 8 m (≥ 3 lt) |
| Penampang & geometri jalan | `Data/DOK. ANDALALIN SETELAH REVISI SIDANG.pdf` | hasil survei 2023 |
| Analisis tapak kelompok | `_Cangkot D3.2.pdf` | kondisi jalan lokal & fasilitas pejalan kaki |

Langkah:
1. **Pengelompokan bangunan** (berdasarkan fungsi eksisting, bukan zona rencana):
   - **Pasar** = bangunan ber-TOPONIM "Pasar" pada data BIG.
   - **Pertokoan** = bangunan non-fasilitas umum yang muka depannya ≤ 20 m dari as Jl. Jend. A. Yani (deret pertama muka jalan).
   - **UMKM** = bangunan di dalam klaster **titik produsen tempe hasil survei** (sentra tempe eksisting di barat laut kawasan).
   - **Permukiman** = sisa bangunan hunian (kode BIG 1201).
   - **Fasilitas umum** (sekolah, masjid, gereja, kantor pos/pegadaian, gudang KAI; 30 bangunan) **dikeluarkan** karena bukan salah satu dari 4 aktivitas.
   - Lihat peta: `Data_Eksisting_Kriteria_Terukur/peta_kelompok_eksisting.png`.
2. **Luas lantai dasar** = luas poligon bangunan (UTM 49S, EPSG:32749).
3. **Jumlah lantai per bangunan** = kelas tinggi yang paling dominan menutupi bangunan tersebut. **Rata-rata lantai** = rata-rata aritmetika jumlah lantai seluruh bangunan dalam kelompok.
4. **Luas lantai total** = luas lantai dasar × jumlah lantai.

### 3.1 Estimasi luas lahan / persil (untuk UMKM, pertokoan, permukiman)
Peta bidang tanah/persil tidak tersedia di folder proyek, jadi luas lahan per bangunan diestimasi dengan **tessellation (Voronoi) jejak bangunan**: setiap titik di kawasan diberikan ke bangunan terdekat, dibatasi maksimal 10 m dari dinding bangunan dan di dalam delineasi. Hasilnya adalah "lahan yang dikuasai" tiap bangunan.

Keterbatasan: estimasi ini **cenderung lebih besar** dari persil sebenarnya karena ikut memasukkan sebagian gang/jalan dan halaman kosong di sekitarnya, sehingga KDB estimasi cenderung **lebih kecil** dari KDB sebenarnya. Jika kelompok punya data **Bidang Tanah BPN**, angka luas lahan sebaiknya diganti dengan data itu.

---

## 4. Data trotoar eksisting

### 4.1 Jl. Jend. Ahmad Yani (muka Pasar dan Pertokoan)
Penampang melintang hasil survei Andalalin 2023 (Gbr. III.19, Tabel III.7) — **tidak ada trotoar**, sisi jalan hanya berupa bahu dan drainase:

| Elemen | Sisi kiri | Sisi kanan | **Rata-rata** |
|---|---|---|---|
| Trotoar | – | – | **0 m (tidak ada)** |
| Bahu jalan | 1,7 m | 2,0 m | **1,85 m** |
| Drainase | 1,7 m | 1,3 m | **1,5 m** |
| Badan jalan | 7 m (perkerasan rigid, 2/2 UD, tanpa median) | | |

Status jalan: jalan provinsi, kolektor primer, kelas II. Laporan kelompok (`_Cangkot D3.2.pdf` hlm. 4) juga mencatat fasilitas pejalan kaki dan pesepeda **belum terpenuhi** di sepanjang Jl. Ahmad Yani; bahu jalan dipakai PKL, bongkar-muat, dan parkir.

> Ada perbedaan data: catatan penampang kelompok (dari DWG) menyebut badan jalan 6 m, lajur 3 m, drainase 0,5 m, sedangkan Andalalin mencatat 7 m. Untuk kondisi eksisting disarankan memakai **Andalalin** karena berupa hasil survei lapangan 2023 yang terdokumentasi.

### 4.2 Jalan lokal/lingkungan (UMKM dan Permukiman)
- Laporan kelompok (`_Cangkot D3.2.pdf` hlm. 23): jalan lokal dan lingkungan "cenderung tidak terlalu lebar, hanya bisa dilintasi maksimal 2 mobil, dan **belum difasilitasi dengan trotoar**." → **lebar trotoar = 0 m**.
- Sebagai pembanding, ruas jalan kabupaten di sekitar pasar yang disurvei Andalalin (Tabel III.7) juga **tanpa trotoar**:

| Ruas (Andalalin 2023) | Lebar perkerasan | Bahu kiri | Bahu kanan |
|---|---|---|---|
| Jl. Stasiun | 4,0 m | 1,0 m | 2,0 m |
| Jl. Cendrawasih | 4,0 m | 1,0 m | 2,0 m |
| Jl. Letkol Sudarso | 4,0 m | 0,3 m | 1,3 m |
| Jl. Betet | 4,0 m | 1,6 m | 1,6 m |
| Jl. Lettu Suparto | 4,7 m | 0,9 m | 0,8 m |
| Jl. Jerukmanis | 4,4 m | 1,5 m | 1,7 m |
| Jl. Kedawung | 4,4 m | 1,5 m | 1,7 m |
| **Rata-rata** | **4,21 m** | **1,11 m** | **1,59 m** (rata-rata kedua sisi **1,35 m**) |

> Ruas-ruas ini berada di sekitar pasar, tetapi belum tentu semuanya di dalam delineasi. Data survei jalan lingkungan kelompok (layer `JALAN_KROYA_AFTER_SURVEY` / `JALAN_LINGKUNGAN_DOANG` di proyek ArcGIS) tidak ada di folder repo, sehingga lebar jalan di dalam blok permukiman/UMKM belum bisa dirata-rata. Jika file itu diunggah, tabel ini bisa diperbarui.

---

## 5. Hal yang perlu diperhatikan sebelum dipakai di slide

1. **Luas lahan** UMKM, pertokoan, dan permukiman adalah **estimasi**. Tulis "± (estimasi tessellation jejak bangunan)" atau ganti dengan data Bidang Tanah BPN jika ada.
2. **Pertokoan** hanya mencakup deret pertama di muka Jl. A. Yani di dalam delineasi. Satu poligon BIG bisa berisi beberapa unit ruko.
3. **UMKM** hanya mencakup sentra tempe (industri rumahan). PKL belum masuk karena belum ada survei PKL.
4. **Lantai** berasal dari peta kelas tinggi (0–4 / 4–8 / > 8 m), jadi bangunan > 8 m dihitung 3 lantai (bisa saja lebih).
5. Data bangunan pasar mencerminkan kondisi **2020–2021**; saat ini bangunan pasar rusak ± 80% sejak kebakaran 23 Des 2021 (KAK Kemen PU).

Lampiran:
- Peta pengelompokan: `Claude outputs/Data_Eksisting_Kriteria_Terukur/peta_kelompok_eksisting.png`
- Data per bangunan (615 baris: kelompok, luas tapak, jumlah lantai, luas lantai, estimasi persil, jarak ke Jl. A. Yani, koordinat): `Claude outputs/Data_Eksisting_Kriteria_Terukur/bangunan_eksisting_per_kelompok.csv`
