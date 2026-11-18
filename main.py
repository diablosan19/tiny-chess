import json,urllib.request as R
U=R.os.getenv("MAKEFUN_ENV_URL")
V={"P":100,"N":300,"B":320,"R":500,"Q":950,"K":0}
BD=(-17,-15,15,17);RD=(-16,-1,1,16);KN=(-33,-31,-18,-14,14,18,31,33);K8=BD+RD
CM={0:-3,7:-2,112:-9,119:-5,4:-4,116:-13};PR="qrbn";MATE=10000;CAP=25000
W="kkkklmmiljmnkkmollnpmmoquuuukkkkkklmjkkkjkkkjkkkjkkkjkkklmmmkklm"
T={p:[(ord(W[j*32+r*4+min(f,7-f)])-107)*5 for r in range(8)for f in range(8)]for p,j in zip("PNBRQK",(0,0,0,1,1,1))}
def post(p,b):
 with R.urlopen(R.Request(U+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"}))as r:return json.load(r)
def K(s):return 0<=s<128 and not s&0x88
def A(b,s,w):
 for ds,ps,sl in(((-15,-17)if w else(15,17),"P",0),(KN,"N",0),(K8,"K",0),(BD,"BQ",1),(RD,"RQ",1)):
  for d in ds:
   t=s+d
   if sl:
    while K(t)and b[t]==".":t+=d
   if K(t)and b[t].isupper()==w and b[t].upper()in ps:return 1
 return 0
def G(st):
 b,turn,cast,ep=st;w=turn=="w";ms=[];ap=ms.append
 for s,p in enumerate(b):
  if s&0x88 or p=="."or p.isupper()!=w:continue
  u=p.upper()
  if u=="P":
   d=16 if w else-16;r=s>>4;pr=6 if w else 1
   for dd in(d-1,d,d+1):
    t=s+dd
    if not K(t):continue
    q=b[t]
    if dd==d:
     if q!=".":continue
     if r!=pr and r==7-pr and b[s+2*d]==".":ap(s|(s+2*d)<<7)
    elif q==".":
     if t!=ep:continue
    elif q.isupper()==w:continue
    if r==pr:
     for x in(1,2,3,4):ap(s|t<<7|x<<14)
    else:ap(s|t<<7)
  else:
   ds=(KN,BD,K8,RD,K8)["NBQRK".index(u)];sl=u in"BQR"
   for d in ds:
    t=s+d
    while K(t)and b[t]==".":ap(s|t<<7);t+=d if sl else 999
    if K(t)and b[t]!="."and b[t].isupper()!=w:ap(s|t<<7)
   if u=="K":
    for sq,bit,em,ck in((4,1,(5,6),(4,5,6)),(4,2,(3,2,1),(4,3,2)),(116,4,(117,118),(116,117,118)),(116,8,(115,114,113),(116,115,114))):
     if s==sq and cast&bit and all(b[x]=="."for x in em)and not any(A(b,x,sq==116)for x in ck):ap(s|ck[-1]<<7)
 return ms
def M(st,m):
 b=st[0];w=st[1]=="w";f,t,pr=m&127,m>>7&127,m>>14;p=b[f];pu=p.upper();undo=(b[:],st[1],st[2],st[3])
 if pu=="P"and t==st[3]and b[t]==".":b[(f&112)|(t&7)]="."
 b[t],b[f]=p,"."
 if pr:b[t]=PR[pr-1].upper()if w else PR[pr-1]
 if pu=="K"and(t-f)in(2,-2):
  rf,rt=(f+3,f+1)if t>f else(f-4,f-1);b[rt]=b[rf];b[rf]="."
 st[2]&=CM.get(f,-1)&CM.get(t,-1)
 st[1]="wb"[w];st[3]=(f+t)//2 if pu=="P"and abs(t-f)==32 else-1
 return undo
def X(st,undo):st[0][:],st[1],st[2],st[3]=undo
def L(st,c=False):
 w=st[1]=="w";out=[]
 for m in G(st):
  if c and not O(st,m):continue
  un=M(st,m)
  if not A(st[0],st[0].index("kK"[w]),not w):out.append(m)
  X(st,un)
 return out
n=0
def O(st,m):
 cap=st[0][m>>7&127]
 return V[cap.upper()]<<5|-V[st[0][m&127].upper()]if cap!="."else 2000 if m>>14 else 0
def S(st,dep,al,be):
 global n;n+=1
 if n>=CAP:raise Exception
 if dep<=0:
  b=st[0];v=0
  for i,p in enumerate(b):
   if p!="."and not i&0x88:
    u=p.upper();v+=V[u]+T[u][(i>>4)*8+i&7]if p.isupper()else-V[u]-T[u][(7-(i>>4))*8+i&7]
  if st[1]=="b":v=-v
  if v>=be:return be
  if v>al:al=v
  if dep<-4:return al
  ms=L(st,1)
 else:
  ms=L(st)
  if not ms:return-MATE if A(st[0],st[0].index("kK"[st[1]=="w"]),st[1]!="w")else 0
 ms.sort(key=lambda m:-O(st,m))
 for m in ms:
  un=M(st,m);sc=-S(st,dep-1,-be,-al);X(st,un)
  if sc>=be:return be
  al=max(al,sc)
 return al
def u(m):
 f,t,pr=m&127,m>>7&127,m>>14
 return chr(97+(f&7))+chr(49+f//16)+chr(97+(t&7))+chr(49+t//16)+(PR[pr-1]if pr else"")
def C(fen,lm):
 global n
 a=fen.split();b=["."]*128;r,f=7,0
 for c in a[0]:
  if c=="/":r-=1;f=0
  elif c.isdigit():f+=int(c)
  else:b[r*16+f]=c;f+=1
 st=[b,a[1],sum(1<<i for i in range(4)if"KQkq"[i]in a[2]),(ord(a[3][-1])-49)*16+ord(a[3][0])-97]
 cand=[m for m in L(st)if u(m)in lm];cand.sort(key=lambda m:-O(st,m))
 if not cand:return lm[0]
 n=0;pv=-MATE-1;bm=cand[0]
 try:
  for dep in range(1,10):
   al=pv-1
   for m in cand:
    un=M(st,m);sc=-S(st,dep-1,-MATE-1,-al);X(st,un)
    if sc>al:al,bm=sc,m
   pv=al
 except:pass
 return u(bm)
if U:
 while 1:
  g=post("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"])})
