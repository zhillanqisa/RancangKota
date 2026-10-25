import math
S=0.001; I=7.678e-8
def kdb(A,c):
    iinf_lm=S*A; iinf=iinf_lm/60
    qinf=c*I*A*1000  # l/s
    q1=qinf/(A/1e4)
    os_=iinf/q1
    k=(A/1e4-os_)/(A/1e4)
    return dict(iinf_lm=iinf_lm,iinf=iinf,qinf=qinf,q1=q1,os=os_,kdb=k)
A=333518
for c in (1.8,1.2,0.8): print(c, {k:round(v,4) for k,v in kdb(A,c).items()})
# FAR
for c in (1.8,1.2,0.8):
    k=kdb(A,c)['kdb']; print('FAR',c,round(1/k,2))
# ALO pasar
Jd=6.5; Is=104.2; Jb=0
H=0.5*(Jd+Is+Jb); print('Htot',H,'h',H-1.5)
# GSB
def t_of(v):
    tab=[(0,.76),(10,.8),(20,.9),(30,1.0),(40,1.22),(50,1.55),(60,2.0)]
    for (v0,t0),(v1,t1) in zip(tab,tab[1:]):
        if v0<=v<=v1: return t0+(t1-t0)*(v-v0)/(v1-v0)
def gsb(Va_k,Vb_k,a1,b1):
    Va=Va_k/1.6; Vb=Vb_k/1.6; ta=t_of(Va)
    Da_ft=0.063*Va**2+1.47*ta*Va+16; Da=Da_ft/3.28
    Db_ft=Vb*Da_ft/Va+16; Db=Db_ft/3.28
    a=Db*(Da-b1)/Da; a2=a-a1
    b2=Da-b1-a1*Da/Db; b=b1+b2
    return dict(Va=Va,Vb=Vb,ta=ta,Da_ft=Da_ft,Da=Da,Db_ft=Db_ft,Db=Db,a2=a2,a=a,b2=b2,b=b)
print({k:round(v,3) for k,v in gsb(40,20,5,1.6).items()})
print({k:round(v,3) for k,v in gsb(20,20,1.6,1.6).items()})
