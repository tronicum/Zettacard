# ADR-0003: Mobile / small-screen layout strategy - fluid, breakpoint-free by design

- **Status:** Proposed
- **Date:** 2026-09-05
- **Deciders:** PO (pending); drafted by an AI agent from a read of the actual repo state on this date
- **Numbering note:** the two earlier ADRs in this directory were written the same day by different agents and both claim the first number (`ADR-0001` in `ADR-exam-e2e-testing.md`, `ADR-001` in `ADR-llm-translation-qa.md`). This document takes `ADR-0003` in the four-digit form so it collides with neither; the translation-QA ADR should be renumbered to `ADR-0002` when it is next touched. Format follows the existing two: Title / Status / Date / Context / Decision Drivers / Considered Options / Decision / Consequences / Implementation Notes.

## Context

Zettacard is a build-step-free static PWA; `netlify.toml` publishes `app/` as-is. The layout lives in one stylesheet, `app/styles.css` (1,926 lines), driven by `app/app.html` and a single classic script `app/app.js` (~7.8k lines). The app's primary audience is phones: `app.html` ships `viewport-fit=cover`, there is an iOS install page (`get-app.html`), and the existing Playwright consent test runs at 390x844.

### The finding this ADR is built around

`app/styles.css` contains **zero `@media` rules**. `grep -n "@media" app/styles.css` returns nothing. There is no small-screen stylesheet, no breakpoint, no `(hover)`/`(pointer)` query, no `prefers-reduced-motion`. Every screen is laid out by one set of rules at every width.

The stylesheet is nevertheless mobile-aware, in a piecemeal but consistent way:

| technique | where (line numbers in `app/styles.css`) |
|---|---|
| **44px tap-target floor** | `.theme-toggle` 44x44 (95-109); `.lang-select` `min-height: 44px` (198-210); `.filters button` `min-height: 44px` (226-236); `.back-btn` `min-height: 44px` (396-405); `.star-btn` `min-height: 44px` (570-583); `.sign-ref-icon` 44x44 (1544-1548). `.role-filters button` is a deliberate 40px "secondary" variant (255-259). |
| **Notch / home-indicator insets** | `header` (124), `main` (284-286), `.detail-header` (390), `.detail-body` (413) - all `calc(<base> + env(safe-area-inset-*))`, documented as DN-23. |
| **Width caps instead of breakpoints** | `main` 720px (279); `.detail-body` 680px (408); `.exam-modal-card` 440px (933) with per-dialog inline overrides of 420/480/560/640px in `app.html`; `.course-media-frame` 520px (1115); `.storage-consent-card` 480px (1866); `.kd-card` 560px (1683). |
| **Wrapping instead of fixed rows** | `.title-row` (127-135), `.header-controls` (144-153), `.filters` (219-224), `.q-card-top` (308-314), `.detail-meta` (416-421), `.option` (470-489), `.cert-card-actions` (1410-1414), `.cert-verify-form` (1458-1462), `.storage-consent-actions` (1891-1896). |
| **Overflow-safe alignment** | `.exam-modal { align-items: safe center }` (899-918); `#app-menu { align-items: safe flex-start }` (928-930). |
| **Horizontal-overflow backstop** | `html, body { overflow-x: hidden }` + `body { max-width: 100vw }` (76-87). |
| **Viewport-relative inner scroll caps** | `max-height: 40-60vh` on the scrollable lists inside dialogs: `#app-menu-list` 60vh (752), `#primer-reader-body`/`#course-reader-body` 50vh (1046), `#primers-list`/`#course-list` 55vh (1074), `.course-media-img` 46vh (1188), `#profile-list` 45vh (1282), `#certificates-list` 55vh (1323), `#sign-reference-list` 60vh (1509), `.kd-terminal-log` 40vh (1782). |
| **Logical properties for RTL** | `margin-inline-start` (362, 1634), `padding-inline-start` (189, 1608), `inset-inline-start` (1614). |

This is not an accident. The file records the project's position explicitly. The 2026-09-02 comment on `.header-controls > .module-switch-btn` (680-687) rejects a breakpoint by name: *"no fixed px breakpoint (a hardcoded number like 480px is wrong for whatever the window/device actually is; this reacts to the real available space via flex-wrap instead of guessing a screen width)"*. The 2026-09-02 comment on `.filters` (212-218) rejects the horizontal chip strip on a phone because *"nothing is ever reachable only by a horizontal gesture"*. The history of layout bugs in this file - the 2026-08-11 header overflow and its 2026-09-02 regression (137-143, and the matching comment in `app.html`), the 2026-08-13 "first module unpickable" bug (901-914), the 160px ellipsis on the offline-prep row (810-819) - were all *unwrapped rows* or *centering traps*, i.e. intrinsic-layout mistakes. None of them would have been prevented by a breakpoint; each was fixed by making the component react to its actual available space.

Several rules that look like problems on first read are deliberate fixes and must be preserved by anything this ADR proposes: `align-items: safe center` on `.exam-modal` (a long module list was pushing its first item permanently above `scrollTop = 0`); `align-items: safe flex-start` on `#app-menu` (a short menu centred in a tall phone screen "reads as floating"); the `[hidden]` overrides on `.role-filters`, `.image-note`, `.exam-modal`, `.exam-view`, `.storage-consent-notice`; the `overflow-x: hidden` backstop; and the `.filters` wrap.

### Measured defects (Playwright, Chromium, iPhone SE 375x667 and iPhone 14 390x844, against the real app served from `app/`)

Rig: `tmp/layout_audit.mjs` (serves `app/` on :8801, walks consent -> module picker -> class picker -> list -> detail at both viewports, records tap-target sizes, horizontal overflow, and modal dead space; screenshots in `tmp/shots/`).

1. **Undersized tap targets in the header.** The "Change exam" control measured **343x30** and the "Exam" button **61x31**, against the project's own 44px floor and Apple's 44pt guidance. The responsible rules:
   - `.module-switch-btn` (665-678): `padding: 7px 10px; font-size: 0.78rem;` and **no `min-height`**. 12.5px text + 14px padding + 2px border = ~30px. The header instance is stretched to full width by `.header-controls > .module-switch-btn { flex: 1 1 100% }` (688-696), which is why it is 343px wide but still 30px tall. The same base rule serves the `#app-menu-list` rows, but those are re-padded to `12px 14px` / `0.9rem` by 757-771 and so land at ~44px - only the header instance is short.
   - `.exam-start-btn` (643-658): `padding: 7px 12px; font-size: 0.82rem;` and **no `min-height`** -> ~31px.
   - Sharing the same shape but not on the screens the rig visited: `.review-btn` (703-713, `7px 10px`, now only rendered inside `#app-menu-list` where 757-771 re-pads it); `.review-know-btn`/`.review-dontknow-btn` (846-854, `10px 14px` at 0.88rem -> ~40px); `.storage-consent-btn` (1898-1907, `10px 14px` at 0.88rem -> ~38px); `.course-media-navbtn` (1243-1253, `min-width: 40px`, `padding: 4px 12px` at 1.2rem -> ~33px tall); `.reveal-btn` (591-602) is ~45px only because of its 0.95rem text, with no floor declared. The `.cert-*` action buttons all carry class `back-btn` (see `renderVerifyLinkRow()`, `renderJwtDownloadBtn()` in `app.js`), so their overrides at 1416-1421, 1431-1435, 1475-1479 and 1494-1498 change padding/font but keep the 44px floor from 402.
2. **Vertical dead space on the class picker.** At 375x667 the class step of `#module-picker` (`.exam-modal-card` with "Class B (car)" / "Class BE (car with trailer)" / "Back") is ~240 CSS px tall and sits centred, leaving roughly 215px of empty background above and below (`tmp/shots/se-03-class-picker.png`). The module-intro carousel that follows (`#module-intro`, `se-04-list.png`) looks the same. This is the `.exam-modal { align-items: safe center }` rule doing exactly what it says; `#app-menu` already received the targeted `safe flex-start` fix for the same visual complaint.
3. **No horizontal overflow** at either width on any of the five screens walked (`document.documentElement.scrollWidth === innerWidth`, no element with `right > innerWidth`). The 2026-09-02 header fix holds. This ADR does not propose any overflow work.
4. **Topic filter chips consume a large share of the first screen.** `renderFilters()` (`app.js` 7044) renders "All" + one chip per topic + the DN-14 "starred only" chip into `.filters`. For `fuehrerschein` that is 13 chips (11 topics in `TOPIC_LABELS.fuehrerschein`); `sportboot_*` 11, `it_sicherheit` 10, `cka` 9, most compliance modules 7. Chips are `min-height: 44px` with `gap: 8px` (52px per row) and `white-space: nowrap`, and English labels such as "Right of way & intersections" are ~200px wide, so on a 343px content width the driving-licence row set wraps to an estimated 6-7 rows, i.e. roughly 300-360px of chips under a ~110px sticky header, before the first `.q-card` is reachable on a 667px-tall screen. (Row counts here are derived from the chip sizes and label lengths, not measured by the rig, which did not walk the list screen with a topic count assertion. Add that assertion - see Implementation Notes §5.)

### What is *not* known yet

Every number above comes from Chromium. WebKit has not been measured. Safari differs in exactly the areas this stylesheet leans on: the eight `max-height: NNvh` caps (Safari's `vh` is the *large* viewport, so a `60vh` list can be taller than the space actually visible while the URL bar is showing); form-control styling (`.lang-select` is a native `<select>` with `appearance` left at default); momentum scrolling and rubber-banding on the `position: fixed; overflow-y: auto` overlays (`.detail`, `.exam-modal`, `.exam-view`); and the `env(safe-area-inset-*)` values, which are only non-zero on real notched hardware or a simulator.

## Decision Drivers

1. **Single-column app.** Every screen is a vertical stack: header, chip row, card list; or a fixed overlay holding one centred card of `max-width` 420-640px. Nothing re-flows into columns on a wide screen; the layout *scales*, it does not *change*. A layout strategy should match that.
2. **The defects are component-sizing defects, not width-dependent ones.** A 30px header button is 30px at 375px and at 1440px. A breakpoint cannot fix it; a `min-height` can, once, for every width.
3. **Track record.** The codebase reached a phone-clean state (no overflow at 375px, insets, wrapping) without a single media query, and its layout bugs were all intrinsic-layout mistakes. The cheapest way to keep future agents from reintroducing them is a small, explicit rule set they can check a diff against - not a second dimension (breakpoints) that doubles the states to verify.
4. **Agent-maintained CSS.** Most edits to this file are made by AI agents in short sessions. Rules must be greppable and local: "every interactive base rule declares `min-height: var(--tap-min)`" is checkable; "remember the 480px block" is not.
5. **Accessibility floor vs. project bar.** WCAG 2.2 SC 2.5.8 *Target Size (Minimum)* (Level AA) requires 24x24 CSS px, with exceptions for spacing, inline text and essential cases; SC 2.5.5 *Target Size (Enhanced)* (Level AAA) is 44x44. The 30/31px header controls pass 2.5.8 and fail only the AAA criterion and Apple's Human Interface Guidelines. Nothing here is a legal-conformance failure at AA; the 44px bar is the project's own, set by the `min-height: 44px` already on `.filters button`, `.back-btn`, `.lang-select`, `.star-btn` and the 44x44 `.theme-toggle`, and it should be applied consistently or consciously lowered - not left to the accident of font size.
6. **Compatibility posture.** The file already avoids `:has()` "so an older engine without :has() support still gets a sized frame" (1127-1129). Whatever is adopted must degrade gracefully on a two-to-three-year-old iOS.
7. **Theming is settled.** Light/dark is done with custom properties on `[data-theme]` (1-61); no `prefers-color-scheme` query is used and this ADR does not touch that. The only theming/layout interaction worth noting is that any `@media` block added for capability queries must not carry colour declarations, so the token system stays the single source of colour.
8. **Testability.** `tmp/layout_audit.mjs` already measures the three things that matter (target size, overflow, dead space). The strategy should be the kind that a script can assert on.

## Considered Options

### Option 1 - Stay breakpoint-free; fix with fluid and intrinsic techniques

**What it is.** Keep zero width-based `@media` rules as a *policy*, not an accident. Fix sizing with floors (`min-height`), viewport- and container-relative maths (`clamp()`, `min()`, `max()`, `dvh`), `flex-wrap` and `safe` alignment. Codify the rule at the top of `styles.css`.

**Strengths.** Matches Drivers 1-4 exactly; one state to test instead of N; the file's own comments already argue for it; every measured defect is fixable this way with a handful of lines; no new syntax the agents have not already used in this file. Also the *only* option in which the 2026-09-02 "no fixed px breakpoint" comment remains true.

**Weaknesses.** Some things are genuinely hard without a query: there is no fluid way to say "on a touch device, don't paint hover states" or "respect reduced motion" - those are *capability* questions, not width questions. A pure "no `@media` at all" rule would forbid the right tool for those. Fluid maths can also be written badly (`clamp()` with `vw` in the middle produces text that resizes with the window but not with the user's zoom - an accessibility regression (WCAG 1.4.4) if used on font sizes); the policy needs a short do/don't list.

**Cost.** Lowest. ~40 lines of CSS for the fixes below plus a comment block.

### Option 2 - Introduce a small number of conventional width breakpoints

**What it is.** The usual `@media (max-width: 480px)` / `(min-width: 768px)` blocks: compact header on phones, roomier spacing on tablets, maybe a two-column card grid on desktop.

**Strengths.** Universally understood; would give a place to put phone-specific tweaks (e.g. hide the "Change exam" label behind an icon under 400px). Could enable a desktop two-column list some day.

**Weaknesses.** Solves problems the app does not have (Driver 1) and does not solve the ones it has (Driver 2). Doubles the manual test matrix and, worse, the *agent* test matrix: a future edit must now be right in two or three width bands, and this file's history shows that even one band has regressed twice. Any breakpoint number contradicts the on-record reasoning at 680-687. A breakpoint keyed on `max-width: 480px` also misclassifies a phone in landscape (844px wide, 390px tall) as "desktop" - which is where the vertical-space problems actually bite. Split-screen iPad and desktop windows narrower than a phone exist too; width is a poor proxy for "is this a phone".

**Cost.** Low to write, ongoing to maintain; each breakpoint is a new place for the next regression to hide.

### Option 3 - CSS container queries

**What it is.** `container-type: inline-size` on the wrappers (`main`, `.exam-modal-card`, `.cert-card`) and `@container (max-width: NNNpx)` rules on the components inside them, plus `cqi` units.

**Strengths.** Asks the right question - "how much room does *this component* have" - which is what `flex-wrap` already approximates. Would be the principled tool if the same component (e.g. `.cert-card-actions`, `.profile-row`) appeared inside cards of different widths (420-640px here) and needed different arrangements. Composes with Option 1 rather than replacing it.

**Weaknesses.** Today no component needs a different *arrangement* by container width - only wrapping, which flex already does. Container size queries shipped in Safari 16 (2022); acceptable for this PWA's audience, but the file's stated posture (Driver 6) is to avoid features that leave older engines with a broken layout, and a container query that fails silently is exactly that. `container-type: inline-size` also creates a size-containment context, which interacts with the `.exam-modal-card` centring/overflow behaviour that took two dated fixes to get right - a real risk for zero present benefit.

**Cost.** Low per use, but every use needs a WebKit check that the project cannot run yet (see "the iOS gap").

### Option 4 - Hybrid: fluid by default; `@media` reserved for capability and preference queries; container queries allowed when a component actually needs them

**What it is.** Option 1 as the rule for *width*, plus an explicit allow-list of non-width media features: `(hover: hover)` / `(pointer: coarse)`, `(prefers-reduced-motion: reduce)`, `(display-mode: standalone)`, `(orientation: ...)` only if a real case appears. Option 3 stays available, case by case, with a WebKit check as the entry ticket.

**Strengths.** Keeps everything Option 1 buys, and fixes its one honest weakness by naming the queries that are *not* about width. Keeps the door open for Option 3 without adopting it speculatively.

**Weaknesses.** Slightly more to explain than "no media queries". The allow-list must be kept short or it becomes Option 2 by the back door (`(pointer: coarse)` is very tempting as a phone proxy; it must not be used to change layout, only to change interaction feedback).

**Cost.** Same as Option 1 plus a one-paragraph rule.

### Summary

| | fixes the 30px buttons | fixes the dead space | addresses the chip rows | adds test states | matches on-record reasoning | WebKit risk |
|---|---|---|---|---|---|---|
| 1 fluid only | yes | yes | partly (needs JS for the rest) | none | yes | low |
| 2 breakpoints | no (needs a floor anyway) | could, per band | could hide chips per band | +2-3 bands | contradicts 680-687 | low-medium |
| 3 container queries | no (needs a floor anyway) | no | no | +1 per query | neutral | medium |
| 4 hybrid | yes | yes | partly (as 1) | none for width; capability queries are additive | yes | low |

## Decision

**Adopt Option 4: the app commits to a fluid, breakpoint-free layout as its strategy. Width-based `@media` rules are not permitted. `@media` is reserved for capability and user-preference features. Container queries may be introduced per component when one genuinely needs a different arrangement by container width, and only with a WebKit check.** The measured defects are fixed with floors and alignment changes inside that strategy, without undoing any of the dated fixes listed in Context.

Reasoning:

- The app is one column that scales. Breakpoints would add a second axis to test and maintain in a file whose regressions have all been single-axis mistakes. The file's own 2026-09-02 comment already made this call for one component; this ADR generalises it.
- Every measured defect is fixable once, for every width, with `min-height`, `safe` alignment and (for the chips) a small interaction change - none of them needs to know the screen width.
- The one thing a "no `@media`" rule would wrongly forbid is capability queries; naming them is cheaper than losing them.
- Container queries are not rejected, they are simply not needed yet; adopting them speculatively would add WebKit-untested behaviour to the overlay stack that carries two hard-won fixes.

### The three specific calls

**Tap targets.** Introduce a single token `--tap-min: 44px` and declare `min-height: var(--tap-min)` on every interactive base rule that lacks it, keeping the deliberate 40px `.role-filters button` exception and its comment. This is a project-bar decision (Driver 5), not a WCAG-AA one; the ADR states that openly so nobody later claims the 30px buttons were a conformance failure.

**Dead space.** Do **not** generalise `safe flex-start` to every `.exam-modal`. The correct split is by *what the dialog is*: a **decision** (class step, `#exam-picker`, `#practice-picker`, `#module-intro` wizard) stays centred - that is the conventional alert/sheet position, and centred-with-`safe` is the fix from 2026-08-13 that must survive; a **screen** (a list or reader whose body is capped at 45-60vh and scrolls) gets the `#app-menu` treatment, `align-items: safe flex-start`, because anchoring at the top is what a screen does and gives its inner list the room it is currently wasting above the card. `#module-picker` keeps `safe center`: its module-list step already start-aligns via the `safe` fallback when the list overflows, and its class step is a decision. The remaining dead space on a two-button decision is accepted; an optional upward bias for tall phones is offered in Implementation Notes §3 but is not required.

**Filter chips.** The wrap is an acceptable trade-off *as a layout* - it is the accessible one, and the 2026-09-02 comment rejecting the horizontal strip is upheld. What is not acceptable long-term is 6-7 rows of chips before content on the module with the most users. The decision is to keep the wrapped chip row as the *expanded* state and add a collapsed state that shows only the active chip plus a "Topics (n)" toggle (details in §4). This is an `app.js` change and is recorded here as the agreed direction, not implemented by this ADR. Rejected: the horizontal strip (on record, and hides content behind a gesture with no affordance); priority-plus (needs JS measurement with `ResizeObserver` and reorders chips on every resize - complexity out of proportion); a native `<select>` (has precedent in `.lang-select`, 168-181, and is the lowest-effort fallback, but loses the at-a-glance topic overview and the `aria-pressed` chip semantics, and would still need the "starred" chip outside it).

## Consequences

### Positive

- One layout state to design, review and test. The Playwright rig asserts the same invariants at every viewport it is given.
- A greppable rule set (§1) that an agent can check a diff against in seconds: no `@media (max-width|min-width)`, every `<button>`/`[role=button]` base rule has `min-height: var(--tap-min)`, every `.exam-modal` alignment is `safe`, no `vw` inside a font-size `clamp()`.
- The header controls, review buttons, consent buttons and slideshow arrows all reach the project's 44px bar with ~10 lines of CSS, at every width, with no new states.
- The dead-space split (decision vs. screen) is principled and reuses a fix that already exists in the file; nothing that was fixed on 2026-08-13 or 2026-09-02 is undone.
- No new syntax beyond what the file already uses (`calc`, `env`, `min-height`, `safe`) except `dvh`, which is introduced with a `vh` fallback line so older engines are unaffected.

### Negative

- Some layouts are simply not expressible without a width query (a two-column card grid on desktop, an icon-only header on very narrow phones). The decision forgoes them. If a genuine case appears, this ADR is superseded, not quietly violated.
- Header height grows by ~14px once "Change exam" and "Exam" hit 44px; on a 667px screen that is 2% of the viewport. Accepted - the alternative (an icon-only header under 400px) is exactly the breakpoint this ADR rejects.
- The chip-collapse change lives in `app.js` and adds one tap to switch topic when collapsed. Learners who change topic often will notice. Mitigation: persist the expanded/collapsed choice per profile like the topic filter already is (`filter-<module>` key, `app.js` 7058).
- `dvh` support starts at iOS 15.4 / Safari 15.4 (2022). Older engines fall back to the `vh` line that precedes it and keep today's behaviour.
- The strategy relies on the audit script being run. Until CI exists it is a pre-deploy discipline, the same gap ADR-0001 already names for the exam suite.
- Nothing in this ADR has been verified on WebKit. The "iOS gap" section lists what must be checked before the `dvh` and dead-space changes are considered done.

## The iOS gap - what must be checked on WebKit, not assumed

All measurements are Chromium. The following are the WebKit-specific behaviours this stylesheet depends on and that the audit cannot see:

1. **Viewport units and the URL bar.** Safari's plain `vh` resolves against the *large* viewport (URL bar collapsed). While the bar is visible, `60vh` on `#app-menu-list` (752) or `#sign-reference-list` (1509) is taller than the space actually on screen, so the inner list can run under the bottom edge of the card. `svh` is the small viewport (bar shown), `lvh` the large, `dvh` the current one and changes as the bar animates - `dvh` is the right unit for "cap this list to what is visible now", with the caveat that a `dvh`-sized element resizes while the bar animates (acceptable for a `max-height`, not for something that would cause layout jumps on the main page). `-webkit-fill-available` is the pre-`dvh` workaround and is not needed once `dvh` is used with a `vh` fallback. **Check:** open each 40-60vh dialog on iPhone Safari with the URL bar visible and scroll the inner list to its end; the last item and the "Back" button must both be reachable.
2. **`100vh`-style overlays.** `.detail`, `.exam-modal`, `.exam-view` use `position: fixed; inset: 0`, which sizes to the *visual* viewport in Safari and is the correct choice (not `height: 100vh`). **Check:** exam view at the last question - `#exam-next-btn` reachable with the keyboard closed, and again after a text-input has raised the keyboard (kubectl drill, profile-add input).
3. **Momentum scrolling and rubber-banding.** Nested scrollers (`.exam-modal` scrolls; `#app-menu-list` scrolls inside it) can trap or chain scroll on iOS. **Check:** scroll to the end of `#sign-reference-list` and keep scrolling; the outer modal should not rubber-band the whole card off-screen, and a fling should not scroll the page behind the dialog (the dialogs are `aria-modal` but the body is not `overflow: hidden` while one is open - verify whether background scroll bleeds through on iOS).
4. **Form controls.** `.lang-select` (198-210) is a native `<select>` with default `appearance`; Safari renders it with its own chevron and padding, and iOS ignores `font-size` below 16px for zoom-on-focus purposes (a `<select>` at 0.85rem = 13.6px triggers the auto-zoom on focus on some iOS versions). **Check:** tapping the language picker must not zoom the page; if it does, the fix is `font-size: 1rem` on `.lang-select`, not a `maximum-scale` meta (which breaks pinch-zoom accessibility).
5. **Safe-area insets.** `env(safe-area-inset-*)` is 0 in every desktop browser and in Chromium emulation. **Check:** on an iPhone with a notch/Dynamic Island, in Safari and as an installed PWA (`display-mode: standalone`, where the status bar overlaps content), the header's first row and the "Back" buttons at the bottom of `.detail-body` must clear the insets. This is the one place `@media (display-mode: standalone)` may legitimately be needed (Option 4's allow-list).
6. **Focus ring and `:active`.** The `:focus-visible` ring (71-74) and the `.option:active` feedback (503-505) were explicitly written because Safari could not be checked at the time (65-70, 498-502). **Check:** tap an option row and confirm the `:active` background shift is visible; tab through with an external keyboard and confirm the 3px ring.
7. **RTL.** `ar` flips direction; the logical properties at 189, 362, 1608, 1614, 1634 handle it, but `.header-controls { justify-content: flex-end }` (149) and `text-align: left` on `.exam-mode-btn` (956) and the menu rows (751, 767) are *physical*. **Check** the header and menu in Arabic; convert `left` to `start` if they mirror wrongly (this is a text-direction issue, not a width issue, so it belongs to this strategy's "intrinsic" rule set).

How to run these: the project owner wants iOS Simulator verification. The cheapest path that does not add a second automation stack (ADR-0001, Option 4 discussion) is Playwright's WebKit build - `npx playwright install webkit` and a second `project` in the config with `...devices["iPhone 14"]` - which runs the *same* `layout_audit.mjs` assertions on the WebKit engine and catches items 1, 3 (partly) and 4. It is not Safari: it has no URL bar, no real insets, no standalone mode, and no iOS keyboard. Items 2, 5 and the standalone half of 3 need Xcode's Simulator with Safari (free, macOS only) or a real device, checked by hand against the list above, once per change to the overlay/alignment rules. Record the result in the change's card; there is no way to script it today.

## Implementation Notes

Nothing below has been applied; this ADR is the only file this round touched. Line numbers refer to `app/styles.css` as of 2026-09-05.

### §1. Codify the rule (top of `styles.css`, after `:root`)

Add a comment block stating the strategy so future agents see it before the first rule:

```css
/* LAYOUT STRATEGY (ADR-0003, 2026-09-05): this stylesheet is fluid and
   breakpoint-free on purpose. Rules:
   - No width-based @media ((min|max)-width). React to available space with
     flex-wrap, min()/max()/clamp(), max-width caps and `safe` alignment.
   - @media is allowed only for capability/preference features:
     (hover: hover), (pointer: coarse), (prefers-reduced-motion: reduce),
     (display-mode: standalone). Never put colour in those blocks - colour
     stays in the [data-theme] tokens above.
   - Every interactive base rule declares min-height: var(--tap-min). The
     only sanctioned smaller control is .role-filters button (40px), and
     it says why.
   - Never put vw/vh inside a font-size clamp() (breaks browser zoom, WCAG 1.4.4).
   - .exam-modal alignment is always `safe ...` (see the 2026-08-13 note).
   - Verify with tmp/layout_audit.mjs (soon scripts/) before deploying. */
```

and the token, in `:root` (after line 27):

```css
  --tap-min: 44px;
```

### §2. Tap targets (the measured 30/31px controls plus the same-shape rules)

Add `min-height: var(--tap-min);` to:

| rule | lines | note |
|---|---|---|
| `.exam-start-btn` | 643-658 | the 61x31 "Exam" button |
| `.module-switch-btn` | 665-678 | the 343x30 "Change exam" button; also raises the inner button of `#app-menu-list > .offline-prep-wrap > .module-switch-btn` (806-824, `padding: 0`) to 44px - check that row still reads as one item; if not, reset `min-height: 0` there with a comment |
| `.review-btn` | 703-713 | consistency; currently only rendered inside the menu where 757-771 already re-pads it |
| `.review-know-btn, .review-dontknow-btn` | 846-854 | ~40px today |
| `.reveal-btn` | 591-602 | ~45px today by accident of font size; make it explicit |
| `.storage-consent-btn` | 1898-1907 | ~38px today; the consent dialog is the first thing a new visitor taps |
| `.course-media-navbtn` | 1243-1253 | ~33px tall; also change `min-width: 40px` to `min-width: var(--tap-min)` |
| `.exam-mode-btn` | 953-978 | already ~46px via padding + 1.35 line-height; declare it so a future font-size change cannot drop it |

Leave `.role-filters button` at `min-height: 40px` (255-259) - its comment explains the deliberate secondary weight, and 40px clears 2.5.8 with room. Do not touch `.badge` (316-322): badges are not interactive.

Optionally, in the same pass, replace the literal `44px` at 100-101, 202, 231, 402, 579 with `var(--tap-min)` so the bar is set in one place. Pure refactor, no visual change.

### §3. Dead space - decision vs. screen dialogs

Extend the existing `#app-menu` rule (928-930) to the *screen* dialogs and leave the decision dialogs on the base `.exam-modal { align-items: safe center }` (915):

```css
/* ADR-0003: top-anchor the "screen" dialogs (a scrolling list or reader
   inside the card) the same way #app-menu already is - they read as a
   page, not as an alert, and a centred card wastes the space its capped
   inner list needs. Decision dialogs (#module-picker's class step,
   #exam-picker, #practice-picker, #module-intro) deliberately stay on the
   base `safe center`. Keep `safe` - see the 2026-08-13 note above. */
#app-menu,
#certificates-view,
#profile-view,
#sign-reference-view,
#primers-view,
#primer-reader,
#course-view,
#course-reader,
#kubectl-drill-view {
  align-items: safe flex-start;
}
```

`#module-picker` is intentionally absent: its module-list step already start-aligns through the `safe` fallback once the list overflows, and its class step is a decision.

For the inner list caps, add a `dvh` line after each existing `vh` line so Safari sizes them to the visible viewport (the `vh` line stays as the fallback for engines without `dvh`):

```css
#app-menu-list          { max-height: 60vh; max-height: 60dvh; }   /* 752 */
#primer-reader-body,
#course-reader-body     { max-height: 50vh; max-height: 50dvh; }   /* 1046 */
#primers-list, #course-list { max-height: 55vh; max-height: 55dvh; } /* 1074 */
.course-media-img       { max-height: 46vh; max-height: 46dvh; }   /* 1188 */
#profile-list           { max-height: 45vh; max-height: 45dvh; }   /* 1282 */
#certificates-list      { max-height: 55vh; max-height: 55dvh; }   /* 1323 */
#sign-reference-list    { max-height: 60vh; max-height: 60dvh; }   /* 1509 */
.kd-terminal-log        { max-height: 40vh; max-height: 40dvh; }   /* 1782 */
```

Optional, not required: if the ~215px above the two-button class step is still judged excessive on tall phones, bias decision dialogs upward *without* leaving `safe center` by giving the container more bottom than top padding, e.g. on `.exam-modal` (917) `padding: 20px 20px calc(20px + 10vh);`. The card then centres in the remaining space and sits ~5vh higher; on a long list the extra padding is only extra scroll room at the end. Try it on a device before adopting; it is a taste call, not a defect fix.

### §4. Filter chips (direction agreed; `app.js` change, separate card)

Keep `.filters` wrapping (219-224). In `renderFilters()` (`app.js` 7044-7085), add a collapsed state:

- Collapsed (default on first render): render the active topic chip (or "All"), the "starred" chip, and one toggle chip `Topics (11) ▾` with `aria-expanded="false"` and `aria-controls="filters"`. One row.
- Expanded: today's full chip set plus the same toggle with `aria-expanded="true"` and `▴`. Focus stays on the toggle; chips remain real `<button aria-pressed>` elements so screen-reader and keyboard behaviour is unchanged from today.
- Selecting a topic collapses the row again and moves focus to the selected chip, so the learner sees what they chose.
- Persist expanded/collapsed per profile next to the existing `filter-<module>` key.

CSS needed: none beyond an optional `.filters-toggle` styled exactly like `.filters button`. The `.role-filters` row (247-276) is unaffected; with only 4-5 role chips it never needs collapsing.

Accessibility cost, stated plainly: one extra activation to change topic when collapsed; the toggle must be a `<button>` with `aria-expanded`, not a `<details>` (whose summary semantics vary across screen readers). Benefit: on `fuehrerschein` at 375px the first card moves from an estimated ~450px down the page to ~170px.

### §5. Testing - promote the audit and connect it to ADR-0001

`tmp/layout_audit.mjs` (66 lines) already does the right things. Promote it, do not rewrite it:

1. Move it to `scripts/layout_audit.mjs`, switch the hard-coded `$HOME/mnt/Zettacard` paths to `process.cwd()`/`import.meta.dirname`, and add `"test:layout": "node scripts/layout_audit.mjs"` to `package.json` next to `test:storage-consent`. It brings its own static server on :8801, so it does not need `scripts/dev-serve.sh`.
2. Turn its report into assertions with a non-zero exit: no visible interactive element under `44x44` except an allow-list (`.role-filters button` at 40px; `.badge` is not interactive and already excluded by the selector); `documentElement.scrollWidth <= innerWidth + 1` on every screen; for *screen* dialogs, `card.top <= 40`; for decision dialogs no dead-space assertion. Add the list screen with a `.filters` row-count measurement (`Math.round((filters.scrollHeight + 8) / 52)`) and assert `<= 2` once §4 lands, `<= 8` until then so the number is at least tracked.
3. Add a third viewport, iPhone 14 **landscape** (844x390), because vertical space is the axis this app is short on and no width breakpoint would ever have looked at it.
4. When ADR-0001's `@playwright/test` runner lands, this script becomes `tests/e2e/layout.spec.mjs`, reusing its `openApp`/`pickModule` helpers and its `webServer`; the assertions above become `expect()`s and the audit gets sharding, retries and traces for free. Until then, run `npm run test:layout` before every deploy as part of the manual check `AGENTS.md` step 4 already asks for. This ADR does not change ADR-0001's decision; it adds one spec file and one `project` (`webkit`, `devices["iPhone 14"]`) to the config it proposes - the "WebKit/Firefox projects for RTL/iOS questions" ADR-0001 explicitly lists as an upgrade path.
5. Keep the by-hand iOS Simulator checklist in "The iOS gap" above as the acceptance test for any change to `.exam-modal`, `.detail`, `.exam-view`, the `vh`/`dvh` caps or the safe-area rules; note the device and iOS version in the card.

### §6. Capability queries permitted by this ADR (none required today)

Listed so the allow-list is concrete; add only when the case is real:

- `@media (hover: hover) { .q-card:hover { ... } }` - moving the hover background (304-306) and `.exam-mode-btn:hover` (980-983) under this query would stop a tapped card from staying "hovered" on touch devices. Low priority; `:active` feedback exists.
- `@media (prefers-reduced-motion: reduce)` - the only motion is two 0.12-0.15s colour transitions (92, 301) and the `scale(1.12)` play-button hover (1181). Not worth a block until there is real motion.
- `@media (display-mode: standalone)` - only if the installed-PWA status bar check (iOS gap, item 5) fails.

### §7. What this ADR deliberately does not do

- It does not change `app/styles.css`, `app/app.js` or `app/app.html`; every change above is a proposal for its own card.
- It does not touch theming, colour tokens or the `[data-theme]` mechanism.
- It does not invent overflow problems: none were measured, and the 2026-09-02 fix is confirmed holding.
- It does not claim WCAG-AA non-conformance for the 30px controls; they meet 2.5.8 and miss the project's own stricter 44px bar.

## Related

- `docs/adr/ADR-exam-e2e-testing.md` (ADR-0001) - the Playwright Test runner this ADR's layout spec plugs into; its Option 4 discussion is where real-Safari automation would be decided.
- `docs/adr/ADR-llm-translation-qa.md` - unrelated in content; noted for the numbering collision.
- `tmp/layout_audit.mjs`, `tmp/shots/se-*.png` - the measurement rig and screenshots behind the numbers in Context.
- `BACKLOG.md` DN-23 (safe-area insets and tap affordance), DN-24 (accessibility audit; focus ring), DN-44 (role filter row), DN-89/DN-90 (consent notice and its Playwright test).
- `app/styles.css` 137-143, 212-218, 680-687, 899-930 - the dated comments this ADR builds on and must not undo.
