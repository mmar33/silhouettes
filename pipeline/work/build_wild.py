import pickle,re,os,json,collections
from fam import FAM,ORDER
labels,paths=pickle.load(open('master_geo.pkl','rb'));groups=pickle.load(open('groups.pkl','rb'));sel=pickle.load(open('sel.pkl','rb'))
idx={p['id']:i for i,p in enumerate(paths)}
groups[sel[52][0]]=[idx['path420']]   # Martes caurina
drop={sel[53][0]}                      # duplicate transistoria label
import os;OUT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
def rnd(d): return re.sub(r'(\d+\.\d)\d+',r'\1',d)
from xml.sax.saxutils import escape as esc
def svgfile(ids,title):
    bbs=[paths[i]['bb'] for i in ids];x0=min(b[0] for b in bbs);y0=min(b[1] for b in bbs);x1=max(b[2] for b in bbs);y1=max(b[3] for b in bbs)
    p=max(x1-x0,y1-y0)*0.03;x0-=p;y0-=p;x1+=p;y1+=p
    w=x1-x0;h=y1-y0;sc=800/max(w,h)
    ids=sorted(ids,key=lambda i:1 if paths[i]['fill']=='#ffffff' else 0)
    body='\n'.join(f'<path fill="{"#ffffff" if paths[i]["fill"]=="#ffffff" else "#000000"}" d="{rnd(paths[i]["d"])}"/>' for i in ids)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" width="{round(w*sc)}" height="{round(h*sc)}">\n'
            f'<title>{esc(title)} — silhouette © Margot Michaud (CC0)</title>\n{body}\n</svg>\n')
items=[];used=collections.Counter();dom=[]
for k,(j,kind,name) in enumerate(sel):
    if j in drop or not groups.get(j): 
        if j not in drop: print('skip no path',name)
        continue
    ids=groups[j]
    base=re.sub(r'[^A-Za-z0-9]+','_',name.replace('×','x')).strip('_')
    used[base]+=1;fn=base+('' if used[base]==1 else f'_{used[base]}')+'.svg'
    if kind=='domestic':
        fn='domestic/other/'+fn;os.makedirs(OUT+'/domestic/other',exist_ok=True)
        open(f'{OUT}/{fn}','w').write(svgfile(ids,name));dom.append(dict(f=fn,fr={'Felis catus':'Chat domestique','Mustela putorius furo':'Furet','Liger (Panthera leo × P. tigris)':'Ligre'}[name],en={'Felis catus':'Domestic cat','Mustela putorius furo':'Ferret','Liger (Panthera leo × P. tigris)':'Liger'}[name],sci=name));continue
    open(f'{OUT}/{fn}','w').write(svgfile(ids,('† ' if kind in('fossil','extinct') else '')+name))
    items.append(dict(f=fn,n=name,x=kind in('fossil','extinct'),fam=FAM[name.split()[0]]))
items.sort(key=lambda d:(ORDER.index(d['fam']),d['n']))
json.dump(dict(wild=items,domother=dom),open('wild_index.json','w'),ensure_ascii=False)
print(len(items),collections.Counter(d['x'] for d in items),len(dom))
