import { createRequire } from 'module';
const require = createRequire(process.env.HOME + '/mnt/Zettacard/package.json');
const { chromium } = require('playwright');
import http from 'http'; import fs from 'fs'; import path from 'path';
const ROOT = process.env.HOME + '/mnt/Zettacard/app';
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.webmanifest':'application/manifest+json','.ico':'image/x-icon'};
const server=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p==='/')p='/app.html';const f=path.join(ROOT,p);if(!f.startsWith(ROOT)||!fs.existsSync(f)||fs.statSync(f).isDirectory()){r.writeHead(404);return r.end('nf');}r.writeHead(200,{'content-type':MIME[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r);});
await new Promise(r=>server.listen(8801,r));
const out=process.env.HOME+'/mnt/Zettacard/tmp/shots'; fs.mkdirSync(out,{recursive:true});

const probe = () => {
  const de=document.documentElement;
  const vis = el => { const r=el.getBoundingClientRect(); const s=getComputedStyle(el);
    return r.width>0 && r.height>0 && s.visibility!=='hidden' && s.display!=='none' && s.opacity!=='0'; };
  const small=[...document.querySelectorAll('button,a[href],[role=button],select,input,summary')]
    .filter(vis).map(e=>{const r=e.getBoundingClientRect();
      return {t:(e.textContent||e.getAttribute('aria-label')||e.id||'').trim().slice(0,30),
              cls:(e.className||'').toString().slice(0,34),w:Math.round(r.width),h:Math.round(r.height)};})
    .filter(x=>x.h<44||x.w<24);
  const ov=[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();
      return r.width>0 && (r.right>innerWidth+1||r.left<-1);})
    .map(e=>({tag:e.tagName,cls:(e.className||'').toString().slice(0,34),
              right:Math.round(e.getBoundingClientRect().right)}));
  // dead space above the first visible card inside a modal
  const card=document.querySelector('.exam-modal:not([hidden]) .exam-modal-card');
  let modal=null;
  if (card){const r=card.getBoundingClientRect();
    modal={topGap:Math.round(r.top),bottomGap:Math.round(innerHeight-r.bottom),cardH:Math.round(r.height)};}
  return {vw:innerWidth,vh:innerHeight,scrollW:de.scrollWidth,horizScroll:de.scrollWidth>innerWidth+1,
          smallTargets:small, overflow:ov.slice(0,8), modal};
};

const results=[];
const browser=await chromium.launch();
for (const d of [{n:'se',w:375,h:667},{n:'i14',w:390,h:844}]){
  const ctx=await browser.newContext({viewport:{width:d.w,height:d.h},deviceScaleFactor:2,isMobile:true,hasTouch:true});
  const page=await ctx.newPage();
  const shot=async(name)=>{await page.screenshot({path:`${out}/${d.n}-${name}.png`});
    results.push({device:d.n,screen:name,...await page.evaluate(probe)});};
  await page.goto('http://localhost:8801/app.html',{waitUntil:'networkidle'});
  await page.waitForTimeout(500);
  await shot('01-consent');
  const yes=page.getByRole('button',{name:/Yes, save locally|Ja, lokal speichern/});
  if (await yes.count()) { await yes.first().click(); await page.waitForTimeout(600); }
  await shot('02-module-picker');
  const drv=page.getByRole('button',{name:/^Driving licence/});
  if (await drv.count()) { await drv.first().click(); await page.waitForTimeout(700); }
  await shot('03-class-picker');
  const cls=page.getByRole('button',{name:/Class B/});
  if (await cls.count()) { await cls.first().click(); await page.waitForTimeout(1200); }
  await shot('04-module-intro');
  // dismiss the module-intro dialog that blocks the list
  for (let i=0;i<4;i++){
    const dlg=page.locator('.exam-modal:not([hidden])');
    if (!(await dlg.count())) break;
    const btn=dlg.locator('button:visible').last();
    if (await btn.count()) { await btn.click({force:true}).catch(()=>{}); await page.waitForTimeout(600); }
    else break;
  }
  await shot('05-list');
  const firstCard=page.locator('.q-card').first();
  if (await firstCard.count()) { await firstCard.click({force:true}).catch(()=>{}); await page.waitForTimeout(700); }
  await shot('06-detail');
  await ctx.close();
}
await browser.close(); server.close();
fs.writeFileSync(out+'/report.json',JSON.stringify(results,null,1));
for (const r of results){
  console.log(`\n### ${r.device} ${r.vw}x${r.vh} — ${r.screen}`);
  console.log(`   horizScroll=${r.horizScroll} scrollW=${r.scrollW} overflow=${r.overflow.length}`);
  if (r.modal) console.log(`   modal: card ${r.modal.cardH}px, dead space ${r.modal.topGap}px above / ${r.modal.bottomGap}px below`);
  if (r.smallTargets.length) console.log(`   small tap targets (${r.smallTargets.length}):`,
    JSON.stringify(r.smallTargets.slice(0,8)));
  if (r.overflow.length) console.log('   OVERFLOW:', JSON.stringify(r.overflow.slice(0,4)));
}
