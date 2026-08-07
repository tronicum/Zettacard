# Scoping: Badge Portability to a Personal Wallet (DN-51)

Status: scoping only, no PO decision to build yet. Surfaced by an independent AI-assisted
brainstorm the PO ran and forwarded (2026-08-07, `mitarbeite_Suche.pdf`), which converged on
similar architecture to what Zettacard already ships and additionally raised a real, unbuilt idea:
today's signed badge is only reachable via this device's `localStorage` and the DN-49 permanent
`/verify/<slug>` page. Nothing is ever handed to the employee in a form they can carry to a wallet
app or a different platform (Credly, LinkedIn, a future employer's HR system) independent of this
one browser session. This document scopes what that would actually take, researched against real
wallet products rather than assumed.

## 1. The problem, stated precisely

A badge earned through a work account is awkward to keep once someone changes jobs, if the only
copy lives in that device's browser storage or is only checkable via a URL they have to remember to
bookmark. The DN-49 permanent link already solves "does this credential still check out" forever
(the slug never expires, the signature re-verifies live). What it doesn't solve is "can the person
*import this into something they own and control*, the way a LinkedIn certification or a Credly
badge lives in an account that's theirs, not their employer's."

## 2. What real badge wallets actually require (researched, not assumed)

Checked against current (2026) products and specs, not just marketing copy:

- **Credly** (Pearson-owned, arguably the largest active general-purpose badge wallet): for a badge
  issued by anyone other than Credly itself, the import mechanism is a **manual file upload** - the
  recipient downloads a `.png`, `.svg`, or `.json` badge file from the issuer and uploads it under
  their Credly profile's "Other" tab. Credly also checks that the email embedded in the badge
  matches an email already on the Credly account.
- **1EdTech Open Badge Passport** and **Canvas Credentials** (Badgr's successor, itself now
  rebranding again to "Parchment Digital Badges") work similarly for third-party badges.
- **Learner Credential Wallet** (the leading pure OB3/W3C-VC mobile wallet, stewarded by the
  OpenWallet Foundation) imports via a link or QR code from a standards-compliant issuer, or the
  newer VC-API Interaction URL protocol - genuinely different plumbing than Credly's upload model.
- **The "email a badge" flow** that's often assumed as the default is real, but it's a
  **claim/redemption link the recipient clicks**, not a file attached to the email. Open Badge
  Wallet and Credly both use "issuance email with a button → recipient accepts → badge lands in
  their account" as the pattern, not an emailed attachment.

Net: there is no single universal "push the badge into any wallet" API. Everything routes through
either (a) a file the user handles themselves, or (b) an email-triggered claim link, or (c) an
OB3-native link/QR flow. (a) is the cheapest to support and requires no server-side email
infrastructure at all.

## 3. OB2 baked images vs. OB3/W3C VC - which format actually matters here

Open Badges 2.0 "baking" embeds the badge assertion JSON directly into a PNG/SVG's own metadata, so
a wallet can extract it straight from the image file with no external lookup. Open Badges 3.0 (what
Zettacard already targets) is JSON-LD, cryptographically signed as a JWT or with a Data Integrity
proof, verified against the issuer's published keys rather than by reading embedded pixels. The
market hasn't fully converged - Credly still explicitly accepts OB2-baked images alongside OB3 JSON
uploads - but Zettacard is already committed to OB3/JWT via `sign-credential.js`, so baking a PNG
would be new, unrelated work with no clear payoff; not recommended.

## 4. A real, already-known blocker worth fixing before anything else

Session history already found (via the two external OB3 validators tested against a real signed
credential - CertLister and 1EdTech's own validator) that Zettacard's current downloadable JSON
credential (`credentialJsonDoc()` in `app/app.js`) has concrete OB3 spec-conformance gaps:
`achievement` has no `id`, and the `proof` field is a custom `{type: "JsonWebSignature", jwt: ...}`
shape rather than the JOSE/Data-Integrity proof shape OB3 validators actually expect. More
fundamentally: OB3's JWT-secured form expects the credential itself to be the compact
JWS(three dot-separated parts), not a JSON document with the JWT nested inside a `proof.jwt`
field - which is exactly what `sign-credential.js` already produces as `record.signedJwt` and
today's UI never offers as a standalone download. **This means real wallet/Credly-style import of
Zettacard's existing credential would likely already fail today**, independent of any new "email
it to yourself" feature - the file shape itself needs fixing first.

## 5. Recommended smallest viable version

1. **DONE (2026-08-07)**: added a "Download signed credential (JWT, for wallets)" button next to
   the existing certificate/JSON downloads (both "My certificates" and the exam-results screen),
   gated to genuinely-signed records, translated across all 12 locales. It's literally
   `record.signedJwt` written to a file - the actual OB3-compliant compact JWS a wallet or validator
   expects, not a wrapper around it. Verified via an extended `scripts/test_full_exam_badge.mjs`
   run (byte-compares the downloaded file against the record's own `signedJwt` after a real signed
   exam pass). This alone makes credential import via Credly-style "upload a file" flows viable for
   the first time, with zero new server work and zero new personal data captured. NOT done as part
   of this step: the separately-flagged `achievement.id`/proof-shape gaps in the existing JSON
   download (`credentialJsonDoc()`) are unrelated to this new button and remain open.
2. **Do not build email capture for this.** Every mainstream badge platform researched treats the
   earner's email as a required field and just accepts the GDPR processing that implies; no
   platform researched does a no-email self-service model. That means Zettacard doing the
   self-service download-only version would be *more* data-minimizing than the market standard, not
   a compromise - a genuine advantage worth keeping, not a gap to close by adding email capture to
   match competitors.
3. **Defer real wallet-side integration** (an actual "add to Credly"/"add to LCW" button, an
   email-claim-link flow, VC-API support) until there's a real user asking for it - it requires
   either outbound email infrastructure (a new capability this app doesn't have and that implies
   real GDPR handling of a personal address) or VC-API server support (real new backend work), for
   a benefit (one-click wallet import vs. "download the file, upload it to Credly yourself")
   that's meaningfully smaller than step 1's fix.

## 6. Open questions for the PO

- Is step 1 (JWT-file download) worth doing now as a small, self-contained fix, or does it wait
  until there's a real B2B/wallet-import ask?
- If email-claim-link delivery is ever wanted later, does the PO want to treat that as a genuinely
  separate, explicitly-consented opt-in (a checkbox, not a required field) to keep Zettacard's
  current zero-PII posture rather than defaulting to the market-standard "email required" pattern?

## Sources

- [Credly: How to Add an Outside Badge to Your Credly Profile](https://support.credly.com/hc/en-us/articles/30107800919707-How-to-Add-an-Outside-Badge-to-Your-Credly-Profile)
- [Credly's support for Open Badge 3.0](https://credlyissuer.zendesk.com/hc/en-us/articles/30498679997595-Credly-s-support-for-Open-Badge-3-0)
- [Learner Credential Wallet — GitHub (OpenWallet Foundation Labs)](https://github.com/openwallet-foundation-labs/learner-credential-wallet)
- [Canvas Credentials becoming Parchment Digital Badges](https://sites.gatech.edu/dlt-blog/2025/10/24/canvas-credentials-is-becoming-parchment-digital-badges)
- [IMS Global / 1EdTech Open Badges 3.0 Specification](https://www.imsglobal.org/spec/ob/v3p0)
- [Mozilla openbadges-backpack: Badge Baking API docs](https://github.com/mozilla/openbadges-backpack/blob/master/docs/apis/baking_api.md)
- [Open Badge Wallet — openbadge.world](https://openbadge.world/about/wallet.html)
- [Earner Personal Data, Consent and GDPR for Issuing Digital Badges](https://knowledge.realideas.org/earner-personal-data-consent-and-gdpr-for-issuing-digital-badges)
- [virtualbadge.io: GDPR for Credentials — Secure and Compliant Issuance](https://www.virtualbadge.io/blog-articles/gdpr-for-credentials-secure-and-compliant-issuance)
