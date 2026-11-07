import re,pickle,math,sys
from lxml import etree
from svgelements import SVG,Path,Rect,Matrix
from PIL import ImageFont
NS='{http://www.w3.org/2000/svg}'
K=96/25.4
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',100)
def tw(t,fs): return font.getlength(t)/100*fs
t=etree.parse('master.svg');labels=[]
def walk(el,M):
    tr=el.get('transform');m=Matrix(M)
    if tr: m=Matrix(tr)*m
    if el.tag==NS+'flowRoot':
        txt=' '.join(''.join(p.itertext()).strip() for p in el.iter(NS+'flowPara')).strip()
        r=el.find('.//'+NS+'rect')
        if r is None or not txt: return
        x,y,w,h=[float(r.get(k)) for k in('x','y','width','height')]
        mm=Matrix(m); rt=r.get('transform')
        if rt: mm=Matrix(rt)*m
        sc=math.hypot(mm.a,mm.b)
        fs=float(re.search(r'font-size:([\d.]+)',el.get('style')).group(1))
        P=lambda a,b: mm.point_in_matrix_space((a,b))
        right=P(x+w,y); top=P(x,y)
        wid=tw(txt,fs)*sc; hgt=fs*1.25*sc
        labels.append(dict(name=txt,x0=(right.x-wid)*K,x1=right.x*K,y0=top.y*K,y1=(top.y+hgt)*K))
        return
    if el.tag==NS+'text': return
    for c in el: walk(c,m)
walk(t.getroot(),Matrix())
svg=SVG.parse('master.svg')
paths=[]
for e in svg.elements():
    if isinstance(e,Path) and not isinstance(e,Rect) and e.values.get('d'):
        try: bb=e.bbox()
        except: continue
        if not bb or (bb[2]-bb[0])<1: continue
        fill=str(e.fill)
        paths.append(dict(id=e.id,bb=bb,fill=fill,d=e.d()))
print(len(labels),len(paths))
pickle.dump((labels,paths),open('master_geo.pkl','wb'))
