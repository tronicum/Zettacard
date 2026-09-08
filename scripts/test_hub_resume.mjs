#!/usr/bin/env node
// ADR-app-0002 § 1: "Weiterlernen, resuming the last topic and position."
//
// This exists because the button did not do that. It set the topic filter to
// "all" and called history.back() - it DISMISSED the hub to reveal an
// unfiltered card list, which made the largest button on the app's main screen
// a close button wearing a verb. Nothing caught it, because the hub closed and
// a list appeared, which looks like success.
//
// So the assertions are about WHERE the learner lands, not that something
// happened: the same topic, the same card, and still true after a reload.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_hub_resume.mjs
import { chromium } from "playwright";
import { existsSync } from "node:fs";
const SITE = process.argv[2] || "http://localhost:8802";
let f=0; const ok=m=>console.log("  ok: "+m); const fail=m=>{console.error("  FAIL: "+m);f++;};
const b = await chromium.launch(existsSync("/opt/pw-browsers/chromium")?{executablePath:"/opt/pw-browsers/chromium"}:{});
const ctx = await b.newContext({viewport:{width:390,height:844}});
const page = await ctx.newPage();
const errs=[]; page.on("pageerror",e=>errs.push(String(e)));
await page.goto(`${SITE}/app.html?exam=fuehrerschein&scope=B`,{waitUntil:"networkidle"});
if (await page.isVisible("#storage-consent-notice")) { await page.click("#storage-consent-yes"); await page.waitForTimeout(500); }
await page.waitForTimeout(1600);

// first visit: nothing to resume, so the button must say START
let label = (await page.locator("#module-hub-primary").innerText()).trim();
/start|starten/i.test(label) ? ok(`first visit says start: "${label}"`) : fail(`first visit says "${label}"`);

// study: pick a topic, open a specific card
await page.locator("#module-hub-primary").click(); await page.waitForTimeout(700);
const chip = page.locator('#filters [data-topic="zeichen_verbot"]');
await chip.click(); await page.waitForTimeout(500);
await page.locator("#list .q-card").nth(2).click(); await page.waitForTimeout(500);
const studiedId = await page.evaluate(() => filteredQuestions()[state.detailIndex].id);
ok(`studied card ${studiedId} in zeichen_verbot`);
await page.goBack(); await page.waitForTimeout(400);

// reopen the hub - it must now offer to CONTINUE
await page.locator("#menu-btn").click(); await page.waitForTimeout(300);
await page.locator("#module-info-btn").click(); await page.waitForTimeout(800);
label = (await page.locator("#module-hub-primary").innerText()).trim();
/continue|weiter/i.test(label) ? ok(`after studying says continue: "${label}"`) : fail(`says "${label}"`);

// ...and the tap must land back on that exact card in that topic
await page.locator("#module-hub-primary").click(); await page.waitForTimeout(900);
const after = await page.evaluate(() => ({
  detail: !document.querySelector("#detail-view").hidden,
  topic: state.topicFilter,
  id: state.detailIndex !== null ? filteredQuestions()[state.detailIndex].id : null,
  hubOpen: !document.querySelector("#module-hub").hidden,
}));
after.detail ? ok("resumes into the card, not the list") : fail("did not reopen a card");
after.topic === "zeichen_verbot" ? ok(`restored the topic: ${after.topic}`) : fail(`topic is ${after.topic}`);
after.id === studiedId ? ok(`restored the exact card: ${after.id}`) : fail(`landed on ${after.id}, expected ${studiedId}`);
after.hubOpen ? fail("hub still open") : ok("hub closed");

// survives a reload - the point of persisting it
await page.reload({waitUntil:"networkidle"}); await page.waitForTimeout(1800);
if (await page.isVisible("#module-hub")) {
  await page.locator("#module-hub-primary").click(); await page.waitForTimeout(900);
  const r = await page.evaluate(() => ({ topic: state.topicFilter,
    id: state.detailIndex !== null ? filteredQuestions()[state.detailIndex].id : null }));
  r.id === studiedId ? ok("resume survives a reload") : fail(`after reload landed on ${r.id}`);
} else fail("cold launch did not land on the hub");
if (errs.length) errs.slice(0,2).forEach(e=>fail("page error: "+e.slice(0,140)));
await b.close();
console.log(f?`\nFAILURES: ${f}`:"\nresume checks passed");
process.exit(f?1:0);
