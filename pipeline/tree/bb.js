const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+__dirname+'/allart.html');
const r=await p.evaluate(()=>[...document.querySelectorAll('svg>g')].map(g=>{const b=g.getBBox();return [b.x,b.y,b.width,b.height]}));
fs.writeFileSync('bboxes.json',JSON.stringify(r));await b.close();console.log(r.length,r.filter(x=>!x[2]).length);})();
