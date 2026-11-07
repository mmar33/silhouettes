import json,math,re,sys
import os;HERE=os.path.dirname(os.path.abspath(__file__));os.chdir(HERE);sys.path.insert(0,os.path.join(HERE,'..','work'))
from PIL import ImageFont
t=json.load(open('tree.json'));A=json.load(open('arts.json'));arts,FAMOF,COL=A['arts'],A['fam'],A['COL']
names=json.load(open('artnames.json'));BB=dict(zip(names,json.load(open('bboxes.json'))))
cur=json.load(open('cur_map.json'));wild=json.load(open('../work/wild_index.json'))['wild']
HARMREV={'Lutra cinerea':'Aonyx cinereus','Lutra capensis':'Aonyx capensis','Neogale vison':'Neovison vison','Neogale frenata':'Mustela frenata','Neogale felipei':'Mustela felipei','Neogale africana':'Mustela africana'}
FILE={}
for v in cur.values(): FILE[v]=v.replace(' ','_')
for k,v in HARMREV.items(): FILE[k]=v.replace(' ','_')
for o in wild:
    FILE.setdefault(o['n'],o['f'][:-4])
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf',100)
def tw(s,fs): return font.getlength(s)/100*fs*0.93
S=3700;C=S/2;R0=820;ROOT=t['a'];K=(R0-6)/ROOT
def R(a): return R0-K*a
GAP=11.0  # degrees left open at top
leaves=[]
def walk(n,d=0):
    if not n['c']: leaves.append(n);return
    for c in n['c']: walk(c,d+1)
walk(t)
NL=len(leaves);step=(360-2*GAP)/(NL-1)
for i,l in enumerate(leaves): l['ang']=GAP+i*step; l['i']=i
def setang(n):
    if not n['c']: return n['ang'],n['ang'],{n['f']}
    lo,hi,fs=999,-999,set()
    for c in n['c']:
        a,b,f=setang(c);lo=min(lo,a);hi=max(hi,b);fs|=f
    n['lo'],n['hi'],n['fams']=lo,hi,fs
    n['ang']=(min(c['ang'] for c in n['c'])+max(c['ang'] for c in n['c']))/2
    return lo,hi,fs
setang(t)

# ---------- degrade continu (OKLCH) selon la position sur le cercle ----------
def _oklch(L,C,h):
    import math
    a=C*math.cos(math.radians(h));b=C*math.sin(math.radians(h))
    l_=L+0.3963377774*a+0.2158037573*b;m_=L-0.1055613458*a-0.0638541728*b;s_=L-0.0894841775*a-1.2914855480*b
    l,m,s=l_**3,m_**3,s_**3
    r=4.0767416621*l-3.3077115913*m+0.2309699292*s;g=-1.2684380046*l+2.6097574011*m-0.3413193965*s;bb=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    def gam(x):
        x=min(max(x,0),1);return 12.92*x if x<=0.0031308 else 1.055*x**(1/2.4)-0.055
    return '#%02x%02x%02x'%tuple(round(gam(v)*255) for v in (r,g,bb))
H0,H1=8,330
def gcol(ang,L=0.70,C=0.135):
    import math
    u=(ang-GAP)/(360-2*GAP);u=min(max(u,0),1);h=H0+(H1-H0)*u
    bump=math.exp(-((h-100)/38)**2)
    return _oklch(L+0.09*bump,C+0.02*bump,h)
def P(r,deg):
    th=math.radians(deg-90);return C+r*math.cos(th),C+r*math.sin(th)
def f(x): return f'{x:.1f}'
out=[]
# background + time scale
out.append(f'<g id="fond"><rect x="0" y="0" width="{S}" height="{S}" fill="#ffffff"/></g>')
ts=['<g id="echelle_temps">']
for a in range(0,int(ROOT)+1,10):
    r=R(a)
    if r<80: continue
    x1,y1=P(r,GAP-3);x2,y2=P(r,360-GAP+3)
    ts.append(f'<path d="M{f(x1)},{f(y1)} A{f(r)},{f(r)} 0 1 1 {f(x2)},{f(y2)}" fill="none" stroke="#d9d9d9" stroke-width="1.4" stroke-dasharray="6 7"/>')
    ts.append(f'<text x="{f(C)}" y="{f(C-r+5)}" style="font-family:Arial,Helvetica,sans-serif;font-size:15px;fill:#888;text-anchor:middle">{a}</text>')
ts.append(f'<text x="{f(C)}" y="{f(C-R0-26)}" style="font-family:Arial,Helvetica,sans-serif;font-size:15px;fill:#888;text-anchor:middle">Ma</text></g>')
out+=ts
# families ring
RF1,RF2=1700,1711
fam_runs=[]
for l in leaves:
    if fam_runs and fam_runs[-1][0]==l['f']: fam_runs[-1][2]=l['ang']
    else: fam_runs.append([l['f'],l['ang'],l['ang']])
FAMORD=[]
for fm,a,b in fam_runs:
    if fm not in FAMORD: FAMORD.append(fm)
def fcol(fm,L=0.70,C=0.135):
    i=FAMORD.index(fm);u=i/(len(FAMORD)-1)
    dL=(-0.07 if i%2 else 0.05)*(L/0.70)
    return gcol(GAP+u*(360-2*GAP),L+dL,C+0.015)
fg=['<g id="familles">']
for fm,a,b in fam_runs:
    a0=a-step*0.42;b0=b+step*0.42
    x1,y1=P(RF2,a0);x2,y2=P(RF2,b0);x3,y3=P(RF1,b0);x4,y4=P(RF1,a0);large=1 if b0-a0>180 else 0
    fg.append(f'<path d="M{f(x1)},{f(y1)} A{RF2},{RF2} 0 {large} 1 {f(x2)},{f(y2)} L{f(x3)},{f(y3)} A{RF1},{RF1} 0 {large} 0 {f(x4)},{f(y4)} Z" fill="{fcol(fm)}"/>')
    mid=(a0+b0)/2;span=b0-a0;col=fcol(fm,0.58,0.13)
    lab=fm.replace(' (hors Carnivora)','*')
    fs=24 if span>8 else (18 if span>4 else 14)
    if span<1.6: continue
    x,y=P(1745,mid)
    rot=mid-180 if 90<mid<270 else mid
    fg.append(f'<text x="0" y="0" transform="translate({f(x)},{f(y)}) rotate({rot:.2f})" style="font-family:Arial,Helvetica,sans-serif;font-weight:bold;font-size:{fs}px;fill:{col};text-anchor:middle;dominant-baseline:central">{lab}</text>')
fg.append('</g>');out+=fg
# branches
br=['<g id="arbre">']
def bcol(n):
    fs=n['fams'] if n['c'] else {n['f']}
    return fcol(next(iter(fs)),0.66,0.13) if len(fs)==1 else '#3a3a3a'
def draw(n):
    rn=R(n['a'])
    if n['c']:
        lo=min(c['ang'] for c in n['c']);hi=max(c['ang'] for c in n['c'])
        x1,y1=P(rn,lo);x2,y2=P(rn,hi);large=1 if hi-lo>180 else 0
        br.append(f'<path d="M{f(x1)},{f(y1)} A{f(rn)},{f(rn)} 0 {large} 1 {f(x2)},{f(y2)}" fill="none" stroke="{bcol(n)}" stroke-width="2.2" stroke-linecap="round"/>')
        for c in n['c']:
            rc=R(c['a']);x1,y1=P(rn,c['ang']);x2,y2=P(rc,c['ang'])
            br.append(f'<path d="M{f(x1)},{f(y1)} L{f(x2)},{f(y2)}" fill="none" stroke="{bcol(c)}" stroke-width="2.2" stroke-linecap="round"/>')
            draw(c)
draw(t)
# root stem
x1,y1=P(0,t['ang']);x2,y2=P(R(t['a']),t['ang'])
br.append('</g>');out+=br
# fossil extensions + labels + silhouettes
LAB0=R0+14;FS=12.5
ext=['<g id="extensions">'];nm=['<g id="noms">'];sl=['<g id="silhouettes">']
NR=5;ROWS=[1150+i*125 for i in range(NR)]

WHITE={'#fff','#ffffff','white','none'}
def recol(art,c):
    art=re.sub(r'(fill|stroke)(:|=")(#[0-9a-fA-F]{3,6}|white|black|none)',lambda m:m.group(0) if m.group(3).lower() in WHITE else m.group(1)+m.group(2)+c,art)
    art=re.sub(r'fill-opacity:0\.\d+','fill-opacity:1',art)
    return art
def sid(name): return re.sub(r'[^A-Za-z0-9]+','_',name).strip('_')
pl=[]
for l in leaves:
    a=l['ang'];name=l['n'];fos=l['x'];disp=('† ' if fos else '')+name
    if l['a']>0.02:
        x1,y1=P(R(l['a']),a);x2,y2=P(LAB0-4,a)
        ext.append(f'<path d="M{f(x1)},{f(y1)} L{f(x2)},{f(y2)}" stroke="#c9c9c9" stroke-width="1" stroke-dasharray="2 3" fill="none"/>')
    x,y=P(LAB0,a)
    if a<=180: rot=a-90;anc='start'
    else: rot=a+90;anc='end'
    style=f'font-family:Arial,Helvetica,sans-serif;font-style:italic;font-size:{FS}px;fill:{"#555" if fos else "#222"};dominant-baseline:central;text-anchor:{anc}'
    nm.append(f'<text x="0" y="0" transform="translate({f(x)},{f(y)}) rotate({rot:.2f})" style="{style}" id="n_{sid(name)}">{disp}</text>')
    lend=LAB0+tw(disp,FS)+6
    rr=ROWS[l['i']%NR]
    bx,by,bw,bh=BB[name]
    # taille homogene : meme boite pour toutes (largeur max, hauteur max), proportionnelle au rayon
    W=84;H=54
    sc=min(W/bw,H/bh)
    cx,cy=P(rr,a)
    pl.append(dict(l=l,name=name,disp=disp,a=a,rr=rr,lend=lend,bx=bx,by=by,bw=bw,bh=bh,sc=sc,cx=cx,cy=cy))
# resolution des chevauchements : on reduit les paires qui se touchent
M=5
def box(p): hw=p['bw']*p['sc']/2+M/2;hh=p['bh']*p['sc']/2+M/2;return p['cx']-hw,p['cy']-hh,p['cx']+hw,p['cy']+hh
for it in range(200):
    hit=0
    for i in range(len(pl)):
        for j in range(i+1,min(i+12,len(pl))):
            a1=box(pl[i]);b1=box(pl[j])
            if a1[0]<b1[2] and b1[0]<a1[2] and a1[1]<b1[3] and b1[1]<a1[3]:
                pl[i]['sc']*=0.97;pl[j]['sc']*=0.97;hit+=1
    if not hit: break
print('iters',it,'hits',hit)
for p in pl:
    a=p['a'];sc=p['sc'];rr=p['rr']
    th=math.radians(a-90);ext_r=abs(math.cos(th))*p['bw']*sc/2+abs(math.sin(th))*p['bh']*sc/2
    lx1,ly1=P(p['lend'],a);lx2,ly2=P(rr-ext_r-4,a)
    if rr-ext_r-4>p['lend']+4: nm.append(f'<path d="M{f(lx1)},{f(ly1)} L{f(lx2)},{f(ly2)}" stroke="#d0d0d0" fill="none" stroke-width="0.9"/>')
    name=p['name']
    sl.append(f'<g id="sil_{sid(name)}" transform="translate({p["cx"]:.2f},{p["cy"]:.2f}) scale({sc:.4f}) translate({-(p["bx"]+p["bw"]/2):.2f},{-(p["by"]+p["bh"]/2):.2f})" data-cx="{p["cx"]:.2f}" data-cy="{p["cy"]:.2f}" data-name="{p["disp"]}" data-file="{FILE[name]}" class="sil"><g class="art">{recol(arts[name],fcol(p['l']['f']))}</g></g>')
import statistics
ss=[p['sc']*max(p['bw'],p['bh'])/84 for p in pl];print('rel size min/med',round(min(ss),2),round(statistics.median(ss),2))
ext.append('</g>');nm.append('</g>');sl.append('</g>')
out+=ext+nm+sl
nfos=sum(1 for l in leaves if l['x']);nact=NL-nfos
title=f'<g id="titre"><text x="70" y="120" style="font-family:Arial,Helvetica,sans-serif;font-weight:bold;font-size:76px;fill:#333;letter-spacing:8px">CARNIVORA</text><text x="74" y="172" style="font-family:Arial,Helvetica,sans-serif;font-size:30px;fill:#666">{nact} espèces et sous-espèces actuelles · {nfos} taxons éteints ou fossiles (†)</text>'\
 f'<text x="60" y="{S-80}" style="font-family:Arial,Helvetica,sans-serif;font-size:18px;fill:#999">Phylogénie datée des espèces actuelles : Upham et al. 2019 (PLoS Biol), arbre MCC node-dated</text>'\
 f'<text x="60" y="{S-54}" style="font-family:Arial,Helvetica,sans-serif;font-size:18px;fill:#999">Fossiles et espèces récemment reconnues ajoutés à la main, positions et âges approximatifs (Paleobiology Database) · * hors Carnivora</text>'\
 f'<text x="60" y="{S-28}" style="font-family:Arial,Helvetica,sans-serif;font-size:18px;fill:#999">Silhouettes : Margot Michaud (CC0)</text></g>'
out.append(title)
svg=f'<svg id="tree" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {S} {S}">'+''.join(out)+'</svg>'
cur_html=open('template.html').read()
i=cur_html.find('<svg id="tree"');j=cur_html.find('</svg>',i)+6
html=cur_html[:i]+svg+cur_html[j:]
html=html.replace('<title>Phylogénie des Carnivora</title>','<title>Phylogénie des Carnivora</title>')
# use data-file for downloads
html=html.replace("return {txt:txt, file:name.replace(/\\s+/g,'_')+'.svg', name:name};","return {txt:txt, file:(g.dataset.file||name.replace(/\\s+/g,'_'))+'.svg', name:name};")
html=html.replace("d.direct=BASE+(RELAIS?'get.html?f='+encodeURIComponent(d.file):encodeURIComponent(d.file));","d.direct=BASE+(RELAIS?'get.html?f='+encodeURIComponent(d.file):encodeURI(d.file));")
open('carnivora_arbre.html','w').write(html)
print(NL,nact,nfos,len(html))
