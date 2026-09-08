#!/usr/bin/env node
// The learning path: a topic row opens the topic's LESSON, not its card list.
//
// The navigation concept's diagnosis was that the app had four topic-shaped
// lists (hub topics, filter chips, practice picker, course lessons) all
// showing the same topics, none ordered as a path - and that the one thing
// carrying a didactic order, the course, was hidden in the menu while the
// hub's "next" pointed at raw cards. Explain-then-try is the order the data
// already encodes, and the only one whose first screen is an explanation in
// the learner's own language.
//
// So this asserts the DESTINATION of each control, which is the thing that
// changed: the row opens a lesson, the quiet escape opens the cards, and
// "next" agrees with the row it names.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_learning_path.mjs

import { chromium } from "playwright";
import { existsSync } from "node:fs";
const SITE = process.argv[2] || "http://localhost:8802";
let f=0; const ok=m=>console.log("  ok: "+m); const fail=m=>{console.error("  FAIL: "+m);f++;};
const b = await chromium.launch(existsSync("/opt/pw-browsers/chromium")?{executablePath:"/opt/pw-browsers/chromium"}:{});
const page = await (await b.newContext({viewport:{width:390,height:844}})).newPage();
const errs=[]; page.on("pageerror",e=>errs.push(String(e)));
await page.goto(`${SITE}/app.html?exam=fuehrerschein&scope=B`,{waitUntil:"networkidle"});
if (await page.isVisible("#storage-consent-notice")) { await page.click("#storage-consent-yes"); await page.waitForTimeout(500); }
await page.waitForTimeout(2200);   // hub + course prefetch

// every topic row must offer a lesson AND a cards escape
const rows = await page.locator("#module-hub-topics .hub-topic-btn").count();
const escapes = await page.locator("#module-hub-topics [data-topic-cards]").count();
rows>0 ? ok(`${rows} topic rows`) : fail("no topic rows");
escapes===rows ? ok(`all ${escapes} rows carry a "just the cards" escape`) : fail(`${escapes} escapes for ${rows} rows`);

// the row itself opens the LESSON
await page.locator("#module-hub-topics .hub-topic-btn").first().click();
await page.waitForTimeout(1100);
if (await page.isVisible("#course-reader")) {
  const t=(await page.locator("#course-reader-title").innerText()).trim();
  const body=(await page.locator("#course-reader-body").innerText()).trim();
  ok(`topic row opens a lesson: "${t}"`);
  body.length>60 ? ok(`lesson has readable content (${body.length} chars)`) : fail("lesson body too short");
} else fail("topic row did not open a lesson");
await page.goBack(); await page.waitForTimeout(700);

// the escape opens the CARDS, filtered to that topic
if (!(await page.isVisible("#module-hub"))) { await page.locator("#menu-btn").click(); await page.waitForTimeout(300); await page.locator("#module-info-btn").click(); await page.waitForTimeout(900); }
const code = await page.locator("#module-hub-topics [data-topic-cards]").first().getAttribute("data-topic-cards");
await page.locator("#module-hub-topics [data-topic-cards]").first().click();
await page.waitForTimeout(800);
const after = await page.evaluate(() => ({ topic: state.topicFilter, cards: document.querySelectorAll("#list .q-card").length,
  reader: !document.querySelector("#course-reader").hidden, hub: !document.querySelector("#module-hub").hidden }));
after.topic===code ? ok(`escape filters to ${after.topic}`) : fail(`escape gave topic ${after.topic}, expected ${code}`);
after.cards>0 && !after.reader ? ok(`escape shows ${after.cards} cards, not a lesson`) : fail("escape did not show the card list");
after.hub ? fail("hub left open") : ok("hub closed");

// "next" must point at a lesson too
if (!(await page.isVisible("#module-hub"))) { await page.locator("#menu-btn").click(); await page.waitForTimeout(300); await page.locator("#module-info-btn").click(); await page.waitForTimeout(900); }
const kind = await page.locator("#module-hub-next").getAttribute("data-next-kind");
await page.locator("#module-hub-next").click(); await page.waitForTimeout(1100);
if (kind==="learn") {
  (await page.isVisible("#course-reader")) ? ok('"next" opens a lesson, not a card list') : fail('"next" did not open a lesson');
} else ok(`next kind is ${kind}, lesson check not applicable`);

if (errs.length) errs.slice(0,3).forEach(e=>fail("page error: "+e.slice(0,150)));
await b.close();
console.log(f?`\nFAILURES: ${f}`:"\nlearning-path checks passed");
process.exit(f?1:0);
