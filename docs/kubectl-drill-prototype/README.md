# kubectl command-recall drill — frontend prototype

Scratch/research code for a later, sequential integration step. **Not wired into
`app/`.** Do not import these files from `app/app.js` — this directory exists so
the integration step can copy logic in, not so the prototype runs live.

Verified working with zero network requests by opening `index.html` directly
from disk (`file://…`) in Chromium via Playwright — see the smoke test in the
session transcript. The `fetch('drills.sample.json')` call is expected to fail
under `file://` in Chromium-based browsers (blocked by CORS for local files);
`app.js` catches that and falls back to `drills.fallback.js`, an inline copy of
the same data as a `window.KUBECTL_DRILLS_FALLBACK` object. That fallback is a
prototype-only workaround — the real integration fetches
`app/data/.../cka_kubectl_drills.json` the same way every other content type in
this app already does (via the service worker's runtime cache), so it won't
need this dance.

## Decision 1: xterm.js vendored vs. custom terminal-look component

**Recommendation: custom lightweight component. Do not add xterm.js.**

Evidence gathered (not assumed):

| | xterm.js (`@xterm/xterm`) |
|---|---|
| License | MIT — confirmed by reading `LICENSE` in `xtermjs/xterm.js` on GitHub directly |
| Latest version | 6.0.0 (npm registry, checked 2026-09-02) |
| Minified bundle | ~280 KB (Bundlephobia, `@xterm/xterm@5.5.0`) |
| Minified + gzip | ~65 KB (Bundlephobia, same version) |
| Plus | Its own `xterm.css`, and in practice most real usages also pull `addon-fit` (to size the terminal to its container) and `addon-web-links`, adding more weight for capability this drill doesn't use |
| "Headless" mode | `@xterm/headless` / `xterm-headless` exists, but it's a **Node.js server-side** package for tracking terminal state on a remote host (e.g. a PTY-over-websocket backend) — it explicitly does *not* include the DOM renderer, and it's meant to be paired *with* the full frontend `xterm` package for actual display, not a smaller drop-in for browser rendering. It doesn't change the calculus here: there is no "lite" browser-rendering build of xterm.js that sheds the ~65 KB gzip cost while still drawing to the DOM. |

What xterm.js actually buys: a full ANSI/VT100 terminal *emulator* — escape-code
parsing, cursor addressing, scrollback buffer, selection, a canvas/WebGL
renderer pipeline. All of that is built for streaming interactive shell
output (a real PTY). This drill's actual interaction is "learner types one
line, presses Enter, gets a few lines of static feedback text appended below."
There are no escape codes to interpret, no cursor movement to render, nothing
"live" streaming character-by-character. xterm.js would be ~65 KB of gzipped,
first-of-its-kind vendored dependency (this app currently has *zero* — see
`AGENTS.md` and the fact `app/app.html` loads only its own `app.js`) bought
almost entirely for capability this feature doesn't use.

The custom component built here (`app.js` + `style.css` in this folder) is
~200 lines total including the task-flow state machine, not just the visual
shell, achieves the same *look* (dark panel, traffic-light dots, monospace
prompt, blinking native caret), and has zero new dependencies — trivially
offline, trivially auditable, matches this repo's existing style (`app/app.js`
is one plain global-scope script, no modules, no bundler).

**Honest tradeoff:** if a future drill needed real ANSI coloring, multi-line
piped output, or genuinely interactive shell behavior (tab-completion,
Ctrl-C, arrow-key history editing a multi-line buffer), xterm.js would earn
its weight at that point. For "type one line, get matched," it doesn't.

## Decision 2: matching engine design (`matcher.js`)

Pure, DOM-free, dependency-free functions attached to
`window.KubectlDrillMatcher`, written so they can be pasted into `app/app.js`
close to verbatim. No ES modules (matches `app/app.js`'s existing plain-script
style).

### Tokenizer

`tokenizeCommand(raw)` — whitespace-splits the learner's raw input, respecting
single- and double-quoted spans (`'foo=bar baz'` stays one token), via a
regex (`"([^"]*)"|'([^']*)'|(\S+)`).

`expandTokens(tokens)` — post-processes the token list two ways:
1. Splits `--flag=value` into two tokens (`--flag`, `value`) so `--namespace=x`
   and `--namespace x` compare equal downstream without the grammar author
   needing to spell out both forms for every flag.
2. Folds a bare leading `k` (the extremely common shell alias for `kubectl`)
   into `kubectl`, but **only** as token index 0, so a resource actually named
   `k` elsewhere in a command is untouched.

### Grammar shape (matches the sample-task shape given in the task brief)

```
accepted_grammar: {
  base_command:       [string, ...]     // ordered verb/noun path, e.g. ["kubectl","get","pods"]
  required_tokens:    [string, ...]     // each MUST appear somewhere, order-independent
  alternative_groups: [[string,...],...]// per group, AT LEAST ONE member must appear
  optional_tokens:    [string, ...]     // documentation only, never scored
}
```

A **"unit"** (an entry in `required_tokens` or an `alternative_groups` member)
is itself a string that may contain multiple words, e.g. `"-n kube-system"`.
This is deliberate: for a lot of kubectl drills the *value* of a flag matters
just as much as the flag itself (the specific namespace, the specific replica
count), so treating `-n kube-system` as one required "unit" — rather than
requiring `-n` and `kube-system` as two independently-satisfiable tokens — is
what stops a learner passing by typing `-n some-other-namespace` and having it
count as correct just because `-n` and the string `kube-system` both showed up
somewhere in the command by coincidence.

### Matching rules

- **`unitPresent(expandedHaystack, unitString)`** — tokenizes the unit string
  the same way as the input, then checks it appears as a **contiguous**,
  case-insensitive run inside the learner's expanded token array, at any
  position. Contiguous because a flag and its value have to actually be
  adjacent to mean anything; position-independent because kubectl doesn't
  care where in the command a flag lands.

- **`baseCommandPresent(expandedHaystack, baseTokens)`** — the verb/noun path
  (`kubectl`, `get`, `pods`, …) must appear **in order** but **not
  necessarily contiguously**, because real kubectl allows global flags to
  land between them (`kubectl -n kube-system get pods` is exactly as valid as
  `kubectl get pods -n kube-system`). Implemented as a simple forward scan:
  for each base token, find the next occurrence at or after the current
  search cursor, advance the cursor past it, fail if any token isn't found.

- **`required_tokens`** — each must independently satisfy `unitPresent`.

- **`alternative_groups`** — each group must have at least one member satisfy
  `unitPresent`. This is how flag synonyms are modeled (`-n`/`--namespace`,
  `-f`/`--follow`, `-c app`/`--container app`/`--container=app`) — the
  content author lists every acceptable phrasing as one group, the matcher
  doesn't need to know anything about kubectl's actual flag grammar.

- **`optional_tokens`** — never checked at all. Purely documentation for the
  content author (and future hint-writing) to note "these are also fine to
  include," e.g. `-o wide`, `--tail=50`. A learner who includes them or
  doesn't is treated identically.

- **Success** = `baseOk && required_tokens all present && every alt group has
  a satisfied member`. No penalty for *extra* unrecognized tokens — a learner
  who adds `--dry-run=client` on task 1 still passes, matching real kubectl's
  tolerance for additional flags that don't change the queried outcome. (If a
  future drill needs to *forbid* certain flags — e.g. penalizing `--force` on
  a delete drill meant to teach graceful termination — that would need a new
  `forbidden_tokens` grammar field; not implemented here since none of the
  sample tasks needed it, but the shape would slot in next to
  `required_tokens` easily.)

- **`score`** (0..1) — a rough "how close" fraction (base + required +
  alt-groups satisfied, over total), computed but **never shown to the
  learner as a number** and never used to decide success/failure — only used
  by `app.js` to decide progressive-disclosure timing (see below). Kept in
  the result object in case the integration step wants a finer-grained hint
  ("you have the right resource but wrong namespace" vs. "wrong command
  entirely") later; the prototype doesn't currently branch hint text on it.

### Feedback / attempt flow (`app.js`)

Per active task: `attempts` counter, `solved` flag, `revealed` flag, all reset
on task change.

1. **Attempt 1 wrong** → generic nudge only ("Not quite — check the command
   and try again."). Deliberately withholds the authored hint on the very
   first miss so a learner isn't punished for a typo by an immediate spoiler.
2. **Attempt 2 wrong** → shows the task's authored `hint` (localized). This is
   a *conceptual* nudge the content author wrote (e.g. "you need a way to
   scope to one namespace"), not anything about *which specific token* the
   matcher found missing — the matcher's internal `requiredMissing` /
   `altGroupMissing` arrays are never surfaced to the UI at all, by design,
   so a determined learner can't reverse-engineer the grammar from error
   messages.
3. **Attempt 3+ wrong** → reveals `reference_command` verbatim plus a
   "try typing it yourself" follow-up line. Input stays enabled — the learner
   can keep practicing against the now-visible answer rather than being
   locked out.
4. **Correct at any point** → `success_message`, input disabled, "Next task"
   button appears and gets focus.

Thresholds are two named constants (`HINT_AFTER_ATTEMPTS = 2`,
`REVEAL_AFTER_ATTEMPTS = 3`) at the top of `app.js` — trivial to retune per
content-author feedback during integration.

## Files in this folder

- `index.html` — page shell, loads the four scripts below in order.
- `style.css` — terminal-look styling (dark panel, traffic-light dots,
  monospace log, blinking native input caret). Dark-only for the prototype;
  the real integration should route through this app's existing theme system
  rather than hardcoding colors again.
- `matcher.js` — the matching engine, DOM-free, designed to be lifted into
  `app/app.js` near-verbatim (see above).
- `app.js` — UI wiring: terminal log rendering, task/attempt state machine,
  en/de toggle. **This part is prototype-specific** and would be rewritten,
  not lifted, to fit `app/app.js`'s existing `UI_STRINGS`/12-locale pattern —
  see UX notes below.
- `drills.sample.json` — 5 hand-written fake tasks in the target shape, for
  prototyping only. Not the real content (a separate agent owns
  `data/cka_kubectl_drills.json`).
- `drills.fallback.js` — inline JS copy of the same 5 tasks, used only as a
  `fetch()` fallback under `file://`. Prototype-only workaround, see top of
  this file; drop entirely during integration.

## UX rough edges to flag for the integration step

- **Progressive-disclosure thresholds are a guess.** 1 free nudge / hint on
  attempt 2 / reveal on attempt 3 felt reasonable while testing but wasn't
  validated against real learners — worth a Student-Review pass once wired
  into the real app (per this repo's normal workflow).
- **Mobile/touch keyboard:** the input is a plain `<input type="text">` (not
  `contenteditable`), specifically because native `<input>` gets far more
  reliable mobile keyboard behavior — predictive text, autocomplete
  suppression via `autocomplete="off" autocapitalize="off" autocorrect="off"
  spellcheck="false"`, and correct `inputmode`. That said, kubectl commands
  are full of characters (`-`, `=`, `/`) that sit behind a symbol-keyboard
  layer on most mobile keyboards, and there's no on-screen help for that here
  — worth considering a row of tappable common-flag chips (`-n`, `-f`, `-o`,
  `--`) above the input for mobile, the way some code-editor mobile UIs do,
  rather than assuming a physical/desktop keyboard.
- **IME (ja/zh) concerns:** not stress-tested here. The known risk with a
  plain `<input>` + a `keydown` Enter handler is that IME composition also
  fires `Enter` to commit a composed candidate, which this prototype's
  `handleSubmit()` would currently treat as "submit the command" — for CJK
  learners typing kubectl commands (which are pure ASCII, so no compose step
  is actually needed for the *command itself*) this is unlikely to bite in
  practice, but the integration step should still guard the Enter handler
  with `event.isComposing` (or check `event.keyCode !== 229`) before treating
  Enter as submit, since this app explicitly supports `zh`/`ja` and other
  ASCII-only inputs in a CJK IME context are a known footgun. Not fixed in
  this prototype because none of the sample tasks exercise it, but flagged
  here explicitly so it isn't missed.
- **No forbidden/negative tokens.** As noted above, the grammar has no way to
  say "this flag specifically must NOT be present" (e.g. penalizing
  `--force --grace-period=0` on a drill meant to teach graceful pod
  termination). Not needed for the 5 sample tasks; likely needed eventually
  for safety-emphasis drills (this app's other modules — Führerschein,
  Arbeitssicherheit — lean heavily on "what NOT to do" content, so CKA drills
  may want the same shape).
- **Terminal window has no resize/scrollback-clearing affordance.** The log
  area just grows and auto-scrolls; fine for 5 short tasks, might want a
  "clear" control or per-task log reset visible to the learner (currently
  the log *does* clear between tasks via `resetTaskState()`, just not
  something the learner can trigger manually mid-task).
- **No `aria-live` region.** Feedback lines are appended via plain
  `textContent`, so a screen reader won't automatically announce new
  terminal output. Worth an `aria-live="polite"` on `#term-log` (or a
  separate visually-hidden live region mirroring the latest feedback line)
  during integration — this app otherwise seems to care about accessibility
  given the 12-locale/RTL support, so silent terminal output would be an
  inconsistency worth avoiding.
