#!/usr/bin/env node
// The landing page's module cards were 22 inert <div>s. The PO found this on
// staging - "the modules are not linked anymore", right next to "jetzt
// starten? for what?" - and the two complaints have the same root: nothing on
// the front page could say which module you were about to open.
//
// They were never linked because a link without a scope did nothing. app.js
// required BOTH ?exam= and ?scope=, so ?exam=motorrad was stripped from the
// URL and then ignored, silently restoring whatever module you last used.
//
// So these assertions are about arrival, not about markup: a card is a link,
// the link names a module that exists, and following it puts you in THAT
// module - including when you already had a different one saved, which is
// the shape DN-57 came back in.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_module_links.mjs
import { chromium } from "playwright";
import { existsSync, readFileSync } from "node:fs";
const SITE = process.argv[2] || "http://localhost:8802";
let f = 0; const ok = m => console.log("  ok: " + m); const fail = m => { console.error("  FAIL: " + m); f++; };

const manifest = JSON.parse(readFileSync("app/data/modules.json", "utf8"));
const mods = manifest.modules || manifest;
const scopesFor = (t) => (mods.find(m => m.exam_type === t) || {}).options || [];

const b = await chromium.launch(existsSync("/opt/pw-browsers/chromium") ? { executablePath: "/opt/pw-browsers/chromium" } : {});
const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
const page = await ctx.newPage();
await page.goto(`${SITE}/index.html`, { waitUntil: "networkidle" });
await page.waitForTimeout(600);

// 1. no inert cards left
const cards = await page.$$eval(".module-card", els => els.map(e => ({
  tag: e.tagName.toLowerCase(), href: e.getAttribute("href") || "", label: (e.querySelector("strong") || {}).textContent || "",
})));
cards.length >= 20 ? ok(`${cards.length} module cards on the landing page`) : fail(`only ${cards.length} cards`);
const inert = cards.filter(c => c.tag !== "a" || !c.href.includes("exam="));
inert.length === 0 ? ok("every card is a link carrying ?exam=") : fail(`${inert.length} inert: ${inert.map(c => c.label).join(", ")}`);

// 2. no dead links - every linked module exists in the manifest
const linked = cards.map(c => new URL(c.href, `${SITE}/`).searchParams.get("exam"));
const dead = linked.filter(t => !mods.some(m => m.exam_type === t));
dead.length === 0 ? ok(`all ${linked.length} links resolve to a real module`) : fail(`dead links: ${dead.join(", ")}`);

// `state` is a module-scope binding in app.js, not window.state - reachable
// as a bare identifier inside evaluate, which is how every other suite here
// reads it. Probing window.state returns undefined for all five fields and
// reads as five failures in a row, which is exactly what it did.
const landed = () => page.evaluate(() => ({
  exam: state.examType, scope: state.scopeCode,
  picker: !document.querySelector("#module-picker").hidden,
  step: state.modulePickerStep,
  pending: state.pendingModule && state.pendingModule.exam_type,
  hub: !document.querySelector("#module-hub").hidden,
}));

// 3. a one-scope module: nothing to ask, so go straight in
await page.goto(`${SITE}/app.html?exam=it_sicherheit`, { waitUntil: "networkidle" });
if (await page.isVisible("#storage-consent-notice")) { await page.click("#storage-consent-yes"); }
await page.waitForTimeout(1800);
let s = await landed();
scopesFor("it_sicherheit").length === 1 ? ok("it_sicherheit has one scope (premise)") : fail("premise wrong");
s.exam === "it_sicherheit" ? ok(`?exam= alone opened it_sicherheit (scope ${s.scope})`) : fail(`landed on ${s.exam}`);
s.picker ? fail("asked for a scope when there is only one") : ok("did not ask a question with one answer");

// 4. a many-scope module: ask, but ask about THIS module
await page.goto(`${SITE}/app.html?exam=motorrad`, { waitUntil: "networkidle" });
await page.waitForTimeout(1800);
s = await landed();
s.picker && s.step === "scope" ? ok("motorrad opened the scope step") : fail(`picker=${s.picker} step=${s.step}`);
s.pending === "motorrad" ? ok("...for motorrad, not the full module list") : fail(`pending is ${s.pending}`);
const scopeBtns = await page.$$eval("#module-picker button", els => els.map(e => e.textContent.trim()).filter(Boolean));
scopeBtns.some(t => /A1/.test(t)) ? ok(`scope options shown: ${scopeBtns.slice(0, 4).join(" / ")}`) : fail(`no A1 among: ${scopeBtns.slice(0, 6).join(" / ")}`);

// 5. DN-57, multi-scope shape: a stated intent beats a saved one
await page.click('#module-picker button:has-text("A1")').catch(() => {});
await page.waitForTimeout(1500);
s = await landed();
s.exam === "motorrad" ? ok(`saved motorrad/${s.scope} for the next visit`) : fail(`selection did not stick: ${s.exam}`);
await page.goto(`${SITE}/app.html?exam=lkw`, { waitUntil: "networkidle" });
await page.waitForTimeout(1800);
s = await landed();
s.pending === "lkw" ? ok("a saved module does not override the card you tapped") : fail(`tapped lkw, got ${s.pending || s.exam}`);

await b.close();
console.log(f ? `\nFAILURES: ${f}` : "\nmodule-link checks passed");
process.exit(f ? 1 : 0);
