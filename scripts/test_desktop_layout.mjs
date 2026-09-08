#!/usr/bin/env node
// The app is built for a 390px phone and every layout fix has been made
// there. That is the right priority and it left a hole: `main` has always
// been a 720px centred column, `header` never was.
//
// Reported from a desktop window - "a fix for mobile phone sized views leads
// to desktop sized (landscape) view to be forced into a more horizontal
// setup". At 1440px the title sat against the far left edge, the buttons
// against the far right, and the 17 topic chips - which wrap, as they must on
// a phone - spread across the whole window in two long rows above a 720px
// column of question cards. Two layouts stacked on one page.
//
// So: the header's rows and the content column must share the same left and
// right edges at every width, and the floating globe must not collide with
// the header controls at any of them. Nothing here asserts a pixel value -
// only that the two halves of the page agree with each other.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_desktop_layout.mjs
import { chromium } from "playwright";
import { existsSync } from "node:fs";
const SITE = process.argv[2] || "http://localhost:8802";
let f = 0; const ok = m => console.log("  ok: " + m); const fail = m => { console.error("  FAIL: " + m); f++; };

const b = await chromium.launch(existsSync("/opt/pw-browsers/chromium") ? { executablePath: "/opt/pw-browsers/chromium" } : {});

// 390 is the phone the app is designed for; 1024 the landscape case the
// report named; 1440 a desktop window; 900 the breakpoint's own edge.
for (const [name, w, h] of [["phone", 390, 844], ["breakpoint", 900, 700], ["landscape", 1024, 600], ["desktop", 1440, 900]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h } });
  const page = await ctx.newPage();
  await page.goto(`${SITE}/app.html?exam=fuehrerschein&scope=B`, { waitUntil: "networkidle" });
  if (await page.isVisible("#storage-consent-notice")) { await page.click("#storage-consent-yes"); }
  await page.waitForTimeout(1800);
  await page.evaluate(() => { try { closeModuleHub(); } catch (e) { } });
  await page.waitForTimeout(500);

  const box = sel => page.evaluate(s => {
    const e = document.querySelector(s); if (!e) return null;
    const r = e.getBoundingClientRect();
    return { left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width) };
  }, sel);

  // #list, not main: main's border box carries its own 16px padding, so the
  // thing to line the header up with is where the CARDS actually start.
  const [title, filters, main, globe] =
    await Promise.all([box(".title-row"), box("#filters"), box("#list"), box("#lang-btn")]);
  // The 74px globe reserve is padding INSIDE .header-controls, so that box
  // extends past its last button by design. Measure the button.
  const controls = await page.evaluate(() => {
    const kids = [...document.querySelectorAll(".header-controls > *")]
      .filter(e => e.offsetParent !== null);
    if (!kids.length) return null;
    return { right: Math.round(Math.max(...kids.map(e => e.getBoundingClientRect().right))) };
  });

  if (!title || !filters || !main) { fail(`${name}: missing element`); continue; }

  // 1. the header's rows sit in the same column as the content
  const dTitle = Math.abs(title.left - main.left) + Math.abs(title.right - main.right);
  const dFilters = Math.abs(filters.left - main.left) + Math.abs(filters.right - main.right);
  dTitle <= 2 ? ok(`${name} (${w}px): title row shares the content column (${title.left}-${title.right})`)
              : fail(`${name}: title row ${title.left}-${title.right}, main ${main.left}-${main.right}`);
  dFilters <= 2 ? ok(`${name} (${w}px): filter chips share it too`)
                : fail(`${name}: filters ${filters.left}-${filters.right}, main ${main.left}-${main.right}`);

  // 2. the column never exceeds its cap, and never exceeds the window
  main.width <= 690 ? ok(`${name}: column is ${main.width}px`) : fail(`${name}: column ran to ${main.width}px`);

  // 3. the floating globe is fixed to the viewport, the header is not - they
  //    must not overlap at any width. This is the mobile bug the 74px reserve
  //    was added for; dropping that reserve above 900px must not bring it back.
  if (globe && controls) {
    const overlap = controls.right > globe.left;
    overlap ? fail(`${name}: header controls (…${controls.right}) run under the globe (${globe.left}…)`)
            : ok(`${name}: globe clears the header controls by ${globe.left - controls.right}px`);
  }
  await ctx.close();
}

await b.close();
console.log(f ? `\nFAILURES: ${f}` : "\ndesktop-layout checks passed");
process.exit(f ? 1 : 0);
