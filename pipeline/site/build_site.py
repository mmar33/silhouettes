"""Assemble la page unique du site SCAR (arbre + domestiques), en anglais.
usage: python3 build_site.py ARBRE_HTML DOM_INDEX_JSON OUT_HTML"""
import re,sys,json,os
HERE=os.path.dirname(os.path.abspath(__file__))
arbre,domidx,outp=sys.argv[1:4]
g=open(os.path.join(HERE,'domestiques_template.html')).read()
dom=json.load(open(domidx))
rows=[[o['f'][len('domestic/'):-4],o['fr'],o['en'],o['fci'],o['k']] for o in dom]
k=g.index('const DOM=');e=g.index('];',k)+2
g=g[:k]+'const DOM='+json.dumps(rows,ensure_ascii=False)+';'+g[e:]
css=g[g.index('<style>')+7:g.index('</style>')]
body=g[g.index('<body>')+6:g.index('<script>')]
js=g[g.index('<script>')+8:g.index('</script>')]
ids=['tabs','bar','q','flt','count','main','list','empty','legend','pager','tip','big','cap','sub']
def ren(s):
    for i in sorted(ids,key=len,reverse=True):
        s=re.sub(r'#'+i+r'\b(?![-\w])','#d'+i,s)
        s=s.replace(f'id="{i}"',f'id="d{i}"').replace(f"getElementById('{i}')",f"getElementById('d{i}')")
    return s
css,body,js=ren(css),ren(body),ren(js)
css=re.sub(r'html,body\{[^}]*\}\n','',css);css=re.sub(r'body\{[^}]*\}\n','',css)
css=css.replace('header{padding:14px 18px 10px;border-bottom:1px solid #eee;flex:none}','#dom header{padding:18px 18px 10px;border-bottom:1px solid #eee}')
css=css.replace('h1{','#dom h1{').replace('h2{','#dom h2{').replace('h2 span{','#dom h2 span{')
css=re.sub(r'#dmain\{flex:1;overflow-y:auto;','#dmain{',css)
css='#dom{font-family:Arial,Helvetica,sans-serif;color:#222;border-top:1px solid #e5e5e5;margin-top:8px}\n'+css
js=js.replace("document.getElementById('dmain').scrollTop=0;","")
body=body.replace('<h1>DOMESTIQUES</h1>','<h1>CARNIVORES DOMESTIQUES</h1>')
t=open(arbre).read()
t=t.replace('html,body{margin:0;height:100%;background:#fff;font-family:Arial,Helvetica,sans-serif;overflow:hidden}',
            'html,body{margin:0;background:#fff;font-family:Arial,Helvetica,sans-serif}')
t=t.replace('#wrap{position:relative;width:100%;height:100%;cursor:grab;touch-action:none}',
            '#wrap{position:relative;width:100%;aspect-ratio:1/1;max-height:100vh;margin:0 auto;cursor:grab;touch-action:pan-y pinch-zoom}')
t=t.replace('</style></head>',css+'</style></head>',1)
k=t.index('<div id="tip"></div>')
t=t[:k]+'<section id="dom">'+body+'</section>\n'+t[k:]
t=t.replace('</script></body></html>','</script>\n<script>'+js+'</script></body></html>')
t=t.replace('<title>Phylogénie des Carnivora</title>','<title>Silhouettes de Carnivora</title>')
open(outp,'w').write(t)
import subprocess
subprocess.run([sys.executable,os.path.join(HERE,'translate_en.py'),outp],check=True)
print('ok',outp,len(t))
