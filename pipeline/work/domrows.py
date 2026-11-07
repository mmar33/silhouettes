import json,collections,pickle
d=json.load(open('dom_geo.json'));T=d['T'];P=d['P']
def cy(b): return (b[1]+b[3])/2
def col(x0,lo,hi): return lo<=x0<hi
hdr={'Nom français (FCI)','Nom anglais (FCI)','N° FCI','Nom français','English name'}
dogs_fr=[t for t in T if col(t['bb'][0],-55,-40) and t['t'] not in hdr]
dogs_en=[t for t in T if col(t['bb'][0],25,40) and t['t'] not in hdr]
dogs_n=[t for t in T if 100<t['bb'][0]<150 and t['t'].isdigit()]
cats_fr=[t for t in T if col(t['bb'][0],150,170) and t['t'] not in hdr]
cats_en=[t for t in T if col(t['bb'][0],200,215) and t['t'] not in hdr]
print(len(dogs_fr),len(dogs_en),len(dogs_n),len(cats_fr),len(cats_en))
def near(lst,y): return min(lst,key=lambda t:abs(cy(t['bb'])-y))
rows=[]
for t in dogs_fr:
    y=cy(t['bb']);rows.append(dict(kind='dog',fr=t['t'],en=near(dogs_en,y)['t'],fci=near(dogs_n,y)['t'],y=y))
for t in cats_fr:
    y=cy(t['bb']);rows.append(dict(kind='cat',fr=t['t'],en=near(cats_en,y)['t'],fci='',y=y))
icons=[i for i,p in enumerate(P) if p['fill']!='none' and p['disp']!='none' and ((-62<p['bb'][0]<-54.5 and p['bb'][2]<-53.5) or (148<p['bb'][0]<158.4 and p['bb'][2]<158.6))]
print('icons',len(icons),collections.Counter(P[i]['fill'] for i in icons))
g=collections.defaultdict(list);far=[]
for i in icons:
    p=P[i];kind='dog' if p['bb'][0]<0 else 'cat';y=cy(p['bb'])
    cand=[k for k,r in enumerate(rows) if r['kind']==kind]
    k=min(cand,key=lambda k:abs(rows[k]['y']-y))
    if abs(rows[k]['y']-y)<2.5: g[k].append(i)
    else: far.append((P[i]['id'],round(y,1)))
nomatch=[r['fr'] for k,r in enumerate(rows) if k not in g]
print('rows',len(rows),'with icon',len(g),'no icon',nomatch,'far',far[:10])
print('multi',[(rows[k]['fr'],len(v)) for k,v in g.items() if len(v)>1])
pickle.dump((rows,dict(g)),open('dom_rows.pkl','wb'))
