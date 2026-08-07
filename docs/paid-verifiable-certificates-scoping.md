# Scoping: Paid, Permanently-Verifiable PDF Certificates (B2B + B2C)

Status: **scoping only, MVP build about to start.** PO has made a fourth scope call since this
document was first written: **the MVP ships at 0€ per certificate — no payment processing at all
for now.** This removes Stripe entirely from the MVP (section 3.2's `stripe-checkout-session` /
`stripe-webhook` functions and all of Phase 2/4 below are deferred, not cancelled — the permanent
verification link is the actual product being validated first; monetizing it is a later,
separate decision once the mechanic itself is proven and there's a real B2B customer asking to pay
for it). Everything else in section 0 (module scope: 4 compliance modules only; storage: Netlify
Database) still stands. What's now open is only "Open questions" (section 6) still relevant to a
free MVP (identity capture, data retention) — pricing/payment questions are moot until a paid tier
is actually revisited.

## 0. The ask, and decisions already made

PO's ask (verbatim intent): extend the existing signed-badge feature (see
`docs/open-badges-signing-scoping.md` and `docs/open-badges-signing-setup.md` — real ES256-signed
JWT credentials, live since 2026-08-07) so that:

- A participant can get a real **PDF** certificate for their completion (today there's only a
  printable HTML certificate and a JSON credential download — see `certificateHtmlDoc()` /
  `credentialJsonDoc()` in `app/app.js`).
- That PDF is backed by a **permanent link on our own site** where anyone (an employer, an
  auditor, a DGUV inspector) can independently check the certificate is real — not just a
  signature a technical person could verify with `jose`, but a page a non-technical verifier can
  just open.
- **B2B customers** would pay for this (they'd want it for compliance audit trails — DGUV/GDPR/AI
  Act training records are exactly the kind of thing a company needs to *prove* happened, to
  someone else, potentially years later).
- **B2C users** could optionally buy a single certificate for a small fee (PO mentioned ~5€) if
  they want the polished/permanent version instead of the existing free HTML/JSON download.

Already decided by PO (this session, via AskUserQuestion) before this doc was written:

1. **Module scope**: only the 4 workplace-compliance modules (Datenschutz, Arbeitssicherheit,
   KI-Verordnung, IT-Sicherheit) — not Fuehrerschein/Motorrad/LKW/Angelschein, which stay
   completely free and unchanged. This matches the actual demand signal (DGUV/GDPR/AI-Act training
   records are the things companies actually need to prove; a driving-theory practice app doesn't
   have the same audit-trail use case).
2. **Backend/storage**: Netlify Database (serverless Postgres, GA since 2026-04-28 — see
   [Netlify's announcement](https://www.netlify.com/changelog/2026-04-28-netlify-database/) and
   [billing/limits docs](https://docs.netlify.com/build/data-and-storage/netlify-database/billing-and-usage/)),
   not a separate provider — stays in the same deploy ecosystem as the existing signing function.
3. **Payments**: Stripe.

## 1. Why this is a real architecture change, not an incremental feature

The whole point of this app, stated repeatedly in `AGENTS.md`, is **"offline-first... zero-backend
static PWA... no feature should require a live backend call to serve content."** The existing
signing function is already a small, deliberate exception to that (a Netlify Function holding a
private key) but it's *stateless* — it signs and returns, nothing is stored. This feature is
different in kind: it requires **persisting real records server-side, indefinitely, tied to a
public URL** — a genuine, mostly one-way architecture step. Worth saying plainly: this isn't
"add a button," it's "the project now has a real backend with real customer data in it,"
with the ops/legal/cost obligations that come with that (see section 4).

## 2. What already exists to build on

- `netlify/functions/sign-credential.js` — signs a completion record as a JWT, returns it, stores
  nothing server-side. The private key (`ZETTACARD_SIGNING_PRIVATE_JWK`) already lives in a
  Netlify env var — same key can keep signing paid credentials, no new keypair needed.
- `app/.well-known/jwks.json` — public JWKS, already live, already used by third-party validators
  (see this session's live test against CertLister's and 1EdTech's OB3 validators — both correctly
  parsed our JWT-VC structure, CertLister just couldn't verify the signature because our issuer is
  a plain URL rather than a `did:web` document; not blocking for this feature, but relevant context
  if a future round wants stronger third-party-validator compatibility).
- `credentialJsonDoc()` / `certificateHtmlDoc()` in `app/app.js` — the existing free-tier shapes;
  the paid tier's PDF should visually descend from `certificateHtmlDoc()`'s design, not invent a
  new look.
- `renderBadgeRow()` / `.cert-badge-*` styles — the visible "signed vs. self-issued" badge UI added
  this session; a paid/permanently-verified tier would want its own third visual state here (e.g. a
  distinct badge style + a "🔗 Verify online" link once a record has a permanent slug).

## 3. Architecture: what needs to be added

### 3.1 Netlify Database — what gets stored

A new table, roughly:

```
credential_records
  id                  (public slug/UUID - this IS the permanent URL, e.g. /verify/<id>)
  exam_type, scope_code, module_label, scope_label
  passed_at, error_points, wrong_high_stakes, total_questions
  signed_jwt, signed_kid, signed_alg      -- same shape as today's client-side record
  issued_at
  paid                (bool)
  stripe_payment_intent_id / stripe_customer_id   -- reference only, NEVER card data
  b2b_org_id          (nullable - null for B2C purchases)
  participant_name    -- see open question in section 6, this may not exist at launch
  created_at
```

**Important, non-negotiable constraint**: Netlify Database is explicitly **not PCI-DSS certified**
(per its own docs) — it must never store card numbers or any raw payment data. Stripe already
handles all of that; we only ever store Stripe's own reference IDs, exactly like any standard
Stripe integration. This isn't a design choice, it's a hard requirement.

Free tier is plenty for an MVP: 3 databases / 5 GB storage / 5 GB data-written per period on
Netlify's free plan — this feature would use one small table, nowhere near those limits at
realistic volume for a while.

### 3.2 New/changed Netlify Functions

**MVP (0€, build this now):**

- **`create-verified-credential`** (extends today's `sign-credential.js` flow): after signing,
  writes the row above and returns a permanent slug/URL alongside the raw JWT — no payment gate,
  every completed compliance-module exam simulation gets one.
- **`verify/[id]`** (or a static-feeling route serving from the DB): the actual public
  verification page. Renders credential details + a clear "✅ Valid" / re-checks the JWT signature
  server-side against the JWKS at request time (belt-and-suspenders alongside the stored
  `signed_jwt`) — this is the page a non-technical DGUV auditor actually opens, not a JSON blob.

**Deferred until a paid tier is actually revisited (not part of the MVP):**

- **`stripe-checkout-session`**: creates a Stripe Checkout session for either the B2C one-off
  (~5€) or a B2B flow (see section 6 — B2B pricing isn't decided yet, this function's shape
  depends on that answer).
- **`stripe-webhook`**: the standard Stripe pattern — Checkout completing does NOT itself create
  the permanent record; the *webhook* (server-to-server, can't be spoofed by editing client state)
  is what actually confirms payment and triggers persistence. This is the same category of
  trust-boundary discipline the existing signing doc already applies to grading (client state is
  never trusted for anything that matters).

### 3.3 PDF generation

Today: zero PDF generation anywhere in this codebase (only HTML + JSON). Two real options:

- **Client-side** (e.g. a library like `jsPDF`/`html2canvas`, or the browser's native "print to
  PDF" pointed at a print-styled version of `certificateHtmlDoc()`'s output): simplest, no new
  serverless surface, but less control over exact typography/layout consistency across
  browsers/devices — "good enough" quality, free to build.
- **Server-rendered** (a Netlify Function running headless Chromium/Playwright against a
  print-styled HTML template, or a PDF library like `pdf-lib`/`pdfkit`): pixel-consistent output
  regardless of the buyer's device/browser, feels more "official" for a paid B2B deliverable, but
  headless-Chromium-in-a-serverless-function has real cold-start/memory-size tradeoffs worth
  testing before committing.

Recommendation: start client-side for the MVP (Phase 3 below), only invest in server-rendered PDF
if real B2B customers push back on quality/consistency.

## 4. Real risks and obligations this creates (read before starting Phase 1)

- **GDPR**: the moment this stores anything tied to a real person (at minimum: whatever identity
  info is captured at payment — see section 6's identity question) server-side, indefinitely,
  this project has real personal-data obligations it doesn't have today (a privacy policy, a
  retention/deletion policy, likely data-processing agreements with Stripe and Netlify). This
  should be folded into the existing legal-review backlog item (DN-12) rather than treated as
  separate — a professional legal pass on the whole compliance-module line needs to cover this too,
  not just the training content itself.
- **Cost at scale**: Stripe's standard EU-card fee (~1.5% + €0.25 per transaction as of general
  Stripe pricing) plus Netlify Database compute/bandwidth credits beyond the free tier — trivial at
  MVP volume, worth modeling once real B2B volume exists.
- **This is a one-way door**: once real customers have paid for permanent links, those links need
  to keep working — there's no "let's simplify the architecture later" undo without breaking a
  paying customer's actual proof-of-completion. Worth being fully sure of the DB/schema choice
  before the first paid transaction, not after.
- **Trust-boundary honesty carries over unchanged**: exactly like the existing signing doc says —
  this still can't prove the exam itself was un-gameable, only that "a record with these exact
  claims was submitted, paid for, and persisted." Worth keeping the same honest framing on the
  verification page itself, not overselling what "verified" means.

## 5. Recommended build order (phased, not all-at-once)

**MVP scope (0€):**

1. **Phase 1 — the actual MVP — DONE, live in production (2026-08-07)**: wired up Netlify Blobs
   (chosen over Netlify Database — simpler and sufficient for simple UUID-keyed record storage,
   no complex queries needed), extended the existing free signing flow so every completed
   compliance-module Exam Simulation can request a permanent slug + a real `/verify/<id>` public
   page, no payment gate at all. This alone is the deliverable: a DGUV auditor or a new employer
   can open a real, permanent, independently-checkable link — for free. See BACKLOG.md's Done
   section (2026-08-07 entry) for the full build/debugging account, including a real multi-step
   Netlify Blobs + deploy-caching saga worth reading before touching these functions again.
   Shipped as `netlify/functions/save-verified-credential-v2.mjs` +
   `netlify/functions/verify-credential-v2.mjs` + `app/_redirects`. Now watching for whether real
   B2B demand for a paid/premium tier actually materializes before building anything in Phase 2.

**Deferred, not scoped further until there's real demand:**

2. **Phase 2 — paid tier** (Stripe, B2C ~5€ one-off + a to-be-decided B2B model): only worth
   building once Phase 1 is live and either a real B2B customer asks to pay for something Phase 1
   doesn't already give them (e.g. a nicer PDF, bulk/org management, an SLA), or B2C demand for a
   premium version shows up. Revisit sections 3.2/6's price and B2B-model questions at that point,
   not now.
3. **Phase 3 — PDF**: client-side generation first (see 3.3), styled to match the existing
   certificate design. Could actually happen alongside or even before Phase 2 if a downloadable PDF
   turns out to matter more than the payment question — worth reassessing once Phase 1 users
   actually ask for it.
4. **Phase 4 — B2B-specific flow**: bulk/org accounts, invoicing — its own scoping conversation
   later.

## 6. Open questions — need a PO decision before Phase 1 starts

- **Identity capture**: a permanent, third-party-checkable certificate arguably needs to show
  *whose* certificate it is — today the app has no login/accounts at all (local device-profile
  names only, e.g. "Default", not verified identities, and definitely not something to put on a
  public compliance record). Since there's no payment step to piggyback a name/email capture on
  anymore, this needs its own small answer for the free MVP: simplest option is a plain optional
  text field ("Name for the certificate") shown once, at the moment of generating the permanent
  link — not a real verified identity, just a label, same trust level as today's local profile
  names. This is also where the PO's earlier "we'll need real login eventually, e.g. Google OAuth"
  comment (this session) becomes relevant again — worth deciding whether Phase 1 needs that now, or
  whether an unverified optional name field is good enough for a free MVP (recommended: the latter
  — don't pull OAuth into scope just to ship a free verification-link MVP).
- **Data retention**: how long does a verification record need to stay live? Indefinitely (the
  "permanent" in "permanent link" implies this), but worth an explicit policy statement rather than
  an implicit assumption, especially since section 4's GDPR note applies even to a free MVP the
  moment a name is attached to a record.
- **Verification page branding/content**: should it show just pass/fail + module + date (matches
  today's certificate), or more detail (e.g. per-topic breakdown)? Worth a quick mockup once Phase
  1 is underway rather than deciding purely in the abstract here.
- Price and B2B-pricing-model questions from the original draft are moot for now — revisit only
  when Phase 2 is actually scheduled.

## Sources

- [Netlify Database is now generally available](https://www.netlify.com/changelog/2026-04-28-netlify-database/)
- [Netlify Database billing, limits, and compliance](https://docs.netlify.com/build/data-and-storage/netlify-database/billing-and-usage/)
- [Netlify Blobs docs](https://docs.netlify.com/build/data-and-storage/netlify-blobs/) (considered as a lighter-weight alternative to a full Postgres table for simple key-value credential storage — worth a quick comparison at the start of Phase 1 rather than assuming Netlify Database is definitely the right shape for what is a fairly simple record store)
