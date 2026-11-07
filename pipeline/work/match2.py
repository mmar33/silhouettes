import pickle,math,collections
labels,paths=pickle.load(open('master_geo.pkl','rb'))
def area(p): x0,y0,x1,y1=p['bb'];return (x1-x0)*(y1-y0)
def score(p,l):
    x0,y0,x1,y1=p['bb'];cx=(x0+x1)/2;w=x1-x0;h=y1-y0
    lx=(l['x0']+l['x1'])/2;dy=l['y0']-y1
    if dy<-0.35*h or dy>max(2.0*h,300): return None
    if lx<x0-0.6*w or lx>x1+0.6*w: return None
    return math.hypot(lx-cx,max(dy,0))+(abs(dy)*4 if dy<0 else 0)
cand=[]
for i,p in enumerate(paths):
    if p['fill']=='#ffffff' or p['fill']=='none': continue
    for j,l in enumerate(labels):
        s=score(p,l)
        if s is not None: cand.append((s/ (area(p)**0.15),i,j))
cand.sort()
main={};used=set()
for s,i,j in cand:
    if j in main or i in used: continue
    main[j]=i;used.add(i)
groups={j:[i] for j,i in main.items()}
# attach remaining paths to main paths whose bbox contains/overlaps them
def ov(a,b):
    return not(a[2]<b[0] or b[2]<a[0] or a[3]<b[1] or b[3]<a[1])
mainbb={j:paths[i]['bb'] for j,i in main.items()}
orph=[]
for i,p in enumerate(paths):
    if i in used: continue
    hits=[j for j,bb in mainbb.items() if ov(p['bb'],bb)]
    if len(hits)==1: groups[hits[0]].append(i)
    elif len(hits)>1:
        # choose main with max overlap area
        def oa(bb):
            a=p['bb'];return max(0,min(a[2],bb[2])-max(a[0],bb[0]))*max(0,min(a[3],bb[3])-max(a[1],bb[1]))
        groups[max(hits,key=lambda j:oa(mainbb[j]))].append(i)
    else: orph.append(i)
print('labels',len(labels),'matched',len(main),'orphans',len(orph))
print('unmatched labels',[labels[j]['name'] for j in range(len(labels)) if j not in main])
print('orphans',[(paths[i]['id'],paths[i]['fill'],[round(v) for v in paths[i]['bb']]) for i in orph][:30])
pickle.dump(groups,open('groups.pkl','wb'))
