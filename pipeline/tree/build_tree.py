import re,json,dendropy,sys
import os;HERE=os.path.dirname(os.path.abspath(__file__));os.chdir(HERE);sys.path.insert(0,'.')
from ages import AGE
sys.path.insert(0,'../work')
from fam import FAM
class N:
    def __init__(s,name=None,age=0.0,ch=None,fam=None,ext=False):
        s.name=name;s.age=age;s.ch=ch or [];s.parent=None;s.fam=fam;s.ext=ext
        for c in s.ch: c.parent=s
    def leaves(s): return [s] if not s.ch else [l for c in s.ch for l in c.leaves()]
# ---------- Upham ----------
t=dendropy.Tree.get(path='carnivora_upham.nwk',schema='newick',preserve_underscores=True)
t.calc_node_ages(is_force_max_age=True)
cur=json.load(open('cur_map.json'))   # upham name -> display
EXTRA={'Bassaricyon gabbii':'Bassaricyon gabbii','Bassaricyon medius':'Bassaricyon medius','Bdeogale omnivora':'Bdeogale omnivora',
'Melogale cucphuongensis':'Melogale cucphuongensis','Pusa sibirica':'Pusa sibirica','Vulpes rueppellii':'Vulpes rueppellii',
'Aonyx congicus':'Lutra congica','Canis anthus':'Canis lupaster','Dusicyon australis':'Dusicyon australis','Dusicyon avus':'Dusicyon avus',
'Neomonachus tropicalis':'Neomonachus tropicalis','Neovison macrodon':'Neogale macrodon','Zalophus japonicus':'Zalophus japonicus','Cryptoprocta spelea':'Cryptoprocta spelea'}
HARM={'Aonyx cinereus':'Lutra cinerea','Aonyx capensis':'Lutra capensis','Neovison vison':'Neogale vison','Mustela frenata':'Neogale frenata',
'Mustela felipei':'Neogale felipei','Mustela africana':'Neogale africana'}
keepmap={}
for k,v in cur.items(): keepmap[k]=HARM.get(v,v)
keepmap.update(EXTRA)
def conv(nd):
    if nd.is_leaf():
        m=re.match(r"([A-Za-z]+_[a-z]+)_([A-Z]+)_CARNIVORA",nd.taxon.label);up=m.group(1).replace('_',' ')
        if up not in keepmap: return None
        disp=keepmap[up];fam=m.group(2).capitalize()
        return N(disp,AGE.get(disp,0.0),fam=fam,ext=disp in AGE)
    ch=[c for c in (conv(x) for x in nd.child_nodes()) if c]
    if not ch: return None
    if len(ch)==1: return ch[0]
    return N(None,nd.age,ch)
root=conv(t.seed_node)
L={l.name:l for l in root.leaves()}
print('upham tips kept',len(L))
def mrca(*names):
    ps=[]
    for n in names:
        a=[];x=L[n]
        while x: a.append(x);x=x.parent
        ps.append(a)
    common=[x for x in ps[0] if all(x in p for p in ps[1:])]
    return common[0]
def insert_above(target,sub,age):
    """insert new node on the branch above target at given age; ancestors are pushed older if needed (Upham ND dates are young)"""
    age=max(age,target.age+0.05,sub.age+0.05)
    j=N(None,age,[]);p=target.parent
    if p:
        p.ch[p.ch.index(target)]=j;j.parent=p
    j.ch=[target,sub];target.parent=j;sub.parent=j
    c=j;p=j.parent
    while p is not None and p.age<=c.age+0.15:
        p.age=c.age+0.3;c=p;p=p.parent
    return j
def leaf(name,fam,ext=True):
    n=N(name,AGE.get(name,0.0),fam=fam,ext=ext);return n
def comb(names,fam,pad=0.25):
    """group of taxa (same genus) -> simple ladder by age"""
    ls=[leaf(n,fam) for n in names]
    ls.sort(key=lambda x:-x.age)
    if len(ls)==1: return ls[0]
    node=ls[-1]
    for x in reversed(ls[:-1]):
        node=N(None,max(x.age,node.age)+pad,[x,node])
    return node
def group(parts,pad=0.3):
    """join already-built subtrees into a ladder (oldest attaches deepest)"""
    parts=sorted(parts,key=lambda x:-x.age)
    node=parts[-1]
    for x in reversed(parts[:-1]):
        node=N(None,max(x.age,node.age)+pad,[x,node])
    return node
def G(fam,*names): return comb(list(names),fam)
def graft(target,sub,extra=0.6):
    return insert_above(target,sub,max(sub.age,target.age)+extra)
def sister(ref,name,frac=0.35,fam=None):
    r=L[ref];a=max(0.15,(r.parent.age-r.age)*frac) if r.parent else 0.5
    n=leaf(name,fam or r.fam,ext=name in AGE and AGE[name]>0.0);n.ext=name in AGE
    if name in AGE: n.age=AGE[name]
    if name in AGE: a=max(a,AGE[name]-r.age+0.3) if False else a
    j=insert_above(r,n,max(r.age+a,n.age+0.3));L[name]=n;return j
# ---------- new extant species (not in Upham) ----------
for ref,new in [('Canis latrans','Canis lycaon'),('Nyctereutes procyonoides','Nyctereutes viverrinus'),('Paradoxurus hermaphroditus','Paradoxurus musanga'),
 ('Paradoxurus musanga','Paradoxurus philippinensis'),('Urva javanica','Urva auropunctata'),('Proteles cristatus','Proteles septentrionalis'),
 ('Pusa hispida','Pusa saimensis'),('Ailurus fulgens','Ailurus styani'),('Canis lupus','Canis lupus dingo'),('Canis lupus','Canis lupus italicus'),
 ('Leopardus tigrinus','Leopardus guttulus'),('Leopardus tigrinus','Leopardus emiliae'),('Leopardus tigrinus','Leopardus pardinoides'),('Leopardus pardinoides','Leopardus tilcayo'),
 ('Leopardus colocolo','Leopardus pajeros'),('Leopardus colocolo','Leopardus braccatus'),('Leopardus braccatus','Leopardus fasciatus'),('Leopardus colocolo','Leopardus garleppi'),
 ('Prionailurus bengalensis','Prionailurus javanensis'),('Felis silvestris','Felis lybica'),('Melogale moschata','Melogale subaurantiaca'),
 ('Mustela nivalis','Mustela aistoodonnivalis'),('Mustela nivalis','Mustela mopbie'),('Mustela erminea','Mustela richardsonii'),('Mustela erminea','Mustela haidarum'),
 ('Conepatus semistriatus','Conepatus amazonicus'),('Spilogale putorius','Spilogale interrupta'),('Spilogale gracilis','Spilogale leucoparia'),
 ('Spilogale angustifrons','Spilogale yucatanensis'),('Arctonyx collaris','Arctonyx albogularis'),('Arctonyx collaris','Arctonyx hoevenii'),
 ('Meles leucurus','Meles amurensis'),('Meles meles','Meles canescens'),('Lontra longicaudis','Lontra annectens'),('Martes americana','Martes caurina')]:
    sister(ref,new)
for n in ['Canis lupus dingo','Canis lupus italicus']: L[n].age=0.0
for n in ['Canis lycaon','Nyctereutes viverrinus','Paradoxurus musanga','Paradoxurus philippinensis','Urva auropunctata','Proteles septentrionalis','Pusa saimensis',
 'Ailurus styani','Leopardus guttulus','Leopardus emiliae','Leopardus pardinoides','Leopardus tilcayo','Leopardus pajeros','Leopardus braccatus','Leopardus fasciatus',
 'Leopardus garleppi','Prionailurus javanensis','Felis lybica','Melogale subaurantiaca','Mustela aistoodonnivalis','Mustela mopbie','Mustela richardsonii',
 'Mustela haidarum','Conepatus amazonicus','Spilogale interrupta','Spilogale leucoparia','Spilogale yucatanensis','Arctonyx albogularis','Arctonyx hoevenii',
 'Meles amurensis','Meles canescens','Lontra annectens','Martes caurina']: L[n].ext=False;L[n].age=0.0
# ---------- fossils ----------
F='Felidae'
sister('Panthera leo','Panthera spelaea',0.5);sister('Panthera spelaea','Panthera atrox',0.5)
sister('Panthera tigris','Panthera zdanskyi',0.6);sister('Panthera onca','Panthera gombaszoegensis',0.7)
graft(mrca('Panthera leo','Panthera tigris'),G(F,'Panthera palaeosinensis'))
graft(mrca('Panthera leo','Panthera uncia'),G(F,'Panthera blytheae'))
sister('Acinonyx jubatus','Acinonyx pardinensis',0.6);sister('Puma concolor','Puma pardoides',0.6);sister('Acinonyx pardinensis','Miracinonyx trumani',0.5)
graft(mrca('Lynx lynx','Lynx rufus'),G(F,'Lynx issiodorensis'))
mach=group([group([G(F,'Homotherium crenatidens','Homotherium johnstoni','Homotherium latidens','Homotherium serum','Homotherium sp.'),G(F,'Xenosmilus hodsonae','Xenosmilus sp.')]),
            G(F,'Machairodus aphanistus','Machairodus africanus'),G(F,'Amphimachairodus giganteus','Amphimachairodus palanderi','Amphimachairodus sp.'),
            G(F,'Nimravides thinobates','Nimravides pedionomus','Nimravides catocopis','Nimravides sp.')])
smil=group([group([G(F,'Smilodon fatalis','Smilodon populator','Smilodon californicus','Smilodon sp.'),G(F,'Megantereon cultridens','Megantereon nihowanensis','Megantereon sp.')]),
            G(F,'Paramachaerodus maximiliani','Paramachaerodus orientalis')])
meta=group([G(F,'Dinofelis diastemata','Dinofelis abeli','Dinofelis sp.'),G(F,'Adelphailurus kansensis'),G(F,'Yoshi garevskii','Yoshi minor')])
sabre=group([mach,smil,meta])
fel=mrca('Panthera leo','Felis silvestris')
j=graft(fel,sabre);j=graft(j,G(F,'Pseudaelurus validus'));j=graft(j,G(F,'Proailurus lemanensis'))
B='Barbourofelidae'
graft(j,group([G(B,'Barbourofelis fricki','Barbourofelis lovei','Barbourofelis morrisi','Barbourofelis whitfordi'),G(B,'Albanosmilus jourdani'),G(B,'Sansanosmilus palmidens'),G(B,'Prosansanosmilus peregrinus')]))
H='Hyaenidae'
sister('Crocuta crocuta','Crocuta crocuta spelaea',0.4)
graft(mrca('Crocuta crocuta','Crocuta crocuta spelaea'),group([G(H,'Pachycrocuta brevirostris'),G(H,'Pliocrocuta perrieri'),G(H,'Adcrocuta eximia')]))
hy=mrca('Crocuta crocuta','Proteles cristatus','Hyaena hyaena')
j=graft(hy,group([G(H,'Lycyaena lunensis'),G(H,'Hyaenictitherium wongii'),G(H,'Ictitherium viverrinum','Ictitherium sp.'),G(H,'Thalassictis hipparionum'),G(H,'Plioviverrops orbignyi'),G(H,'Tungurictis spocki')]))
graft(j,G('Percrocutidae','Percrocuta tungurensis'))
graft(mrca('Urva javanica','Cryptoprocta ferox'),G('Feliformia incertae sedis','Herpestides antiquus'))
graft(mrca('Urva javanica','Paradoxurus hermaphroditus'),group([G('Stenoplesictidae','Palaeoprionodon lamandini'),G('Stenoplesictidae','Stenoplesictis cayluxi')]))
NI='Nimravidae'
nim=group([G(NI,'Hoplophoneus primaevus','Hoplophoneus occidentalis','Hoplophoneus dakotensis','Hoplophoneus sp.'),G(NI,'Eusmilus sicarius','Eusmilus bidentatus','Eusmilus sp.'),
           G(NI,'Nanosmilus kurteni'),G(NI,'Dinictis felina','Dinictis squalidens'),G(NI,'Pogonodon davisi'),G(NI,'Nimravus intermedius'),G(NI,'Eofelis sp.')])
graft(mrca('Panthera leo','Nandinia binotata'),nim)
C='Canidae'
sister('Canis lupus','Canis etruscus',0.8)
canina=mrca('Canis lupus','Lycaon pictus')
j=graft(canina,G(C,'Aenocyon dirus','Aenocyon edwardii'));graft(j,G(C,'Eucyon adoxus'))
graft(mrca('Chrysocyon brachyurus','Lycalopex culpaeus'),G(C,'Theriodictis platensis'))
graft(mrca('Nyctereutes procyonoides','Nyctereutes viverrinus'),G(C,'Nyctereutes megamastoides','Nyctereutes donnezani'))
graft(mrca('Urocyon cinereoargenteus','Urocyon littoralis'),G(C,'Urocyon minicephalus'))
graft(mrca('Vulpes vulpes','Vulpes zerda'),G(C,'Vulpes alopecoides'))
can=mrca('Vulpes vulpes','Canis lupus')
j=graft(can,G(C,'Leptocyon mollis','Leptocyon sp.'))
boro=group([G(C,'Borophagus diversidens','Borophagus orc','Borophagus secundus'),G(C,'Epicyon saevus','Epicyon sp.'),G(C,'Carpocyon webbi','Carpocyon sp.'),
            G(C,'Aelurodon ferox','Aelurodon stirtoni'),G(C,'Paratomarctus temerarius'),G(C,'Tomarctus brevirostris'),G(C,'Paracynarctus kelloggi','Paracynarctus sinclairi'),
            G(C,'Metatomarctus canavus'),G(C,'Archaeocyon pavidus'),G(C,'Otarocyon cooki')])
j=graft(j,boro)
hesp=group([G(C,'Osbornodon iamonensis'),G(C,'Enhydrocyon stenocephalus'),G(C,'Paraenhydrocyon josephi'),G(C,'Philotrox condoni'),G(C,'Sunkahetanka geringensis'),
            G(C,'Mesocyon brachyops','Mesocyon coryphaeus'),G(C,'Cynodesmus thooides'),G(C,'Hesperocyon gregarius'),G(C,'Prohesperocyon wilsoni')])
graft(j,hesp)
U='Ursidae'
sister('Ursus arctos','Ursus spelaeus',0.6);sister('Ursus spelaeus','Ursus deningeri',0.5);graft(mrca('Ursus arctos','Ursus americanus'),G(U,'Ursus etruscus'))
sister('Ailuropoda melanoleuca','Ailuropoda microta',0.6);graft(L['Ailuropoda microta'].parent,G(U,'Indarctos atticus'))
graft(L['Tremarctos ornatus'],group([G(U,'Arctodus simus','Arctodus floridanus','Arctodus pristinus'),G(U,'Arctotherium bonariensis')]))
urs=mrca('Ursus arctos','Ailuropoda melanoleuca')
j=graft(urs,G(U,'Hemicyon ursinus'));j=graft(j,G(U,'Cephalogale gracile','Cephalogale minor','Cephalogale geoffroyi'));j=graft(j,G(U,'Phoberogale minor'));j=graft(j,G(U,'Parictis personi'))
graft(j,group([G('Arctoidea incertae sedis','Kolponomos newportensis'),G('Arctoidea incertae sedis','Allocyon loganensis')]))
P='Phocidae'
sister('Pusa sibirica','Pusa saimensis',0.0) if False else None
graft(mrca('Monachus monachus','Neomonachus tropicalis'),G(P,'Eomonachus belegaerensis'))
graft(mrca('Lobodon carcinophaga','Hydrurga leptonyx'),group([G(P,'Piscophoca pacifica'),G(P,'Sarcodectes magnus')]))
pho=mrca('Phoca vitulina','Monachus monachus')
graft(pho,G('Desmatophocidae','Allodesmus kernensis'))
pin=mrca('Phoca vitulina','Otaria byronia')
PS='Pinnipedimorpha (stem)'
graft(pin,group([G(PS,'Enaliarctos mealsi','Enaliarctos sp.'),G(PS,'Pinnarctidion bishopi'),G(PS,'Potamotherium valletoni'),G(PS,'Puijila darwini')]))
graft(mrca('Ailurus fulgens','Ailurus styani'),group([G('Ailuridae','Simocyon primigenius'),G('Ailuridae','Magerictis imperialensis')]))
graft(mrca('Mephitis mephitis','Mydaus javanensis'),G('Mephitidae','Promephitis lartetii'))
sister('Procyon lotor','Procyon gipsoni',0.7);graft(mrca('Nasua nasua','Nasuella olivacea'),G('Procyonidae','Amphinasua brevirostris'))
graft(mrca('Procyon lotor','Potos flavus'),G('Procyonidae','Pseudobassaris riggsi'))
M='Mustelidae'
graft(mrca('Meles meles','Meles leucurus'),G(M,'Meles thorali'));graft(mrca('Meles meles','Meles anakuma'),G(M,'Promeles palaeattica'))
sister('Mellivora capensis','Mellivora sivalensis',0.6);sister('Lutra lutra','Lutra palaeindicus',0.6);sister('Lutra lutra','Lutra nippon',0.4)
graft(mrca('Galictis cuja','Galictis vittata'),G(M,'Enhydrictis ardea'))
graft(mrca('Martes martes','Martes americana'),G(M,'Martes transistoria'))
graft(mrca('Lutra lutra','Enhydra lutris'),group([G(M,'Siamogale melilutra','Siamogale bounosa'),G(M,'Vishnuonyx maemohensis')]))
mus=mrca('Mustela erminea','Taxidea taxus')
j=graft(mus,group([G(M,'Plionictis sp.'),G(M,'Cernictis sp.'),G(M,'Brachypsalis sp.')]))
j=graft(j,group([G(M,'Leptarctus wortmani','Leptarctus oregonensis'),G(M,'Legionarictis fortidens')]))
j=graft(j,group([G(M,'Promartes olcotti'),G(M,'Zodiolestes daimonelixensis','Zodiolestes sp.'),G(M,'Craterogale simus'),G(M,'Plesiogale angustifrons','Plesiogale paragale')]))
musteloid=mrca('Mustela erminea','Ailurus fulgens')
graft(musteloid,group([G('Musteloidea incertae sedis','Paragale huerzeleri'),G('Musteloidea incertae sedis','Bathygale lemanensis'),G('Musteloidea incertae sedis','Mustelictis piveteaui')]))
arct=mrca('Mustela erminea','Ursus arctos')
graft(arct,G('Amphicynodontidae','Pachycynodon boriei'))
A='Amphicyonidae'
amph=group([G(A,'Amphicyon major','Amphicyon longiramus','Amphicyon galushai','Amphicyon leptorhynchus','Amphicyon ambiguus'),G(A,'Pliocyon medius'),G(A,'Tartarocyon cazanavei'),
            G(A,'Cynelos lemanensis'),G(A,'Adilophontes brachykolos'),G(A,'Mammacyon ferocior'),G(A,'Temnocyon fingeruti','Temnocyon altigenis','Temnocyon ferox','Temnocyon subferox'),
            G(A,'Daphoenus hartshornianus','Daphoenus vetus'),G(A,'Gustafsonia cognita'),G(A,'Cynodictis lacustris','Cynodictis compressidens')])
graft(mrca('Canis lupus','Ursus arctos'),amph)
# stem Carnivora + outgroups
j=graft(root,G('Carnivoraformes (stem)','Quercygale angustidens'),1.0)
j=graft(j,group([G('Carnivoraformes (stem)','Vulpavus ovatus'),G('Carnivoraformes (stem)','Uintacyon sp.')]),1.0)
j=graft(j,G('Viverravidae','Viverravus acutus','Viverravidae Unident'),1.5)
HY='Hyaenodonta (hors Carnivora)'
hyg=group([G(HY,'Hyaenodon horridus'),G(HY,'Pterodon dasyuroides','Hyainailouros sulzeri','Hyainailouroidea Unident'),G(HY,'Cynohyaenodon cayluxi'),G(HY,'Limnocyoninae Unident')],pad=1.0)
ox=G('Oxyaenidae (hors Carnivora)','Patriofelis ferox')
out=N(None,max(hyg.age,ox.age)+2,[hyg,ox])
newroot=N(None,max(j.age,out.age)+4,[out,j])
root=newroot
# ---------- checks & export ----------
leaves=root.leaves();names=[l.name for l in leaves]
import collections
print('tips',len(leaves),'dups',[k for k,v in collections.Counter(names).items() if v>1])
for l in leaves:
    if l.fam is None: l.fam=FAM.get(l.name.split()[0])
bad=[]
def chk(n):
    for c in n.ch:
        if c.age>n.age+1e-9: bad.append((n.age,c.age,[x.name for x in c.leaves()][:2]))
        chk(c)
chk(root);print('neg branches',len(bad),bad[:5])
print('root age',round(root.age,2))
def ser(n): return {'a':n.age,'n':n.name,'f':n.fam,'x':n.ext,'c':[ser(c) for c in n.ch]}
json.dump(ser(root),open('tree.json','w'))
