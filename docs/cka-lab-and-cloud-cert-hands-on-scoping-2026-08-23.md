# Hands-on labs for CKA and cloud certs — build/buy/link scoping (2026-08-23)

**Status:** research + options pass for PO review. **Scoping only — no lab content, no scenario text, no code.**
Triggered by the PO's note: *"the killer.sh stuff can be usefull for an AWS solution architet (or an clone
opensourve based cloud training as well)"* — i.e. is a Killer.sh-style live/graded lab capability worth building
as **shared** infrastructure across several cert modules rather than as a CKA one-off?

**Short answer, up front, so the rest is optional reading:**

1. **AWS Solutions Architect – Associate has no hands-on component at all.** It is 65 multiple-choice /
   multiple-response questions in 130 minutes ([verified against AWS's own exam
   page and exam guide](#10-sources), 2026-08-23). A Killer.sh-analogue for AWS SAA would rehearse a skill the
   exam does not test. This inverts the PO's premise and is the single most decision-relevant fact in this doc.
2. Where hands-on labs *do* matter (the CNCF/Linux Foundation family: CKA, CKAD, CKS, LFCS, CNPE), **Killer.sh
   is already bundled free with the $445 exam fee**. Zettacard cannot undercut free-with-purchase.
3. So the recommendation is **Stage 1+**: keep Zettacard's labs prose-first and offline-safe, and additionally
   author *graded* lab scenarios on **Killercoda** (free to create, free to run, grading built in, scenarios live
   in a Zettacard-owned git repo) — **zero Zettacard-hosted infra, zero exception to the offline-first
   constraint**. Build the **AWS module as an MCQ module**, which is exactly what Zettacard already does well.

**Everything factual about the codebase below was verified in this repo on 2026-08-23.** Every external claim
(pricing, exam format, licensing, service coverage) was fetched live on 2026-08-23; URLs are in §10 and the
retrieval date applies to all of them. Where a number is derived rather than quoted, it is labelled
**[derived]** and the arithmetic is shown so it can be re-run. Pricing and exam formats change — re-verify
before acting on anything here more than a quarter from now. Two of the "obvious" free options in this space
died between the last time this project looked at them and today (see §4.2, §4.5); that is not an accident,
it is the base rate.

---

## 0. Contents

- §1 What Zettacard ships today (verified) — and the constraint that frames everything
- §2 What Killer.sh actually is (verified mechanics and price)
- §3 The offline-first constraint — why this is not a detail
- §4 Building blocks, assessed one by one
  - §4.1 Killercoda — the only genuinely free graded engine still standing
  - §4.2 Play with Kubernetes / Play with Docker — **dead as of 2026-03-01**
  - §4.3 DIY: ephemeral `kind`/`k3d` + browser terminal — with real cost arithmetic
  - §4.4 Commercial hands-on-lab platforms (Instruqt, Strigo) — the "don't build it" price tag
  - §4.5 LocalStack for the AWS angle — **Community edition ended 2026-03-23**
  - §4.6 AWS's own free sandboxes — zero Zettacard infra
- §5 The abuse and liability surface — the part that is not about money
- §6 The staged options menu (Stage 0 → Stage 3), priced
- §7 Is AWS SAA the right second module? — and which certs would actually share a lab engine
- §8 Recommendation (a position, not a menu)
- §9 Punch list — decisions the PO owes before anything is built
- §10 Sources

---

## 1. What Zettacard ships today (verified 2026-08-23)

### 1.1 The CKA module

| Fact | Value | Where verified |
|---|---|---|
| Question bank | **131 questions** | `data/cka_pilot.json`, counted |
| Canonical locale | `en` (only EN-canonical module in the repo) | `data/cka_pilot.json` `meta.canonical_locale` |
| Locales | `en, de, ja, zh` (deliberately 4, not the usual 12) | `data/cka_course.json` `meta.locales` |
| Course | 4 weeks, 570 min total, `cadence_hint` free text | `data/cka_course.json` |
| Lab lessons | **3** (`cka-l2`, `cka-l5`, `cka-l9`), 60/60/75 min | `data/cka_course.json`, `lesson_kind: "lab"` |
| Lab `completion_rule` | **`read`** on all three — labs do **not** gate progress | same |
| Visibility | behind `feature_flag` (the only module using it) | `docs/whitelabel-…-2026-08-17.md` §1.5 |

The honesty framing is already in the data, verbatim, in three places (`data/cka_pilot.json` `meta.description`,
`data/modules_manifest.json` `_comment` and the module's in-app intro `body`):

> "the real CKA exam is 100% performance-based (live kubectl tasks against a real cluster) and is NEVER
> multiple-choice — this module is honestly framed as a concept-check quiz, not an exam simulator, per explicit
> PO direction."

And each lab section body opens by saying Zettacard runs nothing — e.g. `cka-l2-s1`: *"Run this on your own
machine — Zettacard executes nothing."*; `cka-l9-s1`: *"Your cluster, your keyboard — Zettacard executes
nothing."*

**This is an asset, not a gap.** Any option below that changes it (i.e. Zettacard starts executing things) has
to also change that copy in 4 locales, and has to keep the claim true afterwards.

### 1.2 What Zettacard's backend is today

`netlify/functions/` contains exactly three functions — `issue-badge.mjs`, `get-badge.mjs`,
`sign-credential.js` — all credential-related, none content-serving. `netlify.toml` publishes `app/` as a static
site (`command = "true"`). The app describes itself, in its own UI strings, as a
**"zero-backend static PWA"** (`app/app.js:2866`).

**There are no user accounts, no login, no session identity, and no server-side rate limiting anywhere in the
product.** This matters enormously in §5: every ephemeral-sandbox design in the industry is gated on identity,
and Zettacard would have to build identity from zero *before* it could safely build a sandbox at all.

---

## 2. What Killer.sh actually is (verified 2026-08-23)

Both killer.sh and killercoda.com are JavaScript-only and return nothing to a plain fetch; the facts below were
read from their server-rendered text via a text-extraction proxy, and cross-checked against the Linux
Foundation's own CKA product page and the kodekloudhub community FAQ.

**Mechanics (killer.sh/cka, killer.sh/pricing, LF CKA page):**

- **Two sessions per exam purchase**, one in simulator "CKA-A" and one in "CKA-B" — different question sets.
- Each session: **17 questions**, **120-minute countdown**, then the **environment stays open for 36 hours**
  after activation for review. Sessions can be started independently over a **one-year** window.
- **Your own real clusters**, pre-seeded with resources and deliberate breakage — "For some questions you have
  to start completely from scratch, in others you need to work with given resources or configuration and alter
  those."
- **Remote Desktop, like the real exam** — not just a terminal in a web page. The real CKA is *"an online,
  proctored, performance-based test that requires solving multiple tasks from a command line running
  Kubernetes"*, 2 hours (LF's own wording).
- **Automatic scoring**, per-question sub-task breakdown, plus written solutions (~100 pages of material), plus
  an LLM-ish "Brain" per-question feedback layer. Some questions still need manual comparison against the model
  solution.
- Self-described as **harder than the real exam**, deliberately.

**Price (killer.sh/pricing, verified):**

| Item | Price |
|---|---|
| CKA exam (Linux Foundation, exam only) | **$445** |
| …which **includes two Killer.sh sessions** | $0 marginal |
| Killer.sh CKA standalone (two sessions) | **$39.99** |
| Killer.sh rebuy, single session, within 12 months | **$9.99** |
| Killer.sh CNPE / LFCS standalone (two sessions) | **$29.99** |
| Killercoda "Killer Teams" voucher (killercoda COURSE + 5 killer.sh sessions/month) | **$99 / user / month**, dropping to **$49.99** at 3 months and **$29.99** at 6 months |

**Read the $39.99 carefully: a graded, per-candidate, multi-cluster, remote-desktop exam rehearsal retails at
~$20 per session, and is free to anyone who has actually registered for the exam.** That is the number any
Zettacard-built Stage 3 has to beat. It cannot.

The same company (Kim Wüstkamp) runs both killer.sh and killercoda.com, and the Linux Foundation bundles their
simulator into CKA, CKAD, CKS, **CNPE** and **LFCS** — verified on killer.sh's FAQ and on the LF's CNPE product
page ("Once enrolled you will receive access to an exam simulator, provided by Killer.sh… two simulation
attempts… graded results").

---

## 3. The offline-first constraint — why this is not a detail

`AGENTS.md`, non-negotiable constraint **6**, verbatim:

> **Offline-first.** Output stays as flat, static JSON bundles suitable for service-worker precaching. **No
> feature should require a live backend call to serve content.**

Per `AGENTS.md` §7 (roles), only the PO can change a non-negotiable constraint.

**A real interactive lab is a live-backend feature by definition.** A hosted cluster cannot be precached into a
service worker. There is no clever framing that makes Stage 2 or Stage 3 compatible with constraint 6; they are
exceptions, full stop, and this document will not pretend otherwise.

**There is exactly one precedent, and it was handled the right way.** `docs/course-media-sections.md` §6, "Offline
behaviour — a deliberate, disclosed exception":

> "AGENTS.md constraint 6 … has exactly one exception now, and this is it: a YouTube video, an externally hosted
> MP4, or a remotely hosted image genuinely cannot be served from a precached static bundle."

Note what that exception cost, and what discipline came with it:

- It was **discussed with the PO before and after building**, and written up as an exception in its own doc.
- **All text still works offline** — only the media element degrades, to a calm localized one-line note in 12
  locales (`COURSE_STRINGS.*.mediaOffline`).
- Repo-relative assets were explicitly kept **non**-network-dependent, so a course built on local diagrams is
  still fully offline.
- The whole thing was verified with request-log/DOM/screenshot evidence across locales, RTL, and both themes.

**A hands-on lab is a categorically bigger exception than an embedded video**, on four axes at once:

| Axis | Media exception | Lab exception |
|---|---|---|
| Who serves it | YouTube / an external CDN | **Zettacard** (Stage 2/3) |
| Marginal cost per learner | €0 | real compute, real egress |
| Failure mode offline | one-line note, lesson still readable | feature simply absent |
| Abuse surface | none | **arbitrary remote code execution by strangers** (§5) |
| Legal posture | asset licensing (already solved via mandatory `media.license`) | operator liability, GDPR logs, AGB/Impressum obligations, sanctions/export exposure |

**Design invariant to preserve in every option below:** the three lab lessons currently have
`completion_rule: "read"`. **A hands-on lab must never become a prerequisite for course completion or
certificate issuance**, because that would make an online-only feature block an offline-first product's core
promise. Any option that quietly changes those `completion_rule` values is out of scope of this doc and needs
its own PO decision.

---

## 4. Building blocks, assessed

### 4.1 Killercoda — the only genuinely free graded engine still standing

**Is any of it open source?** **No.** The `killercoda` GitHub organisation contains 21 repositories: 20 are
*scenario* repos (`scenario-examples`, `scenarios-helm`, `scenarios-k3s`, `scenarios-istio`, …) plus a fork of
KubeVirt. **There is no platform/engine repository.** The scenario *format* is open and portable (JSON +
Markdown + Bash in a git repo); the runtime that executes it is closed and hosted.

Consequence: **you cannot self-host Killercoda.** What you can do is author on it, for free.

**What the creator side actually gives you (killercoda.com/creators, verified):**

- You point Killercoda at **your own GitHub repository**; every push to the configured branch updates your
  scenarios. Scenario source stays yours, in your repo, in a format you could port.
- Ready-made environment images, with their RAM budgets stated: `ubuntu` (2 GB), `ubuntu-4GB`,
  **`kubernetes-kubeadm-1node` (2 GB)**, `kubernetes-kubeadm-1node-4GB`, **`kubernetes-kubeadm-2nodes` (4 GB)**.
  (Useful independent confirmation for §4.3's sizing: *a single-node kubeadm cluster fits in 2 GB.*)
- **Kubernetes versions are maintained for you** — the published table shows `1.35` → `1.36` on **2026-09-01**,
  with `-rapid` images to test the next version early. Creators are told to make sure their scenarios still work
  after a bump. This is the ongoing maintenance cost Zettacard would otherwise own itself, and it recurs ~3×/year.
- **Verification scripts = grading.** "When the user clicks the **CHECK** button, the script runs automatically.
  It passes if it exits with code `0`." Multi-step verification is supported. This is the single most expensive
  piece of a Killer.sh-style product, available for free.
- Asset upload into the environment on start, code-block "run this" actions, and network-traffic scenarios.
- Ratings/feedback per scenario, filterable by period.

**Limits, which are on the learner's membership, not the creator's:**

| | FREE | Paid (PLUS) |
|---|---|---|
| Scenario session length | **max 1 hour** | max 4 hours |
| Concurrent scenarios | **1** | 3 |
| Number of sessions | unlimited | unlimited |
| Remote Desktop (exam-like) for CKS/Playgrounds | ✗ | ✓ |
| Captcha challenges | yes | no |
| Queues on load | yes | skipped |
| Create + share **public** scenarios | ✓ | ✓ |
| "Course" scenarios (killercoda's own CKA/CKAD/CNPE courses) | ✗ | COURSE tier |

Killercoda's own pricing page does not server-render its individual prices (JS-only); the third-party directory
FreeTier.co lists **PLUS at ~$7.33/mo** and **COURSE at ~$19.99/mo** — treat those two figures as *unverified
third-party*, unlike the Teams prices in §2 which are server-rendered on killercoda.com/teams and are solid.

**Fit against Zettacard's lab lessons:** the three labs are 60/60/75 min. The FREE tier's **1-hour** cap is a
genuine but survivable constraint — it argues for authoring **several short scenarios (15–25 min each) rather
than one 60-minute monolith**, which is better lab design anyway and matches Killercoda's own step model.

**Jurisdiction note, mildly in Zettacard's favour:** killercoda.com publishes a German *Impressum*,
*Datenschutz* and *AGB*. For a German-operated product linking learners out to a third party, an EU/German
counterparty is a materially easier data-protection story than a US one.

**Verdict:** the best value in this entire document. Free to author, free to run, grading included, K8s upkeep
included, scenario source stays in a Zettacard repo. Its risk is dependency (§4.2 shows what that risk looks
like when it lands), and the mitigation is that the prose labs stay authoritative and self-sufficient.

### 4.2 Play with Kubernetes / Play with Docker — dead

Both were fetched directly on 2026-08-23. Both serve the same banner:

> **Deprecation notice:** Play with Kubernetes will be **unavailable starting March 1, 2026**. Visit Docker Docs
> for supported labs and guides.

(identical wording on `labs.play-with-docker.com`; the PWK page footer still reads "© Play with Kubernetes
2017 - 2023"). **Do not link learners at either.** They are Docker-in-Docker playgrounds with no embedding story
and no API worth building on even when they were alive.

**This is the second free community sandbox to die inside three years**: Katacoda — the platform Killercoda was
built to replace — was acquired by O'Reilly and its public platform closed, with the Kubernetes project
publishing "Free Katacoda Kubernetes Tutorials Are Shutting Down" and running an umbrella issue to strip
Katacoda embeds out of kubernetes.io.

**The lesson to carry into the recommendation:** free third-party sandboxes have a demonstrated ~3-year
half-life. That is *not* an argument for self-hosting (self-hosting costs more than the thing is worth, §4.3 +
§5); it is an argument for **never letting a third-party sandbox become load-bearing** — the prose lab and the
static answer key stay the product; the sandbox link is a bonus that can be swapped or dropped in one commit.

### 4.3 DIY: ephemeral `kind`/`k3d` + browser terminal

**The parts all exist and are properly open source:**

| Component | What it is | Licence | Health check (2026-08-23) |
|---|---|---|---|
| `kubernetes-sigs/kind` | Kubernetes in Docker | Apache-2.0 | active, CNCF-adjacent, the standard |
| `k3d-io/k3d` | k3s in Docker, lighter | MIT | active |
| `tsl0922/ttyd` | C + libwebsockets + xterm.js browser terminal | MIT | **last commit 2026-08-12**, 888 commits — alive |
| `butlerx/wetty` | Node/TS browser terminal over SSH | MIT | maintained |
| `sorenisanerd/gotty` | Go browser terminal (maintained fork of `yudai/gotty`) | MIT | maintained fork; original upstream stale |

`gotty`'s own README is worth quoting as a summary of the security posture you inherit:

> "By default, GoTTY doesn't allow clients to send any keystrokes… When you want to permit clients to write
> input to the TTY, add the `-w` option. **However, accepting input from remote clients is dangerous for most
> commands.**"

That is exactly the thing a lab feature must do, on purpose, for anonymous strangers.

**Sizing.** k3s's own docs: a server node wants **2 cores / 2 GB**; their "Small (up to 10 nodes)" deployment
row is **1 vCPU / 2 GB**. Killercoda independently ships its single-node kubeadm image as a **2 GB**
environment. So: **2 GB per single-node learner sandbox, 4 GB for a two-node scenario** is a defensible planning
figure.

**Cost arithmetic — real prices, fetched 2026-08-23, arithmetic shown.**

*Option A — Fly.io Machines (per-second billing, scale-to-zero; published price list):*

| Preset | Price/hour | 1-hour lab session |
|---|---:|---:|
| `shared-cpu-2x`, 2 GB | $0.0164 | **$0.016** |
| `shared-cpu-2x`, 4 GB | $0.0309 | **$0.031** |
| `shared-cpu-4x`, 4 GB | $0.0329 | $0.033 |

**[derived]** 1,000 one-hour single-node sessions/month ≈ **$16–$31 of compute**, plus egress and IPs.

*Option B — Hetzner (fixed monthly host, you pack sessions onto it). Hetzner raised prices across the line on
2026-04-01:*

| Plan | vCPU / RAM | Price/mo (from 2026-04-01) |
|---|---|---:|
| CX23 | 2 / 4 GB | €3.99 |
| CX33 | 4 / 8 GB | €6.49 |
| **CPX32** | **4 / 8 GB** | **€13.99** |
| CPX42 | 8 / 16 GB | €25.49 |

**[derived]**, CPX32: €13.99 ÷ 730 h = **€0.0192 per host-hour**. Reserve ~2 GB for host + orchestrator → 6 GB
usable → **3 concurrent 2-GB sandboxes**. At perfect packing that is **€0.0064 per sandbox-hour**; at a realistic
20 % average occupancy it is **€0.032 per sandbox-hour**, and one €14/month box absorbs
3 × 730 × 0.20 ≈ **438 one-hour sessions per month**.

*Option C — DigitalOcean (per-second billing since 2026-01-01, published list):* 8 GB / 4 vCPU basic Droplet =
**$48/mo, $0.07143/h**. Same packing → **[derived]** $0.0238/sandbox-hour at perfect packing, ~$0.12 at 20 %
occupancy. Roughly 3–4× Hetzner for this workload.

**The honest conclusion from this table is the opposite of what people expect: compute is not the problem.**
A hands-on K8s lab session costs **one to four US cents**. If compute were the only cost, Stage 2 would be
trivially affordable at Zettacard's scale.

**What actually costs money is everything around the compute**, and none of it is optional:

- a session broker (issue, track, expire, reap) — and Zettacard has **no identity layer at all** to hang it on;
- TLS + per-session authentication for the terminal endpoint (a `ttyd` with `-w` and no auth is a public root
  shell);
- an image pull-through cache/mirror, because a locked-down sandbox still has to pull container images;
- egress policy (see §5 — this is where the crypto miners live);
- cgroup CPU/memory/PID quotas and disk quotas;
- a reaper that is *actually* reliable, because the failure mode of an unreliable one is an unbounded bill;
- monitoring, alerting, and a human who responds — **a solo-operator team**;
- Kubernetes version upkeep ~3×/year (Killercoda's public table shows exactly this cadence, §4.1);
- and a second, non-static hosting footprint: Netlify publishes `app/` statically; **none of this can live
  there.** Stage 2 means Zettacard operates servers for the first time.

**[estimate, not sourced]** 3–6 weeks of solo-operator engineering to a first *safe* deployment, then permanent
ops load. The rational comparison is not "€14/month vs Killer.sh's $39.99" — it is "3–6 weeks plus permanent
on-call vs €0 and a link."

### 4.4 Commercial hands-on-lab platforms — the "don't build it" price tag

Included only as a baseline; **no recommendation to buy.**

- **Instruqt** publishes *no* list price. Their pricing page offers only "Consumption-based annual pricing
  packages" with "flexible add-ons", estimated from "annual hours". Third-party contract data (Vendr) reports a
  **median $28,410/year**, range **$10,000–$54,779**, and community reports of **~$15,000 for a 1,000-hour
  prepaid package**.
- **Strigo** likewise publishes no figures — their "Transparent & Affordable" pricing page contains no numbers at
  all; it is quote-based. (Their product pages do advertise an *Embeddable Labs* SKU, i.e. iframe-into-your-own-
  site labs, which is the shape Zettacard would notionally want.)

**[derived]** $15,000 / 1,000 hours = **~$15 per lab-hour**, against ~$0.02–$0.03 of underlying compute — a
**~500×** multiple. That multiple *is* the answer to "should we build this ourselves?": it is not paying for
servers, it is paying for provisioning reliability, grading content, support, abuse handling, and enterprise
compliance. Those are exactly the costs a solo-operator free product cannot absorb — in either direction, buying
or building.

For scale: **one year of Instruqt at the median ≈ 64 × the entire CKA exam fee**, for a module Zettacard ships
free.

### 4.5 LocalStack for the AWS angle — the Community edition is gone

This was the most promising-looking idea in the brief and it has just been undercut by a licence change.

**What changed (LocalStack's own blog, 2025-12-18 and the 2026 pricing post, plus InfoQ's 2026-02 coverage):**

- **"We will end support for LocalStack for AWS Community edition beginning on March 23, 2026."** After that
  date there is **a single Docker image that requires authentication** — the separately Apache-2.0-licensed
  Community image is no longer developed; only the unified, sign-in-gated build gets features and security
  patches.
- A permanent free tier remains, but: **"our free tier will not permit usage for commercial purposes."** Free
  access is scoped to students (GitHub-verified), open-source projects, non-profits, and "recreational" use.
- Paid plans reported from **$39/month (billed annually)**; a third-party pricing tracker lists **Base $45/mo**
  and **Ultimate $89/mo**, and LocalStack's own pricing page (JS-rendered, prices not server-rendered) shows the
  tier ladder Trial / Hobby / Base / Ultimate / Enterprise with per-license seats, Cloud-Pod storage caps and
  monthly ephemeral-instance minutes.

**Why that is close to fatal for the intended use.** Zettacard is a *product*, distributed to the public, even
if free at point of use. Shipping LocalStack as a component of a public learning product is not obviously
"non-commercial, recreational, student" use. Treating that as settled would be exactly the kind of unverified
licence assumption this project's dossier discipline exists to prevent. **It is a licensing negotiation, not a
`docker pull`.**

**And even setting licensing aside, fidelity is wrong for SAA.** LocalStack's service catalogue is genuinely
broad — EC2, VPC-adjacent EC2 resources, S3, IAM, RDS, Lambda, CloudFormation, Route 53, ELB, Auto Scaling,
CloudWatch, EKS, ECS and ~100 more are all listed. But it emulates the **control plane**: API calls succeed and
state is stored. It does not reproduce the **data plane** semantics that AWS SAA questions are actually about.
LocalStack's own EC2 docs say the quiet part out loud:

> "Currently, LocalStack **only supports the `default` security group**."
> "LocalStack for AWS running on a **Linux host is required** as network access to containers is not possible on
> macOS."

An SAA candidate needs to reason about route tables, NAT gateways vs internet gateways, security groups vs
NACLs, cross-AZ failover, multi-AZ RDS, and cost/availability trade-offs. A mock that accepts every
`CreateRouteTable` call and only honours one security group **teaches the API surface, not the architecture** —
and the exam tests the architecture. Add the honesty risk: a learner who "passes" a LocalStack lab could
reasonably believe they have verified a design that would not work in AWS.

Worth logging for completeness: the community reaction produced alternatives (Moto for mocking, plus newer
emulator projects), but none is remotely mature enough to bet a module on, and none changes the fidelity
argument above.

**Verdict: LocalStack is not the AWS answer.** Not because it is bad software — it is good software for its
actual job, local dev/test of application code — but because its licence no longer fits a public product and its
fidelity does not fit an architecture exam.

### 4.6 AWS's own free options — zero Zettacard infra

If AWS hands-on pointers are wanted at all (see §7 for why they are optional), these require **nothing** from
Zettacard beyond a curated link:

- **AWS Skill Builder** (skillbuilder.aws/subscriptions, verified): a **free account** includes 900+ digital
  courses, learning plans, badges, Exam Prep Review, and *limited* Exam Prep Practice; **Guided AWS Builder
  Labs "Cloud Foundations only"**, AWS Cloud Quest and AWS SimuLearn limited to the Cloud Practitioner and
  Generative AI Practitioner roles. **Paid: $29/month, or $449/year**, which unlocks the full Builder Labs
  catalogue plus official practice exams. So: real, live-AWS labs with no risk of a surprise bill — but the
  SAA-relevant ones sit behind $29/mo.
- **AWS Workshop Studio** — AWS's public self-paced workshop catalogue; most workshops run in **your own AWS
  account** (so, your own bill).
- **AWS Free Tier**, changed materially on **2025-07-16**: new customers get **$100 in credits at sign-up plus up
  to $100 more** for using services like EC2 and Bedrock, and **"the free account plan expires either 6 months
  after sign-up or when Free Tier credits are depleted, whichever comes first."** AWS's announcement describes
  monitoring/forecasting tooling but **does not describe an automatic hard spending cap.** So the "learner runs
  up a bill" risk is *reduced but not eliminated* — and it is the learner's own bill, not Zettacard's. Any
  Zettacard-authored pointer to real AWS must say this plainly, in the same register as the existing "Zettacard
  executes nothing" copy.
- **AWS Educate** — still live as AWS's no-AWS-account-needed education entry point; positioning shifts often
  enough that it should be re-checked before being linked, not linked on the strength of this sentence.

---

## 5. The abuse and liability surface

This section applies only to Stage 2 and Stage 3. **It is the reason those stages are not "just €14/month".**

**Someone will mine crypto in your free container. This is not hypothetical, it is an industrialised business.**
The PURPLEURCHIN campaign (Sysdig TRT; also covered by Trend Micro, BleepingComputer, CSA) automated the abuse of
free CI/CD and free-trial compute at scale:

- **30+ GitHub accounts**, **2,000 free Heroku accounts**, **900 Buddy.works accounts**, **130+ rotating Docker
  Hub images**; repos created and burned within one to two days.
- Platforms hit: GitHub Actions, Heroku, Buddy.works, CircleCI, Semaphore, **Fly.io** (i.e. one of the exact
  providers priced in §4.3).
- The economics are deliberately asymmetric: Sysdig estimates each abused free GitHub account costs the provider
  **~$15/month** (others $7–$10), that GitHub-side theft alone reached **~$103,000**, and that **mining a single
  Monero would cost the provider more than $100,000**. The attacker's yield is trivial; **the provider eats the
  whole cost.**
- Defences implied: CAPTCHA that is not trivially bypassable, IP-based account-creation limits, VPN detection,
  browser-automation detection.

Now map that onto Zettacard specifically:

| Requirement | Zettacard today |
|---|---|
| Accounts / identity to rate-limit against | **none** (`app/app.js` self-describes as a zero-backend static PWA) |
| CAPTCHA or bot defence | none |
| Server-side session state | none |
| Egress control | n/a — nothing is hosted |
| Someone on call when a box is pegged at 100 % CPU at 03:00 | one person |

So the true Stage 2 dependency chain is: **identity → rate limiting → abuse detection → sandbox**, and only the
last item is the feature anyone asked for. Killercoda's FREE tier's CAPTCHA-and-queues friction, which reads as
an annoyance from the outside, *is* this problem being solved — and PLUS's headline benefit is literally "no
Captcha bot challenges", i.e. paying is the identity signal.

Beyond mining, Stage 2 makes Zettacard an operator of **anonymous remote code execution for the public**, which
brings, at minimum:

- **Outbound abuse liability** — a sandbox with unrestricted egress is a port scanner, a spam relay, and a DDoS
  node. Abuse complaints land on Zettacard's provider account and can end in provider termination.
- **Container escape** as a live risk class: `kind`/`k3d` labs realistically need privileged or near-privileged
  containers, which is the weakest isolation posture in the catalogue. Firecracker-style microVMs are the
  correct answer and a large step up in complexity.
- **GDPR/DSGVO** — session logs and IPs are personal data; a German operator needs the processing recorded, a
  retention period, and an updated Datenschutzerklärung. Zettacard's static-site posture today largely dodges
  this.
- **Sanctions/export considerations** for providing compute to arbitrary jurisdictions.
- **Cost blowout as a *safety* property, not a budget one**: the failure mode of a broken reaper is not "we spent
  €14", it is an unbounded bill on a personal credit card.

None of this is unsolvable. All of it is *permanent* work for one person, in exchange for a feature whose
best-in-class version is already free to every learner who has registered for the exam.

---

## 6. The staged options menu

Ordered cheapest/lowest-commitment first. **"Constraint" = does it require an exception to `AGENTS.md` #6?**

### Stage 0 — prose-only labs, learner brings their own environment *(already shipped)*

- **Delivers:** 3 lab lessons, 195 minutes, deliberately unrunnable-by-Zettacard, `completion_rule: "read"`.
- **Zettacard infra:** none. **Money:** €0. **Engineering:** done.
- **Constraint:** ✅ **no exception.** Fully offline: the lab text is in the same precacheable
  `course.json` / `course_locales/*.json` pair as everything else.
- **Weakness, stated honestly:** no feedback loop. A learner who mistypes a selector gets no signal that they
  did. That is the actual product gap worth closing — and note that it is a *grading* gap, not a *hosting* gap.

### Stage 1 — curated outbound links + a Zettacard-hosted static answer key

- **Delivers:** each lab lesson gains (a) a link to a suitable free external sandbox and (b) a
  **Zettacard-hosted, static, offline-available self-check list**: for each task, the exact command to run and
  the exact expected output — the thing Stage 0 is missing.
- **Zettacard infra:** none beyond the existing static bundle.
- **Money:** €0.
- **Engineering:** small but non-zero, and there is a known blocker: **`related[]` renders as prose only, with
  no `href` and no link** (`app/app.js:4864–4874`, per the whitelabel doc §1.2). Making `related[]` linkable is
  generic course-layer infrastructure worth having regardless.
- **Constraint:** ✅ **no exception**, provided the link degrades the way media does — the checklist and all
  prose remain fully offline, and only the outbound link is dead when offline. Reuse the `mediaOffline` pattern
  and its 12-locale string discipline rather than inventing a second one.
- **Risk:** link rot with a demonstrated ~3-year half-life (§4.2). Mitigation: the checklist is the deliverable,
  the link is a garnish.

### Stage 1+ — *(recommended)* Stage 1, plus Zettacard-authored **graded** Killercoda scenarios

- **Delivers:** what Stage 0 actually lacks — **automated pass/fail feedback** ("you broke the selector; now
  `kubectl get endpointslices` is empty — CHECK") — on a real cluster, with **zero Zettacard-hosted infra**.
  Scenario source lives in a **Zettacard-owned public git repo** under `CC BY-NC-SA 4.0`, consistent with every
  other piece of Zettacard content.
- **Zettacard infra:** none. **Money:** €0 to author and €0 to the learner on Killercoda's FREE tier.
- **Engineering:** the same `related[]` link work as Stage 1, plus scenario authoring (JSON + Markdown + Bash +
  verification scripts). Author **short scenarios of 15–25 min** to fit the FREE tier's 1-hour cap and 1-concurrent
  limit.
- **Constraint:** ✅ **no exception** — identical posture to an embedded YouTube video, and arguably weaker, since
  it is an ordinary outbound link rather than an embed.
- **Ongoing cost:** scenarios must be re-tested at each Kubernetes bump (Killercoda's public schedule:
  1.35 → 1.36 on **2026-09-01**). That is a real recurring chore, but it is *testing*, not *operating*.
- **Risk:** dependency on a third party that could shut down or start charging. **Bounded** because (a) the prose
  labs remain complete and authoritative, (b) the scenario source is portable text in Zettacard's own repo, and
  (c) removal is one commit.

### Stage 2 — Zettacard self-hosts an ephemeral sandbox layer

- **Delivers:** an in-product browser terminal against a per-learner `kind`/`k3d` cluster, time-boxed and
  auto-reaped.
- **Money:** **cheap** — **[derived]** $0.016–$0.031 per learner-hour on Fly.io; ~€14/month of Hetzner absorbs
  ~438 one-hour sessions.
- **Engineering:** **expensive** — **[estimate]** 3–6 weeks to a first *safe* deployment, then permanent ops.
  Requires building **identity and rate limiting first** (§5), a second non-static hosting footprint outside
  Netlify, and K8s-version upkeep forever.
- **Constraint:** 🚨 **genuine architectural exception to `AGENTS.md` #6.** Larger than the media exception on
  every axis (§3 table).
- **Additional load:** anonymous RCE for the public, crypto-mining abuse as a *certainty* not a risk, outbound
  abuse liability, container-escape exposure, GDPR logs, unbounded-bill failure mode.
- **Verdict: not now.** If it is ever done, it needs **its own scoping doc and its own PO sign-off**, exactly as
  the media exception got — it must not arrive as a side effect of this document.

### Stage 3 — a full Killer.sh-style graded, proctored simulator

- **Delivers:** what Killer.sh already delivers (§2): 17 seeded scenarios, 120-minute countdown, 36-hour review
  window, per-sub-task automatic scoring, remote desktop, written solutions.
- **Money and engineering:** everything in Stage 2, plus per-question cluster fixtures and graders (the
  genuinely hard part), plus proctoring, plus keeping ~34 scenarios green across ~3 Kubernetes releases a year.
- **Constraint:** 🚨 the Stage 2 exception, permanently, at higher intensity.
- **The market answer, which is decisive:** Killer.sh charges **$39.99 for two sessions** and is **bundled free
  with the $445 exam** for CKA, CKAD, CKS, CNPE and LFCS. The incumbent's price to Zettacard's target learner is
  **zero**, it is operated by a specialist company, and it is endorsed by the certifying body. **Building this is
  building a worse copy of a free good.**
- **Verdict: no. Not at any point on the current roadmap.**

### Summary table

| | Delivers grading | Zettacard infra | Money | Eng. effort | Constraint 6 |
|---|---|---|---|---|---|
| **Stage 0** *(shipped)* | ✗ | none | €0 | done | ✅ none |
| **Stage 1** | ✗ (self-check only) | none | €0 | S | ✅ none |
| **Stage 1+** ⭐ | ✅ automated | none | €0 | S–M | ✅ none |
| **Stage 2** | ✅ (if built) | **servers** | ~€0.02/learner-h + ops | **L** | 🚨 exception |
| **Stage 3** | ✅ + proctored | **servers** | ops + content forever | **XL** | 🚨 exception |

---

## 7. Is AWS Solutions Architect the right second module?

### 7.1 The finding that changes the argument: AWS SAA is multiple-choice only

Verified twice, independently, on 2026-08-23:

- **aws.amazon.com/certification/certified-solutions-architect-associate/**: "**65 questions; either multiple
  choice or multiple response**", **130 minutes**, **$150 USD**.
- **AWS's own exam guide (docs.aws.amazon.com, SAA-C03)**: question types are **multiple choice** (1 correct of
  4) and **multiple response** (2+ correct of 5+); **50 scored + 15 unscored = 65**; passing score **720** on a
  100–1,000 scale; compensatory scoring. **No hands-on or lab component is mentioned anywhere.**

And this is not an SAA quirk — it is AWS-wide, and AWS has moved *away* from hands-on:

- The one AWS certification that ever had a performance-based component was **SysOps Administrator – Associate**,
  whose "exam labs" were discontinued. That certification has since been renamed **AWS Certified CloudOps
  Engineer – Associate** (SOA-C02 → **SOA-C03**, last day for SOA-C02: **2025-09-29**), and its current AWS
  product page states the same format as SAA: **"65 questions; either multiple choice or multiple response"**,
  130 minutes. **The AWS portfolio is now MCQ end to end.**

**Consequences, in order of importance:**

1. **A lab engine does not help anyone pass an AWS exam.** Hands-on AWS practice builds real skill and is
   genuinely valuable, but it is *not exam-format rehearsal*. The CKA argument ("our quiz cannot simulate the
   exam because the exam is hands-on") **does not transfer to AWS. It reverses.**
2. **For AWS, Zettacard can build the real thing** — a genuine format-faithful practice module — using the
   capability it already has: **131-question banks with fact/text-layer separation, 12-locale discipline,
   explanations, and topic tagging.** Same machinery as `datenschutz`, `dora`, `nis2`. **No new infrastructure.
   No constraint exception. No compute. No abuse surface.** This is the cheapest genuinely new capability on the
   table, and it is a *better* fit for a free offline-first PWA than any lab could ever be.
3. **The honesty framing changes with it** — and gets easier. For CKA the disclosure is "this is not an exam
   simulator, because the real thing is hands-on." For AWS SAA the disclosure is the ordinary Zettacard one:
   original questions, not sourced from any vendor's catalogue, not affiliated with or endorsed by AWS, does not
   reproduce confidential exam content. **Note the trademark/NDA discipline that comes with it:** AWS exam
   content is confidential; every question must be independently authored from the public exam guide and AWS
   documentation, exactly as `kartellrecht` was authored from statute rather than from competitors' banks. That
   is an existing, well-exercised project norm, not a new one.
4. **Caveat to verify before authoring:** AWS revises exams on its own schedule (SAA-C03 is current as at
   2026-08-23; SOA just went C02 → C03). Pin the exam-guide version in `meta` and re-check the guide at authoring
   time — the same discipline the compliance dossiers use for statute versions.

### 7.2 Which certifications would actually share a lab engine?

| Certification | Format | Hands-on? | Would share a lab engine? |
|---|---|---|---|
| **CKA** | performance-based, 2 h, $445 | ✅ | ✅ — **but Killer.sh is bundled free** |
| **CKAD / CKS** | performance-based (Killer.sh bundled) | ✅ | ✅ — same problem |
| **LFCS** | performance-based (Killer.sh bundled) | ✅ | ✅ — same problem |
| **CNPE** (new CNCF cert) | performance-based, 2 h, **$445**, "Linux-based remote desktop", Killer.sh bundled | ✅ | ✅ — same problem |
| **RHCSA (EX200)** | performance-based, "configurations must persist after reboot", no internet, no notes | ✅ | ⚠️ Red Hat-controlled ecosystem; lab images would be Rocky/Alma/CentOS Stream, not RHEL |
| **HashiCorp Terraform Associate** | **"Assessment Type: Multiple choice"**, 1 h | ✗ | ✗ — MCQ module instead |
| **HashiCorp Terraform Authoring & Operations Professional** | **"Lab-based and multiple choice"** | ✅ | ✅ — a genuine hybrid, but a small, senior audience |
| **AWS SAA / CloudOps / all AWS** | 65 Q, MCQ / multi-response | ✗ | ✗ — **MCQ module instead** |

**The pattern is a pincer, and it is the analytical core of this document:**

> **Where hands-on labs matter (the LF/CNCF family), the best-in-class graded simulator is already free to every
> candidate who paid the exam fee. Where labs do not matter (the entire AWS portfolio, Terraform Associate),
> building labs does not help anyone pass.**

There is no cell in that matrix where a Zettacard-built lab engine is the highest-value use of the next month of
engineering. The only genuine candidates for shared use — CKA, CKAD, CKS, LFCS, CNPE — are precisely the ones
where the incumbent is free.

### 7.3 The PO's other half — "open-source-based cloud training"

This is a *different product* and deserves not to be conflated with exam prep. Teaching Kubernetes / OpenTofu /
Linux as **skills**, with hands-on practice and no certification body in the loop, is the one framing where a
lab engine's value is not undercut by a free incumbent — because there is no exam, so there is no exam
simulator to compete with.

But it is a different business: it points at **B2B/paid training**, not at a free offline-first PWA, and it would
have to fund its own infrastructure rather than borrow the consumer product's. It also overlaps heavily with the
whitelabel line already scoped in `docs/whitelabel-regulatory-training-scoping-2026-08-17.md`. **Recommendation:
park it as a separate scoping question and do not let it justify Stage 2 infrastructure inside the consumer
product.**

---

## 8. Recommendation

**Do Stage 1+. Do not build Stage 2 or Stage 3. Make the next cert module an MCQ module, not a lab module.**

In priority order:

**1. Ship the static self-check layer (Stage 1). Highest value per hour of work in this document.**
The real gap in the current labs is not "no cluster" — the learner already has a cluster, that is the whole
design. The gap is **no feedback**. A per-task "run this, expect exactly this" checklist, authored as ordinary
course sections, is fully offline, fully within constraint 6, needs no infrastructure, and closes most of the
gap. It also creates the raw material for step 2.

**2. Author graded Killercoda scenarios (Stage 1+), source-controlled in a Zettacard repo under CC BY-NC-SA.**
Free to author, free to run, grading via verification scripts included, 2 GB kubeadm images and Kubernetes
upkeep included. Author them as **15–25 minute scenarios** to fit the FREE tier's 1-hour cap. Link them from the
lab lessons' `related[]` — which requires making `related[]` actually linkable, a generic course-layer
improvement worth landing anyway. Keep the prose labs authoritative so the course survives Killercoda going the
way of Katacoda and Play-with-Kubernetes.

**3. Make the AWS module an MCQ module.** AWS SAA is 65 MCQ/multi-response questions in 130 minutes. Zettacard's
existing question-bank machinery is a *format-faithful* answer to that exam — which is something it can honestly
say about AWS and can never honestly say about CKA. This is the cheapest new capability available, it needs no
infrastructure, and it needs no exception to anything. **If the PO wants a second technical module, this is it.**
Author strictly from the public exam guide and AWS documentation, never from any vendor's question bank, and pin
the exam-guide version in `meta`.

**4. If AWS hands-on pointers are wanted, link AWS's own** (Skill Builder free tier, Workshop Studio) and state
plainly that AWS Free Tier is **$100 + up to $100 in credits and expires at 6 months or credit exhaustion,
whichever comes first**, with **no automatic hard spend cap** documented. Never point a learner at a real AWS
account without that sentence.

**5. Do not adopt LocalStack.** Community edition ended **2026-03-23**; the remaining free tier **excludes
commercial use**; and even licensed, it emulates control-plane APIs (with, by its own docs, only the `default`
security group) rather than the networking and availability semantics SAA actually tests. Wrong licence and wrong
fidelity, in that order.

**6. Revisit Stage 2 only on a funded trigger, never on curiosity.** A concrete trigger: *a paying B2B customer
asks for hands-on labs and the contract covers the infrastructure and the operational burden.* Until then, the
arithmetic is unambiguous — €0.02/learner-hour of compute against **3–6 weeks [estimate]** of solo-operator
engineering plus permanent on-call plus an identity layer built from nothing plus a guaranteed crypto-mining
abuse problem, to reproduce something the learner already receives free with their exam registration.

**Why take this position rather than presenting the menu neutrally:** Zettacard's structural advantage is that
it ships *good content* at *zero marginal cost* with *no operational surface*. Stage 2 trades that advantage for
a feature where a well-funded specialist already gives the product away. Stage 1+ buys most of the learning
benefit — real clusters, real grading — for €0 and no exception, and the AWS MCQ module converts the PO's
instinct ("do more with this") into the thing Zettacard is uniquely good at.

**A note on the PO's framing, directly:** the intuition that a Killer.sh-style capability generalises across
certs is sound *as an engineering observation* — one sandbox engine really would serve CKA, CKAD, CKS, LFCS and
CNPE. It fails on market structure, not on architecture. Those five certs are exactly the ones where the
certifying body already ships a superior simulator at no marginal cost, and the cert the PO named as the second
customer — AWS SAA — turns out not to want a lab at all.

---

## 9. Punch list — decisions the PO owes

1. **Approve or reject Stage 1+** (Killercoda scenarios authored by Zettacard, linked out from lab lessons).
   Ownership question attached: Killercoda profile and GitHub repo under Zettacard's name?
2. **Confirm the licence for scenario source** — `CC BY-NC-SA 4.0` like all other content, or something more
   permissive given it lives in a third-party ecosystem?
3. **Confirm the design invariant**: labs stay `completion_rule: "read"` and never gate course completion or
   certificate issuance. (Recommended: yes, write it into the course-layer doc so it cannot drift.)
4. **Approve making `related[]` linkable** in the course reader — small generic change to `app/app.js`, needed by
   Stage 1 and Stage 1+ alike, and useful to every other course.
5. **Decide the second technical module**: AWS SAA as an **MCQ** module (recommended), or something else. If
   AWS: confirm the locale set (CKA's minimal 4, or the full 12?) and the exam-guide version to pin.
6. **Explicitly close Stage 2/Stage 3 for now**, so this does not get re-litigated informally. If Stage 2 is ever
   reopened, it gets its own scoping doc and its own sign-off, per the media-exception precedent.
7. **Decide whether "open-source-based cloud training"** (§7.3) is a separate product line worth scoping — it is
   the only framing in which a Zettacard-run lab engine is not competing with a free incumbent.
8. **Set a re-verification date.** Everything in §4 and §7 is priced/format-verified as at 2026-08-23; LocalStack,
   Killercoda, Hetzner and AWS all changed terms within the last 12 months.

---

## 10. Sources

All fetched **2026-08-23**. Sites marked *(JS-only)* return no content to a plain fetch and were read via a
text-extraction proxy; their figures should be spot-checked in a browser before being quoted externally.

**Killer.sh / Linux Foundation**
- https://killer.sh/cka *(JS-only)* — two sessions (CKA-A/CKA-B), 17+17 scenarios, 120-min countdown, 36-hour window, remote desktop, auto-score, ~100 pages of solutions
- https://killer.sh/pricing *(JS-only)* — $39.99 CKA/CKS/CKAD two sessions; $29.99 CNPE/LFCS; $9.99 rebuy; LF exams include two sessions
- https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/ — **$445**, 2 h, performance-based, Killer.sh included, one retake, Kubernetes v1.35
- https://training.linuxfoundation.org/certification/certified-cloud-native-platform-engineer-cnpe/ — **$445**, 2 h, performance-based, Linux remote desktop, Killer.sh (20 questions)
- https://github.com/kodekloudhub/community-faq/blob/main/docs/killer-sh.md — 36-hour sessions, bundled with exam, "more difficult than the real certification"

**Killercoda**
- https://killercoda.com/creators *(JS-only)* — GitHub-repo-driven scenarios; env images incl. `kubernetes-kubeadm-1node` (2 GB) / `-2nodes` (4 GB); K8s 1.35 → **1.36 on 2026-09-01**; verification scripts (`CHECK`, exit 0); FREE = 1 h / 1 concurrent, paid = 4 h / 3 concurrent
- https://killercoda.com/pricing *(JS-only)*, https://killercoda.com/faq *(JS-only)* — FREE / PLUS / COURSE tiers
- https://killercoda.com/teams *(JS-only)* — **$99 / $49.99 / $29.99 per user/month** at 1 / 3 / 6 months
- https://github.com/orgs/killercoda/repositories — 21 repos, **all scenarios/forks, no platform engine**
- https://freetier.co/directory/products/killercoda — third-party: PLUS ~$7.33/mo, COURSE ~$19.99/mo *(unverified)*

**Dead playgrounds**
- https://labs.play-with-k8s.com/ — "**unavailable starting March 1, 2026**"
- https://labs.play-with-docker.com/ — same notice
- https://kubernetes.io/blog/2023/02/14/kubernetes-katacoda-tutorials-stop-from-2023-03-31/ and https://github.com/kubernetes/website/issues/33936 — Katacoda shutdown precedent

**DIY building blocks**
- https://github.com/tsl0922/ttyd (MIT, last commit 2026-08-12), https://github.com/butlerx/wetty (MIT), https://github.com/sorenisanerd/gotty (MIT; "accepting input from remote clients is dangerous")
- https://github.com/kubernetes-sigs/kind, https://github.com/k3d-io/k3d
- https://docs.k3s.io/installation/requirements — server 2 cores / 2 GB; "Small ≤10 nodes" 1 vCPU / 2 GB

**Infrastructure pricing**
- https://fly.io/docs/about/pricing/ — `shared-cpu-2x` 2 GB **$0.0164/h**, 4 GB **$0.0309/h**; per-second billing
- https://www.digitalocean.com/pricing/droplets — 8 GB/4 vCPU **$48/mo, $0.07143/h**; **per-second billing effective 2026-01-01**
- https://betterstack.com/community/guides/web-servers/hetzner-cloud-review/ and https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ — **2026-04-01 price rise**; CPX32 4/8 GB **€13.99/mo**, CX23 2/4 GB €3.99, CPX42 8/16 GB €25.49

**Commercial lab platforms**
- https://instruqt.com/pricing — consumption-based annual, **no public figures**
- https://www.vendr.com/buyer-guides/instruqt — median **$28,410/yr**, range $10,000–$54,779, ~**$15,000 / 1,000 prepaid hours**
- https://strigo.io/pricing/ — **no figures published**; "Embeddable Labs" SKU exists

**LocalStack**
- https://blog.localstack.cloud/the-road-ahead-for-localstack/ (2025-12-18) and https://blog.localstack.cloud/2026-upcoming-pricing-changes/ — **"end support for … Community edition beginning on March 23, 2026"**; single authenticated image; **"our free tier will not permit usage for commercial purposes"**
- https://www.infoq.com/news/2026/02/localstack-aws-community/ — paid from **$39/mo billed annually**; community reaction; Moto and other alternatives
- https://www.srvrlss.io/provider/localstack/ — third-party tier/price summary (Base $45/mo, Ultimate $89/mo) *(unverified)*
- https://docs.localstack.cloud/aws/services/ — full service catalogue
- https://docs.localstack.cloud/aws/services/ec2 — **"LocalStack only supports the `default` security group"**; Linux host required

**AWS exam format and free options**
- https://aws.amazon.com/certification/certified-solutions-architect-associate/ — **"65 questions; either multiple choice or multiple response"**, 130 min, **$150**
- https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html — SAA-C03: MC + MR only, 50 scored + 15 unscored, pass 720/1000, **no lab component**
- https://aws.amazon.com/certification/certified-cloudops-engineer-associate/ — SysOps → **CloudOps**, **65 questions MC/MR**, 130 min
- https://aws.amazon.com/blogs/training-and-certification/exam-update-and-new-name-for-operations-certification/ — SOA-C02 → SOA-C03, last SOA-C02 day **2025-09-29**
- https://skillbuilder.aws/subscriptions — **$29/mo, $449/yr**; free account: Builder Labs **"Cloud Foundations only"**, Cloud Quest/SimuLearn limited to Cloud Practitioner + GenAI Practitioner
- https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/ — **$100 + up to $100** credits; **"expires either 6 months after sign-up or when Free Tier credits are depleted, whichever comes first"**
- https://aws.amazon.com/education/awseducate/

**Other certifications**
- https://developer.hashicorp.com/certifications/infrastructure-automation — Terraform Associate **"Assessment Type: Multiple choice"**; Terraform Authoring & Operations Professional **"Lab-based and multiple choice"**
- https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam — performance-based, "configurations must persist after reboot", no internet or notes

**Abuse / security**
- https://www.sysdig.com/blog/massive-cryptomining-operation-github-actions — PURPLEURCHIN: 30+ GitHub, 2,000 Heroku, 900 Buddy.works accounts, 130+ Docker Hub images; **~$15/mo cost per abused GitHub account**, ~$103,000 total; **>$100,000 provider cost per Monero mined**; Fly.io among targets
- https://www.trendmicro.com/en_us/research/22/g/unpacking-cloud-based-cryptocurrency-miners-that-abuse-github-ac.html, https://www.bleepingcomputer.com/news/security/massive-cryptomining-campaign-abuses-free-tier-cloud-dev-resources/

**Zettacard repo (verified in-repo 2026-08-23)**
- `AGENTS.md` constraint 6 (offline-first) and §7 (PO owns constraint changes)
- `docs/course-media-sections.md` §6 — the one existing, disclosed exception, and the discipline that came with it
- `docs/whitelabel-regulatory-training-scoping-2026-08-17.md` §1.2 — `related[]` renders prose-only (`app.js:4864–4874`)
- `data/cka_pilot.json` (131 Q, EN-canonical, "not an exam simulator"), `data/cka_course.json` (3 lab lessons, `completion_rule: "read"`), `data/modules_manifest.json` (CKA `_comment` + in-app disclosure), `netlify/functions/` (3 credential functions), `app/app.js:2866` ("zero-backend static PWA")
