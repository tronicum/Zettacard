# Setup: real signed credentials (Netlify Function + JWKS)

This is the implementation of the "smallest viable version of the recommended step" from
`docs/open-badges-signing-scoping.md` section 4: a Netlify Function
(`netlify/functions/sign-credential.js`) signs completion records as plain JWTs against a public
key published at `app/.well-known/jwks.json`. Read the scoping doc first for the full reasoning;
this doc is just the "how to actually turn this on" checklist plus the verifier walkthrough.

## What you (the person with Netlify deploy access) need to do before this works live

1. **Generate a real production keypair** (do not reuse any keypair generated during development/
   testing of this feature - treat those as compromised/throwaway since they may have passed
   through logs, chat, or a sandbox):
   ```
   node scripts/generate_signing_keypair.mjs
   ```
   This prints a public JWKS block and a private JWK.

2. **Set the Netlify env var** on the real site (Site settings -> Environment variables, or
   `netlify env:set`):
   - Name: `ZETTACARD_SIGNING_PRIVATE_JWK`
   - Value: the entire private JWK JSON object printed by the script, as one line, e.g.
     `{"kty":"EC","x":"...","y":"...","crv":"P-256","d":"...","kid":"...","alg":"ES256","use":"sig"}`
   - Scope it to at least the Production deploy context (add Deploy Previews/Branch deploys too
     only if you want signing to work there as well - if you do, consider a separate non-production
     keypair for those contexts so a leaked preview-deploy log can't compromise the production key).
   - Never put this value in `netlify.toml`, any committed file, or a public deploy log.

3. **Replace `app/.well-known/jwks.json`** with the public JWKS block the script printed (the
   `keys` array). This file IS meant to be committed - it's public key material only, and it's
   what verifiers fetch. The repo currently contains a **development/test keypair only**, used to
   prove the sign -> publish -> verify round trip works (see "Round-trip test" below) - swap it
   for your real production public key before relying on this in production, and make sure the
   `kid` in the JWKS matches the `kid` embedded in the private JWK you set in step 2 (the script
   generates both from the same run, so as long as you use its output for both, they'll match).

4. **Deploy.** Netlify's build reads `netlify.toml`'s `[functions] directory = "netlify/functions"`
   and bundles `sign-credential.js` together with its `jose` dependency (resolved via the repo-root
   `package.json` - this file exists purely so Netlify's function bundler can find/install `jose`;
   the rest of the app remains build-step-free per `netlify.toml`'s existing comments). No other
   Netlify config changes are needed - the existing SPA-fallback redirect does not swallow either
   `/.well-known/jwks.json` (a real static file) or `/.netlify/functions/*` (handled separately from
   the publish-directory redirect rules).

5. **Smoke-test in production** once deployed: pass a real exam simulation, download the JSON
   credential, confirm it has `"verified": true` and a `proof.jwt` field (not `"unverified": true`),
   then run it through the verification steps below.

## Key rotation (minimal plan, per scoping doc section 4 item 5)

- Rotate at least annually, or immediately if the private key is ever suspected to have leaked.
- When rotating: generate a new keypair, ADD its public JWK to the `keys` array in
  `app/.well-known/jwks.json` (don't remove the old one yet), set the new private JWK as the env
  var (functions pick up new env vars on next deploy), then remove the old public key from the
  JWKS only after enough time has passed that no currently-relevant issued credential still needs
  it verifiable (e.g. keep old keys for at least as long as the longest `renewal_months` among the
  compliance modules - see `data/*/core.json` `meta.renewal_months` - since that's roughly how long
  a credential stays "current" for its holder).

## Staging environment (added 2026-08-11)

`zettacard-staging` (Netlify site id `480e3ec6-76f6-414e-a7bc-eb3e661f5816`,
`https://zettacard-staging.netlify.app`) is a separate Netlify site deploying the same repo, used
to verify changes before they hit `zettacard.de` production. Deploy to it the same way as
production - the direct-deploy MCP flow, pointed at the staging site id instead of the production
one - since `git push` from this sandbox is still blocked (see BACKLOG.md's standing note on that).

Per this doc's own key-rotation guidance above ("consider a separate non-production keypair... so a
leaked preview-deploy log can't compromise the production key"), staging has its **own** signing
keypair, not a copy of production's:

- Staging's private key (kid `a3b138a4-d8d6-4902-9a49-9fbaa1e9d082`) is set as
  `ZETTACARD_SIGNING_PRIVATE_JWK` on the `zettacard-staging` site only - it was never committed or
  logged anywhere production-reachable.
- Its public JWK was ADDED (not swapped in) to `app/.well-known/jwks.json`'s `keys` array, alongside
  production's real key (kid `be87070e-0843-4868-9f24-8af7b1021096`). Both sites deploy the same
  file, and `verify-credential-v2.mjs` already resolves the right key by matching `record.signedKid`
  against the array - so this "just works" without any function-code changes, on both sites.
- Practical effect: a credential signed on staging is cryptographically distinguishable from a real
  production credential (different `kid`, different issuer `URL` via `process.env.URL`, which Netlify
  sets per-site automatically) - there's no way to mistake a staging test badge for a real one, even
  though both verify successfully against the one shared JWKS file.
- `ZC_TEST_VAR` (an old placeholder env var, unrelated to signing) was not copied to staging - only
  the signing key, since that's the only env var either function actually reads.

## How anyone can verify a signed credential themselves

A downloaded credential JSON with `"verified": true` has a `proof.jwt` field (a compact JWT string)
and a `proof.jwksUrl` field pointing at the public key set. To verify it:

1. Fetch the JWKS: `GET https://zettacard.netlify.app/.well-known/jwks.json`
2. Find the key whose `kid` matches the JWT's protected header `kid` (or `proof.kid` in the
   credential JSON) and the `alg` (`ES256`).
3. Verify the JWT's signature against that public key and inspect its `vc` claim for the actual
   credential content (issuer, achievement, criteria, `validFrom`, etc).

Example using `jose` (Node.js) - this is exactly what
`scripts/test_sign_credential.js` does as an automated round-trip check:

```js
import { importJWK, jwtVerify } from "jose";

const jwksRes = await fetch("https://zettacard.netlify.app/.well-known/jwks.json");
const jwks = await jwksRes.json();

const jwt = "..."; // from credential.proof.jwt
const header = JSON.parse(Buffer.from(jwt.split(".")[0], "base64url").toString());
const jwk = jwks.keys.find((k) => k.kid === header.kid);

const publicKey = await importJWK(jwk, header.alg);
const { payload } = await jwtVerify(jwt, publicKey); // throws if signature/claims don't check out
console.log(payload.vc); // the actual Open Badges 3.0 / VC-shaped credential content
```

A non-Node verifier can use any standard JWT/JOSE library (Python `jwcrypto`/`pyjwt` with JWK
support, Go `jose`/`jwx`, etc.) - the mechanics are identical: fetch the JWKS, match `kid`, verify.

For a fuller/standards-body validator pass (recommended before treating this as "done" per the
scoping doc's item 4), feed a real signed credential through 1EdTech's public validator
(https://github.com/1EdTech/digital-credentials-public-validator) or a public OB3 validator such
as CertLister's (https://certlister.com/ob3-validator/) - this hasn't been done yet as part of this
implementation pass and remains a follow-up before calling OB3 conformance itself confirmed (the
JWT signs and verifies correctly against the JWKS today; whether a third-party OB3-specific
validator accepts this exact JWT-VC shape/context combination is a separate, not-yet-checked
question).

## Known limitation (honest, on purpose)

`sign-credential.js` validates the *shape* and *plausibility* of a submitted completion record
(types, value ranges, timestamp freshness) but cannot re-grade the exam - the question bank and
grading logic live entirely client-side (`app/app.js`), and this function has no independent answer
key to check against. The signature proves "Zettacard's key attests this exact record was accepted
by the signing endpoint," not "this exact exam attempt was tamper-proof end-to-end." See the long
comment at the top of `netlify/functions/sign-credential.js` for the full reasoning - this is a
known, accepted limitation of a client-only exam architecture, not something hidden or glossed over.
