#!/usr/bin/env node
// Roadmap 4.1: the hub's next action defaults per module `kind`.
//
// ADR-app-0002 § 0 put `kind` in the manifest precisely to carry this
// distinction, and the hub never read it — so all 29 modules got the same
// advice, which is only right for one of the four kinds:
//
//   licence/cert  a real exam exists elsewhere and the learner has usually
//                 not met the material. Explanation first. (Unchanged.)
//   compliance    no official exam exists anywhere; our record IS the proof,
//                 and the learner is typically a professional here to
//                 demonstrate what they already know. Opening with lesson one
//                 wastes their hour. A Kurzcheck measures first.
//   compare       these modules confer nothing and have no simulation to
//                 earn. Pointing "next" at a lesson or an exam would promise
//                 a destination that does not exist.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_kind_policy.mjs
import { chromium } from "playwright";
import { existsSync, readFileSync } from "node:fs";
const SITE = process.argv[2] || "http://localhost:8802";
let f = 0; const ok = m => console.log("  ok: " + m); const fail = m => { console.error("  FAIL: " + m); f++; };

const mods = JSON.parse(readFileSync("app/data/modules.json", "utf8")).modules;
const kindOf = t => (mods.find(m => m.exam_type === t) || {}).kind;

const b = await chromium.launch(existsSync("/opt/pw-browsers/chromium") ? { executablePath: "/opt/pw-browsers/chromium" } : {});

async function hub(examType, scope) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  const errs = []; page.on("pageerror", e => errs.push(String(e)));
  await page.goto(`${SITE}/app.html?exam=${examType}&scope=${scope}`, { waitUntil: "networkidle" });
  if (await page.isVisible("#storage-consent-notice")) { await page.click("#storage-consent-yes"); }
  await page.waitForTimeout(1800);
  return { ctx, page, errs };
}
const snap = page => page.evaluate(() => ({
  open: !document.querySelector("#module-hub").hidden,
  primary: document.querySelector("#module-hub-primary").innerText.trim(),
  primaryKind: document.querySelector("#module-hub-primary").dataset.primaryKind,
  next: document.querySelector("#module-hub-next").innerText.trim(),
  nextKind: document.querySelector("#module-hub-next").dataset.nextKind,
}));

// 1. compliance, first visit — the check is the PRIMARY, not a footnote
kindOf("datenschutz") === "compliance" ? ok("datenschutz is a compliance module (premise)") : fail("premise wrong");
let { ctx, page } = await hub("datenschutz", "ALL");
let s = await snap(page);
s.nextKind === "check" && s.next.length > 3
  ? ok(`compliance first visit suggests the Kurzcheck: "${s.next}"`)
  : fail(`nextKind=${s.nextKind}, label ${JSON.stringify(s.next)}`);
s.primaryKind === "check" ? ok(`...and it is the biggest button: "${s.primary}"`)
                          : fail(`primary is "${s.primary}" (${s.primaryKind}) — the policy would be advisory`);

// tapping it starts a mixed practice run, not a lesson and not a card list
await page.click("#module-hub-primary");
await page.waitForTimeout(1200);
let landed = await page.evaluate(() => ({
  practice: !document.querySelector("#practice-view").hidden,
  scope: state.practiceQuiz && state.practiceQuiz.scopeTopic,
  n: state.practiceQuiz && state.practiceQuiz.questions.length,
  picker: !document.querySelector("#practice-picker").hidden,
  reader: !document.querySelector("#course-reader").hidden,
}));
landed.practice && landed.scope === "mixed"
  ? ok(`the check runs: ${landed.n} mixed questions`) : fail(`landed on ${JSON.stringify(landed)}`);
!landed.picker ? ok("it does not hand the learner a topic menu first") : fail("opened the practice picker");
!landed.reader ? ok("it is not a lesson") : fail("opened a lesson");
await ctx.close();

// 2. compare — no lesson, no simulation, because neither is reachable
kindOf("uk_gb") === "compare" ? ok("uk_gb is a compare module (premise)") : fail("premise wrong");
({ ctx, page } = await hub("uk_gb", "ALL"));
s = await snap(page);
// The label is asserted, not just the kind. The first run of this test passed
// on nextKind alone while the button rendered EMPTY - a next action with no
// words on it is not a next action, and "the right kind" is exactly the sort
// of assertion that keeps passing while the screen is broken.
s.nextKind === "cards" && s.next.length > 3
  ? ok(`compare points at the cards: "${s.next}"`)
  : fail(`nextKind=${s.nextKind}, label ${JSON.stringify(s.next)}`);
s.primaryKind !== "check" ? ok("compare is never sent to a Kurzcheck") : fail("compare got the check");
await page.click("#module-hub-next");
await page.waitForTimeout(900);
landed = await page.evaluate(() => ({
  hub: !document.querySelector("#module-hub").hidden,
  reader: !document.querySelector("#course-reader").hidden,
  exam: !document.querySelector("#exam-view").hidden,
  cards: document.querySelectorAll("#list div.q-card").length,
}));
!landed.reader && !landed.exam ? ok("no lesson and no exam were promised") : fail(JSON.stringify(landed));
landed.cards > 0 ? ok(`${landed.cards} cards on screen`) : fail("no cards after tapping next");
await ctx.close();

// 3. licence — unchanged, still guided
kindOf("fuehrerschein") === "licence" ? ok("fuehrerschein is a licence module (premise)") : fail("premise wrong");
({ ctx, page } = await hub("fuehrerschein", "B"));
s = await snap(page);
s.nextKind === "learn" && s.next.length > 3
  ? ok(`licence still leads with explanation: "${s.next}"`)
  : fail(`nextKind=${s.nextKind}, label ${JSON.stringify(s.next)}`);
s.primaryKind === "resume" ? ok("licence keeps its resume primary") : fail(`primary is ${s.primaryKind}`);
await ctx.close();

// 4. the policy is read from `kind`, not hardcoded per module
const seen = await (async () => {
  const c = await b.newContext(); const p = await c.newPage();
  await p.goto(`${SITE}/app.html?exam=fuehrerschein&scope=B`, { waitUntil: "networkidle" });
  if (await p.isVisible("#storage-consent-notice")) await p.click("#storage-consent-yes");
  await p.waitForTimeout(1500);
  const r = await p.evaluate((types) => types.map(t => [t, hubNextPolicy(t)]),
    ["datenschutz", "dora", "cka", "aevo", "uk_gb", "switzerland_ch", "motorrad"]);
  await c.close(); return r;
})();
const want = { datenschutz: "check_first", dora: "check_first", cka: "guided", aevo: "guided",
               uk_gb: "cards", switzerland_ch: "cards", motorrad: "guided" };
const wrong = seen.filter(([t, p]) => want[t] !== p);
wrong.length === 0 ? ok(`policy resolves from kind for all ${seen.length} sampled modules`)
                   : fail(`wrong policy: ${JSON.stringify(wrong)}`);

await b.close();
console.log(f ? `\nFAILURES: ${f}` : "\nkind-policy checks passed");
process.exit(f ? 1 : 0);
