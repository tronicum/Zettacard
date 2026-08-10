# Scoping: Antitrust/Kartellrecht + KYC/AML — Enterprise Compliance Modules

Status: research complete, no PO decision yet on build order/pricing model. Written after the PO's
"let's go hard on compliance courses... banks and financial services companies would probably also pay
a premium for such stuff" direction (2026-08-10), aimed specifically at large-corporation buyers rather
than the individual/small-business-leaning positioning of the existing 5 compliance modules. Every
factual/legal claim below is WebSearch-verified via two dedicated research passes (2026-08-10), sources
listed inline and at the end of each section — see `docs/compliance-business-case.md` and
`claude/compliance-competitor-pricing-and-course-gaps.md` (Claude Project doc) for the prior research
this builds on.

## 0. The ask, distilled

Two new course candidates, both explicitly framed by the PO as high-value/premium enterprise targets:

1. **"Monopoly compliance"** → antitrust/competition-law compliance (German: Kartellrecht) — training to
   prevent price-fixing, market/customer allocation, bid-rigging, and abuse-of-dominance violations.
2. **"Know Your Customer" (KYC)** → anti-money-laundering/customer-due-diligence compliance for banks and
   financial-services companies (German: Geldwäschegesetz/GwG obligations).

The premise to test: do large corporations (and specifically banks/financial-services companies for #2)
have a strong enough legal/financial incentive to pay a real premium for this, versus the existing
modules' more consumer/SME-leaning pricing?

## 1. Antitrust / Kartellrecht — legal basis and urgency

**No explicit statutory training mandate** — this is the key difference from Arbeitssicherheit (DGUV V1's
"at least annually") and GwG/KYC below. The substantive law (Art. 101/102 TFEU, §1 GWB cartel
prohibition, §19 GWB abuse of dominance) doesn't require periodic training. What the law DOES provide:

- **§81d GWB** (10th GWB amendment, 2021) lets the Bundeskartellamt/courts weigh "appropriate and
  effective precautions to prevent and detect violations" when setting fines — discretionary, not
  mandatory ([FGS](https://www.fgs.de/en/news-and-insights/blog/detail/kartellbussgeldrecht-nach-der-10-gwb-novelle)).
- The **Bundeskartellamt's own compliance guidance** lists "staff selection, training, and monitoring" as
  one of nine recommended (not mandatory) building blocks, explicitly scaled to company size
  ([Baker Tilly](https://www.bakertilly.de/beitrag/kartellrechtliche-compliance-bundeskartellamt-erlaeutert-sein-verstaendnis-der-standards-effektiver-compliance)).
- **§125 GWB "Selbstreinigung"**: a company excluded from public tenders after a cartel finding (via the
  Wettbewerbsregister) can only regain tender eligibility by demonstrating preventive measures —
  training/awareness programs are explicitly named as one such measure
  ([Deloitte Legal](https://www.deloittelegal.de/dl/de/services/legal/perspectives/wettbewerbsregister-compliance-selbstreinigung.html)).

**Honest positioning**: this is a fine-mitigation/tender-eligibility story, not "the law requires you to
train staff every year." Marketing copy should say "reduces fine exposure and is a Bundeskartellamt/court-
recognized mitigating factor" — not "legally mandated."

**Recent urgency signals** (real, current, good sales hooks, but enforcement-driven rather than new-law-
driven):
- €60.3m road-construction bid-rigging fine, Germany, Aug 6 2026 — coded communications ("beer prices,"
  "hotel costs") over public infrastructure tenders
  ([cosinex](https://blog.cosinex.de/2026/08/06/strassensanierung-603-millionen-euro-bussgeld-wegen-submissionsabsprachen/)).
- €458m EU automotive-recycling cartel fine, April 2025 (VW, Renault/Nissan, Stellantis, ACEA)
  ([EU Commission](https://germany.representation.ec.europa.eu/news/kartellrecht-kommission-verhangt-geldbussen-hohe-von-458-millionen-euro-gegen-automobilhersteller-2025-04-02_de)).
- First-ever EU labour-market cartel fine: Delivery Hero/Glovo, €329m, June 2025, for no-poach agreements
  — signals HR/recruitment coordination is now a live antitrust risk, a genuinely new angle most existing
  training libraries won't yet cover ([Goodwin](https://www.goodwinlaw.com/en/insights/publications/2025/08/alerts-practices-antc-eu-issues-first-fines-for-labour-market-cartel)).

**Competitive landscape**: mirrors the whistleblower-training pattern — law-firm seminars price per-person-
per-event (Beck-Akademie: **€499+VAT for a half-day session**), while e-learning vendors (lawpilots, WEKA)
offer micro-courses with opaque/quote-based pricing. No disclosed cheap, transparent-pricing e-learning
competitor found. **Real gap for a transparently-priced quiz product.**

**Buyer profile**: NOT exclusively large-corporation — Bundeskartellamt guidance explicitly scales
expectations to company size, so SMEs are plausible buyers too. Highest-risk/highest-motivation sectors:
construction/civil engineering (recurring bid-rigging pattern), automotive/supply chain, chemicals,
food/retail distribution, and now HR/recruitment functions generally post-Delivery Hero. Target seats:
sales, marketing, procurement/tendering, and management staff specifically (not the whole workforce
uniformly, unlike GDPR/Arbeitssicherheit).

**Price signal**: no antitrust-specific per-seat pricing disclosed anywhere. General B2B compliance
e-learning benchmarks: $5–17/employee/month, or $60–200/employee/year
([Coggno](https://coggno.com/blog/compliance-training-pricing-2026/)). The €499/session law-firm seminar
price is the strongest anchor for "what buyers are already used to paying per person" — a lot of headroom
above a typical €5-20 per-seat e-learning price if positioned as "the accessible alternative to a €499
seminar," not just "cheaper than free."

## 2. KYC/AML (Geldwäschegesetz) — legal basis and urgency

**Yes — explicit statutory training mandate, unlike antitrust.** §6(2) Nr. 6 GwG requires obligated
entities ("Verpflichtete") to ensure staff are made aware of money-laundering/terrorist-financing
typologies and are trained "initially and on an ongoing basis" ("erstmalig und danach fortlaufend").
BaFin guidance confirms this covers **almost all employees**, not just designated AML officers — only
staff with no connection to the core business (e.g. cleaning staff) are exempted
([Cash.](https://www.cash-online.de/a/fortbildungspflicht-im-bereich-geldwaesche-das-betrifft-fast-alle-mitarbeiter-551697/)).
E-learning is explicitly permitted ("IT-gestützte Schulungsprogramme"). **Caveat**: the exact numeric
frequency (annual, etc.) isn't spelled out verbatim in the statute text itself — it's "initial + ongoing,"
operationalized as effectively-annual by supervisory practice; the primary gesetze-im-internet.de source
text itself was blocked by robots.txt during this research pass and should be directly re-checked before
using in binding marketing copy.

**Buyer universe is much broader than "banks"**: §2 GwG's "Verpflichtete" list includes credit
institutions, financial service providers (incl. crypto-asset service providers), payment/e-money
institutions and their agents, insurers (life + specific lines), asset managers, lawyers/notaries (defined
transactions), tax advisors/auditors, corporate service providers, real estate brokers, gambling operators,
and goods/art dealers (~16 sectoral categories) — banks are one segment among many, and fintechs/crypto
firms are plausibly under-served, newer buyers with less-established compliance-training habits.

**Recent urgency signals**:
- New EU AML package: **AMLR (Regulation)** + **AMLD6 (Directive)** adopted, phasing in toward 2027, plus
  the new **AMLA (Anti-Money Laundering Authority)**, based in Frankfurt, operational with a 2026-2028
  work programme — direct EU-level supervision of large cross-border banks is new
  ([Freshfields](https://www.freshfields.com/en/our-thinking/blogs/risk-and-compliance/unveiling-amlas-blueprint-a-snapshot-of-the-2026-2028-work-programme-and-key-re-102mm45)).
- **Deutsche Bank**: €23.05m BaFin fine, March 2025, for AML risk-management shortcomings
  ([RegLab](https://www.reglab.com/en/news-overview/bafin-fines-deutsche-bank-for-aml-shortcomings)).
- **Varengold Bank**: €3.3m fine (confirmed Aug 2025) + €500k coercive fine (Feb 2025) for failing to file
  suspicious-transaction reports and processing prohibited Iran-linked transactions
  ([Fincrime Central](https://fincrimecentral.com/varengold-bank-money-laundering-fine-bafin/)).

**Competitive landscape**: a real, directly comparable German competitor already validates the exact
low-cost, high-volume model Zettacard would pursue — **exkulpa's GwG e-learning: €36/person (1-20 users),
€30/person (21-50 users), quote-gated above 51**
([exkulpa](https://exkulpa.de/akademie/gwg-schulung-fuer-mitarbeiter/)). Other German vendors: B.ISI 360,
pequris, mitarbeiterschule.de, Kerberos Compliance, S+P Unternehmerforum (seminar side). Enterprise-suite
side (ComplyAdvantage, Deloitte AML Academy, Diligent) bundles training into transaction-monitoring
platform contracts, quote-gated. Individual ACAMS/CAMS certification (~$2,740+ first year) is a career
credential for individual compliance professionals, not a mass-seat comparator.

**Evidence banks pay a premium**: Coggno's 2026 benchmark reports financial-services/credit-union
organizations average **~$1,097/employee/year** on training generally (credit unions highest at
$1,331/year) — markedly above construction, healthcare, manufacturing, retail
([Coggno](https://coggno.com/blog/lms/compliance-training-cost-per-employee-2026-industry-benchmarks-construction-healthcare-manufacturing-retail/)).
This is total training spend, not KYC-specific, so directional not exact — but it does support the PO's
instinct that financial-services buyers spend more than other sectors.

**Recommended price anchor**: **€25-50/employee/year** for bulk/enterprise licensing — matches the direct
exkulpa comparable, plausibly at a modest premium given financial-services' demonstrated willingness to
spend more generally, with volume discounts for large bank headcounts (hundreds to thousands of
front-line/onboarding staff, not just the compliance department).

## 3. Comparison table

| | Antitrust/Kartellrecht | KYC/AML (GwG) |
|---|---|---|
| Explicit legal training mandate | No (fine-mitigation/tender-eligibility incentive only) | Yes (§6(2) Nr. 6 GwG, "initial + ongoing") |
| Buyer universe | Any company, esp. construction/automotive/chemicals/retail + now HR functions | ~16 GwG "Verpflichtete" categories - banks, fintech, crypto, insurers, real estate, lawyers/notaries, etc. |
| Target seats within a company | Sales/marketing/procurement/management (targeted, not whole workforce) | Almost all employees (broad, per BaFin guidance) |
| Direct low-cost e-learning competitor found | No (only opaque-priced micro-courses + expensive seminars) | Yes (exkulpa, real published tiered pricing) |
| Urgency driver | Enforcement volume + novel scope (no-poach/HR) | New statute-adjacent mandate (§6 GwG) + new EU supervisory body (AMLA) + recent bank fines |
| Suggested price anchor | Position against €499/seminar-session norm; per-seat e-learning price TBD, real headroom above typical €5-20 | €25-50/employee/year (direct comparable) |

**Read**: KYC/AML has the stronger, cleaner "real legal requirement" pitch and a validated direct
competitor pricing model to anchor against — the safer, faster-to-market bet. Antitrust has a weaker legal-
mandate story (must be marketed honestly as risk-mitigation, not compliance-mandatory) but a bigger price
gap to exploit (€499/session seminar norm vs. cheap e-learning) and zero disclosed direct e-learning
competitor pricing, which is either whitespace or a sign nobody's found a working model there yet.

## 4. Content structure (draft, both modules, pending PO build-order decision)

Following the same schema every other compliance module already uses (`data/*_pilot.json`, question/
correct-option/explanation/legal_basis/roles fields, `split_module()` in `data/build_modules.py`,
`TOPIC_LABELS`/`COMPLIANCE_MODULES` entries in `app.js`), 20-question DE/EN pilot first (matching the
Hinweisgeberschutz launch pattern), scaled to 40 questions/12 locales only after PO sign-off, per this
project's established pilot-then-scale discipline.

**Antitrust/Kartellrecht candidate topics** (5, mirroring the existing modules' 5-topic structure):
1. Grundlagen: was ist ein Kartell (§1 GWB, Art. 101 TFEU basics - horizontal/vertical agreements)
2. Preisabsprachen und Marktaufteilung (price-fixing, customer/market allocation, bid-rigging)
3. Marktbeherrschung und Missbrauch (§19 GWB abuse of dominance)
4. Verhalten bei Wettbewerberkontakten (trade associations, benchmarking, information exchange red flags)
5. Folgen von Verstößen und Compliance-Programme (fines, §125 GWB Selbstreinigung, whistleblowing overlap
   with the existing Hinweisgeberschutz module - a genuine cross-sell angle)

**KYC/AML candidate topics** (5):
1. Grundlagen der Geldwäsche (what money laundering is, the 3-stage model, §2 GwG "Verpflichtete" scope)
2. Kundensorgfaltspflichten / KYC-Prozess (customer due diligence levels, identification requirements)
3. Verdachtsmeldewesen (suspicious-activity detection and reporting duties, FIU Germany)
4. Verstärkte Sorgfaltspflichten (enhanced due diligence - PEPs, high-risk countries, complex/unusual
   transactions)
5. Sanktionen und Folgen (BaFin enforcement, recent fine examples, individual/institutional consequences)

## 5. Open questions for the PO

1. **Build order**: both simultaneously, or KYC/AML first (cleaner legal-mandate story, validated direct
   competitor pricing, single clearest "banks pay a premium" narrative)?
2. **Pricing model**: every existing compliance module currently ships at the same 0€-for-the-quiz-content
   MVP posture as the rest of the app (per `docs/paid-verifiable-certificates-scoping.md`'s "MVP ships at
   0€" decision) — does the PO want these two new modules to break from that and actually charge a
   per-seat/per-employee licence fee from day one, given the explicit "premium" framing? If so, that's a
   genuinely new business-model decision (invoicing, seat management, account/team features), not just a
   content question - see `docs/business-team-features-scoping.md` for what that would require.
3. **Legal review pass**: per the PO's own instruction, a dedicated legal-review pass (planned via a
   `fable`-model agent, run once real question content exists to review, not on this scoping doc) should
   happen before either module ships - same discipline as DN-12's existing legal-review gate for the other
   compliance modules. Scheduling this for after the pilot content is drafted, not before, since there's
   nothing substantive to review yet.
4. Should antitrust be marketed with the honest "risk-mitigation, not legal mandate" framing from Section 1,
   or does the PO want a softer/different positioning given it's less clean a pitch than KYC/AML?

## Sources

All URLs cited inline above; full research transcripts available in this session's two research-agent
dispatches (antitrust/Kartellrecht pass and KYC/AML pass, both 2026-08-10).
