import pickle,json,re,os,collections
from svgelements import SVG,Path,Rect
d=json.load(open('dom_geo.json'));P=d['P']
rows,g=pickle.load(open('dom_rows.pkl','rb'))
need={P[i]['id'] for v in g.values() for i in v}
svg=SVG.parse('domestic.svg');D={}
for e in svg.elements():
    if isinstance(e,Path) and not isinstance(e,Rect) and e.id in need: D[e.id]=e
print(len(need),len(D))
import os;OUT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','domestic'))
def rnd(s): return re.sub(r'(\d+\.\d\d)\d+',r'\1',s)
from xml.sax.saxutils import escape as esc
def title(s):
    s=s.strip()
    if s.isupper(): s=s.title().replace("'S","'s")
    return re.sub(r'\s+',' ',s)
used=collections.Counter();out=[]
for k,ids in sorted(g.items(),key=lambda kv:rows[kv[0]]['y']):
    r=rows[k];es=[D[P[i]['id']] for i in ids if P[i]['id'] in D]
    bbs=[e.bbox() for e in es];x0=min(b[0] for b in bbs);y0=min(b[1] for b in bbs);x1=max(b[2] for b in bbs);y1=max(b[3] for b in bbs)
    p=max(x1-x0,y1-y0)*0.03;x0-=p;y0-=p;x1+=p;y1+=p;w=x1-x0;h=y1-y0;sc=800/max(w,h)
    en=title(r['en']);fr=title(r['fr'])
    base=re.sub(r'[^A-Za-z0-9]+','_',en.encode('ascii','ignore').decode()).strip('_')
    sub='dogs' if r['kind']=='dog' else 'cats'
    used[sub+base]+=1;fn=f"{sub}/{base}{'' if used[sub+base]==1 else '_'+str(used[sub+base])}.svg"
    body='\n'.join(f'<path fill="#000000" d="{rnd(e.d())}"/>' for e in es)
    os.makedirs(f'{OUT}/{sub}',exist_ok=True)
    open(f'{OUT}/{fn}','w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" width="{round(w*sc)}" height="{round(h*sc)}">\n<title>{esc(en)} — silhouette © Margot Michaud (CC0)</title>\n{body}\n</svg>\n')
    out.append(dict(f='domestic/'+fn,k=r['kind'],fr=fr,en=en,fci=r['fci']))
json.dump(out,open('dom_index.json','w'),ensure_ascii=False)
print(len(out),collections.Counter(o['k'] for o in out))
