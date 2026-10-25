import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch
import math
from calc import kdb, gsb
BG='#fcf7e3'; OL='#4c5928'; TX='#2f3318'; RD='#b03a2e'; LT='#ebe6c9'; GR='#7d8a3c'
OUT='../gambar/'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':TX})
def fmt(x,d=2): return f"{x:,.{d}f}".replace(',','X').replace('.',',').replace('X','.')
def card(fig,x,y,w,h,title,lines,fs=11.5,tfs=13,lh=None):
    ax=fig.add_axes([x,y,w,h]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.add_patch(FancyBboxPatch((0.005,0.005),0.99,0.99,boxstyle='round,pad=0,rounding_size=0.02',fc='white',ec=OL,lw=1.4))
    ax.add_patch(Rectangle((0.005,0.88),0.99,0.115,fc=OL,ec=OL))
    ax.text(0.03,0.937,title,color='white',fontsize=tfs,weight='bold',va='center')
    n=len(lines); lh=lh or min(0.085,0.84/max(n,1)); yy=0.85-lh*0.6
    for ln in lines:
        bold=ln.startswith('**'); red=ln.startswith('!!')
        t=ln.strip('*').lstrip('!')
        ax.text(0.03,yy,t,fontsize=fs,va='center',weight='bold' if (bold or red) else 'normal',color=RD if red else TX,family='DejaVu Sans Mono' if t.startswith('  ') else 'DejaVu Sans')
        yy-=lh
    return ax
def save(fig,name):
    fig.savefig(OUT+name,dpi=100,facecolor=BG); plt.close(fig); print('saved',name)

A=333518; K18=kdb(A,1.8); K12=kdb(A,1.2); K08=kdb(A,0.8)
G=gsb(40,20,5,1.6)

# ---------- 1. KDB hitung (analisis) ----------
fig=plt.figure(figsize=(10.59,7.5)); fig.patch.set_facecolor(BG)
fig.text(0.02,0.955,'Perhitungan KDB berdasarkan infiltrasi air tanah (buku ajar, Pokok Bahasan I)',fontsize=14,weight='bold',color=OL)
card(fig,0.02,0.05,0.56,0.87,'Kawasan inti (pusat kota, kemiringan 0–5%, c = 1,8)',[
 'Diketahui: A = 333.518 m² = 33,35 ha',
 'S = 0,001 ;  I = 7,678 × 10⁻⁸ m/detik ;  c = 1,8 (Tabel A.1)',
 '**a) Iinf = S × A',
 f'  = 0,001 × 333.518 = {fmt(K18["iinf_lm"],1)} l/menit',
 f'  = {fmt(K18["iinf"])} l/detik',
 '**b) Qinf = c × I × A',
 f'  = 1,8 × 7,678.10⁻⁸ × 333.518',
 f'  = 0,0461 m³/detik = {fmt(K18["qinf"])} l/detik',
 '**c) Q1Ha = (1 Ha × Qinf) / A',
 f'  = {fmt(K18["qinf"])} / 33,35 = {fmt(K18["q1"],3)} l/dtk/ha',
 '**d) OS = Iinf / Q1Ha',
 f'  = {fmt(K18["iinf"])} / {fmt(K18["q1"],3)} = {fmt(K18["os"])} ha',
 '**e) KDB = (A − OS) × 100% / A',
 f'  = (33,35 − {fmt(K18["os"])}) / 33,35',
 f'!!  = {fmt(K18["kdb"]*100,1)}% ≈ 88%',
],fs=12,lh=0.056)
ax=card(fig,0.6,0.05,0.38,0.87,'Nilai c per tipe daerah tangkapan',[],tfs=12)
rows=[('Tipe zona','c','OS*','KDB maks'),
      ('Pusat kota / komersial\n(K-1, kantor pos, TPS3R)','1,8',fmt(K18['os']),fmt(K18['kdb']*100,1)+'%'),
      ('Cukup terbuka, ±50% hijau\n(permukiman, tempe,\npendidikan, balai)','1,2',fmt(K12['os']),fmt(K12['kdb']*100,1)+'%'),
      ('Terbuka hijau\n(RTH, taman, sawah)','0,8',fmt(K08['os']),fmt(K08['kdb']*100,1)+'%')]
ys=[0.80,0.66,0.47,0.30]
for r,y in zip(rows,ys):
    hd=(y==0.80)
    for x,t in zip((0.04,0.52,0.61,0.80),r):
        ax.text(x,y,t,fontsize=10.5 if not hd else 10.5,weight='bold' if hd else 'normal',va='center',color=OL if hd else TX)
    ax.plot([0.03,0.97],[y-0.075 if hd else y-0.095]*2,color=LT,lw=1)
ax.text(0.04,0.15,'*OS (ha) dihitung untuk A kawasan 33,35 ha.\nKDB tidak bergantung luas: OS/A = 1/(6 × c × 0,7678).\nKemiringan Kroya 0–5% (datar).',fontsize=9.5,va='center',color='#5b5e44')
save(fig,'kdb_hitung.jpg')

# ---------- 2. KDB per zona (respon) ----------
Z=[('Pasar Induk',8053,1.8,65.3,3),('Kato, kios & ruko',4722,1.8,45.5,3),('Halaman depan PKL',938,1.8,22.8,1),
   ('Koridor dagang & jasa',33469,1.8,47.5,3),('Digital hub',100,1.8,81.1,1),('Gedung parkir UMKM/PKL',643,1.8,86.7,3),
   ('Rumah tinggal komersial',8770,1.8,42.0,3),('Kantor pos',1645,1.8,50.1,2),('TPS3R',688,1.8,54.6,1),
   ('Permukiman eksisting',178124,1.2,32.2,3),('Klaster tempe',38446,1.2,25.4,2),('Pendidikan',20596,1.2,41.3,3),
   ('Balai pelatihan UMKM',343,1.2,33.3,1),('RTH sempadan rel',20410,0.8,12.8,3),('Taman kawasan',1378,0.8,0.0,0),('Sawah',15202,0.8,0.1,2)]
kmax={1.8:K18['kdb']*100,1.2:K12['kdb']*100,0.8:K08['kdb']*100}
fig=plt.figure(figsize=(10.59,7.5)); fig.patch.set_facecolor(BG)
fig.text(0.02,0.955,'KDB rencana Rev 24 Okt vs KDB maksimum hasil infiltrasi',fontsize=14,weight='bold',color=OL)
ax=fig.add_axes([0.29,0.1,0.66,0.82]); ax.set_facecolor(BG)
for i,(n,a,c,k,l) in enumerate(Z[::-1]):
    m=kmax[c]; ax.barh(i,m,color=LT,height=0.75); ax.barh(i,k,color=OL if k<=m else RD,height=0.45)
    ax.text(k+1,i,f'{fmt(k,1)}%',va='center',fontsize=9.5,color=TX)
    ax.text(94,i,f'maks {fmt(m,1)}%',va='center',fontsize=8.5,color='#7a7a5a')
ax.set_yticks(range(len(Z))); ax.set_yticklabels([f'{z[0]} (c={str(z[2]).replace(".",",")})' for z in Z[::-1]],fontsize=9.5)
ax.set_xlim(0,106); ax.set_xlabel('KDB (%)')
for s in ('top','right'): ax.spines[s].set_visible(False)
fig.text(0.02,0.03,'Semua zona ≤ KDB maks infiltrasi. Gedung parkir 86,7% paling dekat batas 87,9%. OS kawasan wajib ≥ 4,02 ha; ruang terbuka rencana ±22,6 ha.',fontsize=9.5,color='#5b5e44')
save(fig,'kdb_zona.jpg')

# ---------- 3. Ketinggian hitung ----------
fig=plt.figure(figsize=(10.59,7.5)); fig.patch.set_facecolor(BG)
fig.text(0.02,0.955,'Perhitungan ketinggian maksimum (buku ajar, Pokok Bahasan II)',fontsize=14,weight='bold',color=OL)
card(fig,0.02,0.52,0.47,0.4,'a) Jalur terbang pesawat',[
 'Bandara terdekat: Tunggul Wulung, Cilacap',
 'Jarak ke kawasan ±23 km',
 'Tabel B.2: keliling 1 ≤ 2.272,5 m (Tm1 45,5 m);',
 'keliling 2 ≤ 9.090 m (Tm1 151,5 m)',
 '!!23 km > 9.090 m → di luar zona KKOP,',
 '!!tidak membatasi tinggi bangunan',
],fs=11,lh=0.13)
card(fig,0.51,0.52,0.47,0.4,'b) FAR & grafik LUI',[
 'FAR = total luas lantai / luas lantai dasar',
 '  = A / (KDB × A) = 1 / 0,879',
 '  = 1,14 (c 1,2 → 1,22; c 0,8 → 1,37)',
 'Grafik LUI (Gambar B.2): FAR 1,14–1,37',
 '→ LUI ±6,5 → setara 6 lantai',
 '!!Tinggi maks ≈ 6 lantai × 4 m = 24 m',
],fs=11,lh=0.13)
card(fig,0.02,0.05,0.47,0.44,'c) ALO 45° – Pasar Induk',[
 'Jd = ½ ROW A. Yani rencana (13 m) = 6,5 m',
 'Is = panjang tapak pasar = 104,2 m',
 'Jb = 0 (berbatasan langsung dengan persil)',
 'Htot = 0,5 (Jd + Is + Jb) tg α',
 '  = 0,5 (6,5 + 104,2 + 0) × 1 = 55,35 m',
 "h' = Htot − 1,5 tg α = 53,85 m",
 '!!≈ 13 lantai',
],fs=11,lh=0.115)
ax=card(fig,0.51,0.05,0.47,0.44,'Kesimpulan (ambil nilai terendah)',[
 'Jalur pesawat : tidak berlaku',
 'FAR / LUI     : 6 lantai (24 m)',
 "ALO 45°       : 13 lantai (53,85 m)",
 '!!Tinggi maks kawasan = 6 lantai / 24 m',
 'Rencana tertinggi: pasar & gedung',
 'parkir 3 lantai (±13,3 m) → memenuhi',
],fs=11,lh=0.12)
save(fig,'tinggi_hitung.jpg')

# ---------- 4. GSB hitung ----------
fig=plt.figure(figsize=(10.59,7.5)); fig.patch.set_facecolor(BG)
fig.text(0.02,0.955,'Perhitungan GSB simpang Jl. A. Yani × Jl. Cendrawasih (Pokok Bahasan III)',fontsize=13.5,weight='bold',color=OL)
card(fig,0.02,0.05,0.47,0.87,'Diketahui',[
 '**Jalan a = Jl. A. Yani (kolektor primer)',
 'Va = 40 km/jam ÷ 1,6 = 25 mil/jam',
 'ta = 0,95 dtk (Tabel C.2, interpolasi)',
 'a1 = ½ badan jalan + trotoar',
 '  = 3 m + 2 m = 5 m',
 '**Jalan b = Jl. Cendrawasih (lingkungan)',
 'Vb = 20 km/jam ÷ 1,6 = 12,5 mil/jam',
 'b1 = ½ × 3,2 m + 0 (tanpa trotoar)',
 '  = 1,6 m',
 '',
 'Kecepatan rencana: kolektor primer',
 '≥ 40 km/jam, jalan lingkungan ±20 km/jam',
 '(PP 34/2006). Badan jalan A. Yani 6 m',
 '< 7 m minimum kolektor (Tabel C.1).',
],fs=11,lh=0.06)
card(fig,0.51,0.05,0.47,0.87,'Langkah menjawab',[
 '**1. Da = 0,063 Va² + 1,47 ta Va + 16',
 f'  = 39,38 + 34,91 + 16 = {fmt(G["Da_ft"])} ft',
 f'  ÷ 3,28 = {fmt(G["Da"])} m',
 '**2. Vb = (Db − 16) Va / Da',
 f'  12,5 = (Db − 16) × 25 / {fmt(G["Da_ft"])}',
 f'  Db = {fmt(G["Db_ft"])} ft = {fmt(G["Db"])} m',
 '**3. Db = (a1+a2) Da / (Da − (b1+b2))',
 f'  b2 = 0 → a2 = {fmt(G["a2"])} m',
 f'  a2 = 0 → b2 = {fmt(G["b2"])} m',
 '**4. Garis sempadan',
 f'!!  a = a1 + a2 = 5 + {fmt(G["a2"],1)} = {fmt(G["a"],1)} m',
 f'!!  b = b1 + b2 = 1,6 + {fmt(G["b2"],1)} = {fmt(G["b"],1)} m',
 '(diukur dari as jalan, berlaku di kavling sudut)',
],fs=11,lh=0.064)
save(fig,'gsb_hitung.jpg')

# ---------- 5. GSB simpang schematic ----------
fig=plt.figure(figsize=(10.59,7.5)); fig.patch.set_facecolor(BG)
fig.text(0.02,0.955,'Respon GSB kavling sudut simpang A. Yani × Cendrawasih (skematik)',fontsize=13.5,weight='bold',color=OL)
ax=fig.add_axes([0.03,0.06,0.94,0.86]); ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-48,30); ax.set_ylim(-30,30)
# A. Yani vertical at x=0 (badan 6 m), trotoar 2 m each side
ax.add_patch(Rectangle((-3,-30),6,60,fc='#8d8d8d',ec='none'))
ax.add_patch(Rectangle((-5,-30),2,60,fc='#d9d2b6',ec='none')); ax.add_patch(Rectangle((3,-30),2,60,fc='#d9d2b6',ec='none'))
ax.plot([0,0],[-30,30],ls=(0,(6,4)),color='white',lw=1.2)
# Cendrawasih horizontal to the west at y=0 width 3.2
ax.add_patch(Rectangle((-48,-1.6),43,3.2,fc='#8d8d8d',ec='none'))
ax.plot([-48,-5],[0,0],ls=(0,(4,4)),color='white',lw=1)
a=G['a']; b=G['b']
for sgn in (1,-1):
    # corner zone: setback lines
    ax.add_patch(Polygon([(-5,sgn*1.6),(-a,sgn*1.6),(-5,sgn*b)],closed=True,fc=RD,alpha=0.18,ec='none'))
    ax.plot([-a,-a],[sgn*1.6,sgn*12],color=RD,lw=2)
    ax.plot([-5,-14],[sgn*b,sgn*b],color=RD,lw=2)
    # ruko existing blocks
    ax.add_patch(Rectangle((-17,sgn*2.2 if sgn>0 else -2.2-9),11.5,9,fc='#c9604f',ec='#7a2a20',alpha=0.55))
ax.add_patch(Rectangle((8,-22),20,44,fc='#c9604f',ec='#7a2a20')); ax.text(18,0,'Pasar\nInduk\n(seberang simpang T,\ndi luar segitiga\npandang)',ha='center',va='center',fontsize=9.5,color='white',weight='bold')
ax.text(0,27,'Jl. A. Yani',rotation=90,ha='center',va='top',color='white',fontsize=10,weight='bold')
ax.text(-40,0,'Jl. Cendrawasih 3,2 m',ha='left',va='center',color='white',fontsize=9,weight='bold')
ax.annotate('',xy=(-a,-14),xytext=(0,-14),arrowprops=dict(arrowstyle='<->',color=TX))
ax.text(-6,-15.5,f'a = {fmt(a,1)} m dari as A. Yani',ha='right',va='top',fontsize=10,color=RD,weight='bold')
ax.annotate('',xy=(-8,b),xytext=(-8,0),arrowprops=dict(arrowstyle='<->',color=TX))
ax.text(-19,b-1,f'b = {fmt(b,1)} m\ndari as Cendrawasih',ha='right',va='center',fontsize=10,color=RD,weight='bold')
ax.text(-11.3,7,'ruko\nsudut',ha='center',va='center',fontsize=9,color='white'); ax.text(-11.3,-7,'ruko\nsudut',ha='center',va='center',fontsize=9,color='white')
ax.text(-47,-27,'Arsir merah = area bebas bangunan/penghalang\npandang di kavling sudut. Pilih salah satu:\nmundur a = 17,6 m dari as A. Yani, atau\nb = 20,1 m dari as Cendrawasih.',fontsize=9.3,color=TX,va='bottom')
save(fig,'gsb_simpang.jpg')

# ---------- 6. Jarak antar bangunan ----------
fig=plt.figure(figsize=(10.59,7.5)); fig.patch.set_facecolor(BG)
fig.text(0.02,0.955,'Jarak antar bangunan: ALO (tinggi / tg 45°) & DPU 1987 (Tabel B.3)',fontsize=13.5,weight='bold',color=OL)
ax=fig.add_axes([0.02,0.62,0.4,0.28]); ax.axis('off')
tb=[('Tinggi bangunan','Jarak DPU'),('0 – 8 m','3 m'),('8 – 14 m','3 – 6 m'),('14 – 40 m','6 – 8 m'),('> 40 m','> 8 m')]
t=ax.table(cellText=tb[1:],colLabels=tb[0],loc='center',cellLoc='center'); t.auto_set_font_size(False); t.set_fontsize(11); t.scale(1,1.6)
for (r,c),cell in t.get_celld().items():
    cell.set_edgecolor(OL)
    if r==0: cell.set_facecolor(OL); cell.get_text().set_color('white'); cell.get_text().set_weight('bold')
    else: cell.set_facecolor('white')
card(fig,0.45,0.6,0.53,0.32,'Tinggi maks kawasan 24 m (6 lantai)',[
 'ALO: jarak = 24 m / tg 45° = 24 / 1 = 24 m',
 'DPU: tinggi 14–40 m → jarak 6 – 8 m',
 'Bangunan rencana ≤ 3 lantai: jarak',
 'minimum DPU 3 m (≤ 8 m) atau 3–6 m (8–14 m)',
],fs=11,lh=0.17)
ax=fig.add_axes([0.02,0.05,0.96,0.5]); ax.axis('off')
rows=[('Pasangan bangunan','Tinggi','Jarak','DPU','ALO 45°'),
 ('Pasar ↔ Kato','±13,3 m','9,0 m','3–6 m ✓','13,3 m ✗'),
 ('Pasar ↔ rumah','±13,3 m','14,2 m','3–6 m ✓','13,3 m ✓'),
 ('Gedung parkir ↔ kantor pos','±12,5 m','1,0 m','3–6 m ✗','12,5 m ✗'),
 ('TPS3R ↔ bangunan servis','1 lt (±4 m)','1,6 m','3 m ✗','4 m ✗'),
 ('Balai pelatihan ↔ rumah','1 lt (±4 m)','2,8 m','3 m ✗','4 m ✗')]
t=ax.table(cellText=rows[1:],colLabels=rows[0],loc='center',cellLoc='center',colWidths=[0.34,0.15,0.13,0.18,0.18]); t.auto_set_font_size(False); t.set_fontsize(11.5); t.scale(1,2.1)
for (r,c),cell in t.get_celld().items():
    cell.set_edgecolor(OL)
    if r==0: cell.set_facecolor(OL); cell.get_text().set_color('white'); cell.get_text().set_weight('bold')
    else:
        cell.set_facecolor('white' if r%2 else '#f6f2dc')
        if '✗' in cell.get_text().get_text(): cell.get_text().set_color(RD); cell.get_text().set_weight('bold')
fig.text(0.02,0.02,'Jarak diukur dari DWG Rev 24 Okt. Sumber tabel: buku ajar Perancangan Kota (Ristianti, 2020), Tabel B.3 (Dep. PU, 1987).',fontsize=9,color='#5b5e44')
save(fig,'jarak_hitung.jpg')
