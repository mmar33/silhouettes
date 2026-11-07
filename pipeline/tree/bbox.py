import json,subprocess,re,os
HERE=os.path.dirname(os.path.abspath(__file__));os.chdir(HERE)
REPO=os.path.abspath(os.path.join(HERE,'..','..'))
t=json.load(open('tree.json'));old=json.load(open('old_art.json'));WF={o['n']:o['f'] for o in json.load(open('../work/wild_index.json'))['wild']}
def newart(n):
    s=open(os.path.join(REPO,WF[n])).read()
    return [('w' if c.lower()=='#ffffff' else 'k',d) for c,d in re.findall(r'<path fill="(#[0-9a-fA-F]{6})" d="([^"]+)"',s)]
COL={'Viverridae':'#e36776','Eupleridae':'#fac97f','Herpestidae':'#ff8d41','Hyaenidae':'#c77037','Prionodontidae':'#f07ca7','Felidae':'#b973c5','Nandiniidae':'#fbe91b',
'Canidae':'#737ac1','Ursidae':'#d3e55c','Otariidae':'#82d9e3','Odobenidae':'#40a6d8','Phocidae':'#62aff3','Ailuridae':'#93e23f','Procyonidae':'#81ada7',
'Mustelidae':'#7fc57f','Mephitidae':'#808080',
'Barbourofelidae':'#8e5aa8','Nimravidae':'#6b5b95','Percrocutidae':'#9c5a2c','Stenoplesictidae':'#d98c8c','Feliformia incertae sedis':'#c4a080',
'Amphicyonidae':'#4b5ea8','Amphicynodontidae':'#a8b56a','Arctoidea incertae sedis':'#8f9a5e','Pinnipedimorpha (stem)':'#4f97ad','Desmatophocidae':'#3d84a8',
'Musteloidea incertae sedis':'#5d9a5d','Viverravidae':'#a3a3a3','Carnivoraformes (stem)':'#8a8a8a','Hyaenodonta (hors Carnivora)':'#5c5c5c','Oxyaenidae (hors Carnivora)':'#757575'}
fam={}
def w(n):
    if not n['c']: fam[n['n']]=n['f']
    for c in n['c']: w(c)
w(t)
miss=[f for f in set(fam.values()) if f not in COL];print('missing colors',miss)
arts={}
for n,f in fam.items():
    if n in old: arts[n]=old[n]
    else: arts[n]=''.join(f'<path fill="{"#ffffff" if k=="w" else COL.get(f,"#000000")}" d="{d}"/>' for k,d in newart(n))
json.dump({'arts':arts,'fam':fam,'COL':COL},open('arts.json','w'))
html='<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'+''.join(f'<g id="a{i}">{a}</g>' for i,a in enumerate(arts.values()))+'</svg>'
open('allart.html','w').write('<html><body>'+html+'</body></html>')
json.dump(list(arts.keys()),open('artnames.json','w'))
