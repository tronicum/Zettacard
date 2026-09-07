import { chromium } from 'playwright';
import http from 'http';
import fs from 'fs';
import path from 'path';

const ROOT = process.env.HOME + '/mnt/Zettacard/app';
const MIME = {'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.webmanifest':'application/manifest+json'};
const server = http.createServer((req,res)=>{
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/app.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('nf'); }
  res.writeHead(200, {'content-type': MIME[path.extname(f)] || 'application/octet-stream'});
  fs.createReadStream(f).pipe(res);
});
await new Promise(r=>server.listen(8799,r));

const devices = [
  {name:'iphone-se',   w:375, h:667},
  {name:'iphone-14',   w:390, h:844},
  {name:'iphone-promax',w:430,h:932},
];
const browser = await chromium.launch();
const out = process.env.HOME + '/mnt/Zettacard/_layout_shots';
fs.mkdirSync(out,{recursive:true});
const report = [];
for (const d of devices) {
  const ctx = await browser.newContext({viewport:{width:d.w,height:d.h}, deviceScaleFactor:2, isMobile:true, hasTouch:true});
  const page = await ctx.newPage();
  await page.goto('http://localhost:8799/app.html', {waitUntil:'networkidle'});
  await page.waitForTimeout(800);
  await page.screenshot({path:`${out}/${d.name}.png`});
  const m = await page.evaluate(()=>{
    const de=document.documentElement;
    const filters=document.querySelector('.filters');
    const fr=filters?filters.getBoundingClientRect():null;
    const firstCard=document.querySelector('.card,[class*=card],article');
    const overflow=[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>innerWidth+1}).map(e=>({tag:e.tagName,cls:(e.className||'').toString().slice(0,40),right:Math.round(e.getBoundingClientRect().right)}));
    const smalls=[...document.querySelectorAll('button,a,[role=button],select,input')].map(e=>{const r=e.getBoundingClientRect();return{txt:(e.textContent||'').trim().slice(0,24),w:Math.round(r.width),h:Math.round(r.height)}}).filter(x=>x.h>0&&x.h<44);
    return {vw:innerWidth, vh:innerHeight, scrollW:de.scrollWidth, horizScroll:de.scrollWidth>innerWidth,
      filtersHeight: fr?Math.round(fr.height):null, filtersBottom: fr?Math.round(fr.bottom):null,
      pctScreenUsedByChrome: fr?Math.round(fr.bottom/innerHeight*100):null,
      overflowCount:overflow.length, overflow:overflow.slice(0,8),
      smallTapCount:smalls.length, smalls:smalls.slice(0,10)};
  });
  report.push({device:d.name, ...m});
  await ctx.close();
}
await browser.close(); server.close();
console.log(JSON.stringify(report,null,1));
