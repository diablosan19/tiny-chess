import json,random,urllib.request as R
U=R.os.getenv("MAKEFUN_ENV_URL")
def P(p,b):
 return json.load(R.urlopen(R.Request(U+p,json.dumps(b).encode())))
V=(0,100,320,330,500,900,0,0,0,100,320,330,500,900,0)
PHW=(0,0,1,1,2,4,0)
BD=(-17,-15,15,17);RD=(-16,-1,1,16);KN=(-33,-31,-18,-14,14,18,31,33);K8=BD+RD
CM={0:13,4:12,7:14,112:7,116:3,119:11}
Q6=[i for i in range(128)if not i&136]
def _ok(s):return 0<=s<128 and not s&136
NR=[];KR=[];BR=[];RR=[];PAW=[];PBW=[]
for s in range(128):
 if not _ok(s):NR.append(());KR.append(());BR.append(());RR.append(());PAW.append(());PBW.append(());continue
 NR.append(tuple(s+d for d in KN if _ok(s+d)))
 KR.append(tuple(s+d for d in K8 if _ok(s+d)))
 def _rays(ds):
  out=[]
  for d in ds:
   ray=[];t=s+d
   while _ok(t):ray.append(t);t+=d
   out.append(tuple(ray))
  return tuple(out)
 BR.append(_rays(BD));RR.append(_rays(RD))
 PAW.append(tuple(t for t in(s-15,s-17)if _ok(t)))
 PBW.append(tuple(t for t in(s+15,s+17)if _ok(t)))
QR=[BR[i]+RR[i]for i in range(128)]
RAYS=((),(),None,BR,RR,QR,None)
_PS=(
"iiiijkkejhgiiiimjjknkkmossssiiii",
"_accaeijcjklcilmcjlmciklaeii_acc",
"eggggjiigkkkgikkgjjkgijkgiiieggg",
"iiijhiiihiiihiiihiiihiiijkkkiiii",
"egghgijigjjjhijjiijjgijjgijieggh",
"caa_caa_caa_caa_eccageeemmiimoki",
"_ccccciickmockoqckoqckmocegi_ace")
TP={}
for p in(1,2,3,4,5):
 s=_PS[p-1];t=[0]*128
 for i in Q6:
  f=i&7;t[i]=V[p]+(ord(s[(7-(i>>4))*4+(f if f<4 else 7-f)])-105)*5
 TP[p]=t;TP[p+8]=[-t[i^112]for i in range(128)]
TP[6]=TP[14]=[0]*128
KT=[0]*128;KE=[0]*128
for i in Q6:
 f=i&7;j=(7-(i>>4))*4+(f if f<4 else 7-f);KT[i]=(ord(_PS[5][j])-105)*5;KE[i]=(ord(_PS[6][j])-105)*5
PBB=(0,5,10,18,30,48,70,0)
AW=[()]*128;AB=[()]*128
for s in Q6:
 f=s&7;r=s>>4
 AW[s]=tuple(q*16+g for q in range(r+1,8) for g in(f-1,f,f+1)if 0<=g<8)
 AB[s]=tuple(q*16+g for q in range(r) for g in(f-1,f,f+1)if 0<=g<8)
def PP():
 s=0;b=B
 for i in Q6:
  p=b[i]
  if p==1:
   r=i>>4;f=i&7;ok=1
   for t in AW[i]:
    if b[t]==9:ok=0;break
   if ok:
    v=PBB[r]
    if(f>0 and b[i-1]==1)or(f<7 and b[i+1]==1)or(r>1 and((f>0 and b[i-17]==1)or(f<7 and b[i-15]==1))):v+=v//2
    s+=v
  elif p==9:
   r=i>>4;f=i&7;ok=1
   for t in AB[i]:
    if b[t]==1:ok=0;break
   if ok:
    v=PBB[7-r]
    if(f>0 and b[i-1]==9)or(f<7 and b[i+1]==9)or(r<6 and((f>0 and b[i+17]==9)or(f<7 and b[i+15]==9))):v+=v//2
    s-=v
 return s
def SE():
 ph=PH
 s=EV+(KT[KS[0]]*ph+KE[KS[0]]*(16-ph))//16-(KT[KS[1]^112]*ph+KE[KS[1]^112]*(16-ph))//16+PP()
 return s if W else -s
_r=random.Random(1)
Z=[[_r.getrandbits(64)for _ in range(128)]for _ in range(15)]
ZC=[_r.getrandbits(64)for _ in range(16)];ZE=[_r.getrandbits(64)for _ in range(8)];ZS=_r.getrandbits(64)
B=[0]*128;W=True;CS=0;EP=-1;KEY=0;EV=0;PH=0;KS=[4,116];KL=[[0,0]for _ in range(128)]
TT={};REP=set();n=0;CAP=120000
M=99999
def AT(sq,byw):
 b=B
 if byw:
  for t in PAW[sq]:
   if b[t]==1:return 1
  pn,pk,pb,pr=2,6,(3,5),(4,5)
 else:
  for t in PBW[sq]:
   if b[t]==9:return 1
  pn,pk,pb,pr=10,14,(11,13),(12,13)
 for t in NR[sq]:
  if b[t]==pn:return 1
 for t in KR[sq]:
  if b[t]==pk:return 1
 for rays,ps in((BR[sq],pb),(RR[sq],pr)):
  for ray in rays:
   for t in ray:
    p=b[t]
    if p:
     if p in ps:return 1
     break
 return 0
def G(co=False):
 b=B;w=W;ms=[];ap=ms.append
 for s in Q6:
  p=b[s]
  if not p or(p<8)!=w:continue
  u=p&7
  if u==1:
   d=16 if w else-16;r=s>>4;pr=6 if w else 1
   t=s+d
   if not b[t]:
    if r==pr:
     for x in(5,4,3,2):ap(s|t<<7|x<<14)
    elif not co:
     ap(s|t<<7)
     if r==7-pr and not b[s+2*d]:ap(s|(s+2*d)<<7)
   for t in(PBW if w else PAW)[s]:
    q=b[t]
    if(q and(q<8)!=w)or t==EP:
     if r==pr:
      for x in(5,4,3,2):ap(s|t<<7|x<<14)
     else:ap(s|t<<7)
  elif u==2 or u==6:
   for t in(NR if u==2 else KR)[s]:
    q=b[t]
    if(q and(q<8)!=w)or(not co and not q):ap(s|t<<7)
   if u==6 and not co:
    base=0 if w else 112
    if s==base+4:
     for bit,g in((1,1),(2,-1)):
      if CS&(bit if w else bit<<2)and not b[s+g]and not b[s+2*g]and(g>0 or not b[s+3*g])and not AT(s,not w)and not AT(s+g,not w)and not AT(s+2*g,not w):ap(s|(s+2*g)<<7)
  else:
   for ray in RAYS[u][s]:
    for t in ray:
     q=b[t]
     if not q:
      if not co:ap(s|t<<7)
     else:
      if(q<8)!=w:ap(s|t<<7)
      break
 return ms
def MK(m):
 global W,CS,EP,KEY,EV,PH
 b=B;f=m&127;t=m>>7&127;pr=m>>14;p=b[f];u=p&7;w=p<8
 cap=b[t];csq=t
 if u==1 and t==EP and not cap:
  csq=(f&112)|(t&7);cap=b[csq]
 un=(m,p,cap,csq,CS,EP,KEY,EV,PH)
 KEY^=ZS^Z[p][f];EV-=TP[p][f]
 if cap:
  KEY^=Z[cap][csq];EV-=TP[cap][csq];PH-=PHW[cap&7]
  b[csq]=0
 np=p
 if pr:
  np=pr|(0 if w else 8);KEY^=Z[np][t];EV+=TP[np][t];PH+=PHW[pr]
 else:
  KEY^=Z[p][t];EV+=TP[p][t]
 b[f]=0;b[t]=np
 if u==6:
  KS[not w]=t
  if abs(t-f)==2:
   rf,rt=(f+3,f+1)if t>f else(f-4,f-1);rp=b[rf]
   b[rt]=rp;b[rf]=0;KEY^=Z[rp][rf]^Z[rp][rt];EV+=TP[rp][rt]-TP[rp][rf]
 ncs=CS&CM.get(f,15)&CM.get(t,15)
 KEY^=ZC[CS]^ZC[ncs];CS=ncs
 if EP>=0:KEY^=ZE[EP&7]
 EP=(f+t)//2 if u==1 and abs(t-f)==32 else-1
 if EP>=0:KEY^=ZE[EP&7]
 W=not w
 return un
def UM(un):
 global W,CS,EP,KEY,EV,PH
 m,p,cap,csq,CS,EP,KEY,EV,PH=un
 b=B;f=m&127;t=m>>7&127;u=p&7;w=p<8
 W=w
 if u==6:
  KS[not w]=f
  if abs(t-f)==2:
   rf,rt=(f+3,f+1)if t>f else(f-4,f-1);b[rf]=b[rt];b[rt]=0
 b[f]=p;b[t]=0
 if cap:b[csq]=cap
def LG():
 w=W;out=[]
 for m in G():
  un=MK(m)
  if not AT(KS[not w],not w):out.append(m)
  UM(un)
 return out
def SC(m):
 cap=B[m>>7&127]
 if cap:return V[cap&7]*32-V[B[m&127]&7]
 return 2000 if m>>14 else 0
def QS(al,be,ply):
 global n;n+=1
 if n>=CAP:raise 1
 w=W;chk=AT(KS[not w],not w)
 if chk:
  bs=-M;fd=False
 else:
  ph=PH
  st=SE()
  if st>=be:return st
  if st>al:al=st
  bs=st;fd=True
 for m in sorted(G()if chk else G(1),key=lambda m:-SC(m)):
  if not chk:
   t=m>>7&127;v=B[t]
   if not v and t==EP:v=1
   if st+V[v&7]+(V[m>>14]if m>>14 else 0)+200<al:continue
  un=MK(m)
  if AT(KS[not w],not w):UM(un);continue
  fd=True
  sc=-QS(-be,-al,ply+1);UM(un)
  if sc>bs:bs=sc
  if sc>al:al=sc
  if al>=be:break
 return bs if fd else-M+ply
def S(dep,al,be,ply,nm=1):
 global n,W,KEY,EP;n+=1
 if n>=CAP:raise 1
 if ply and KEY in REP:return 0
 if dep<=0:return QS(al,be,ply)
 w=W;chk=AT(KS[not w],not w)
 if chk:dep+=1
 e=TT.get(KEY)
 tm=0
 if e:
  tm=e[3]
  if e[0]>=dep:
   sc=e[2]
   if sc>M-1000:sc-=ply
   elif sc<-M+1000:sc+=ply
   if e[1]==0:return sc
   if e[1]==1 and sc>=be:return sc
   if e[1]==2 and sc<=al:return sc
 REP.add(KEY)
 if nm and dep>=3 and not chk and PH>0:
  se=SE()
  if se>=be:
   ok=KEY;oe=EP
   if EP>=0:KEY^=ZE[EP&7]
   EP=-1;W=not W;KEY^=ZS
   sc=-S(dep-3,-be,-be+1,ply+1,0)
   W=not W;KEY=ok;EP=oe
   if sc>=be:
    REP.discard(KEY)
    return be
 ms=G()
 a0=al;bs=-M;bm=0
 kl=KL[ply if ply<128 else 127]
 def keyf(m):
  return(1<<40 if m==tm else 0)+(1<<30 if m==kl[0] else 1<<29 if m==kl[1] else 0)+SC(m)*64
 ms.sort(key=keyf,reverse=True)
 pv=True;mi=0
 for m in ms:
  q=SC(m)==0
  un=MK(m)
  if AT(KS[not w],not w):UM(un);continue
  mi+=1
  if pv:sc=-S(dep-1,-be,-al,ply+1)
  else:
   if mi>4 and dep>=3 and not chk and q:
    sc=-S(dep-2,-al-1,-al,ply+1)
    if sc>al:sc=-S(dep-1,-al-1,-al,ply+1)
   else:sc=-S(dep-1,-al-1,-al,ply+1)
   if al<sc<be:sc=-S(dep-1,-be,-sc,ply+1)
  UM(un);pv=False
  if sc>bs:bs,bm=sc,m
  if sc>al:al=sc
  if al>=be:
   if not SC(m) and m!=kl[0]:kl[1]=kl[0];kl[0]=m
   break
 REP.discard(KEY)
 if not bm:return-M+ply if chk else 0
 sv=bs
 if sv>M-1000:sv+=ply
 elif sv<-M+1000:sv-=ply
 TT[KEY]=(dep,0 if a0<bs<be else 1 if bs>=be else 2,sv,bm)
 return bs
def U2(m):
 f,t,pr=m&127,m>>7&127,m>>14
 return chr(97+(f&7))+str(1+f//16)+chr(97+(t&7))+str(1+t//16)+("  nbrq"[pr]if pr else"")
def PA(fen):
 global B,W,CS,EP,KEY,EV,PH
 a=fen.split();B=[0]*128;r,f=7,0
 for c in a[0]:
  if c=="/":r-=1;f=0
  elif c.isdigit():f+=int(c)
  else:
   p="PNBRQK".index(c.upper())+1+8*c.islower();B[r*16+f]=p;f+=1
 W=a[1]=="w";CS=sum(1<<"KQkq".index(c)for c in a[2]if c>"-")
 EP=-1 if a[3]=="-"else(ord(a[3][1])-49)*16+ord(a[3][0])-97
 KEY=0;EV=0;PH=0
 for i in Q6:
  p=B[i]
  if p:
   KEY^=Z[p][i];EV+=TP[p][i];PH+=PHW[p&7]
   if p&7==6:KS[p>8]=i
 KEY^=ZC[CS]
 if not W:KEY^=ZS
 if EP>=0:KEY^=ZE[EP&7]
def C(fen,lm,hist=()):
 global n
 PA(fen)
 REP.clear();REP.update(hist)
 ms=[m for m in LG()if U2(m)in lm]
 if len(ms)==1:return U2(ms[0])
 ms.sort(key=lambda m:-SC(m))
 n=0;best=ms[0]
 try:
  for dep in range(1,64):
   al=-M;bm=best;pv=True
   for m in ms:
    un=MK(m)
    if pv:sc=-S(dep-1,-M,M,1)
    else:
     sc=-S(dep-1,-al-1,-al,1)
     if sc>al:sc=-S(dep-1,-M,-al,1)
    UM(un);pv=False
    if sc>al:al,bm=sc,m
   best=bm
   ms.remove(best);ms.insert(0,best)
   if n>=CAP:break
 except Exception:pass
 return U2(best)
def HI(g):
 PA(g["start_fen"]);ks=[]
 for u in g["moves"]:
  for m in LG():
   if U2(m)==u:MK(m);break
  ks.append(KEY)
 return ks
while U:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  h=HI(g)
  g=P("/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"],h)})
