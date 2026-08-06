# Business Case: Is Zettacard's Compliance-Training Side a Real Business?

Status: research/business-scoping only. Nothing here is a decision, a commitment, or legal advice — see
Section 4 for an explicit statement on that. Written for the product owner to decide whether it's worth
investing more real time (content depth, the team/account features scoped in
`docs/business-team-features-scoping.md`, sales) into the four compliance modules (Datenschutz,
Arbeitssicherheit, KI-Verordnung/AI Act, IT-Sicherheit), versus leaving them as a free extra alongside the
driving/fishing-license content. Every factual claim below is WebSearch-verified as of 2026-08-06, with
sources listed inline and collected at the end; nothing is asserted from model training-data memory alone,
because two of the four legal drivers here (NIS2, the AI Act) have changed meaningfully since any model's
training cutoff and getting them wrong in a document meant to justify *selling* compliance training would
be its own kind of embarrassing.

## 1. Is there a real, current legal push behind these four topics?

Yes, and it's more concrete than "GDPR is a thing" hand-waving — three of the four have a specific,
datable legal event within the last nine months of this document's writing, which is unusually good timing
if Zettacard wanted to move on this.

**NIS2 in Germany is no longer "coming soon" — it's already law.** The NIS2-Umsetzungsgesetz passed the
Bundestag on 13 November 2025, the Bundesrat on 21 November 2025, was published in the
Bundesgesetzblatt on 5 December 2025, and entered into force on **6 December 2025** — with, notably, no
transition period, meaning risk-management measures, incident-reporting duties, and management-liability
exposure applied immediately, not on some future phase-in date ([DNV](https://www.dnv.de/news/2025/nis-2-umsetzungsgesetz/);
[Heuking](https://www.heuking.de/en/news-events/newsletter-articles/detail/get-ready-nis2-implementation-act-in-germany-in-force.html)).
Roughly 29,500 German companies fall into the "essential" or "important" entity categories the law
targets, and the BSI's registration portal opened 6 January 2026 with a registration deadline of
6 March 2026 ([nisd2.eu](https://nisd2.eu/en/wiki/timelines-and-status/nis2-in-germany)) — both already in
the past relative to today's date, so any affected company that hasn't registered is already overdue, which
is exactly the kind of anxiety that turns into training-budget line items. The training obligation itself
sits in the NIS2 implementing annex rather than the headline law: **NIS2UmsVO Annex 8.2** requires
"regelmäßig" (regular) security-awareness training for personnel in security-relevant roles, with no fixed
statutory cadence — annual is the de facto convention, not a hard number
([nis2-umsetzung.com](https://nis2-umsetzung.com/nis2umsvoannex/8-2-sicherheitsschulungen/)). This is the
same conclusion the sibling `docs/business-team-features-scoping.md` document already reached
independently, and it holds up on a second pass.

**The EU AI Act's Article 4 AI-literacy obligation has technically been in force since 2 February 2025, but
2 August 2026 is when it actually gets teeth** — that date is *four days before this document was written*.
Article 4 requires providers and deployers of AI systems to ensure "a sufficient level of AI literacy"
among staff (not just technical staff — anyone operating, or affected by, an AI system), scaled to role,
risk, and existing knowledge, with no fixed curriculum mandated
([Travers Smith](https://www.traverssmith.com/knowledge/knowledge-container/the-eu-ai-acts-ai-literacy-requirement-key-considerations/)).
What changes on 2 August 2026 specifically is that national market-surveillance authorities gain the
formal supervisory power to actually enforce it, and the rest of the Act's non-high-risk obligations become
applicable alongside it — meaning the window where this was a paper obligation nobody was checking has just
closed ([letscopilot.com](https://letscopilot.com/article-4-of-the-eu-ai-act-what-changes-on-sunday-2-august-2026/)).
For a compliance-training product, this is close to ideal timing: the obligation is universal (any company
using AI tools, which by 2026 is nearly all of them), genuinely new (most companies have no existing AI
literacy program the way they have decades-old GDPR or safety training habits), and just became
enforceable, all at once.

**Datenschutz (GDPR)** has no numbered training-frequency requirement, but Art. 39(1)(b) explicitly tasks
the DPO with staff "awareness-raising and training," and Art. 32(1)'s "appropriate technical and
organisational measures" language is widely read (including by the EDPB, which frames training as "a
continuous function rather than a one-time event") as requiring recurring, not one-off, training
([GDPR Local](https://gdprlocal.com/gdpr-training-requirements/)). This is the most mature, most
"expected/normalized" of the four — also the most competitively crowded, see Section 2.

**Arbeitssicherheit** is the one with an unambiguous, decades-old, numbered statutory requirement:
ArbSchG § 12 establishes the employer's duty to instruct staff, and **DGUV Vorschrift 1 § 4 operationalizes
it as "mindestens einmal jährlich"** — at least once a year, with shorter intervals for minors and
higher-hazard roles ([safexcon.de](https://safexcon.de/unterweisung-arbeitssicherheit/);
[bfga.de](https://www.bfga.de/arbeitsschutz/unterweisungen/)). This is the least "new news" of the four
(everyone has known about this for years), but it's also the most reliably recurring revenue driver of the
four if training records genuinely need refreshing every twelve months by law, not by convention.

The upshot: three of the four modules have a real, current, legally-grounded reason a company should be
buying training right now, not a hypothetical future one — and two of those three (NIS2, AI Act) are
recent enough that most existing training vendors' content libraries may not have fully caught up either,
which is a real if narrow window of opportunity rather than a crowded, settled market on those two specific
topics.

## 2. Who else is already selling this, and at what price

The honest headline: **this is not an empty market. It's a real, moderately-to-highly crowded one, and
Zettacard would be entering behind established, well-funded players**, not first-to-market.

Global market size for e-learning/compliance corporate training was estimated at roughly **USD 128.7
billion in 2025**, forecast to grow at a **22% CAGR through 2034**; Europe is estimated at roughly 26% of
that (~USD 33.5B), and Germany specifically at roughly 9% of the global figure (~USD 3B in 2025), with the
German market characterized as "regulation-focused," concentrated in manufacturing and other regulated
industries ([Fortune Business Insights](https://www.fortunebusinessinsights.com/e-learning-compliance-corporate-training-market-103729)).
These are broad-strokes market-research-firm numbers (the kind that should be treated as an order-of-
magnitude signal, not a precise figure to build a financial model on), but the direction is unambiguous:
this is a large, fast-growing, already-well-served market, not an underserved niche.

**SoSafe** (German-headquartered, the most directly comparable competitor given it's explicitly
German-market-native and has expanded from pure security-awareness into Datenschutz modules) uses a
degressive per-seat pricing model across four tiers (Essential/Professional/Premium/Ultimate) — exact
numbers are quote-gated, not published, but the tier structure shows the real competitive shape: basic
training content is table stakes even at the entry tier, while phishing simulation, role-based training,
analytics ("Human Risk OS"), and API integration are what higher tiers actually charge more for
([SoSafe pricing](https://sosafe-awareness.com/pricing/)). **usecure** is similarly quote-gated but
transparent about its bundle: per-user/per-month billed annually, and — notably — the product isn't just
training content, it's training *plus* phishing simulation (uPhish), breach monitoring (uBreach), and
policy-acceptance tracking (uPolicy) as one integrated suite
([usecure pricing](https://usecure.io/pricing)). **KnowBe4**, the US-based category leader, has one
published data point — a base license reportedly starting around **$3,665/year** — but otherwise pricing is
"contact us," varying by seat count and contract
([ITQlick](https://www.itqlick.com/knowbe4/pricing)). **Mitarbeiterschule.de** and **Reteach** are
German-market compliance e-learning/training-management platforms explicitly targeting the same
Datenschutz/Arbeitssicherheit space Zettacard's modules cover, and general-purpose corporate LMS platforms
(TalentLMS, Docebo, iSpring Learn — the last of which markets a German-language compliance product
directly) round out the field.

The pattern across every competitor above is the same, and it's the single most important competitive fact
for this document: **none of them are selling "quiz content."** They're selling the tracking, reporting,
phishing-simulation, and audit-evidence layer *around* training content — the content itself is close to a
commodity in this market. Zettacard today has good content (12-language, WebSearch-cited legal-basis
questions across all four topics) and literally none of that surrounding layer — no accounts, no
per-employee completion tracking visible to an employer, no CSV export, no phishing simulation, no policy-
acceptance workflow. `docs/business-team-features-scoping.md` scopes exactly the smallest real version of
the tracking layer and is honest that it doesn't exist yet. This means Zettacard's current free/personal-use
build is not competitive with any of these vendors *as a B2B product* today — it would need the
account/tracking layer just to be in the same conversation, and even then would be a genuinely new,
unproven entrant against companies with years of enterprise sales relationships and, in KnowBe4's and
SoSafe's cases, real venture funding and hundreds of employees.

Where Zettacard is genuinely differentiated, and it's a real if narrow angle: **12-language parity across
all four modules out of the box**, and **the driving/fishing-license content living in the same app** — no
competitor above straddles consumer personal-license exam prep and B2B compliance training in one product.
Whether that's a strength (cross-sell, broader brand recognition, "the app my employees already have on
their phone for their Führerschein") or a confusing muddle (a B2B buyer wondering why a fishing-license app
is pitching them GDPR training) is a genuine open question, not a settled advantage — flagged honestly
rather than spun.

## 3. Revenue model options

**(a) B2B per-seat/per-month SaaS subscription**, sold directly to SMBs needing to demonstrate training
coverage. Pro: matches the market's dominant model (every competitor above prices this way), predictable
recurring revenue, aligns naturally with the annual-renewal cadence Arbeitssicherheit and (informally)
Datenschutz/IT-Sicherheit already have. Con: requires the full account/tracking/admin layer
(`docs/business-team-features-scoping.md`'s entire scope) before it's sellable at all, requires a real sales
motion this project has never done, and competes head-on against funded incumbents on their home turf — the
hardest version of this to win.

**(b) Freemium personal use (current model) + a separate paid "business" tier** with the team/admin
features. Pro: doesn't abandon the existing free-user base or 12-language investment, lets the personal
product keep growing organically while the business tier is built and validated incrementally — directly
the shape `docs/business-team-features-scoping.md`'s v1 recommendation (team codes, CSV export, no
accounts yet) already assumes. Con: still needs that same backend/tracking work as (a) before any revenue
exists; "freemium converts to paid" is a notoriously low-conversion motion without a strong wedge, and
compliance-training buyers are typically employers, not individual employees who'd self-upgrade.

**(c) B2B2C via partnerships** — selling through existing HR/compliance consultancies, or bundling into a
company's existing HR-software stack, rather than selling to end employers directly. Pro: leans on
someone else's existing customer relationships and sales trust rather than building a sales function from
scratch; consultancies and HR platforms are exactly the buyers who'd value ready-made, well-translated
content without building it themselves. Con: margin gets shared or compressed, and Zettacard becomes
dependent on a partner's roadmap and relationship — the same lock-in risk
`docs/business-team-features-scoping.md`'s option (c) flags for the tracking-backend "buy vs. build"
question, mirrored here on the go-to-market side.

**(d) White-label/licensing the content+platform** to training providers (LMS vendors, HR consultancies,
even one of the competitors above) who want a modern, 12-language, mobile-first product without building
one. Pro: monetizes exactly the asset Zettacard genuinely has today (verified multilingual content, working
quiz/exam/certificate infrastructure) without needing to build the account/tracking layer or run any sales
motion at all — the license buyer handles distribution and their own tracking layer. Con: caps upside (a
content licensing deal is worth much less than owning the end-customer relationship), and requires the
content to survive real due diligence from a sophisticated buyer, which raises the bar on the legal-review
gap in Section 5 rather than lowering it.

None of these four is obviously "the" answer from research alone — (d) is the lowest-effort, lowest-risk
way to test whether the content itself has commercial value before committing to (a)/(b)'s much larger
build, and is the most consistent next step given today's actual codebase state (Section 5).

## 4. Legal/liability considerations of monetizing this — and an explicit non-legal-advice notice

If a business pays for and relies on Zettacard to demonstrate its employees are trained — for an auditor,
a regulator, or in the event of an incident or accident — the stakes for getting the content wrong shift
qualitatively. Today, wrong or incomplete free practice-question content is a quality bug. The moment
someone pays specifically because they're relying on it for compliance evidence, wrong or incomplete
content becomes something a company could point to as the reason their compliance program failed — and
Zettacard, as the vendor whose product they relied on, would be a natural target of that argument.
Standard practice in this space (visible in every competitor's public terms, though this document did not
attempt a full contract-law review) is some combination of: explicit disclaimers that the training
supplements rather than replaces the employer's own legal compliance program and judgment; limitation-of-
liability clauses capping vendor exposure (typically to fees paid); express statements that content is
"believed accurate" but not warranted as legally complete or current; and — critically — clear allocation
that the *employer*, not the vendor, remains the party legally responsible for its own regulatory
compliance (the training vendor sells a tool, not an indemnity).

**This document is a business-research summary, not legal or professional advice, and none of the above
should be read as a legal opinion on what disclaimer language would actually hold up or what liability
exposure Zettacard would actually carry.** That determination requires actual legal counsel, with real
knowledge of German and EU contract/liability law and this specific product's actual content and terms —
exactly the same posture this project's `BACKLOG.md` already takes on **DN-12** ("Professional legal review
pass on all published content... needed before any public/commercial release") and that
`docs/business-team-features-scoping.md` independently reaches on the GDPR/data-processing side of the
team-tracking feature. Monetizing compliance training specifically raises the stakes on DN-12 rather than
adding a separate concern: a paid product whose buyers are explicitly relying on it for compliance evidence
needs that legal review as a hard precondition of charging money, not as a nice-to-have that can wait until
after launch.

## 5. A realistic, staged path

**What already exists that's a genuine head start**: full 12-language content parity across all four
compliance modules at 40 questions each with WebSearch-verified legal-basis citations (per the DN-44/DN-48
backlog history); working quiz, training-mode, and exam-simulation infrastructure already gated at the
30-question exam threshold these modules clear; an existing (currently unsigned/self-issued) certificate
and Open Badges-3.0-shaped credential system, with `docs/open-badges-signing-scoping.md` already scoping
what a real, cryptographically-verifiable version would require; and a local profile-switcher pattern that,
while explicitly not an accounts system, is at least a namespacing precedent the team-account work in
`docs/business-team-features-scoping.md` can build on rather than starting from zero UX conventions.

**What's a real gap, not a detail**: zero accounts, zero backend, zero cross-device tracking of any kind —
`docs/business-team-features-scoping.md` scopes this honestly as a genuine architectural step, not a small
addition; zero payment processing; zero sales or marketing motion or existing B2B customer relationships;
and, most importantly for anything sold as compliance evidence, the content's current legal-review status
is explicitly "not reviewed" per DN-12/DN-44's backlog entries, which is a real blocker to charging money
for it under Section 4's reasoning, not a formality to route around.

**A realistic v1 pilot**: given the legal-currency analysis in Section 1, **Arbeitssicherheit and the AI
Act module are the strongest pair to lead with** — Arbeitssicherheit because it has the single clearest,
oldest, most unambiguous statutory training mandate (DGUV Vorschrift 1's annual requirement) of the four,
making the sales pitch ("you are legally required to do this every year, here's evidence you did") the
simplest to make; and the AI Act module because its enforcement window opened four days before this
document was written, meaning most buyers genuinely don't have an existing vendor relationship or habit for
it yet — the rare case of arriving early rather than late. Datenschutz is the most commoditized of the four
(hardest to differentiate against SoSafe/Mitarbeiterschule.de/Reteach, all of whom already own this
category), and IT-Sicherheit/NIS2, while newly urgent, is also the most technically demanding to keep
accurate given NIS2UmsVO's evolving implementing guidance — both are reasonable modules 3 and 4, not the
opening pitch.

Given a small team with no existing B2B sales function, **1-3 pilot customers is the realistic target for
a genuine first pass**, not a self-service launch — likely reached through a warm-intro or consultancy
partnership (option (c) above) rather than cold outbound, sized specifically so the team can hand-hold each
pilot through the "team code, no self-service" v1 that `docs/business-team-features-scoping.md` already
recommends, and so the DN-12 legal review can realistically be scoped to what a handful of real pilot
customers' actual usage would need rather than an abstract "review everything" mandate. The order of
operations that follows from everything above: get a real legal review scoped and budgeted for
specifically the Arbeitssicherheit and AI Act content (not all four modules at once — that's a bigger and
slower ask than a pilot needs), build the smallest team-tracking v1 already scoped in the sibling document,
and only then approach 1-3 real pilot customers — testing option (d)'s content-licensing angle in parallel
costs comparatively little and could validate or invalidate the whole direction faster than building the
full backend first.

## Bottom line

The legal drivers here are real and, for two of the four topics, unusually well-timed — this is not a
made-up urgency. But the competitive field is real too, well-funded, and selling a materially more complete
product (tracking, phishing simulation, audit-ready reporting) than Zettacard has today; content alone,
however good, is not what this market pays for. The honest read is that this is worth a small, deliberately
narrow next step — legal review plus a minimal tracking layer plus 1-3 hand-held pilots on the two
strongest-timed modules — rather than either a full "let's become a compliance-training company" pivot or
dismissing it outright.

## Sources

- [Get ready: NIS2 Implementation Act in Germany in force! (Heuking)](https://www.heuking.de/en/news-events/newsletter-articles/detail/get-ready-nis2-implementation-act-in-germany-in-force.html)
- [Umsetzungsgesetz der NIS-2-Richtlinie in Kraft getreten (DNV)](https://www.dnv.de/news/2025/nis-2-umsetzungsgesetz/)
- [NIS2 in Germany 2026: Deadlines, Fines & BSIG Guide (nisd2.eu)](https://nisd2.eu/en/wiki/timelines-and-status/nis2-in-germany)
- [NIS2-Anforderungen: Sicherheitsschulungen & Awarenesstraining (nis2-umsetzung.com)](https://nis2-umsetzung.com/nis2umsvoannex/8-2-sicherheitsschulungen/)
- [Article 4 of the EU AI Act: what changes on Sunday, 2 August 2026 (letscopilot.com)](https://letscopilot.com/article-4-of-the-eu-ai-act-what-changes-on-sunday-2-august-2026/)
- [The EU AI Act's AI literacy requirement – key considerations (Travers Smith)](https://www.traverssmith.com/knowledge/knowledge-container/the-eu-ai-acts-ai-literacy-requirement-key-considerations/)
- [Jährliche Unterweisung Arbeitssicherheit: Ihre Pflichten (safexcon.de)](https://safexcon.de/unterweisung-arbeitssicherheit/)
- [Unterweisungen nach § 12 Arbeitsschutzgesetz (bfga.de)](https://www.bfga.de/arbeitsschutz/unterweisungen/)
- [GDPR Training Requirements: What Businesses Need to Know (GDPR Local)](https://gdprlocal.com/gdpr-training-requirements/)
- [E Learning Compliance Corporate Training Market Size (Fortune Business Insights)](https://www.fortunebusinessinsights.com/e-learning-compliance-corporate-training-market-103729)
- [SoSafe pricing & plans (SoSafe)](https://sosafe-awareness.com/pricing/)
- [usecure Pricing](https://usecure.io/pricing)
- [KnowBe4 Pricing 2026 (ITQlick)](https://www.itqlick.com/knowbe4/pricing)
- [Compliance Schulung: Anbieter und Themen (iSpring)](https://www.ispringlearn.de/blog/compliance-schulung)
- [Compliance E-Learning für Unternehmen (Mitarbeiterschule.de)](https://mitarbeiterschule.de/)
- [Compliance Suite Business (Reteach)](https://www.reteach.com/compliance-suite/)
- Existing repo context: `BACKLOG.md` (DN-12, DN-44 entries), `docs/business-team-features-scoping.md`,
  `docs/open-badges-signing-scoping.md`
