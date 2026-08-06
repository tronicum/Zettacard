# Scoping: Business/Team Compliance-Tracking Features

Status: research/scoping only — nothing here is scheduled or built. Written to be read before anyone
picks up the actual implementation work. Sibling document to
`docs/open-badges-signing-scoping.md`; read that one first if you haven't, since it covers the
adjacent "how would Zettacard ever sign a credential" question and the same zero-backend baseline
this document starts from.

## 0. Where we are today

Zettacard is a fully client-side static PWA on Netlify. All state — language, selected module,
per-module progress, completions, and the (currently unsigned) credential JSON — lives in
`localStorage`, per browser/device. The recently-added local profile switcher (`app/app.js`, see
`PROFILE_REGISTRY_KEY`/`PROFILE_ACTIVE_KEY` and `migrateOrInitProfiles()`) lets multiple people share
one device without mixing up progress, but it is explicitly **not** an identity or account system —
it's a namespace prefix on localStorage keys, scoped to one physical device, with no server involved
and no way for anyone else to ever see it. There are zero accounts, zero auth, and zero backend
anywhere in the app today.

The PO's interest here is specifically the **4 compliance modules** (DN-44: Datenschutz, IT-Sicherheit,
Arbeitssicherheit, KI-Verordnung/AI Act) — the idea that an employer or a designated compliance
officer could see, across their employees, who has completed which of these modules and when. This
is a different kind of feature from anything shipped so far: it requires the app to know about
*people other than the one using the device right now*, which is impossible without a server holding
that data somewhere it can be queried from more than one device. This document treats that as the
real architectural step it is, not something to route around.

## 1. What team compliance tracking actually needs to be credible

Talking to a real compliance officer (or just imagining what an auditor would ask for) narrows this
down fast. The bar is not "can we show a list on screen" — it's **"can this data survive an audit
request."** Minimum viable data model:

- **An organization/company entity.** Even a v1 needs *something* that groups a set of employees
  together — a company name, an internal ID, and (for billing/contact purposes eventually) an admin
  email. Without this there's no way to scope "show me my company's employees" vs. everyone else's.
- **A roster** — at minimum, a list of employee identifiers (email is the natural v1 choice; a name
  is nice-to-have but not load-bearing). Notably this does *not* require the employee to have a
  "real" account with a password from day one (see Section 3) — an email is enough to anchor a
  completion record to a person.
- **Per-employee, per-module completion records**, each with: which module, a timestamp, pass/fail
  (and ideally the score, matching what `recordCompletion()` already captures locally today), and —
  this is the detail that turns "a nice dashboard" into "something an auditor accepts" — **the date
  needs to be provably tied to the actual completion event**, not just self-reported. If completions
  are submitted client-side with a timestamp the client controls, that timestamp is only as trustworthy
  as an unsigned credential is today (see the Open Badges scoping doc, Section 0) — server-set
  timestamps (recorded when the submission hits the backend, not trusting a client-supplied date) are
  the minimum bar for this to mean anything in an audit.
- **A view for the admin**: at minimum a **CSV export** (auditors and HR/compliance tooling live on
  spreadsheets; this is the lowest-effort, highest-credibility artifact to hand over), and ideally a
  simple dashboard listing employees × modules × last-completed-date × pass/fail, with an obvious
  visual flag for "overdue" (see the annual-renewal point below) or "never completed."
- **Retention** of these records needs a deliberate policy, not an accident of "we never delete
  anything" — see Section 4, this is a GDPR obligation, not just a UX nicety.

### Annual renewal: which of the 4 compliance areas actually require it

This matters a lot for the data model — if a module needs to be *redone periodically* to stay
"current," a completion record needs a validity window, not just a single completed/not-completed
flag, and the admin dashboard needs a "due for renewal" state, not just "done." Checked each of the
four areas against real legal/regulatory sources rather than assuming compliance-training vendors'
marketing copy is accurate:

- **Arbeitssicherheit (occupational safety)** — **yes, explicitly annual, by statute.** ArbSchG § 12
  establishes the employer's duty to instruct employees adequately on safety; **DGUV Vorschrift 1 § 4
  operationalizes this as "mindestens einmal jährlich"** (at least once per year), with shorter
  intervals for minors (half-yearly, per JArbSchG) and for higher-hazard tasks, plus ad hoc
  retraining triggers (new equipment, after an accident, changed processes). This is the clearest,
  most legally explicit annual-renewal requirement of the four — a real product built on this should
  treat Arbeitssicherheit completions as expiring after 12 months by default.
- **IT-Sicherheit (mapped here to NIS2/ISO 27001-style awareness training)** — **recurring, but not a
  fixed statutory interval.** NIS2UmsVO Annex 8.2.1/8.2.5 requires personnel in security-relevant
  roles be trained "regelmäßig" (regularly) and that the training program itself be "regelmäßig
  aktualisiert und durchgeführt" (regularly updated and conducted) — recurrence is legally required,
  but the exact cadence is left to the organization's risk assessment rather than fixed at "annual" in
  the statute. Annual is the de facto industry-standard interval ISO 27001/NIS2 guidance converges
  on, and is a reasonable default, but it's an organizational choice here, not a hard legal number the
  way DGUV Vorschrift 1 is for Arbeitssicherheit.
- **Datenschutz (GDPR/BDSG)** — **no fixed legal frequency, but recurring is expected in practice.**
  GDPR Art. 39(1)(b) requires the DPO to carry out "awareness-raising and training," and Art. 32(1)
  requires "appropriate technical and organisational measures," but neither article states a
  frequency. Regulatory guidance (e.g. the UK ICO, whose guidance is widely used as a de facto GDPR
  interpretation reference even outside the UK) recommends refresher training "at least annually,"
  and the EDPB frames training as "a continuous function rather than a one-time event." Practically:
  a regulator is unlikely to accept "our staff did GDPR training three years ago and never since" as
  satisfying the Art. 5(2) accountability principle, so treat this as "annual is the safe practical
  default" even though it isn't a numbered statutory requirement the way DGUV Vorschrift 1 is.
- **KI-Verordnung (EU AI Act, Article 4 AI literacy)** — **explicitly NOT tied to a fixed recurring
  interval by the statute itself.** Article 4 (in force since 2 February 2025, enforcement/supervision
  from 2 August 2026) requires providers/deployers to ensure "a sufficient level of AI literacy"
  among staff, but the Commission's own guidance frames this as scaled to "the role of each
  organisation in the AI value chain, the risk level of the systems used, and the current knowledge
  of staff" — closer to a one-time-plus-role-based-updates model than a calendar-driven annual
  requirement. This is the one of the four that's legitimately closest to "one-time, updated only
  when role/risk/system changes," not annual by default.

**Product implication**: the data model needs a per-module (not per-completion-record) "renewal
policy" flag — realistically: Arbeitssicherheit = hard 12-month expiry, IT-Sicherheit = recommended
12-month expiry (soft/configurable), Datenschutz = recommended 12-month expiry (soft/configurable),
KI-Verordnung = no fixed expiry, flagged instead for re-completion on role change or major regulation
update. This is different from treating "completed" as a permanent, non-expiring state the way the
current unsigned-credential system implicitly does — get this modeled explicitly rather than
inherited by accident from the current single-completion-per-module UX.

## 2. Backend architecture options

Three genuinely different shapes, in increasing order of "how much of a real company this makes
Zettacard":

### (a) Lightweight serverless backend on existing Netlify infra (Netlify Functions + a managed DB)

Netlify Functions (already the natural fit, per the signing-scoping doc's option (a)) handling a
small number of endpoints — submit-completion, list-completions-for-org, export-CSV — backed by a
managed database rather than anything self-hosted. Real, currently-relevant managed-DB options as of
this research: **Supabase** (Postgres-based, generous free tier historically ~500MB DB + built-in
auth/row-level-security, Pro tier around $25/month once a pilot needs to graduate off the free tier),
**Neon** (serverless Postgres, free tier with a scale-to-zero model good for spiky/low-traffic usage),
and **PlanetScale** (MySQL-compatible, notably changed its free-tier posture over the past couple of
years — worth re-confirming current terms at build time rather than trusting older "PlanetScale has a
free tier" assumptions, since providers in this space have moved free tiers around repeatedly).

- **Complexity**: Moderate. A handful of endpoints, a real schema (orgs, employees, completions), and
  — the part that's new architecturally, not just "one more table" — a security model: an
  organization's admin must only ever be able to query *their own* organization's data, which is
  exactly what Postgres row-level security (Supabase's headline feature) is built for, or otherwise an
  application-layer check on every query if using a DB without built-in RLS.
- **Ops burden**: Low. No servers to patch, managed DB handles backups/availability, Netlify Functions
  scale automatically. The team owns: DB migrations, backup/retention policy, and — because this now
  holds real employee personal data — actual security discipline (see Section 4), which is a step up
  from "we lost some localStorage progress, no big deal."
- **Cost**: Near-zero for a pilot on free tiers; graduates to roughly $25-30/month range once past
  free-tier limits (Supabase Pro-equivalent pricing), which is trivial next to what buying an
  off-the-shelf LMS would cost per seat (option (c) below).
- **Vendor lock-in**: Low-to-moderate — Postgres-based options (Supabase, Neon) keep data in a
  standard, exportable format; a future migration off any single vendor is realistic, not a rewrite.
- **Verdict**: The natural "smallest real backend" option, directly analogous to option (a) in the
  signing-scoping doc, and the one most consistent with everything the project has done so far.

### (b) A full framework backend (Node/Express-style API + Postgres, self-hosted or PaaS)

A traditional standalone backend service — e.g. a small Express/Fastify (or similar) API with its own
Postgres instance, deployed either self-hosted (a VPS) or on a PaaS (Render, Railway, Fly.io), fully
decoupled from Netlify's serverless-function model.

- **Complexity**: Higher than (a) for equivalent functionality — same schema/security-model work as
  (a), *plus* now owning deployment, process management, and (if self-hosted) the underlying server
  entirely, none of which Netlify Functions require thinking about at all.
- **Ops burden**: Meaningfully higher — someone now owns uptime, patching, scaling, and incident
  response for a standing service, not a managed serverless function. This is a real 24/7 operational
  commitment, which nothing else in this project's history has required.
- **Cost**: Comparable to (a) at small scale on a PaaS (Render/Railway-class pricing is in a similar
  ballpark to a managed-DB-plus-serverless-functions bill), but the ops burden is the real cost here,
  not the dollar figure.
- **Vendor lock-in**: Lowest of the three — a self-owned API and a standard Postgres instance is the
  most portable option architecturally.
- **Verdict**: Only worth it if the team anticipates needing capabilities Netlify Functions genuinely
  can't do well (long-running jobs, websockets for a live dashboard, complex background processing) —
  none of which team compliance tracking actually needs for a v1. This is more infrastructure than the
  problem currently calls for; it's the option to reach for later if the product outgrows (a), not the
  one to start with.

### (c) Build on an existing LMS/compliance-training SaaS instead of building a backend at all

Don't build tracking infrastructure — integrate with (or simply recommend/white-label) an existing
platform that already does employee compliance-training tracking. Real, currently-relevant players
surveyed: general-purpose corporate LMS platforms with compliance-tracking features (**TalentLMS**,
**Docebo**, **iSpring Learn** — iSpring in particular markets a German-language compliance-training
product, "iSpring Learn," directly at this market), and German-market-specific compliance/awareness
platforms (**SoSafe** — a well-known German security-awareness-training vendor that has expanded into
Datenschutz/data-protection modules; **Mitarbeiterschule.de** and **Reteach** — German compliance
e-learning/training-management platforms explicitly targeting the Datenschutz/Arbeitssicherheit
training space Zettacard's compliance modules also cover).

- **Complexity**: Lowest for Zettacard specifically — this is integration work (API calls to report
  completions into their system, or literally just directing employers to buy seats there instead) or,
  more radically, no integration at all: acknowledge that dedicated, already-compliant tracking
  platforms exist and decide whether Zettacard's compliance content is better positioned as content
  feeding *into* one of these (a content/API partnership) rather than as a tracking platform competing
  with them.
- **Ops burden**: Lowest of all three for anything related to tracking-infrastructure correctness,
  security, and retention — that becomes the vendor's problem entirely, the same trade this document's
  sibling doc identifies for option (c) there (managed OB3-issuing platforms).
- **Cost**: The only option with a real, ongoing per-seat/per-employee subscription cost from day one
  — this class of platform is generally priced per active learner/month, which could meaningfully
  undercut or overcut building in-house depending on employee-count assumptions; needs a real quote
  before deciding, not a guess.
- **Vendor lock-in**: Highest — if Zettacard becomes primarily a content source feeding someone else's
  tracking platform, the employer relationship and the completion data live with the vendor, not
  Zettacard.
- **Verdict**: The right lens for a genuine "buy vs. build" decision the PO should make explicitly,
  not skip. Given the existing content-authoring investment (DN-44's verified legal-basis citations
  across 80+ questions per module at 40 each) is Zettacard's real asset, it's plausible the more
  durable business move is content-licensing/partnership with an existing tracking platform rather
  than becoming a tracking platform from scratch — but that's a business-strategy call, not something
  this document should resolve unilaterally.

## 3. Auth approach

The app has literally zero auth today, so anything chosen here is a first, not an iteration. Keep it
proportionate to a v1 pilot, not to eventual scale:

- **Magic-link email auth** — send a one-time login link to an email address, no password ever
  created or stored. Well-suited to low-frequency admin logins (a compliance officer checking the
  dashboard monthly, not daily), avoids ever handling/storing password hashes, and is the lowest-
  complexity real auth mechanism available (a handful of well-established libraries/services handle
  this — e.g. Supabase's built-in magic-link auth pairs directly with option (a)'s DB choice, meaning
  choosing Supabase for the DB could hand this feature over "for free"). Downside: depends on the
  admin's email actually being reachable/trusted, and doesn't extend cleanly to SSO-requiring
  enterprise customers later.
- **SSO/SAML** — the standard for larger orgs' IT departments, but genuinely too heavy for a first
  version: it requires per-customer configuration (each org's identity provider), a meaningfully
  bigger auth-library/vendor surface (Okta/Auth0-class tooling), and solves a problem ("our 500-person
  org needs centralized identity") this product doesn't have yet at pilot scale. Correctly deferred to
  a "we have paying enterprise customers asking for it" milestone, not built speculatively.
- **Invite-code-based scheme** — the lightest option: an admin gets a code (or a link containing one)
  representing "you belong to Org X"; employees complete a module with that code present, and their
  completion record gets tagged to that org without the employee ever needing a real account at all.
  This maps directly onto the v1 recommendation in Section 5 — it needs no password, no email-sending
  infrastructure, and no session-management beyond "does this code look valid." The admin side still
  needs *some* real auth (magic link is the natural pairing) since they're the one viewing/exporting
  other people's data, but the employee side arguably doesn't need any account concept for a v1 at
  all — just "this completion, tagged with this code."
- **Recommendation for v1**: invite-code on the employee side (no employee account needed at all),
  magic-link (or even a single shared admin password to start, see Section 5's explicit "not proud of
  this, but honest" framing) on the admin side. SSO stays out of scope entirely until there's a real
  enterprise customer asking, not speculatively built in.

## 4. Data privacy/GDPR implications

This needs to be said plainly, and with a straight face given the irony: **one of the four compliance
modules this feature is built around is Datenschutz/GDPR itself.** Storing "which employees completed
which training, and when" is processing employees' personal data (an email address plus a training
history tied to an identifiable person), which means the employer becomes a **data controller** under
GDPR the moment this feature exists, and Zettacard (hosting the data) is very likely a **data
processor** acting on the employer's behalf — a relationship that itself needs a data-processing
agreement (GDPR Art. 28), not just an assumption that "it's fine, it's just training records."

Concretely, a real launch of this feature would need real answers — not invented by an engineering
session — to at least:

- **Legal basis** for the employer to process this data (likely legitimate interest or a legal
  obligation basis, given some of the underlying training itself is legally mandated — but which basis
  applies, and how it's documented, is a legal question, not an engineering one).
- **Data minimization** — does the roster need real names, or is an email/employee-ID sufficient?
  Does a completion record need to store anything beyond pass/fail + timestamp + module?
- **Retention limits** — how long can/should a completion record be kept after an employee leaves the
  org, or after the training's own renewal window has passed? "Keep everything forever" is not a
  defensible retention policy under GDPR's storage-limitation principle (Art. 5(1)(e)).
- **Data subject rights** — an employee whose completion history is stored has the same GDPR rights
  (access, erasure, portability) over that record as over any other personal data about them, which
  the product needs a real mechanism to honor, not just a support-ticket promise.
- **Cross-border/hosting considerations** — where the managed DB (option (a)/(b)) or SaaS vendor
  (option (c)) actually stores the data matters for GDPR compliance, and needs to be checked per
  vendor rather than assumed.

**This is flagged with exactly the same posture as BACKLOG.md's DN-12 entry** ("Professional legal
review pass on all published content... needed before any public/commercial release") — this document
does not attempt to resolve these questions, because they are genuinely questions for a person with
real legal qualification to answer for the specific jurisdiction(s) and specific data flows involved,
not something an engineering-scoping document (or the AI session that wrote it) should decide on its
own. Building this feature without that review is building a Datenschutz-training product that itself
mishandles Datenschutz — the single worst possible look this product could have, and worth calling out
explicitly rather than leaving implicit.

## 5. Pragmatic v1 recommendation

Given the project's current all-client-side, zero-infra Netlify deploy, the goal is the **smallest
real step that delivers visible value to a compliance officer**, not the smallest step toward the
full picture in Section 1. Concretely:

### In v1

1. **Team code, not accounts.** An admin generates a "team code" (a short random string) representing
   their org. No org table needed beyond "this code exists and has a display name" — literally could
   start as a single row typed in by hand for a pilot customer, not a self-service signup flow.
2. **Employees complete a module with the team code embedded** — e.g. a URL parameter or a field
   entered once per profile (reusing the existing local-profile concept, not replacing it) — and on
   passing/completing, the client submits a completion record (module, timestamp — **server-assigned,
   not trusted from the client**, pass/fail, score) to one Netlify Function endpoint that appends a row
   to a lightweight DB (Supabase, per option (a) above — reuses the exact infra choice the signing-
   scoping doc already leans toward for its own serverless function, meaning both features could
   eventually share the same backend surface).
3. **A simple, admin-only page listing completions for that team code** — a plain list: employee
   identifier, module, date, pass/fail — gated by something real but minimal (a shared password per
   org to start is honest and adequate for a first pilot with one or two real customers; magic-link
   per Section 3 is the natural very-next step, not a v1 blocker).
4. **CSV export button** on that admin page — this alone is most of the "credible to an audit" value
   from Section 1, and is cheap to build once the data exists in a real DB.
5. **The four-way renewal-policy split from Section 1** modeled from day one even in v1's simple
   schema (a `renewal_months` value per module: 12 for Arbeitssicherheit, 12 for IT-Sicherheit and
   Datenschutz as a soft/configurable default, null for KI-Verordnung) — cheap to add now, expensive to
   retrofit onto existing rows later.
6. **A real (if brief) legal-review pass per Section 4** before this goes anywhere near a real paying
   customer's real employee data — not before writing the code, but absolutely before anyone's actual
   employees' actual completion records live in it.

### Explicitly deferred to v2/v3

- Self-service org signup/admin onboarding (v1 is "we set up your team code for you by hand").
- Employee-side accounts of any kind (v1 tags completions to a team code, not to a logged-in person
  beyond their local profile).
- Magic-link or any auth beyond a shared admin password (real auth is a fast follow, not a blocker).
- SSO/SAML (only once there's a real enterprise customer asking).
- A full dashboard (charts, overdue-training highlighting, per-employee history views) beyond a plain
  list + CSV — valuable, but CSV export already unlocks the audit-facing value; the dashboard is
  polish on top, not the load-bearing part.
- Automated renewal reminders/notifications (needs email infra this project doesn't have yet at all).
- Any of the buy-vs-build decision in option (c) being acted on — that's a business call for the PO,
  not something this v1 plan assumes either way.

This keeps the same discipline as the signing-scoping document's recommendation: the smallest change
that produces something *genuinely* useful (here: an auditable, exportable, cross-device completion
record an employer can actually show someone), without committing to full-accounts/SSO/dashboard
polish before it's clear the pilot has real demand.

## Sources consulted

- [Sicherheitsunterweisung im Betrieb: Pflichten & Inhalte (weka.de)](https://www.weka.de/arbeitsschutz-gefahrstoffe/sicherheitsunterweisung-eine-unternehmerpflicht/)
- [Jährliche Unterweisung Arbeitssicherheit: Ihre Pflichten (safexcon.de)](https://safexcon.de/unterweisung-arbeitssicherheit/)
- [Unterweisungen nach § 12 Arbeitsschutzgesetz (bfga.de)](https://www.bfga.de/arbeitsschutz/unterweisungen/)
- [The EU AI Act's AI literacy requirement – key considerations (Travers Smith)](https://www.traverssmith.com/knowledge/knowledge-container/the-eu-ai-acts-ai-literacy-requirement-key-considerations/)
- [Upcoming EU AI Act Obligations: Mandatory Training and Prohibited Practices (Latham & Watkins)](https://www.lw.com/en/insights/upcoming-eu-ai-act-obligations-mandatory-training-and-prohibited-practices)
- [EU AI Act Article 4: AI Literacy Obligation for Providers and Deployers (Delbion)](https://www.delbion.com/en/insights/mandatory-ai-training-eu-ai-act/)
- [NIS2-Anforderungen: Sicherheitsschulungen & Awarenesstraining (nis2-umsetzung.com)](https://nis2-umsetzung.com/nis2umsvoannex/8-2-sicherheitsschulungen/)
- [NIS2 Checklist & Awareness Training Guide (Guardey)](https://www.guardey.com/nis2-guide-2026/)
- [GDPR Training Requirements: What Businesses Need to Know (GDPR Local)](https://gdprlocal.com/gdpr-training-requirements/)
- [GDPR employee awareness training requirements (CyberArrow)](https://www.cyberarrow.io/blog/gdpr-employee-awareness-training-requirements/)
- [Supabase Pricing in 2026: What You'll Actually Pay (Makerkit)](https://makerkit.dev/blog/saas/supabase-pricing)
- [Database Pricing Comparison, July 2026 (buildmvpfast.com)](https://www.buildmvpfast.com/api-costs/database)
- [Database Free Tier Comparison 2026 — Supabase vs Neon vs Firebase vs Turso vs PlanetScale (agentdeals.dev)](https://agentdeals.dev/database-free-tier-comparison-2026)
- [PlanetScale Review 2026 - Features, Pricing & Alternatives (srvrlss.io)](https://www.srvrlss.io/provider/planetscale/)
- [Top 7 Employee Training Tracking Software for 2026 (TalentLMS)](https://www.talentlms.com/blog/employee-training-tracking-software/)
- [Best Corporate Learning Management Systems (LMS) of 2026 (Docebo)](https://www.docebo.com/learning-network/blog/corporate-learning-management-systems/)
- [Compliance Schulung: Anbieter und Themen (iSpring)](https://www.ispringlearn.de/blog/compliance-schulung)
- [SoSafe ergänzt Plattform um Datenschutz-Module (SoSafe)](https://sosafe-awareness.com/company/press/sosafe-offers-data-protection-training/)
- [Compliance E-Learning für Unternehmen (Mitarbeiterschule.de)](https://mitarbeiterschule.de/)
- [Compliance Suite Business (Reteach)](https://www.reteach.com/compliance-suite/)
- [Magic Links vs OTP: Picking the Passwordless Fallback (CIAM Compass)](https://guptadeepak.com/ciam-compass/guides/magic-links-vs-otp/)
- [Customer portal authentication options: SSO, magic links, and invite-only access (Supportbench)](https://www.supportbench.com/customer-portal-authentication-sso-magic-links-invite-only-access/)
- [User Authentication Best Practices for B2B SaaS in 2026 (Security Boulevard)](https://securityboulevard.com/2026/05/user-authentication-best-practices-for-b2b-saas-in-2026-a-security-engineers-checklist/)
- Existing repo context: `docs/open-badges-signing-scoping.md`, `BACKLOG.md` (DN-12, DN-44 entries),
  `app/app.js` (profile switcher / `recordCompletion()` / `credentialJsonDoc()`).
