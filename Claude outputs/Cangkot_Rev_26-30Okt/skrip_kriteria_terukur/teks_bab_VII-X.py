from content import A as A0, P as P0
A=dict(A0); A.update(kdb_hitung='MAHZBU29ltI',kdb_zona='MAHZBZ7Zso8',tinggi_hitung='MAHZBd0FtQY',gsb_hitung='MAHZBTu81zY',gsb_simpang='MAHZBT2Er2A',jarak_hitung='MAHZBWV4Vsk',metode_kt='MAHZBZIofak',amplop_rekap='MAHZBXWbsA0')
P=dict(P0)
P[77]=dict(title="Analisis Koefisien Dasar Bangunan (KDB)",
 img=['kdb_eksisting','kdb_hitung','kdb_zona'],
 alt=['KDB eksisting per zona dari data bangunan BIG/OSM','Perhitungan KDB metode infiltrasi air tanah: Iinf, Qinf, Q1Ha, OS, dan KDB 87,9%','Grafik KDB rencana per zona dibanding KDB maksimum hasil infiltrasi'],
 d="Luas kawasan (A) 33,35 ha dengan kemiringan 0–5% (datar).\nTapak bangunan eksisting 105.679 m², sehingga KDB eksisting 31,7%; tertinggi di Pasar Induk (54%) dan koridor dagang (48%).\nKonstanta buku ajar: S = 0,001; I = 7,678 × 10⁻⁸ m/detik; c dari Tabel A.1.",
 a="Iinf = 0,001 × 333.518 = 333,5 l/menit = 5,56 l/detik.\nQinf = 1,8 × 7,678.10⁻⁸ × 333.518 = 46,09 l/detik; Q1Ha = 1,382 l/detik/ha.\nOS = 5,56 / 1,382 = 4,02 ha, sehingga KDB = (33,35 − 4,02) / 33,35 = 87,9% ≈ 88%.\nZona c = 1,2 → KDB maks 81,9%; zona c = 0,8 → 72,9%.",
 r="KDB maks: zona pusat/komersial 88%, permukiman dan pendidikan 82%, RTH dan sawah 73%.\nSemua zona rencana memenuhi. Gedung parkir (86,7%) paling dekat batas, sehingga tapaknya diperkecil menjadi 486 m² (75,6%).\nKDB kawasan rencana 32,2%; lahan tak terbangun ±22,6 ha, jauh di atas OS minimum 4,02 ha.")
P[78]=dict(title="Analisis Ketinggian Bangunan",
 img=['tinggi_eksisting','tinggi_hitung','tinggi_rencana'],
 alt=['Peta ketinggian bangunan eksisting','Perhitungan ketinggian: jalur pesawat, FAR dan grafik LUI, ALO 45 derajat Pasar Induk, kesimpulan 6 lantai','Peta ketinggian bangunan rencana Rev 24 Okt'],
 d="Permukiman didominasi bangunan 1–2 lantai (4–8 m); bangunan ≥3 lantai hanya setempat di koridor A. Yani, Kato, dan sekolah.\nBandara terdekat Tunggul Wulung (Cilacap) berjarak ±23 km.\nTapak Pasar Induk: Is = 104,2 m; ROW A. Yani rencana 13 m; KDB maks 87,9%.",
 a="Jalur pesawat: 23 km > 9.090 m (batas keliling 2, Tabel B.2), jadi tidak membatasi.\nFAR = 1 / 0,879 = 1,14 → grafik LUI ±6,5 → 6 lantai (±24 m).\nALO 45°: Htot = 0,5 (6,5 + 104,2 + 0) = 55,35 m; h' = 53,85 m ≈ 13 lantai.\nDiambil nilai terendah: tinggi maks 6 lantai / 24 m.",
 r="Tinggi maksimum kawasan ditetapkan 6 lantai (24 m).\nBangunan baru tertinggi adalah Pasar Induk dan gedung parkir, 3 lantai (±13,3 m); digital hub, TPS3R, dan balai pelatihan 1 lantai.\nProporsi tapak rencana: 1 lantai 32,0%, 2 lantai 55,3%, ≥3 lantai 12,6%; semuanya di bawah 6 lantai.")
P[79]=dict(title="Analisis Garis Sempadan Bangunan",
 img=['gsb_section','gsb_hitung','gsb_simpang'],
 alt=['Penampang Jl. A. Yani rencana dan garis sempadan bangunan pasar','Perhitungan GSB metode jarak pengereman simpang Jl. A. Yani dan Jl. Cendrawasih','Skema GSB kavling sudut simpang A. Yani dan Cendrawasih, a 17,6 m dan b 20,1 m'],
 d="Jl. A. Yani (kolektor primer): badan jalan 6 m, rencana trotoar 2 m; kecepatan rencana 40 km/jam.\nJl. Cendrawasih (lingkungan): lebar 3,2 m tanpa trotoar; kecepatan ±20 km/jam.\nWaktu reaksi ta = 0,95 detik (Tabel C.2, 25 mil/jam).",
 a="a1 = 3 + 2 = 5 m; b1 = 1,6 m; Va = 25 mil/jam; Vb = 12,5 mil/jam.\nDa = 0,063(25)² + 1,47(0,95)(25) + 16 = 90,29 ft = 27,53 m; Db = 61,14 ft = 18,64 m.\nb2 = 0 → a2 = 12,56 m, jadi a = 17,6 m; a2 = 0 → b2 = 18,54 m, jadi b = 20,1 m (dari as jalan).",
 r="Kavling sudut simpang A. Yani × Cendrawasih bebas bangunan dan penghalang pandang sampai a = 17,6 m dari as A. Yani atau b = 20,1 m dari as Cendrawasih.\nRuko sudut eksisting tidak menambah lantai, kanopi, atau reklame di sudut; bila dibangun ulang wajib mengikuti GSB.\nPasar Induk berada di seberang simpang T, di luar segitiga pandang.")
P[80]=dict(title="Analisis Jarak Antar Bangunan",
 img=['jarak_map','jarak_hitung','gp_respon'],
 alt=['Peta jarak antar bangunan baru pada DWG Rev 24 Okt','Tabel jarak antar bangunan berdasarkan ALO 45 derajat dan Tabel B.3 DPU 1987','Usulan penyesuaian tapak gedung parkir'],
 d="Jarak diukur dari DWG Rev 24 Okt untuk lima pasangan bangunan baru.\nPasar–Kato 9,0 m; pasar–rumah 14,2 m; gedung parkir–kantor pos 1,0 m; TPS3R–bangunan servis 1,6 m; balai pelatihan–rumah 2,8 m.\nAcuan buku ajar: ALO (jarak = tinggi / tg 45°) dan Tabel B.3 DPU 1987.",
 a="Tinggi maks kawasan 24 m: ALO → 24 m; DPU (14–40 m) → 6–8 m.\nPasar–rumah (14,2 m) memenuhi DPU dan ALO; pasar–Kato (9,0 m) memenuhi DPU 3–6 m, tetapi kurang dari ALO 13,3 m.\nGedung parkir–kantor pos, TPS3R–bangunan servis, dan balai pelatihan–rumah belum memenuhi jarak minimum DPU 3 m.",
 r="Tapak gedung parkir diperkecil menjadi 36 × 13,5 m (486 m²) sehingga berjarak 3,0 m dari kantor pos.\nTPS3R dan balai pelatihan (1 lantai) digeser hingga berjarak ≥3 m.\nMassa lantai 1–2 pasar di sisi Kato setinggi ±8,84 m (FFL lantai 3) < 9,0 m, sehingga memenuhi ALO 45°; lantai 3 sisi Kato dibuat mundur.")
P[83]=dict(P0[83],title="Analisis Sumbu dan Hierarki",
 d="Jl. A. Yani membentang utara–selatan sebagai sumbu utama kawasan; pintu utama pasar berada di tengah fasad barat, tegak lurus jalan.\nBangunan Pasar Induk saat ini mangkrak; rancangan baru 92 × 54 m, 3 lantai (tapak 4.968 m²).\nMedian tapak rumah sekitar 108,5 m² (n = 488), umumnya 1–2 lantai.",
 a="Sumbu A. Yani kuat sebagai jalur gerak, tetapi belum punya penanda awal dan akhir; sumbu pintu utama pasar belum terbaca dari jalan.\nMassa pasar ±46 kali tapak rumah median, sehingga menjadi elemen dominan dan puncak hierarki kawasan.\nTanpa elemen peralihan, muka pasar terasa menekan bagi pejalan kaki.",
 r="Sumbu A. Yani ditegaskan dengan trotoar, jalur hijau, dan pohon berulang dari simpang Betet (ME) sampai perlintasan KA (X).\nSumbu silang dari simpang Cendrawasih ke pintu utama pasar dipertegas zebra cross, kanopi, dan halaman depan.\nHierarki massa: pasar 3 lantai → Kato/ruko 2–3 lantai → selasar PKL 1 lantai → permukiman 1–2 lantai.")
P[84]=dict(P0[84],title="Analisis Irama, Kontekstual, Kontras",
 alt=['Foto koridor Jl. A. Yani eksisting','Kontekstual: atap genteng merah-bata pada pasar, Kato, dan ruko; trotoar menerus','Irama pohon peneduh dan jalur hijau di kedua sisi Jl. A. Yani'],
 d="Koridor Jl. A. Yani belum memiliki trotoar dan jalur hijau menerus; pohon peneduh hanya ada setempat.\nRuko, Kato, dan rumah memakai atap pelana/limasan genteng merah bata.\nMuka bangunan tertutup lapak PKL, parkir, dan reklame yang beragam.",
 a="Bahasa atap genteng yang seragam membentuk karakter kontekstual, tetapi belum diikat elemen jalan yang sama.\nTidak ada pengulangan elemen berjarak teratur, sehingga irama koridor belum terbentuk.\nMassa pasar 3 lantai dengan skylight akan kontras terhadap ruko 1–2 lantai; kontras ini perlu diarahkan agar pasar terbaca sebagai pusat.",
 r="Pohon peneduh ditanam berulang tiap ±5–10 m (±133 titik di koridor A. Yani), berlanjut di RTH sempadan rel sebagai irama kawasan.\nAtap pasar, Kato, dan ruko tetap genteng merah bata agar kontekstual.\nKontras dipusatkan pada skylight pasar dan kanopi pintu utama; reklame ruko diseragamkan ukuran dan letaknya.")
P[85]=dict(P0[85],title="Analisis Simetri, Balance, dan Proporsi",
 d="Jl. A. Yani lebar 6 m; jarak fasad ruko ke fasad pasar (D) ±17,5 m.\nRuko sisi barat umumnya 2 lantai (±8 m), pasar 3 lantai (±13,3 m).\nPintu utama pasar berada di tengah fasad barat; halaman depan belum tertata.",
 a="D/H terhadap pasar = 17,5/13,3 ≈ 1,3 (seimbang, terlingkupi); terhadap ruko = 17,5/8 ≈ 2,2 (mulai terbuka). Ashihara: D/H 1–2 ideal.\nKedua sisi jalan tidak sama tinggi, sehingga keseimbangan koridor bersifat asimetris.\nSumbu pintu utama dapat menjadi poros simetri halaman depan.",
 r="Halaman depan disusun simetris terhadap sumbu pintu utama: selasar PKL dan showcase di sisi utara dan selatan.\nPohon peneduh di sisi ruko mengimbangi massa pasar dan menutup kesan terbuka (D/H 2,2).\nSelasar 1 lantai menjadi skala manusia di depan pasar; ruko maksimal 3 lantai agar D/H tetap 1–2.")
