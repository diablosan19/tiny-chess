import json,urllib.request as R
U=R.os.getenv("MAKEFUN_ENV_URL")
V=dict(zip("PNBRQK",(100,300,320,500,950,0)))
BD=(-17,-15,15,17);RD=(-16,-1,1,16);KN=(-33,-31,-18,-14,14,18,31,33);K8=BD+RD
CM={0:-3,7:-2,112:-9,119:-5,4:-4,116:-13};PR="qrbn";CAP=40000
W="kkkklmmiljmnkkmollnpmmoquuuukkkkkklmjkkkjkkkjkkkjkkkjkkklmmmkklm"
T={p:[V[p]+(ord(W[j*32+(i>>3)*4+min(i&7,7-i&7)])-107)*5 for i in range(64)]for p,j in zip("PNBRQK",(0,0,0,1,1,1))}
Q6=[i for i in range(128)if not i&136]
TT={};KL=[0]*99;n=0
def post(p,b):
 return json.load(R.urlopen(R.Request(U+p,json.dumps(b).encode(),{"content-type":"application/json"})))
def K(s):return s<128 and not s&136
def A(b,s,w):
 for ds,ps in((BD[:2]if w else BD[2:],"P"),(KN,"N"),(K8,"K"),(BD,"BQ"),(RD,"RQ")):
  for d in ds:
   t=s+d
   if len(ps)>1:
    while K(t)and b[t]==".":t+=d
   if K(t)and b[t]in(ps if w else ps.lower()):return 1
def Q(st,w):return A(st[0],st[0].index("kK"[w]),not w)
def G(st):
 b=st[0];w=st[1]=="w";ms=[];ap=ms.append
 for s in Q6:
  p=b[s]
  if p=="."or p.isupper()!=w:continue
  u=p.upper()
  if u=="P":
   d=(-16,16)[w];r=s>>4;pr=(1,6)[w]
   for dd in(d-1,d,d+1):
    t=s+dd
    if not K(t):continue
    q=b[t]
    if dd==d:
     if q!=".":continue
     if r==7-pr and b[s+2*d]==".":ap(s|(s+2*d)<<7)
    elif q==".":
     if t!=st[3]:continue
    elif q.isupper()==w:continue
    if r==pr:
     for x in(1,2,3,4):ap(s|t<<7|x<<14)
    else:ap(s|t<<7)
  else:
   ds=(KN,BD,K8,RD,K8)["NBQRK".index(u)]
   for d in ds:
    t=s+d
    while K(t)and b[t]==".":ap(s|t<<7);t+=d if u in"BQR"else 999
    if K(t)and b[t]!="."and b[t].isupper()!=w:ap(s|t<<7)
   if u=="K":
    for sq,bit,g in((4,1,1),(4,2,-1),(116,4,1),(116,8,-1)):
     if s==sq and st[2]&bit and all(b[s+g*i]=="."for i in range(1,3+(g<0)))and not any(A(b,s+g*i,s>60)for i in(0,1,2)):ap(s|(s+2*g)<<7)
 return ms
def M(st,m):
 b=st[0];w=st[1]=="w";f,t,pr=m&127,m>>7&127,m>>14;p=b[f];pu=p.upper();un=(b[:],st[1],st[2],st[3])
 if pu=="P"and t==st[3]and b[t]==".":b[(f&112)|(t&7)]="."
 b[t],b[f]=p,"."
 if pr:b[t]=PR[pr-1]if not w else"QRBN"[pr-1]
 if pu=="K"and abs(t-f)==2:
  rf,rt=(f+3,f+1)if t>f else(f-4,f-1);b[rt]=b[rf];b[rf]="."
 st[2]&=CM.get(f,-1)&CM.get(t,-1)
 st[1]="wb"[w];st[3]=(f+t)//2 if pu=="P"and abs(t-f)==32 else-1
 return un
def X(st,un):st[0][:],st[1],st[2],st[3]=un
def L(st,c=False):
 w=st[1]=="w";out=[]
 for m in G(st):
  if c and not O(st,m):continue
  un=M(st,m)
  if not Q(st,w):out.append(m)
  X(st,un)
 return out
def O(st,m):
 b=st[0];cap=b[m>>7&127]
 return(V[cap.upper()]<<5)-V[b[m&127].upper()]if cap!="."else 2000 if m>>14 else 0
def S(st,dep,al,be):
 global n;n+=1;tm=bm=0
 if n>=CAP:raise 1
 if dep<=0:
  v=0
  for i in Q6:
   p=st[0][i]
   if p!=".":v+=T[p][(i>>4)*8+i&7]if p.isupper()else-T[p.upper()][(7-(i>>4))*8+i&7]
  if st[1]=="b":v=-v
  if v>=be:return be
  al=max(al,v)
  if dep<-4:return al
  ms=L(st,1)
 else:
  k="".join(st[0])+st[1];e=TT.get(k)
  if e:
   tm=e[2]
   if e[3]:return e[1]
  ms=L(st)
  if not ms:return-9999 if Q(st,st[1]=="w")else 0
  a0=al
 ms.sort(key=lambda m:-(O(st,m)+(m==tm)*1e5+(m==KL[dep])*999))
 for m in ms:
  un=M(st,m);sc=-S(st,dep-1,-be,-al);X(st,un)
  if sc>=be:
   if dep>0 and not O(st,m):KL[dep]=m
   return be
  if sc>al:al,bm=sc,m
 if dep>0:TT[k]=(dep,al,bm,a0<al<be)
 return al
def u(m):
 f,t,pr=m&127,m>>7&127,m>>14
 return"abcdefgh"[f&7]+str(1+f//16)+"abcdefgh"[t&7]+str(1+t//16)+(PR[pr-1]if pr else"")
def C(fen,lm):
 global n;TT.clear()
 a=fen.split();b=["."]*128;r,f=7,0
 for c in a[0]:
  if c=="/":r-=1;f=0
  elif c.isdigit():f+=int(c)
  else:b[r*16+f]=c;f+=1
 st=[b,a[1],sum(1<<"KQkq".index(c)for c in a[2]if c>"-"),(ord(a[3][-1])-49)*16+ord(a[3][0])-97]
 cand=[m for m in L(st)if u(m)in lm];cand.sort(key=lambda m:-O(st,m))
 n=0;pv=-10001;bm=cand[0]
 try:
  for dep in range(64):
   al=pv-1
   for m in cand:
    un=M(st,m);sc=-S(st,dep-1,-10001,-al);X(st,un)
    if sc>al:al,bm=sc,m
   pv=al
 except:pass
 return u(bm)
while U:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"])})
