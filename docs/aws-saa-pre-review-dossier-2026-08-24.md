# AWS Certified Solutions Architect – Associate (SAA-C03) — pre-review dossier (2026-08-24)

**Status:** AI-prepared research groundwork only — **NOT reviewed by anyone**. Not legal advice, and not a technical review either. Nobody who holds this certification has looked at the draft.

**Requested:** verify AWS's current SAA exam guide from AWS's own sources, write this dossier, and draft a first-round pilot question bank.

**Delivered:** this dossier **and** `data/aws_saa_pilot_DRAFT.json` (36 questions, EN canonical + DE + JA + ZH) plus its deterministic generator `data/gen_aws_saa_draft.py`.

**Files touched:** this file, `data/aws_saa_pilot_DRAFT.json`, `data/gen_aws_saa_draft.py`. Nothing else. `data/build_modules.py`, `data/modules_manifest.json`, `app/app.js`, `app/data/**` and `app/legal/**` are untouched; no build was run; nothing was staged or committed. The `_DRAFT` suffix keeps the pilot out of the live build path by construction, exactly as for `bewachungsgewerbe_pilot_DRAFT.json` and the other draft modules from this round.

---

## 0. The findings, first, because two of them change how the module must be described

### 0.1 SAA-C03 is multiple-choice only, so the `cka` disclaimer must NOT be carried across

`docs/cka-lab-and-cloud-cert-hands-on-scoping-2026-08-23.md` §7.1 established this for the PO yesterday. It is re-verified here independently, from AWS's own pages, on 2026-08-24:

| Fact | AWS's own words | Source |
|---|---|---|
| Question count and types | *"65 questions; either multiple choice or multiple response"* | certification product page |
| Scored vs unscored | 50 scored, 15 unscored | exam guide |
| Multiple choice | one correct response, three distractors | exam guide |
| Multiple response | two or more correct responses out of five or more options | exam guide |
| Duration | 130 minutes | certification product page |
| Price | 150 USD | certification product page |
| Passing score | **720**, on a scaled range of 100–1,000 | exam guide |
| Scoring model | compensatory — no per-domain pass requirement | exam guide |
| Hands-on component | **none anywhere in the exam** | exam guide (question types are exhaustively MC + MR) |

`cka`'s `meta.description` and its in-app intro both carry a deliberate, PO-directed disclaimer: *"the real CKA exam is 100% hands-on … this module is a concept-check, not an exam simulator."* That disclaimer is **true for CKA and false for SAA**, and copying it across would be a factual error about AWS in shipped copy. The generator has a mechanical guard against exactly that copy-paste (`main()` fails the build if any question carries the phrase "100% hands-on", "100% performance-based" or "performance-based exam").

The positive claim this module *may* honestly make is narrow and worth stating precisely: **the format is faithful** — original single-select and multi-select questions, scenario-style, distributed across AWS's published domain weightings. It is **not** a claim about coverage or about predicting the real question pool, which is confidential (§4.3) and which no third party can see.

### 0.2 SAA-C03 is still current, and the "SAA-C04" material in circulation is not AWS's

Checked directly, because the brief asked and because getting it wrong would date the module on day one. **AWS's own "Coming Soon" page** (`aws.amazon.com/certification/coming-soon/`, retrieved 2026-08-24) lists **exactly one** exam update: SysOps Administrator – Associate becoming **CloudOps Engineer – Associate** (SOA-C02 → SOA-C03, last SOA-C02 day 2025-09-29). **No SAA update, no SAA-C04, no beta.** The exam guide's own URL slug is still `solutions-architect-associate-03`, and the product page still shows the C03 format.

Meanwhile a plain web search for `"SAA-C04"` returns paid courses and blog "SAA-C04 exam guides 2026" from at least three commercial vendors. **None of those is AWS.** Recorded here as a standing rule for the next agent: *do not take a vendor blog's word for an exam version.* Check AWS's Coming Soon page and the exam guide's own URL. This is the same discipline the Bewachungsgewerbe dossier §6 arrived at from the other direction — read the instrument, not the commentary.

### 0.3 The licensing analysis is materially different from `cka`'s, and the difference is the whole reason this module is safe

This is the one place where an agent coming from the `cka` round would go wrong by analogy. Set out in full at §5.

---

## 1. Method and instruments read

All retrieval **2026-08-24**, by `WebFetch` against AWS's own hosts (`aws.amazon.com`, `docs.aws.amazon.com`). Domain weightings and task statements were read in **both** the HTML exam guide and the PDF exam guide, independently, and agreed.

| Instrument | Retrieved from | What was read |
|---|---|---|
| **SAA-C03 Exam Guide (HTML)** | `docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html` | exam code, 50 scored + 15 unscored, question-type definitions, 720/1,000, the four domains and their weightings |
| **SAA-C03 Exam Guide (PDF)** | `docs.aws.amazon.com/pdfs/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.pdf` | the same, **plus** all fourteen task statements, read as a cross-check on the HTML |
| **Certification product page** | `aws.amazon.com/certification/certified-solutions-architect-associate/` | 65 questions, MC/MR, 130 minutes, 150 USD |
| **AWS Certification Coming Soon** | `aws.amazon.com/certification/coming-soon/` | currency check — see §0.2 |
| **AWS Certification Agreement** | `aws.amazon.com/certification/certification-agreement/` | confidentiality of Credential Assessment Materials; the ban on disclosing exam content |
| **AWS Site Terms** | `aws.amazon.com/terms/` | ownership of AWS Site content; the limited personal-use licence; the express exclusion of commercial and derivative use |
| **AWS Trademark Guidelines** | `aws.amazon.com/trademark-guidelines/` | nominative fair use; the educational-use sentence; the no-affiliation rule |
| **15 AWS service documentation pages** | `docs.aws.amazon.com/...` | the substantive answer verification — itemised at §3 |

**Deliberately not opened, not read, not cited for anything:** every commercial exam-prep vendor, "dump"/recalled-question site, paid course and third-party book that dominates the search results for this topic. Several appeared in search results and were **not fetched**. AGENTS.md constraint 1 bans third-party exam-prep companies' text outright, and unlike the StVO sign-icon carve-out there is no visual-accuracy exception that could ever apply to a question bank. AWS Skill Builder's own practice questions were also not used — they are AWS's, but they are *practice-exam content*, which is precisely the category §4.3 says to stay away from.

---

## 2. The exam's structure — the Tier A spine of the module

### 2.1 Domains and weightings, verbatim from the exam guide

| # | Content domain | Weight | Task statements |
|---|---|---|---|
| 1 | Design Secure Architectures | **30%** | 1.1 Design secure access to AWS resources · 1.2 Design secure workloads and applications · 1.3 Determine appropriate data security controls |
| 2 | Design Resilient Architectures | **26%** | 2.1 Design scalable and loosely coupled architectures · 2.2 Design highly available and/or fault-tolerant architectures |
| 3 | Design High-Performing Architectures | **24%** | 3.1 Storage · 3.2 Compute · 3.3 Database · 3.4 Network · 3.5 Data ingestion and transformation |
| 4 | Design Cost-Optimized Architectures | **20%** | 4.1 Storage · 4.2 Compute · 4.3 Database · 4.4 Network |

Two things about this table are worth flagging to anyone drafting from memory rather than from the guide:

- **Security is the largest domain, not resilience.** The intuitive ordering ("resilient architectures" first, because that is how the certification is usually described) is wrong: Design Secure Architectures carries 30%, the single largest share. The draft's distribution follows the published weights, not the intuition.
- **The exam guide's own caveat:** it states that it *"does not provide a comprehensive list of the content on the exam."* The task statements are a floor on scope, not a ceiling. Same structural caveat as Anlage 2 BewachV in the Bewachungsgewerbe round (§3.3 there) — worth remembering before anyone markets this module as "full coverage."

### 2.2 Scoring — and a trap for the in-app pass threshold

AWS scores 100–1,000 with **720 to pass**, on a **compensatory** model. A scaled score is **not** a percentage of questions answered correctly and cannot be converted into one; 720/1000 is **not** "72%". The draft's `meta.pass_rule_note` says so explicitly, because the app's existing modules all carry percentage thresholds and the obvious mistake is to print "72% to pass" on the module card. Any threshold shown for this module is a **Zettacard practice threshold** and has to be labelled that way.

---

## 3. Answer verification — what was actually checked, and the one thing it caught

Every correct answer in the draft was verified against AWS's own service documentation on 2026-08-24. Fifteen pages were fetched and read; each question's `legal_basis` field names the page its answer rests on. The load-bearing checks:

| Verified fact | AWS's own wording (abbreviated) | Used by |
|---|---|---|
| Gateway VPC endpoints exist for **S3 and DynamoDB only**; **no additional charge**; endpoint route wins by longest prefix match over `0.0.0.0/0` | *"Gateway VPC endpoints provide reliable connectivity to Amazon S3 and DynamoDB…"* / *"There is no additional charge for using gateway endpoints."* | secure-04, cost-05 |
| RDS Multi-AZ **DB instance** standby is **not readable** | *"You can't use a standby replica to serve read traffic."* | resilient-03 |
| A NAT gateway is **zonal**, redundant only within its own AZ | *"To improve resiliency, create a NAT gateway in each Availability Zone…"* | resilient-04 |
| Security group vs network ACL: allow-only/stateful/instance-level vs allow-and-deny/stateless/subnet-level, ordered evaluation | AWS's own comparison table | secure-05 |
| Aurora: **up to 15** replicas, **shared cluster volume**, automatic promotion | *"An Aurora DB cluster can contain up to 15 Aurora Replicas."* | resilient-07 |
| gp3 includes **3,000 IOPS / 125 MiB/s** at any size and **does not use burst performance**; gp2 baseline is **3 IOPS per GiB**, bursting to 3,000 | *"gp3 volumes do not use burst performance."* | performance-02 |
| S3 storage classes: Standard-IA / One Zone-IA **30-day** minimum, Glacier Instant Retrieval / Flexible **90-day**, Deep Archive **180-day**; One Zone-IA is **1 AZ**; Intelligent-Tiering has **no retrieval fee and no minimum duration** | storage-class comparison table | cost-01, cost-02, cost-06 |
| Single `PUT` is limited to **5 GB**; multipart covers 5 MB – 50 TB | *"With a single PUT operation, you can upload a single object up to 5 GB in size."* | performance-09 |
| Global Accelerator gives **two static anycast IPv4 addresses** (four for dual-stack) from the AWS edge network | what-is page | performance-04 |
| SCPs **grant nothing** and **do not affect the management account** | *"No permissions are granted by an SCP."* / *"SCPs don't affect users or roles in the management account."* | secure-03 |
| Compute Savings Plans apply *"regardless of instance family, instance size, OS, tenancy, or AWS Region"* and cover **Fargate and Lambda** | Savings Plans user guide | cost-03 |
| Lambda **provisioned** concurrency = pre-initialised environments (cold-start fix, chargeable, version/alias only); **reserved** concurrency = a both-ways bound on concurrency, no charge, no pre-warming | provisioned-concurrency page | performance-05 |
| Spot interruption notice is issued **two minutes** before stop/terminate (hibernation excepted) | interruption-notices page | cost-04 |

### 3.1 The check that earned its keep: an ACM claim that has gone stale

The first draft of question `aws-saa-secure-10` asserted, as most SAA material still does, that *"the private key of an ACM public certificate cannot be exported, so this option is impossible."*

**That is no longer true.** `docs.aws.amazon.com/acm/latest/userguide/export-public-certificate.html` states that **ACM public certificates created on or after 17 June 2025 can be exported**, private key included, via console, CLI (`export-certificate`) or API, and `acm-exportable-certificates.html` records that *"You are subject to an additional charge for exportable public SSL/TLS certificates."* Exportability is chosen when the certificate is requested; it does not retroactively apply to an existing certificate.

The question was rewritten. The correct answer did not change (set the target group protocol to HTTPS and put a certificate on the instances — the ALB encrypts to the target but does not validate its chain, which is why a private-CA or self-signed certificate is acceptable), but the *reasoning* did: the distractor now fails because an **ordinary** ACM public certificate is not exportable and because reusing the internet-facing certificate on the backend is not how backend encryption is configured, rather than because export is impossible.

**Recorded as a lesson, not a footnote.** This is precisely the failure mode a vendor-specific technical module invites: a fact that was true for years, is repeated everywhere, and quietly stopped being true. It is also an argument for the six-month re-verification interval at §7 rather than the twelve-to-thirty-six-month intervals the statute-based modules use.

---

## 4. Sourcing safety — why this module is buildable without touching proprietary material

### 4.1 What is being used, and what kind of thing it is

The module rests on two AWS-owned sources and nothing else:

1. **The public exam guide.** It supplies the exam code, question counts, question-type definitions, duration, passing score, the four domain names and their percentage weightings, and the fourteen task statement titles. Every one of those is a **fact about an examination** — a number, a structural statement, or a functional heading. Facts are not copyrightable, and short functional headings are not protectable expression. Nothing beyond those headings is reproduced.
2. **Public AWS service documentation.** Used the same way a textbook author uses a manual: to establish what a service actually does, so that a scenario question about it is *correct*. No sentence of it is reproduced. The questions, options, distractors and explanations are original text written for this module.

### 4.2 What is not being used, and why the ban is absolute here

AGENTS.md constraint 1 bans *"any third-party exam-prep or compliance-training company's text."* For this topic the search results are almost entirely such companies, plus "dump" sites that publish recalled exam questions. **None was fetched.** There is no analogue of the sign-icon visual-accuracy carve-out that could apply: a question bank is exactly the artefact the constraint exists to protect.

Two categories deserve to be named specifically because they look more legitimate than they are:

- **Paid AWS training (Skill Builder's practice exams, official practice question sets).** These are AWS's own, which makes them feel safe. They are not: they are *assessment material*, they sit behind a paid subscription, and using them would put this module one step from the confidentiality problem in §4.3. Not opened.
- **Third-party books and courses.** Same ban, no ambiguity.

### 4.3 AWS exam content is confidential, and that is a stronger constraint than copyright

The **AWS Certification Agreement** provides that *"all Credential Assessment Materials are AWS Confidential Information"* and that candidates must not *"disclose or disseminate the content of any Certification Exam or Credential Assessment Materials."* It defines *"Unauthorized Content Disclosures"* to include materials *"listed on third-party websites without the express permission of AWS."*

This matters even though Zettacard has signed nothing: it is what makes every "dump" site's content **the fruit of somebody's breach**, and it is the reason a module like this must be authored *forward* from the public exam guide rather than *backward* from anyone's recollection of real questions. The draft contains no recalled question, no reconstructed question, and no question derived from one. Stated plainly in `meta.description` so the position is visible to a reviewer without reading this dossier.

### 4.4 Trademarks — permitted, but with a condition that has to be honoured in shipped copy

AWS's trademark guidelines say *"AWS does not object to fair use of its marks by third parties, so long as the use would not be confusing for customers"* and *"AWS does not object to limited fair use of such materials for educational or non-profit purposes."* They also say, unambiguously: *"Fair use does not permit you to state or imply affiliation, sponsorship, or endorsement by AWS."*

Naming the certification and the services is therefore fine. What is **not** fine is any module label, badge, landing-page section or completion credential that could read as AWS-endorsed. This is a real risk for Zettacard specifically, because the app issues **signed completion credentials** (`netlify/functions/sign-credential.js`). A credential that says "AWS Certified Solutions Architect" without qualification would be exactly the confusion the guidelines forbid. See open item 3.

---

## 5. Licensing — the default is right here, but for the opposite reason to `cka`

AGENTS.md constraint 3 is explicit that CC BY-NC-SA 4.0 is *"the default for content we author, not a universal blanket"*, and that a module ingesting third-party material under other terms must declare its **real** licence. So this was checked rather than assumed.

**Finding: CC BY-NC-SA 4.0, unchanged, with no attribution field and no divergence — because this module ingests nothing.**

The reasoning matters more than the conclusion, because the obvious analogy is wrong:

| | `cka` | `aws_saa` |
|---|---|---|
| Structural source | CNCF `cncf/curriculum` | AWS SAA-C03 exam guide |
| Its licence | **CC-BY 4.0+** — an open licence that *permits* reuse with attribution | **None.** AWS Site Terms grant only a *"limited license to access and make personal use of the AWS Site"* and expressly exclude *"any resale or commercial use"* and *"any derivative use"* |
| So the source could be… | **ingested**, with attribution | **not ingested at all** — only consulted as a factual reference |
| Resulting obligation | attribution to CNCF | **none to inherit** |

In other words: `cka` could safely lean on its source *because* that source was openly licensed. This module is safe *because* it leans on nothing — the AWS material is a reference for facts (structure, weightings, service behaviour), and every word of expressive content is this project's own. The stricter licence position on the AWS side produces the cleaner outcome, which is counter-intuitive enough to be worth writing down.

Consequences recorded in `meta.license_note`:

- `license`: `CC BY-NC-SA 4.0`; `license_url` as usual.
- **No `attribution` field**, because there is no third-party licence to satisfy — unlike `sportboot_binnen`/`sportboot_see`, whose ELWIS/MIT attribution exists because those modules genuinely ingested something.
- The **NonCommercial** term is a comfortable fit rather than an awkward one here: whatever else it does, it keeps the module out of the "commercial use of AWS Site content" territory the Site Terms are aimed at. That is a happy alignment, not a licence to relax anything.
- The **trademark** position is separate from the copyright position and is recorded separately, in `meta.trademark_note`. Conflating the two is the usual mistake.

**One thing that is missing and must be added before launch, not before review:** an **AWS row in `app/legal/quellen.html`'s per-source table**, per AGENTS.md constraint 3's requirement that licensing provenance stays visible in one place. Suggested content — *body/source:* Amazon Web Services, Inc.; *licence:* AWS Site Terms — no reuse licence; used as a factual reference only, no AWS text reproduced; *note:* public SAA-C03 exam guide + public service documentation; AWS marks used nominatively; no affiliation or endorsement. Deliberately **not** added in this round, because `app/` is out of scope for a `_DRAFT` module and adding it would imply the module ships.

---

## 6. Source confidence

**Tier A — AWS's own published material, read directly. Everything the recommendation and every draft question rests on.**

1. **SAA-C03 exam guide**, read in **both** HTML and PDF, independently. Source of the exam code, 50 + 15 question split, question-type definitions, 720/1,000 compensatory passing score, four domains, four weightings, fourteen task statements. The two renderings agreed on every figure.
2. **AWS certification product page** — 65 questions, MC/MR, 130 minutes, 150 USD. Independent of (1) and consistent with it.
3. **AWS Certification "Coming Soon"** — currency check; no SAA update announced (§0.2).
4. **Fifteen AWS service documentation pages** — the substantive answer verification, itemised at §3. Each question's `legal_basis` names the page it rests on.
5. **AWS Site Terms, Trademark Guidelines, Certification Agreement** — the licensing, trademark and confidentiality analysis at §4–§5, each quoted from the instrument itself.

**Tier B — this repo's own prior work, relied on for framing rather than for facts.**

6. **`docs/cka-lab-and-cloud-cert-hands-on-scoping-2026-08-23.md`** — established the MCQ-only finding for the PO one day earlier and recommended building the AWS module as an MCQ module. Its §7.1 findings were **re-verified independently here** rather than inherited; they hold. Its §10 sources list agrees with §1 above.
7. **`data/cka_pilot.json` and the `cka` entry in `data/modules_manifest.json`** — the locale-scope and framing precedent this module follows (§0.1, and the locale note in the draft's `meta`).

**Tier C — orientation only, load-bearing for nothing.**

8. Search-result listings for AWS exam-prep vendors and "SAA-C04" blog posts — used **only** to establish what had to be avoided (§1) and to demonstrate the version-confusion risk (§0.2). None was fetched, read or cited for content.

**Confidence in the headline findings: very high.** The exam structure is a published AWS document read twice in two formats, cross-checked against a second AWS page and a third AWS page for currency. The residual risks are (a) that AWS revises the exam or a service on its own schedule — see the ACM case at §3.1, which is the concrete demonstration; and (b) that the exam guide's own caveat means the task statements are a floor on scope, not a ceiling (§2.1).

**Confidence in the 36 draft answers: high, but explicitly not self-certified.** Every one was checked against AWS documentation this session, and one was found wrong and fixed. That is exactly the process AGENTS.md's "don't trust self-reported 'looks right'" rule says is *not* sufficient on its own: the agent that wrote the questions also checked them. A human technical review is open item 1 and is not optional.

---

## 7. Recommendation

### 7.1 Build it, and let it say the true thing about its format

The sourcing basis is clean and, unusually, cleaner than for several modules already shipped: the exam's structure is published by the examiner itself, the substantive content is public product documentation, and the module ingests neither. There is no blocker to resolve, because there was never a vendor dependency to begin with.

**Recommended label:** *"AWS Certified Solutions Architect – Associate (SAA-C03) — practice questions"*, with a visible statement that (a) this is unofficial practice material, not affiliated with, sponsored by or endorsed by AWS; (b) the questions are original and no real exam content is reproduced; (c) the real exam is 65 questions in 130 minutes with a scaled 720/1,000 pass mark — **and no per-domain minimum**, which candidates routinely assume exists.

**Do not** carry across `cka`'s "not an exam simulator" disclaimer (§0.1). The honest framing here is the ordinary one.

### 7.2 Locale scope — the `cka` precedent, followed deliberately and flagged as such

The draft ships **EN canonical + DE + JA + ZH**: the same four-locale set, and the same EN-canonical choice, that `cka` established on 2026-08-15 with PO approval as *"the first module with EN as canonical/source locale … and first with a deliberately minimal 4-locale set (en/de/ja/zh) rather than the full 12."*

**This is a precedent being followed, not a fresh exception being claimed.** The distinction matters for the PO's decision: the question is not "should this module get an exception?" but "is the technical-certification exception the right standing policy?" If the answer is no, it applies equally to `cka` and to this module, and both need a translation round rather than one being singled out. Nothing in the draft's schema assumes four locales; `meta.locales` is a list and the generator reads it.

Arguments visible from here, offered without a recommendation because this is a scope decision and therefore the PO's:

- **For the minimal set:** AWS authors the exam and its documentation in English; AWS service names are untranslated in every locale anyway; the candidate population is overwhelmingly working professionals who read English technical material daily. Translation cost scales with 36 questions × locales and would triple for the full 12.
- **Against:** unlike CKA, AWS **does** deliver the SAA exam in several languages, and Zettacard's multilingual reach is a genuine differentiator in exactly the markets a cloud-certification module would target. The full-12 rule exists for a reason and this is the second module in a row to depart from it — two departures is where a "precedent" quietly becomes a policy nobody decided.

### 7.3 Open items for the PO / human review

1. **Technical accuracy review by a human who knows these services.** Not optional, and not satisfied by §3. Every answer was verified against AWS documentation by the agent that wrote the questions, and AGENTS.md is explicit that an agent's own claim its work is right is not verification. §3.1 shows why: one answer's *reasoning* was stale in a way that a reader without the current documentation in front of them would not have caught.
2. **Decide the locale policy for technical-certification modules** (§7.2) — as a policy covering `cka` and `aws_saa` together, not as a one-off for either.
3. **Trademark and credential positioning check before any public launch.** Specifically: the module label, the landing-page copy, and — the one with real exposure — the text of any **signed completion credential** this module can issue. A credential reading "AWS Certified Solutions Architect" without qualification would state or imply exactly the endorsement AWS's guidelines forbid (§4.4). Needs a decision on wording, e.g. "Zettacard practice module: AWS Certified Solutions Architect – Associate (SAA-C03) preparation".
4. **Add the AWS row to `app/legal/quellen.html`** when the module is wired in — draft wording at §5. Deliberately not added in this round.
5. **Decide whether a full-length 65-question timed mock is in scope.** The format is faithful enough to support one honestly, which is a capability Zettacard has for no other technical module. This 36-question pilot is not it, and building it is a separate card with its own weighting arithmetic (65 questions at 30/26/24/20 gives 19.5/16.9/15.6/13).
6. **Do not print a percentage pass mark** (§2.2). 720/1,000 is a scaled score and is not 72%. Any threshold in the app is Zettacard's own and must be labelled as such.
7. **Re-verification no later than 2027-02-28**, and immediately if AWS announces an SAA update. Six months, deliberately shorter than the statute-based modules' interval, because vendor documentation moves faster than statute — §3.1 is the proof. Two distinct checks: the exam version and its parameters, and the asserted service behaviour. The volatile facts are listed in the draft's `meta.renewal_note`.
8. **Standing note for the next agent:** when a widely-repeated technical "fact" underpins a distractor, check the current documentation before shipping it, not the collective memory of the internet. The ACM export rule (§3.1) had been true for roughly a decade and stopped being true in June 2025; every secondary source still says otherwise.

---

## 8. What was drafted

`data/aws_saa_pilot_DRAFT.json` — **36 questions**, EN canonical + DE + JA + ZH, generated deterministically by `data/gen_aws_saa_draft.py`, which runs its own integrity, weighting and constraint-1 checks and exits non-zero on failure.

`topic_code` maps **1:1 onto AWS's four published content domains**, so the distribution is checkable against the published weightings rather than against an invented taxonomy. The generator asserts that every domain's share is within 1.5 percentage points of AWS's figure and fails the build otherwise:

| `topic_code` | Content domain | Q | Share | AWS publishes |
|---|---|---|---|---|
| `secure_architectures` | Design Secure Architectures | 11 | 30.6% | 30% |
| `resilient_architectures` | Design Resilient Architectures | 9 | 25.0% | 26% |
| `high_performing_architectures` | Design High-Performing Architectures | 9 | 25.0% | 24% |
| `cost_optimized_architectures` | Design Cost-Optimized Architectures | 7 | 19.4% | 20% |

Every question carries a `legal_basis` naming **the task statement it was authored against** and **the AWS documentation page its answer was verified against**. All fourteen task statements are represented. Questions are written in the applied-scenario style the real exam uses ("a company needs X; which design meets the requirement?"), with distractors built from the specific confusions the underlying documentation exposes — standby-is-readable, gateway-vs-interface endpoint, security-group-deny, gp2 burst credits, Glacier Deep Archive for a millisecond requirement.

- **Question types:** 31 single-select + **5 multi-select** (`multi_choice`, the app's existing type). Multi-select questions follow AWS's own definition of a multiple-response item — **two or more correct out of five or more options** — and the generator enforces that shape. **The 5-of-36 ratio is an authoring choice, not a claim:** AWS does not publish the real ratio, and `meta.exam_format_note` says so rather than presenting 14% as a verified figure.
- **Points:** 15 × 1 (grundstoff) + 21 × 2 (applied tier) = 57, following the `cka` convention. Explicitly disconnected from AWS's scaled scoring in `meta.point_system`.
- **`high_stakes: true` on 11** — the ones where being wrong in production means a security defect or an availability defect, not merely a suboptimal choice.
- **Answer-key spread** a/b/c/d = 11/10/11/9 across all correct answers, so the key is not learnable.

**Not drafted, deliberately:** anything resting on a vendor's question wording or structure; anything derived from a recalled or "dumped" exam question; any claim about the real exam's multiple-response ratio, its question pool or its coverage; any per-domain pass rule (there is none — scoring is compensatory); any full-length 65-question mock (open item 5); any service behaviour that could not be verified against AWS documentation this session.

---

**Reminder:** this document is draft research groundwork. It has not been reviewed by a qualified lawyer, by anyone holding this certification, or by AWS. No content derived from it should be shipped to learners before the technical review at open item 1 and the trademark check at open item 3. The draft question bank carries `legal_review_status` accordingly and is unwired from every build path.
