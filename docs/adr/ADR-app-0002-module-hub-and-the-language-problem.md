# ADR-app-0002 — The module hub, the two languages, and what a badge means

**Status:** Accepted, 2026-09-06
**Repo:** `Zettacard` (app code)
**Related:** `ADR-app-0001` (presenting the content), `zettacard-kb/docs/adr/ADR-0001` (KB is content master), `ADR-0003` (verification is a label, not a wall), `data-rules.md` § 3b (module kinds), § 7 (locale tiers)

## Context

The app now carries **29 modules**. It was designed around one. Four failures follow
from that, and they were reported by the PO in a single sitting, which is a good
sign they are one failure wearing four hats.

**1. The module is invisible.** `#app-title` holds the prominent header slot and
reads "Zettacard — Lernkarten". The module the user is actually studying is a
single line inside `#module-switch-btn`: `Führerschein · Klasse B`. The app names
itself louder than it names your subject. PO: *"the module or the topic of a
training is kind of hidden to one line, we must structure the visual aspect
somehow."*

**2. "Prüfung" means four things.** In today's German UI it is the module
("Welche Prüfung lernst du?", "Prüfung wechseln"), the mode selector
("Prüfungsmodus"), the certificate-bearing run ("Prüfungssimulation"), and the
run that explicitly is not one ("Übungsprüfung"). A learner cannot form a mental
model from vocabulary that overloaded, and a translator cannot translate it.

**3. UI language and content language diverge, silently.** The interface exists
in 18 languages. The questions do not:

| Coverage | Modules |
|---|---|
| 18 | `fuehrerschein` |
| 15 | the compliance set (9 modules) |
| 12 | `angelschein` (+2 regional), `motorrad`, `lkw`, `fuehrerschein_bus` |
| 4 | `cka` (de, en, ja, zh) |
| 2 | `aevo`, `dora`, `nis2`, `fadp_ch`, both `sportboot_*`, and all four `compare` modules |

Today a Greek speaker selects Ελληνικά, opens Sportboot and reads English, with no
message and no marker. The app tells them a silent untruth about itself.

**4. The language picker is hidden, and that is a trap.** It sits inside
`#app-menu`, behind an unlabelled ☰. It was moved there on 2026-09-02 for a real
reason — at 390px the old `<select>` rendered ~195px off-screen and was
unreachable — but the cure is worse than the disease for the population this app
exists to serve. PO: *"the hamburger menu hides the language, if you end with an
RTL language it's hard to find back."* A user who lands in Persian by accident has
no route back except clearing site data.

## Decision

### 0. One manifest field carries the weight

Every module gains **`kind`** ∈ `licence` | `compliance` | `cert` | `compare`.

Twenty-nine one-word values, written once. Grouping in the picker, the label on
the exam run, whether a badge is issued and what it is called, and the chip on the
hub are all **derived from `kind`**. Nothing about a module's presentation is
hand-written 29 times. A proposal that needs a paragraph per module is the wrong
proposal.

`kind` is a presentation fact and lives in `modules_manifest.json`. It is
adjacent to but not the same as the KB's `module_kind` (`exam_prep`,
`compliance`, `fun_translation`, `ui_strings`), which is a **licensing and
authoring** fact. Keep them separate and let the exporter map one to the other; a
single field serving both would eventually be changed for one reason and break the
other.

### 1. A module hub, not a module intro

Landing on a module opens a **hub**. The distinction matters and is the reason
this ADR exists rather than a ticket:

> An **intro** explains the module. It is read once, and then costs a tap forever.
> A **hub** is where the user decides what to do next. It carries state and the
> primary action, so the tap is one they were going to make anyway.

Anki's deck overview is the reference. Nobody resents it, because it earns its
place with due counts and a start button.

Hub contents, top to bottom, at 390px:

1. Module name, large. Kind chip beneath — "Staatliche Prüfung · Klasse B",
   "Pflichtschulung", "Zum Vergleich".
2. **Primary button: "Weiterlernen"**, resuming the last topic and position.
   First run: "Lernen starten".
3. Progress: learned / total, due today, last simulation result.
4. Topics, with per-topic progress.
5. The runs, as buttons — never behind a mode selector.
6. Coverage notice, **only when the user's language is not fully covered**.
7. "Über dieses Modul", collapsed: scope, question count, source and licence line,
   what the badge is worth.

What does **not** go on the hub: the app's name, marketing copy, the licence text
above the fold, the question count as a headline.

Navigation: cold launch lands on the hub of the last-used module. Back from cards
lands on the hub; back from the hub lands on the picker. Routes
`#/` → `#/m/<id>` → `#/m/<id>/learn/<topic>` and `#/m/<id>/exam/<run>`. The
existing pushState overlay pattern already supports this — it gives Back a meaning
it does not currently have.

### 2. The picker: one list, grouped by `kind`

One list. The `compare` modules are **not** moved to a separate screen: that is a
second navigation to build and translate, and it hides them from exactly the
person they are for — someone who has finished Führerschein and is browsing.

- **Meine Module** — only when the profile has started something. One or two rows
  for almost everyone, and the real answer to a 29-row list.
- **Führerschein** — Klasse B, Motorrad, LKW, Bus. First: largest audience, and
  the migrant learner must find it without reading German.
- **Weitere staatliche Prüfungen** — Angelschein, Sportboot, Waffensachkunde,
  Amateurfunk.
- **Pflichtschulungen** — the compliance set.
- **Berufliche Zertifikate** — AEVO, CKA.
- **Andere Länder — zum Vergleich** — the four `compare` modules, last, visually
  muted, each row already carrying "kein Nachweis" so nobody opens one under a
  misapprehension.

**Variants collapse to one row.** Angelschein is one row with a Bayern / NRW /
allgemein selector on the hub; Amateurfunk one row with Klasse A / E. Three rows
beginning "Angelschein …" read as three different exams to someone who does not
read German well.

Each row: name, a one-line "what this is", question count, a language marker for
**the user's current language**, and progress if any. Pass rules are hub material,
not picker material.

### 3. The vocabulary

**First, the thing that is not a button.** The PO's framing, and it is the key to
the whole naming problem:

> *"Vorprüfung describes the fact that you are learning FOR the self-assessment.
> It's the training before the exam. Don't take Vorprüfung literally. We are a
> Lernplattform that prepares you for an official course or certificate… that's
> the whole point we got to Prüfungssimulator. You are doing the process of
> learning to achieve the Prüfung."*

**The Vorprüfung is the platform, not a screen in it.** Everything a user does
here is the training before the exam. That is what `Prüfungssimulator` names, and
it is why no single button should be called Vorprüfung. Earlier drafts of this ADR
kept trying to find the one screen that was "the Vorprüfung"; there isn't one.

| Concept | German (authoritative) | English |
|---|---|---|
| The thing you study | **Modul** | Module |
| A section within it | **Thema** | Topic |
| Flashcards — free browse, by topic, spaced | **Lernen** | Learn |
| Per-topic quiz, answer revealed as you go | **Übungsquiz** | Practice quiz |
| The exam-shaped run, clock optional | **Prüfungssimulation** | **Readiness check** |
| What a run yields | **Lernnachweis** | **Self-assessment** |

Six notes.

**On `Lernnachweis` / self-assessment.** These are not a translation pair, and
that is deliberate. `Nachweis` means evidence you can put in front of someone
else, and English splits that between "proof" (right force, wrong register) and
"record" (right register, too passive); "certificate of completion" overclaims
precisely the thing this product does not sell. The concept is also a German
institutional invention — the Berufsgenossenschaft model — so the difficulty is a
fact about the thing, not a gap in our English.

PO's resolution, and it is better than any of the candidates: **the concept is a
self-assessment, and `Lernnachweis` is the German way of naming it.** English and
the other 16 locales say self-assessment. That is literally what it is: a measure
derived from the user's own answers, verified by nobody. It carries no credential
smell in any language, while German keeps the institutional weight the German
market actually recognises.

**"Lernen" was the missing concept.** It is what users do ninety percent of the
time and it had no name, which is part of why "Prüfung" spread to cover
everything.

**There is one run, not two — and the code says so.** `startExam("training")` and
`startExam("simulation")` both call `drawExamQuestions()`. Same draw, same count,
same questions. They differ by exactly three things: a clock, skip-and-revisit,
and whether the result is kept. That is one activity with a difficulty dial, not
two activities. So:

- **One button** on the hub, one run, with a **"mit Zeitlimit"** toggle.
- **Every run is recorded**, and the record states the conditions it was taken
  under. An untimed run is marked as such. That is more honest than issuing
  nothing, and it removes the incentive to treat the untimed run as a way to
  practise unobserved.
- **"Prüfungsmodus" is deleted.** It was never a concept — only an artifact of
  putting two runs behind one door.

**`startPracticeQuiz()` is not an exam and must stop being filed as one.** It is
per-topic and reveals the answer as you go; mechanically it is a study tool. It
moves under **Lernen** on the hub as **Übungsquiz**, and the word "Prüfung"
disappears from it entirely — which is correct, because it is not one.

**`Prüfungssimulation` is the one place "Prüfung" is literally accurate**, so it
keeps the word. `compliance` modules label the same run **Abschlusstest**, because
that is what employers and their LMSs call it. Generic "Modul" is for menus and
settings; everywhere else the UI says the module's actual name — "Was möchtest du
lernen?", not "Welche Prüfung lernst du?".

**On `Readiness check`.** Like `Lernnachweis`, not a translation of the German.
`Prüfungssimulation` describes what the run *resembles*; `readiness check`
describes what it is *for* — you take it to find out whether you would pass. It
also travels into the other 16 locales better than "mock exam", which is chiefly
British, or "practice exam", which reads low-stakes when the point is that the
conditions are real.

### 4. What a badge is, and what it is not

This was nearly got wrong, so it is written down.

**Zettacard is a Prüfungssimulator. It is not an *amtlicher* one.** The standing
line — *"Zettacard ist kein amtlicher Prüfungssimulator. Original-Lerninhalte,
CC BY-NC-SA 4.0."* — puts the emphasis on the wrong word when read quickly. The
disclaimed word is **amtlich**. Simulating the exam is the point of the product;
an earlier draft of this ADR proposed minimising the simulation and was wrong.

**The badge is a self-assessment, not a certificate we sell.** It records that the
holder studied, sat a run, and reached the level passing requires. We provide study
material and, from the user's own answers, an assessment of where they stand. We do
not issue credentials, and the English word says so out loud.

**What the badge *means* is not the same in every module**, and that is not
sloppiness — it is the domain. PO: *"because not all are the same it's hard to
make hard calls here… for some, we are proving the Lernfortschritt."* The split
falls exactly on `kind`, which is why `kind` exists:

- **`licence`** — a real state exam exists elsewhere. The run is a **prediction**:
  would you pass it? The badge says *ready for it*, never that you hold it. The
  pass screen carries the "this is not the real exam" line and no credential
  framing.
- **`cert`** — as `licence`. An external exam exists; the badge attests readiness
  for it.
- **`compliance`** — **there is no official exam anywhere.** Nothing external to
  be ready *for*, so the run is not a prediction; its output **is** the record —
  proof of **Lernfortschritt**. That is not a gap in our product, it is a gap in
  the domain: the Berufsgenossenschaften invented exactly this pattern, and it is
  the market SoSafe and its competitors serve. A worker must be able to show they
  understood the training. Removing the run would remove the module's reason to
  exist.
- **`compare`** — **no badge.** No exam anywhere to be ready for, and nothing to
  attest. These modules keep Lernen and the run, because self-testing is how
  anyone learns, and completing one yields a deliberately playful outcome instead
  — the PO's framing: *"a fun meme or outcome. Think of 'I beat the Sword Master'
  in Monkey Island."* It must be visually and verbally incapable of being mistaken
  for a Lernnachweis: no seal, no signature, no download, no name on it. That is
  the whole design constraint.

### 5. Language: there are three, and one control

The user makes **one** language choice. Behind it sit three distinct things, and
conflating them is what produced the silent English fallback.

1. **UI language** — 18 locales, complete.
2. **Study language** — per module, 2 to 18, and about to become fractional per
   question.
3. **Exam language** — the languages the *real* exam may be sat in. For the
   driving theory exam that is 12 (`data-rules.md` § 7, `official_exam_language`).
   A Greek speaker studies in Greek and sits the real exam in German or English.

Consequences:

- A **Prüfungssimulation runs in a real exam language.** Where the chosen language
  is not one, the app says so and offers the alternatives: *"Die Prüfung gibt es
  nicht auf Griechisch. Simulation auf Deutsch oder Englisch?"* One manifest
  field, `examLanguages`, published for `licence` modules and null elsewhere.
- Study-language glosses (keeping `Vorfahrt` or `Zeichen 136` in German alongside
  the translation) are right in **Lernen** and wrong in the **simulation**, which
  should read as the real thing.

**Coverage is reported as a fraction, never as a module-level badge.** Partial
per-question translation is already in flight — Hebrew 236/531, Greek 118/531,
Portuguese 59/531 — so "18 Sprachen" would be true of the module and false of the
card on screen. Therefore:

- Picker rows and the hub show a fraction: "Ελληνικά: 118 von 531".
- Any card served in a fallback language carries a small per-card marker naming
  the language it is actually in.
- `build_modules.py` already computes per-locale counts and discards them. It
  writes them to the manifest instead.

### 6. The header

Once the hub exists, the persistent header stops having to be the whole app:

```
[‹]  Führerschein · Klasse B          [🌐] [☰]
      Vorfahrt · 12/40
```

- **Back chevron**, start-edge, mirrored in RTL. Goes up one level.
- **Module name**, ellipsised at the logical end, tapping it opens the hub. The
  subtitle carries topic and position — session state belongs to the screen, not
  the app.
- **Globe**, icon-only, the same footprint as ☰ (~44px, against
  `.lang-select-wrap`'s ~195px, which is what caused the 2026-09-02 overflow).
  Opens a sheet listing every language in **its own endonym**, built from
  `app/index.json`, with `dir` per row. Icon-only is not a style choice: a globe is
  script-independent, which is what makes it findable by someone who cannot read
  the current UI.
- **☰** — profile, About, privacy, storage. Nothing needed mid-session.

Leaving the header: the app's name (it belongs on the picker and About; mid-session
the brand is worth nothing to a learner), the exam-start button (starting an exam
from inside a study session is a mode break — it belongs on the hub), and the
module-switch button (the name is the button).

**During a Prüfungssimulation the header is replaced by an exam bar** — question
n/N, clock if the run is timed, Abbrechen. No globe: you cannot change language
mid-exam in the real one either. This also gives the run a visual seriousness that
Lernen and the Übungsquiz deliberately lack, which is how a user tells the two
apart without reading a label.

### 7. `RTL_LANGS` is deleted

`const RTL_LANGS = new Set(["ar", "fa"])` is a hard-coded set that had to have
`fa` added by hand on 2026-09-06, *after* Persian shipped rendering
left-to-right. Direction is a property of a language, it is already in
`index.json`, and every `document.documentElement.setAttribute("dir", …)` call
goes through one function reading the registry. The hard-coded pair survives only
as the fallback before the registry loads.

## Consequences

**The vocabulary rename must happen in the KB.** UI strings are mastered in
`zettacard-kb/content/_ui` (ADR-app-0001) and *also* still hard-coded as
`UI_STRINGS` in `app.js` — a fork the PO knowingly accepted as temporary. Renaming
~15 keys across 18 locales in `app.js` would make that fork permanent and invert
the authority direction ADR-0001 exists to protect. So: rename in the KB,
re-export, and retire the `app.js` dictionaries. The exception ends here.

**New manifest fields:** `kind`, `examLanguages`, per-locale question counts.
The first is hand-written once; the other two are generated.

**Not decided here, and deliberately:**

- **Profiles have no home in the information architecture.** The Lernnachweis is
  the only artefact in the app carrying a person's name, and it is the reason
  profiles exist at all — yet a shared family phone can produce a compliance
  record under the wrong name. The certificate should confirm the name at issue
  time rather than trusting the profile label. Own ADR.
