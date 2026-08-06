# Scoping: Real Cryptographic Signing for Zettacard Credentials

Status: **step 1 of the recommendation below (section 4) is implemented** — a Netlify Function
(`netlify/functions/sign-credential.js`) plus static JWKS (`app/.well-known/jwks.json`) now sign
completion records as real JWT credentials, with a graceful offline/unreachable fallback to the
original self-issued/unverified shape. See `docs/open-badges-signing-setup.md` for the exact env
var / deploy steps still required before this is live (private key generation and the Netlify env
var still need to be done by someone with real deploy access - not done as part of this pass), the
key-rotation plan, and the third-party verification walkthrough. The rest of this document (options
b/c/d, section 3's positioning discipline, etc.) remains as originally written and still applies.

## 0. Where we are today

`app/app.js` (`credentialJsonDoc()`, around line 1014, see comment block from line 911) already
produces a JSON object shaped like an Open Badges 3.0 / W3C Verifiable Credential 2.0 payload
(`@context` includes `https://www.w3.org/ns/credentials/v2` and the OB3 context, `type` includes
`OpenBadgeCredential`). It is explicitly marked `unverified: true` with an `unverifiedReason` string,
and the UI disclaimer says the same thing in both languages. There is no issuer keypair, no signature,
no resolvable issuer identity — it's a locally-generated file a user downloads, nothing more. This is
the honest current baseline this document proposes moving on from.

The app is a zero-backend static PWA on Netlify. Any signing approach has to either add a minimal
backend surface or avoid needing one at all.

## 1. Signing architecture options

### (a) Serverless function holding an issuer private key (Netlify Functions / Cloudflare Workers)

A function invoked when a user requests a credential after a real exam-simulation pass. It holds (or
fetches from a secrets store) the issuer's private key, builds the VC payload server-side, signs it,
and returns the signed credential to the client for download.

- **Complexity**: Moderate. Requires: a function endpoint, a signing library (e.g. `jose` for
  JWT-based VCs, or a Data Integrity/JSON-LD signing library for `Ed25519Signature2020`), a way to
  authenticate the request as "this device really did complete a real exam pass" (today that's purely
  client-side state — moving signing server-side reopens the question of how the server knows the
  exam was actually passed, since currently `localStorage` is the only source of truth and is
  trivially editable client-side).
- **Ops burden**: Low-to-moderate. Netlify Functions and Cloudflare Workers both support secret/environment-variable
  storage for the private key without it ever appearing in client code or a public repo
  ([Cloudflare Workers secrets docs](https://developers.cloudflare.com/workers/configuration/secrets/),
  [Netlify env var guide](https://www.netlify.com/blog/a-guide-to-storing-api-keys-securely-with-environment-variables/)).
  Both platforms are effectively zero-maintenance (no servers to patch), but you now own key rotation policy,
  incident response if the key leaks, and rate-limiting/abuse handling for a public signing endpoint.
- **Cost**: Both Netlify Functions and Cloudflare Workers have generous free tiers adequate for a
  low-volume exam-prep app; this stays near-zero at current traffic.
- **Verdict**: The natural "smallest real backend" option, and the one that best preserves the
  product's current UX (instant download after passing).

### (b) Manual/batch signing process

No live signing endpoint. Instead, exam-pass events (or user-submitted requests) are collected
(e.g. a form submission, an email, or a periodic export) and a human/script signs a batch of
credentials offline using a key kept outside the app entirely, then the signed credential is
delivered back to the user (email, download link) out of band.

- **Complexity**: Low to build (a script + a manual step), but shifts effort into an ongoing
  manual process rather than eliminating it.
- **Ops burden**: No hosting/uptime concern at all, but real recurring human labor, latency (not
  real-time — could be hours to days), and it doesn't scale past small volumes.
- **Cost**: Effectively free in infrastructure, costly in time.
- **Verdict**: Reasonable as a *very first* proof of concept ("can we sign one real credential and
  get a verifier to accept it") but not viable as the actual product experience — passing an exam
  and not getting your credential for days undermines the whole feature.

### (c) Integrate with an existing third-party Open Badges issuing platform/API

Instead of building signing in-house, use a managed credentialing platform (e.g. Sertifier, Open
Badge Factory, CertifyMe, Certopus, POK, Certifier — all currently marketed as OB3-capable issuing
platforms) via their API: Zettacard calls their API after a passed exam, they mint and sign the
badge under their own (or a delegated) issuer identity, and hand back a verifiable credential/link.

- **Complexity**: Low-to-moderate — mostly integration work (API key, HTTP call from a still-needed
  small serverless function, since these platforms also need a server-side call to protect API
  keys), no cryptography to implement or get wrong yourself.
- **Ops burden**: Lowest of all options for anything crypto-related — key management, DID/JWKS
  hosting, and signing-suite correctness become the vendor's problem, not Zettacard's. Tradeoff:
  vendor lock-in, a recurring subscription cost, and the issuer identity a verifier sees may be
  "Zettacard via [Platform]" rather than a clean `did:web` under Zettacard's own domain, depending
  on the platform's white-labeling options.
- **Cost**: Ongoing subscription/usage fees (varies by platform and volume) — the only option with
  a real recurring monetary cost baked in from day one.
- **Verdict**: Worth a cost/lock-in comparison before deciding, but attractive precisely because it
  minimizes Zettacard's own cryptographic surface area and rotation/uptime responsibility.

### (d) DID-based (e.g. `did:web`) vs. simpler non-DID signing

Two sub-choices, largely orthogonal to (a)/(b)/(c):

- **`did:web` + JSON-LD Data Integrity proof (e.g. `Ed25519Signature2020`)**: The issuer identity is
  a DID resolvable at Zettacard's own domain (e.g. `did:web:zettacard.example`), backed by a
  `did.json` document served at a well-known path containing the public key. Credentials are signed
  with a JSON-LD Data Integrity proof. This is the "fuller" VC ecosystem approach and aligns with
  what the W3C VC Data Model and OB3 examples typically show. `Ed25519Signature2020` remains an
  actively maintained W3C Data Integrity suite with a live conformance test suite
  ([w3c/vc-di-ed25519signature2020-test-suite](https://github.com/w3c/vc-di-ed25519signature2020-test-suite)).
- **JWT-based VC (a signed JWT whose payload is the VC/OB3 claims, no DID required)**: Simpler to
  implement (any JWT library, e.g. `jose`, handles this), doesn't require standing up a DID document
  at all — the "issuer" can just be a plain HTTPS URL to a JWKS endpoint. There's active IETF work
  in this space too (`SD-JWT VC`, currently an IETF draft:
  [draft-ietf-oauth-sd-jwt-vc](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/)), for
  selective-disclosure JWT-based credentials, though that's more relevant if Zettacard ever needs to
  let a holder disclose only part of a credential — likely overkill for a first version.
- **Complexity comparison**: `did:web` + JSON-LD signing is more moving parts (DID document hosting,
  correct JSON-LD canonicalization, a Data Integrity library) but is the more "native" Open Badges
  3.0/VC approach and is what verifier tools are built and tested against most. A plain signed-JWT
  VC with a JWKS endpoint is simpler to implement correctly and easier to reason about (it's "just
  a JWT"), at the cost of being a less canonical/idiomatic OB3 presentation — some verifier tooling
  may expect the JSON-LD/Data Integrity shape specifically, or need the JWT variant configured.
- **Ops burden**: `did:web` requires the DID document to stay reachable at a stable URL forever (it's
  effectively a permanent public artifact — this is very compatible with Zettacard's existing static
  hosting, since a DID document is just a static JSON file). A JWKS endpoint has the same "must stay
  up and correct forever" property, also easy to serve statically. Both require a real key-rotation
  plan since verifiers may cache or expect the key at a stable location for however long issued
  credentials remain "current."

## 2. Verification story

For a third party to actually verify a Zettacard-issued credential, they need to be able to resolve
the issuer's public verification material and check the signature against it:

- **If `did:web`**: a verifier resolves `https://zettacard.example/.well-known/did.json` (or the
  appropriate `did:web` path convention) to get the DID document, extracts the verification method
  (public key), and checks the Data Integrity proof on the credential.
- **If JWT/JWKS-based**: a verifier fetches a JWKS endpoint (a static JSON file listing public keys
  by `kid`) referenced by the credential/JWT header, and verifies the JWT signature against the
  matching key.

Both of these are static JSON files/endpoints — genuinely compatible with the project's zero-backend,
static-hosting philosophy for the *verification* side, even if *issuing* needs a signing function
somewhere (options a/b/c above).

**Existing verifier tooling, as of this research (Aug 2026)**: The original Mozilla/IMS "badgecheck"
tooling has effectively been superseded — the actively maintained validator is 1EdTech's
[digital-credentials-public-validator](https://github.com/1EdTech/digital-credentials-public-validator),
which is the current public validator for Open Badges (and Comprehensive Learner Record) credentials
from the standard's own steward. There's also at least one independent public OB3 validator,
[CertLister's OB3 Validator](https://certlister.com/ob3-validator/), and
[Virtualbadge.io's Open Badges Validator](https://virtualbadge.io/resources/open-badges-validator). A
properly-formed, standards-conformant OB3 credential with a resolvable `did:web` or JWKS-based
verification method **should** validate against these out of the box, since that's exactly the
conformance surface they're built to test — but this needs to be confirmed empirically against a real
signed test credential before assuming it, since JSON-LD context/canonicalization details and exact
proof-suite support vary between validators. Third-party employer tooling is unlikely to build custom
OB3 support from scratch; realistically, they would either use one of these public validators
themselves or trust a "verified ✓" badge Zettacard's own site shows after doing the check internally.

## 3. What this app can honestly claim, even fully signed

This matters independent of the signing mechanism, and the recommendation below assumes it:

- German Arbeitssicherheit (occupational safety) training obligations are legally
  **tätigkeitsbezogen** — activity-specific to the actual workplace, equipment, and hazards a given
  employee faces. A generic exam-simulation pass in an app cannot certify that site-specific,
  role-specific training occurred.
- The EU AI Act's training/literacy obligations are similarly **role-based** — tailored to what a
  specific person does with AI systems in their specific job.
- Consequently, **a real cryptographic signature only proves who issued the credential and that its
  content hasn't been tampered with — it does not and cannot upgrade what the credential's content is
  entitled to claim.** Signing changes "can I trust this JSON wasn't faked by the holder" from "no"
  to "yes." It does not change "does this satisfy tätigkeitsbezogene Unterweisungspflicht" from "no"
  to "yes."
- The credential, signed or not, should keep claiming only: *"this person completed a general
  baseline exam simulation on topic X, on this date, with these results."* Any future signed
  credential's `achievement.description`/`criteria.narrative` field should continue to say this
  plainly, and product copy/UI should continue to make clear that a new employer/site must still
  layer their own activity-specific supplement on top — signing must not be allowed to make the
  credential *sound* more authoritative than its content actually is. This is a copy/positioning
  discipline issue as much as a technical one, and should be revisited explicitly when this is
  actually built, not just inherited from this doc.

## 4. Recommendation

**Given the zero-backend, low-operational-overhead philosophy that has held so far, the most
sensible first real step is option (a) — a single small serverless function (Netlify Function is
the more natural fit for a Netlify-hosted project) that signs credentials as plain signed JWTs
against a JWKS endpoint, not a full `did:web` + JSON-LD Data Integrity setup.**

Rationale: this is the smallest change that produces a *genuinely* third-party-verifiable credential.
It adds exactly one small serverless endpoint plus one static JSON file (the JWKS), both of which fit
comfortably alongside the existing static hosting rather than requiring a "real backend" in any
heavier sense. It avoids committing to JSON-LD canonicalization correctness or DID document
maintenance before it's clear the extra rigor is needed, and it avoids a recurring vendor subscription
(option c) before validating there's real demand for this feature. Option (b) (manual/batch) is the
even-smaller path if the team wants to sanity-check "does a verifier tool actually accept a
Zettacard-signed credential" before writing any endpoint at all — that could be a true proof-of-concept
predecessor to (a), not an alternative to it.

### Smallest viable version of the recommended step

1. Generate one Ed25519 (or similar) issuer keypair; store the private key as a Netlify Function
   environment secret; publish the public key as a static JWKS JSON file at a stable, permanent URL
   on the existing site.
2. Add one Netlify Function endpoint that: accepts an exam-completion record (same shape already
   produced by `recordCompletion()`), builds the same `credentialJsonDoc()`-style payload minus the
   `unverified`/`unverifiedReason` fields, signs it as a JWT, and returns it.
3. Change the "Download credential (JSON)" button to call this endpoint instead of building the
   unsigned JSON locally, with an honest fallback: if the function is unreachable (offline PWA use is
   a real scenario here), keep offering today's self-issued/unverified JSON as a degraded fallback
   rather than blocking the download entirely.
4. Manually verify one issued credential against the 1EdTech public validator and/or CertLister's OB3
   validator before treating this as done, to confirm real-world verifier compatibility rather than
   assuming spec conformance is sufficient.
5. Write down a key-rotation plan (even a minimal one — e.g. "rotate annually, keep the old public
   key in the JWKS for N months so previously issued credentials don't break") before shipping this
   to real users, since this is the piece most likely to be forgotten later.
6. Leave the "what a signed credential can honestly claim" language (Section 3) unchanged in the
   credential content and UI — signing is additive trust in the issuer's identity, not a change in
   scope of what's being attested.

## Sources consulted

- [Open Badges 3.0: What Is the Status in 2026?](https://www.virtualbadge.io/blog-articles/open-badges-3-0-what-is-the-status-in-2026)
- [Open Badges Specification 3.0 Candidate Final Public (1EdTech)](https://1edtech.github.io/openbadges-specification/ob_v3p0.html)
- [1EdTech: New Open Badges 3.0 Standard Provides Enhanced Security and Mobility](https://www.1edtech.org/1edtech-article/new-open-badges-30-standard-provides-enhanced-security-and-mobility/411060)
- [1EdTech digital-credentials-public-validator (GitHub)](https://github.com/1EdTech/digital-credentials-public-validator)
- [CertLister OB3 Validator](https://certlister.com/ob3-validator/)
- [Virtualbadge.io Open Badges Validator](https://virtualbadge.io/resources/open-badges-validator)
- [w3c/vc-di-ed25519signature2020-test-suite (GitHub)](https://github.com/w3c/vc-di-ed25519signature2020-test-suite)
- [SD-JWT-based Verifiable Digital Credentials — IETF draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/)
- [How to create a did:web and issue/verify W3C Verifiable Credentials (Medium)](https://medium.com/@skounis/how-to-create-a-did-web-and-issue-and-verify-w3c-verifiable-credentials-bcd5215e378d)
- [Cloudflare Workers: Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)
- [Netlify: A Guide to Storing API Keys Securely with Environment Variables](https://www.netlify.com/blog/a-guide-to-storing-api-keys-securely-with-environment-variables/)
- Managed issuing platforms surveyed for option (c): Sertifier, Open Badge Factory, CertifyMe,
  Certopus, POK, Certifier (via general 2026 digital-credential-platform roundups — no single
  platform verified in depth; a follow-up spike should get current pricing/API details directly
  before committing to option (c)).
