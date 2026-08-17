# Course media sections (`section_kind: "media"`)

**Landed:** 2026-08-17 · **Applies to:** every module with `hasCourse: true`
(today: `cka`, `aevo`, `datenschutz`, `arbeitssicherheit`, `ki_act`,
`it_sicherheit`, `hinweisgeberschutz`, `kyc_aml`, `kartellrecht`, `dora`,
`nis2`) and any future one, e.g. a Führerschein course.

This is generic infrastructure, not content. **No shipped course uses it yet** —
it was verified with a throwaway fixture that was removed before commit, so the
PO can paste real assets in without any placeholder junk having gone live in the
meantime.

Where the pieces live:

| Concern | File |
|---|---|
| Authoring | `data/<module>_course.json` |
| Build (validate, normalise, fact/text split) | `data/build_modules.py` — `split_media()`, `_norm_media_facts()`, `normalize_youtube_id()`, `check_media_src()` |
| Runtime rendering | `app/app.js` — `renderCourseMedia()` and its four helpers |
| UI strings (12 locales) | `app/app.js` — `COURSE_STRINGS.*.media*` |
| Styling | `app/styles.css` — `.course-media*` |
| Container element | `app/app.html` — `#course-reader-media` |

---

## 1. The four types

| `media.type` | What it renders | Key fields |
|---|---|---|
| `youtube` | Click-to-load facade: thumbnail + play button; the `<iframe>` (on `youtube-nocookie.com`) is only created **after** the click | `youtube_id` |
| `video_mp4` | `<video controls preload="none">` pointing at an **external** URL | `src`, optional `poster` |
| `image` | One responsive `<img>` | `src`, `alt_text` |
| `slideshow` | Hand-rolled prev/next carousel, "2 / 5" indicator, ←/→ keys, per-slide caption | `slides[]` (≥ 2), each `src` + `alt_text` (+ optional `caption`) |

## 2. Fields, and which layer each one lives in

A section is `section_kind: "media"` **iff** it has a `media` object — the build
hard-fails on either half without the other, so the two can't drift apart.

**Locale-independent (stay in `course.json`) — facts:**

| Field | Req. | Notes |
|---|---|---|
| `type` | ✅ | `youtube` \| `video_mp4` \| `image` \| `slideshow` |
| `youtube_id` | youtube | Bare 11-char id **or** any usual URL (`watch?v=`, `youtu.be/`, `/embed/`, `/shorts/`). The build normalises to the bare id and fails loudly on anything unrecognisable. |
| `src` | mp4/image | `video_mp4`: absolute `https://` only (see §5). `image`: `https://` **or** a path relative to `app/`, e.g. `assets/diagrams/vorfahrt-01.svg`. |
| `poster` | – | mp4 only, same URL rules as an image `src`. |
| `slides[]` | slideshow | Ordered; ≥ 2 (use `type: "image"` for one). Each: `src`, `alt_text`, optional `caption`, optional `slide_id`. |
| `license` | ✅ | Short human label: `"CC BY 4.0"`, `"Zettacard original"`, `"YouTube Standard License"`. **Required on every media object** — this is the per-asset licensing gap the course-layer design doc flagged as a hard blocker (§2.7/§7); no asset can land without saying what it's licensed under. |
| `license_url` | – | Rendered as a link on the label. |
| `attribution` | – | Free text, e.g. `"Photo: A. Beispiel"`, `"© Blender Foundation"`. |
| `source_url` | – | Where the asset came from, when not self-authored. Rendered as a host-name link. |

Naming follows the project's existing convention: `license` / `license_url`
spelled exactly as in every module's `meta` block (`datenschutz_pilot.json`
etc.), sitting **inline** on the record rather than in a separate table — the
same way `legal_basis` and `license_ref` already sit inline on a section. Note
the two are different things and both are allowed on one section:
`section.license_ref` covers the section's own **prose**, `media.license`
covers the **asset**.

**Locale-dependent (pulled into `course_locales/<lang>.json`) — display text:**

| Field | Req. | Notes |
|---|---|---|
| `alt_text` | image (per media), slideshow (per slide) | `{locale: text}`. Optional for youtube/mp4, where it also becomes the play button's / video's accessible label. |
| `caption` | – | `{locale: text}`. One caption line under the media; on a slideshow, per slide. |

The split is the same one every other content type here uses: a URL doesn't
change per language, alt text does. Locale keys use the existing
"the key IS the entity id" scheme — `<section_id>` for the media's own
`alt_text`/`caption`, `<section_id>-m<n>` for slide *n* (override with an
explicit `slide_id` if you want, but you never need to invent one).

## 3. Worked example — paste-ready

Authored form, in `data/<module>_course.json`, inside a lesson's `sections`
array (locale objects trimmed to de/en; add whatever locales that course
declares):

```json
{
  "section_id": "fs-l3-s2",
  "order": 1,
  "section_kind": "media",
  "legal_basis": "§ 8 StVO",
  "license_ref": "CC-BY-NC-SA-4.0",
  "review_status": "draft",
  "generator": "authored:claude-opus/2026-08-17",
  "title": {
    "de": "Rechts vor links im Video",
    "en": "Right-before-left, on video"
  },
  "body": {
    "de": "Achte im Video besonders auf den Moment, in dem beide Fahrzeuge gleichzeitig anhalten.",
    "en": "Watch for the moment where both vehicles stop at the same time."
  },
  "media": {
    "type": "youtube",
    "youtube_id": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "license": "CC BY 4.0",
    "license_url": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "Video: Zettacard",
    "source_url": "https://example.org/where-it-came-from",
    "alt_text": {
      "de": "Kreuzung ohne Vorfahrtsschilder aus der Fahrerperspektive",
      "en": "Unsigned intersection from the driver's point of view"
    },
    "caption": {
      "de": "Untertitel auf Deutsch verfügbar.",
      "en": "German subtitles available."
    }
  }
}
```

After `cd data && python3 build_modules.py`, that becomes:

`app/data/<module>/course.json` (facts only, no per-locale duplication):

```json
{
  "section_id": "fs-l3-s2",
  "order": 1,
  "section_kind": "media",
  "legal_basis": "§ 8 StVO",
  "license_ref": "CC-BY-NC-SA-4.0",
  "review_status": "draft",
  "generator": "authored:claude-opus/2026-08-17",
  "media": {
    "type": "youtube",
    "license": "CC BY 4.0",
    "license_url": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "Video: Zettacard",
    "source_url": "https://example.org/where-it-came-from",
    "youtube_id": "dQw4w9WgXcQ",
    "alt_text_key": "fs-l3-s2",
    "caption_key": "fs-l3-s2"
  },
  "title_key": "fs-l3-s2",
  "body_key": "fs-l3-s2"
}
```

`app/data/<module>/course_locales/de.json`:

```json
{
  "fs-l3-s2": {
    "title": "Rechts vor links im Video",
    "body": "Achte im Video besonders auf den Moment, …",
    "alt_text": "Kreuzung ohne Vorfahrtsschilder aus der Fahrerperspektive",
    "caption": "Untertitel auf Deutsch verfügbar."
  }
}
```

### The other three, abbreviated

```json
"media": {
  "type": "video_mp4",
  "src": "https://cdn.example.com/zettacard/vorfahrt-01.mp4",
  "poster": "assets/diagrams/vorfahrt-01-poster.png",
  "license": "Zettacard original",
  "attribution": "Video: Zettacard",
  "alt_text": { "de": "…", "en": "…" },
  "caption":  { "de": "…", "en": "…" }
}
```

```json
"media": {
  "type": "image",
  "src": "assets/diagrams/vorfahrt-01.svg",
  "license": "Zettacard original",
  "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
  "alt_text": { "de": "…", "en": "…" },
  "caption":  { "de": "…", "en": "…" }
}
```

```json
"media": {
  "type": "slideshow",
  "license": "Zettacard original",
  "attribution": "Diagramme: Zettacard, nach StVO Anlage 3",
  "slides": [
    { "src": "assets/diagrams/abbiegen-step1.svg",
      "alt_text": { "de": "…", "en": "…" },
      "caption":  { "de": "Schritt 1 – …", "en": "Step 1 – …" } },
    { "src": "assets/diagrams/abbiegen-step2.svg",
      "alt_text": { "de": "…", "en": "…" },
      "caption":  { "de": "Schritt 2 – …", "en": "Step 2 – …" } }
  ]
}
```

## 4. What a human actually has to do to wire a real asset

1. Add the section to `data/cka_course.json` / `data/aevo_course.json` /
   `data/<new>_course.json`, copying a block above. Populate **every locale
   that course declares** (`courses[0].locales`) for `alt_text`/`caption` —
   for `cka` that's `en, de, ja, zh`; for `aevo` `de, en`.
2. For an `image`/`slideshow` asset that lives in this repo, drop the file
   under `app/assets/…` and reference it as `assets/…` (no leading slash).
3. `cd data && python3 build_modules.py`. It prints a per-module locale-gap
   line and ends with `Sanity checks passed.`; a bad media object raises
   instead, with the offending `<module>/<section_id>.media` path in the
   message.
4. Open the module's Course view and step to that section. Nothing else —
   no `app.js`, `styles.css`, `modules_manifest.json` or service-worker
   change is needed for new media content.

Common build errors and what they mean:

- `not a recognisable YouTube video id or URL` — pasted a Vimeo/other link, or the id isn't 11 chars.
- `video_mp4 src must be an absolute https:// URL on external hosting` — see §5.
- `media.license is required` — add the label.
- `image media needs alt_text` / `slides[n]: needs alt_text` — accessibility, non-negotiable.
- `slideshow media needs at least 2 slides` — use `type: "image"`.
- `has a media object but section_kind is 'prose'` — set `section_kind: "media"`.

## 5. Decisions baked in (PO, 2026-08-17)

- **YouTube is a 2-click / facade embed on `youtube-nocookie.com`.** Before the
  click the only third-party request is the static thumbnail on
  `i.ytimg.com` (a cookieless image, not the player bundle); the `<iframe>` is
  created inside the click handler. A localized notice says so, and disappears
  once the player is loaded. Verified by request log, not by assertion.
- **MP4 is external-URL-only and never committed to this repo.** The build
  rejects a repo-relative `video_mp4` src outright. `preload="none"`, so
  nothing is downloaded until the learner presses play.
- **Licensing is inline per media object**, not the design doc's full `ASSET`
  entity — that stays the right long-term shape, this is the scoped version of
  it, and `license` being mandatory closes the "third-party asset with no
  recorded licence" hole today.
- **No new dependency.** The carousel is hand-rolled; this app still has zero
  third-party JS.

## 6. Offline behaviour — a deliberate, disclosed exception

AGENTS.md constraint 6 (offline-first, no feature needing a live backend to
serve content) has exactly one exception now, and this is it: a YouTube video,
an externally hosted MP4, or a remotely hosted image genuinely cannot be served
from a precached static bundle.

What that does and does not mean:

- **All text still works offline.** A media section's title, body, alt text and
  caption come from the same precacheable `course.json` / `course_locales/*.json`
  pair as every other section.
- **Remote media offline** → the media element is replaced by a calm one-line
  localized note (`COURSE_STRINGS.*.mediaOffline`, 12 locales) instead of a
  broken-image icon or blank space. `online`/`offline` listeners re-render the
  open lesson as soon as connectivity returns.
- **Repo-relative images/slideshows are NOT treated as network-dependent** —
  they're same-origin static files the service worker runtime-caches like a sign
  SVG, and `offlineAssetUrls()` now also lists them, so "make available offline"
  fetches a course's local media too. A Führerschein course built on local
  PNG/SVG diagrams therefore works fully offline.
- `service-worker.js` now lets **cross-origin** requests fall through
  untouched (no `respondWith`), which is what makes an external `<video>`'s
  Range requests behave. Same-origin behaviour is unchanged.

## 7. How this was verified (2026-08-17)

A throwaway lesson with all four media types was injected into
`data/cka_course.json`, built, rendered in headless Chromium at 430 px, then
removed. Confirmed by request log / DOM inspection / screenshots:

- facade: exactly **one** cross-origin request (`i.ytimg.com/…/hqdefault.jpg`)
  before the click, and `youtube-nocookie.com/embed/<id>?autoplay=1&rel=0`
  only after it; notice removed on load
- mp4: **0** requests before play, 1 after; real CC BY 3.0 clip decoded and
  advanced (`currentTime` 2.46 s, `videoWidth` 427); `preload="none"`
- image: correct `alt`, renders at natural aspect ratio
- slideshow: `1 / 3` → `3 / 3`, button `disabled` at both ends, ←/→ keys,
  per-slide caption and alt text
- offline: note shown for youtube + mp4, local slideshow unaffected, recovery
  on `online`
- locales sampled de / en / ar (incl. RTL: mirrored chevrons and `dir="ltr"` on
  the position indicator so "1 / 3" isn't bidi-reordered into "3 / 1")
- dark and light theme
- `python3 build_modules.py` clean, zero locale gaps, all 27 modules

Known pre-existing (NOT caused by this work, seen on prose-only lessons too):
in RTL the course-reader card lays out to the right of the viewport origin, so
a full-page screenshot at scrollX 0 clips it. Worth its own card.

## 8. Known limitations, found in first real use (2026-08-17)

The throwaway fixture in §7 exercised the mechanics; the `fuehrerschein` course's
right-of-way scenario lessons (`data/fuehrerschein_course.json`, BACKLOG DN-79) are the
first real shipped content to use `section_kind: "media"`, and surfaced two design gaps
worth recording rather than silently working around in every future course:

- **DOM order is body-then-media, always** (`#course-reader-body` before
  `#course-reader-media` in `app/app.html`). Fine for an illustrative image that
  supports prose the learner reads first. Wrong for a "figure out the answer, then
  check the diagram" scenario, where a learner reading top-to-bottom sees the written
  explanation before the picture it explains - `fuehrerschein`'s scenario lessons
  worked around this by writing the prose as post-hoc reasoning ("here's why", not
  "try to guess first") rather than fighting the fixed order. A real fix would be a
  per-section `media_position: "before_body" | "after_body"` flag (default
  `after_body`, matching today's only behaviour) threaded through
  `renderCourseLesson()` - not built, since it's a real UI change to shared
  infrastructure and wasn't needed to ship this round's content, but the workaround
  costs something didactically and is worth a real fix if scenario-style sections
  become common (the driving-scenario format is exactly the shape the Führerschein
  module needs more of).
- **`media.attribution` is schema'd as locale-independent** (§2), which is correct for
  a proper-noun credit like `"© Blender Foundation"` but breaks for a full sentence
  credit line, since German words inside an `attribution` string leak into every
  locale's rendered course including non-German ones. `fuehrerschein`'s scenario
  sections have no third-party attribution to carry (self-authored diagrams, `license:
  "Zettacard original"` already covers it) so this round simply omitted
  `attribution` rather than fight the schema - a real gap only once a course credits
  a genuinely third-party, non-proper-noun-labelled asset. If/when that happens,
  either keep `attribution` disciplined to proper-noun-style strings only, or split it
  into a locale-dependent field alongside `alt_text`/`caption`.
