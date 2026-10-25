from draw import *
G2=gsb(20,20,1.6,1.6)
# ---------- metode ----------
fig=plt.figure(figsize=(24,14.46)); fig.patch.set_facecolor(BG)
fig.text(0.012,0.955,'Metode perhitungan kriteria terukur (amplop bangunan) – buku ajar Perancangan Kota (Ristianti, 2020)',fontsize=24,weight='bold',color=OL)
W=0.237; X=[0.012+i*(W+0.009) for i in range(4)]
card(fig,X[0],0.05,W,0.87,'1. KDB – infiltrasi air tanah',[
 'Iinf = S × A   (S = 0,001)','  l/menit ÷ 60 → l/detik',
 'Qinf = c × I × A','  I = 7,678×10⁻⁸ m/detik',
 'Q1Ha = (1 Ha × Qinf) / A','OS = Iinf / Q1Ha','KDB = (A − OS) × 100% / A','',
 '**Tabel A.1 Koefisien infiltrasi (c)','**  Daerah         0–5%  5–10%  10–30%',
 '  Sedikit terbuka  1,8   1,9    2,2','  Cukup terbuka    1,2   1,4    1,7','  Terbuka hijau    0,8   1,0    1,2','',
 '!!Kroya datar (0–5%): c = 1,8 / 1,2 / 0,8'],fs=15,tfs=18,lh=0.055)
card(fig,X[1],0.05,W,0.87,'2. Ketinggian bangunan',[
 '**a) Jalur terbang pesawat','Tm = Tm1 ± St','  (+ bila lokasi lebih rendah dari bandara)',
 'Tabel B.2: keliling 1 ≤ 2.272,5 m → 45,5 m','keliling 2 ≤ 9.090 m → 151,5 m',
 '**b) FAR & grafik LUI','FAR = total luas lantai / luas lantai dasar','  → baca jumlah lantai di Gambar B.2',
 '**c) ALO (α = 45°)','Htot = 0,5 (Jd + Is + Jb) tg α',"h' = Htot − 1,5 tg α",'  Jd/Jb = ½ lebar jalan depan/belakang','  Is = panjang site','',
 '!!Dipakai nilai terendah dari a, b, c'],fs=15,tfs=18,lh=0.055)
card(fig,X[2],0.05,W,0.87,'3. Jarak antar bangunan',[
 '**a) ALO','Jarak = tinggi bangunan / tg ALO','  = tinggi / tg 45° = tinggi','',
 '**b) Tabel B.3 (Dep. PU, 1987)','**  Tinggi bangunan   Jarak','  0 – 8 m           3 m','  8 – 14 m          3 – 6 m','  14 – 40 m         6 – 8 m','  > 40 m            > 8 m','',
 'Fungsi: sirkulasi, pencahayaan,','keselamatan kebakaran dan bencana'],fs=15,tfs=18,lh=0.06)
card(fig,X[3],0.05,W,0.87,'4. GSB – jarak pengereman',[
 'Da = 0,063 Va² + 1,47 ta Va + 16  (ft)','Vb = (Db − 16) Va / Da','Db = (a1+a2) Da / (Da − (b1+b2))',
 'a1, b1 = ½ badan jalan + trotoar','a = a1 + a2 ;  b = b1 + b2','km/jam ÷ 1,6 ; feet ÷ 3,28','',
 '**Tabel C.2 waktu reaksi (t)','  V (mil/jam) 0    10   20   30','  t (detik)   0,76 0,80 0,90 1,00','  V (mil/jam) 40   50   60','  t (detik)   1,22 1,55 2,00','',
 '**Tabel C.1 badan jalan minimum','Arteri 8 · kolektor 7 · lokal 6 ·','lingkungan 3,5 · setapak 2,5 m'],fs=15,tfs=18,lh=0.051)
save(fig,'metode_kt.jpg')

# ---------- rekap ----------
fig=plt.figure(figsize=(24,14.46)); fig.patch.set_facecolor(BG)
fig.text(0.012,0.955,'Rekapitulasi amplop bangunan per zona tapak – hasil perhitungan buku ajar vs rencana Rev 24 Okt',fontsize=24,weight='bold',color=OL)
yani={'Pasar Induk','Kato, kios & ruko','Halaman depan PKL','Koridor dagang & jasa','Kantor pos'}
jar={'Gedung parkir UMKM/PKL':'1,0→3,0 m*','TPS3R':'1,6→3,0 m*','Balai pelatihan UMKM':'2,8→3,0 m*'}
hdr=['Zona tapak','Luas (m²)','c','KDB maks\ninfiltrasi','KDB\nrencana','Tinggi maks\n(FAR/LUI)','Lantai\nrencana','Jarak min\n(DPU)','GSB kavling sudut\n(dari as jalan)','Status']
rows=[]
for n,a,c,k,l in Z:
    m=kmax[c]
    tinggi_r={0:'–',1:'1 lt (±4 m)',2:'2 lt (±8 m)',3:'3 lt (±13 m)'}[l]
    dpu='3 m' if l<=2 else '3–6 m'
    g='a 17,6 / b 20,1 m' if n in yani else (f'a {fmt(G2["a"],1)} / b {fmt(G2["b"],1)} m' if l>0 else '–')
    st='✓' if k<=m else '✗'
    if n in jar: st='✓ setelah\ngeser'; dpu=dpu+' ('+jar[n]+')'
    rows.append([n,f'{a:,}'.replace(',','.'),str(c).replace('.',','),fmt(m,1)+'%',fmt(k,1)+'%','6 lt / 24 m',tinggi_r,dpu,g,st])
ax=fig.add_axes([0.012,0.08,0.976,0.85]); ax.axis('off')
t=ax.table(cellText=rows,colLabels=hdr,loc='upper center',cellLoc='center',colWidths=[0.17,0.07,0.04,0.08,0.07,0.09,0.09,0.13,0.15,0.08])
t.auto_set_font_size(False); t.set_fontsize(15); t.scale(1,3.25)
for (r,c),cell in t.get_celld().items():
    cell.set_edgecolor(OL)
    if r==0: cell.set_facecolor(OL); cell.get_text().set_color('white'); cell.get_text().set_weight('bold'); cell.set_height(cell.get_height()*1.5)
    else:
        cell.set_facecolor('white' if r%2 else '#f6f2dc')
fig.text(0.012,0.035,'KDB maks: metode infiltrasi (c per tipe daerah tangkapan, kemiringan 0–5%). Tinggi maks: nilai terendah dari jalur pesawat (tidak berlaku, bandara ±23 km), FAR/LUI (6 lt) dan ALO 45° (13 lt).\n'
 'GSB: kavling sudut simpang A. Yani × jalan lingkungan (a dari as A. Yani, b dari as jalan lingkungan) dan simpang antar jalan lingkungan (Va = Vb = 20 km/jam). *Jarak setelah respon (geser/perkecil tapak).',fontsize=13,color='#5b5e44')
save(fig,'amplop_rekap.jpg')
