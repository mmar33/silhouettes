const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1400}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+__dirname+'/carnivora_arbre.html');await p.waitForTimeout(2500);await p.screenshot({path:'full.png'});
// zoom into a region
await p.evaluate(()=>{document.getElementById('tree').setAttribute('viewBox',process_vb)}).catch(()=>{});
for(const [n,vb] of [['z1','2300 300 1100 1100'],['z2','100 1300 1100 1100'],['z3','1200 2500 1300 1100']]){await p.evaluate(v=>document.getElementById('tree').setAttribute('viewBox',v),vb);await p.waitForTimeout(400);await p.screenshot({path:n+'.png'});}
console.log('errors',errs);await b.close();})();
