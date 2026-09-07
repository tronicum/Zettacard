// Netlify Function: manually issues a signed, salted-hash-identity TEST
// badge, used to verify the identity-hashing + signing + Blobs-storage
// pipeline end-to-end (crypto.randomUUID() badge id -> hashed identity ->
// ES256-signed JWT -> Netlify Blobs -> get-badge.mjs retrieval), NOT for
// real exam-completion credentials.
//
// -----------------------------------------------------------------------
// Why this is a SEPARATE function from sign-credential.js, not a mode/flag
// on it: see the original 2026-08-16 issue-badge.js's comment (same
// reasoning, unchanged) - sign-credential.js is already live signing real
// exam-completion credentials, and bolting a test-badge branch onto it
// would risk regressing the one thing it must never do, for the sake of a
// feature that has nothing to do with exam completions.
// -----------------------------------------------------------------------
//
// -----------------------------------------------------------------------
// 2026-08-16, round 3: converted from Functions v1 (exports.handler,
// event/callback style) to Functions v2 (export default, Request/Response
// style) SPECIFICALLY to fix a real, root-caused Netlify Blobs bug, not as
// a style preference:
//
// The v1 version passed an explicit { siteID, token } to getStore(),
// reading the token from a manually-created NETLIFY_BLOBS_TOKEN secret env
// var, because v1 functions never get Netlify's automatic Blobs credential
// injection (confirmed via Netlify's own official coding-context guidance:
// "This does NOT apply to legacy V1 functions which require manual
// siteID/token configuration"). That part worked as designed. What did NOT
// work: the token never actually reached process.env at runtime
// (getStore() kept throwing MissingBlobsEnvironmentError with
// hasToken: false), even after two rounds of fixing/broadening the env
// var's scopes. Root-caused this round via a set of harmless non-secret
// probe env vars deployed alongside a temporary diagnostic: a probe named
// with the exact same "NETLIFY_" and even "NETLIFY_BLOBS_" prefix as the
// real token reached process.env fine, ruling out any name-reservation
// theory - but a probe var created with envVarIsSecret: true (matching the
// real token's own "secret" flag, everything else identical) did NOT reach
// process.env. Conclusion: this project's zip/API deploy method (see
// docs/netlify-deploy-status.md) does not inject secret-flagged env vars
// into function runtimes at all - a Netlify platform behavior, not a
// config mistake in this repo. The two fixes available were (a) un-mark
// the token as non-secret, which trades a real security property (a
// Netlify Personal Access Token sitting in cleartext in the dashboard) for
// convenience - a decision for a human, not this session - or (b) stop
// needing a manually-managed secret at all by switching to Functions v2,
// which gets Netlify's automatic, zero-config, per-deploy-scoped Blobs
// credentials. Verified live via a throwaway blobs-v2-probe.mjs function
// (deployed, called getStore() with zero options, wrote+read a blob
// successfully) before converting this real function, precisely to avoid
// discovering a v2-specific problem only after committing to the rewrite.
// (b) was chosen: no secret to manage, no token to rotate or leak, works
// identically for this site's non-git-linked deploy method. The
// NETLIFY_BLOBS_TOKEN env var itself and the old blobsStoreOptions()
// helper are gone - genuinely unneeded now, not just unused.
// -----------------------------------------------------------------------
import crypto from "node:crypto";
import { importJWK, SignJWT } from "jose";
import { getStore } from "@netlify/blobs";
import { hashIdentity } from "./lib/identity-hash.mjs";
import { MODULE_ACHIEVEMENTS } from "./lib/module-achievements.mjs";
import { buildLinkedInAddUrl } from "./lib/linkedin.mjs";

const ALG = "ES256";
// Same issuer identity/JWKS as sign-credential.js - see that file's
// comment for the full reasoning. Duplicated here rather than factored
// into a shared constants module so this file stays a single self-
// contained unit and sign-credential.js's live behavior is never at risk
// of being affected by a change made for this file's sake.
const ISSUER_URL = process.env.URL || "https://zettacard.netlify.app";
const JWKS_PATH = "/.well-known/jwks.json";

const BLOBS_STORE_NAME = "test-badges";

// 2026-08-17: placeholder achievement image, added because Open Badges 3.0
// credentials are expected to carry a real image (and Credly's own
// importer renders it - shipping with none at all was worse than a
// placeholder while real art is still being designed). Points at a static
// file under app/assets/, which is already served with a CDN-friendly
// Cache-Control (see netlify.toml's "/assets/*" header rule) - no redirect
// needed, this is just a normal static asset. Swap
// app/assets/badges/test-badge.svg's *contents* for the real art when it
// exists; the path/URL below can stay the same, so no code change is
// needed to pick up new artwork for badges issued after the swap.
// 2026-09-03: this is now only the FALLBACK image, used when the caller
// doesn't supply a `moduleType` (see MODULE_ACHIEVEMENTS in
// ./lib/module-achievements.mjs for the per-module images that replace it
// when one is given).
const ACHIEVEMENT_IMAGE_PATH = "/assets/badges/test-badge.svg";

const ALLOWED_MODULE_TYPES = Object.keys(MODULE_ACHIEVEMENTS);

const MAX_NAME_LEN = 200;
const MAX_ACHIEVEMENT_NAME_LEN = 200;
const MAX_ACHIEVEMENT_DESC_LEN = 500;
// Not part of the task's explicit field-length spec, but a defensive
// sanity bound in the same spirit as sign-credential.js's MAX_LABEL_LEN -
// RFC 5321 caps a full email address at 254 characters; 320 gives a little
// slack without accepting arbitrarily long junk into a hashed field.
const MAX_EMAIL_LEN = 320;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function jsonResponse(statusCode, body) {
  return new Response(JSON.stringify(body), {
    status: statusCode,
    headers: { "content-type": "application/json" },
  });
}

// Validates shape/types/plausibility of the client-submitted test-badge
// request. Returns { ok: true, record } or { ok: false, error }. Mirrors
// validateCompletionPayload's style in sign-credential.js: explicit,
// individually-messaged 400 rejections, no silent coercion of bad input
// into "close enough" values.
//
// 2026-09-03: gained the optional `moduleType` field. Resolution order,
// per field, is: an explicitly-supplied achievementName/achievementDescription
// wins over MODULE_ACHIEVEMENTS[moduleType]'s corresponding value, which
// wins over the old hardcoded default (there is no hardcoded default for
// achievementName/achievementDescription any more - see below - so in
// practice this is "explicit value, else the module's value"). This keeps
// today's existing validation behavior for a caller that supplies neither
// moduleType nor achievementName: it was already required before this
// change, so a request with neither still needs to supply
// achievementName+achievementDescription directly, exactly as before.
function validateIssueBadgePayload(payload) {
  if (!payload || typeof payload !== "object") {
    return { ok: false, error: "Request body must be a JSON object." };
  }
  const { name, email, achievementName, achievementDescription, moduleType, test } = payload;

  // `test` must be exactly boolean true - this endpoint issues ONLY test
  // badges for now, so a missing/falsy/truthy-but-not-boolean value is
  // rejected outright rather than assumed. This is a deliberate guardrail,
  // not an oversight: there is no real-completion path through this
  // function at all yet, and requiring an explicit `test: true` makes that
  // impossible to trigger by accident (e.g. a client bug that omits the
  // field) as this endpoint's scope grows in the future.
  if (test !== true) {
    return { ok: false, error: "'test' must be exactly boolean true - this endpoint currently issues only test badges." };
  }

  let normalizedName;
  if (name !== undefined && name !== null) {
    if (typeof name !== "string" || name.length < 1 || name.length > MAX_NAME_LEN) {
      return { ok: false, error: "Invalid 'name' (must be a string of 1-200 characters if present)." };
    }
    normalizedName = name;
  }

  if (typeof email !== "string" || email.length < 1 || email.length > MAX_EMAIL_LEN || !EMAIL_RE.test(email)) {
    return { ok: false, error: "Invalid or missing 'email'." };
  }

  // moduleType is optional, but if present must be one of the four known
  // keys - fail closed (400) rather than silently falling through to "no
  // module metadata" on a typo'd/unknown value, which would otherwise
  // require achievementName/achievementDescription to also be present to
  // not also fail, masking the real mistake.
  let normalizedModuleType = null;
  if (moduleType !== undefined && moduleType !== null) {
    if (typeof moduleType !== "string" || !Object.prototype.hasOwnProperty.call(MODULE_ACHIEVEMENTS, moduleType)) {
      return { ok: false, error: "Unknown moduleType.", allowed: ALLOWED_MODULE_TYPES };
    }
    normalizedModuleType = moduleType;
  }

  const moduleMeta = normalizedModuleType ? MODULE_ACHIEVEMENTS[normalizedModuleType] : null;

  // Resolution order: explicit achievementName/achievementDescription wins
  // over the module's corresponding value. Either an explicit
  // achievementName or a moduleType must be present (same for
  // achievementDescription) - this is the backward-compatible relaxation
  // of what used to be an unconditionally-required field.
  let resolvedAchievementName;
  if (achievementName !== undefined && achievementName !== null) {
    if (typeof achievementName !== "string" || achievementName.length < 1 || achievementName.length > MAX_ACHIEVEMENT_NAME_LEN) {
      return { ok: false, error: "Invalid 'achievementName' (must be a string of 1-200 characters if present)." };
    }
    resolvedAchievementName = achievementName;
  } else if (moduleMeta) {
    resolvedAchievementName = moduleMeta.name;
  } else {
    return { ok: false, error: "Invalid or missing 'achievementName' (or supply a known 'moduleType')." };
  }

  let resolvedAchievementDescription;
  if (achievementDescription !== undefined && achievementDescription !== null) {
    if (typeof achievementDescription !== "string" || achievementDescription.length < 1 || achievementDescription.length > MAX_ACHIEVEMENT_DESC_LEN) {
      return { ok: false, error: "Invalid 'achievementDescription' (must be a string of 1-500 characters if present)." };
    }
    resolvedAchievementDescription = achievementDescription;
  } else if (moduleMeta) {
    resolvedAchievementDescription = moduleMeta.description;
  } else {
    return { ok: false, error: "Invalid or missing 'achievementDescription' (or supply a known 'moduleType')." };
  }

  // The achievement image: the module's own image if moduleType was given,
  // else the existing generic placeholder - see ACHIEVEMENT_IMAGE_PATH's
  // comment above. Resolved here (still a bare filename/path, not a full
  // URL) so the caller of buildCredentialClaims() below doesn't need to
  // know about MODULE_ACHIEVEMENTS at all.
  const achievementImagePath = moduleMeta ? `/assets/badges/${moduleMeta.image}` : ACHIEVEMENT_IMAGE_PATH;

  return {
    ok: true,
    record: {
      name: normalizedName,
      email,
      achievementName: resolvedAchievementName,
      achievementDescription: resolvedAchievementDescription,
      moduleType: normalizedModuleType,
      achievementImagePath,
    },
  };
}

// Builds the VC/OB3 claims for a manually-issued test badge. Follows the
// exact same @context/type/issuer conventions as sign-credential.js's
// buildCredentialClaims() (same ISSUER_URL, same @context array, same
// type: ["VerifiableCredential", "OpenBadgeCredential"]), but with a
// credentialSubject shaped for a hashed, privacy-preserving identity
// rather than sign-credential.js's fully anonymous default.
function buildCredentialClaims({ name, achievementName, achievementDescription, achievementImagePath, emailHash, emailSalt, nameHash, nameSalt, issuedAtIso, badgeId }) {
  const identifier = [
    {
      type: "IdentityObject",
      hashed: true,
      identityHash: emailHash,
      // Matches this project's own already validator-confirmed
      // identityType value from the live sign-credential.js flow (see
      // BACKLOG.md's "Optional multi-email identity binding" entry) - do
      // not invent a different string here.
      identityType: "email",
      salt: emailSalt,
    },
  ];
  if (name) {
    identifier.push({
      type: "IdentityObject",
      hashed: true,
      identityHash: nameHash,
      // Generic/catch-all identityType - deliberately NOT "name", which is
      // not a confirmed-valid OB3 identityType value and risks failing
      // external validator conformance checks the way this project's
      // DN-51 work already had to fix once before for a different
      // proof-shape gap.
      identityType: "identifier",
      salt: nameSalt,
    });
  }

  return {
    "@context": ["https://www.w3.org/ns/credentials/v2", "https://purl.imsglobal.org/spec/ob/v3p0/context.json"],
    type: ["VerifiableCredential", "OpenBadgeCredential"],
    issuer: { type: "Profile", id: ISSUER_URL, name: "Zettacard" },
    // sign-credential.js sets validFrom from the completion record's own
    // passedAt timestamp; a manually-issued test badge has no equivalent
    // "when it was earned" moment, so this uses the signing time itself -
    // the only timestamp that's actually meaningful for a badge that
    // exists purely to prove the pipeline works, not to record a real
    // achievement date.
    validFrom: issuedAtIso,
    // 2026-08-16, round 4: added `id` on the top-level credential.
    // BACKLOG.md's DN-51 re-verification round (2026-08-11) already found,
    // via real runs of the 1EdTech (vc.1ed.tech) and CertLister external
    // OB3 validators against sign-credential.js's output, that a credential
    // with no `vc.id` fails 1EdTech's JSON Schema check outright ("required
    // property 'id' not found") - that validator schema-checks the decoded
    // `vc` object directly and does not do the jti->id promotion VC-JWT
    // notionally allows. That fix was written up as a follow-up for
    // sign-credential.js at the time but this file (built later, 2026-08-16)
    // was never updated to include it - the same gap, unfixed, in a second
    // place.
    //
    // 2026-08-17, round 5: changed from a bare urn:uuid: URI to the real
    // dereferenceable /badges/:id/credential.json URL added this round (see
    // netlify.toml + get-badge.mjs). Both are spec-legal URI forms for
    // vc.id, but a URL a verifier can actually GET and get the credential
    // back from is strictly more useful than an opaque urn - it's the same
    // discoverability principle the `jku` header claim above already
    // applies to the issuer's signing key, just applied to the credential
    // itself. jti (below, on the JWT) still carries the bare badgeId -
    // that's a separate, narrower "unique token identifier" concept and
    // doesn't need to be a URL.
    // See the badgeUrl/credentialJsonUrl fallback comment above the
    // buildCredentialClaims() call site - same direct-function-URL
    // fallback applied here so vc.id is itself a working, dereferenceable
    // URL, not just the response fields.
    id: `${ISSUER_URL}/.netlify/functions/get-badge?id=${badgeId}&format=json`,
    credentialSubject: {
      type: "AchievementSubject",
      // Only include `name` here if the caller supplied one - this is the
      // VISIBLE plaintext name (Open Badges/VC credentialSubject.name is a
      // normal, spec-legal property, not something that needs hashing to
      // be valid - the separate hashed copy in `identifier` above is for
      // privacy-preserving third-party identity matching, e.g. wallet
      // import tools like Credly that check a hashed identifier against
      // the uploader's own account, not for concealing the visible name
      // which is deliberately shown).
      ...(name ? { name } : {}),
      identifier,
      achievement: {
        type: "Achievement",
        name: achievementName,
        description: `TEST BADGE — not earned via a real exam-simulation pass. ${achievementDescription}`,
        criteria: {
          narrative: "Manually issued to verify the Zettacard identity-hashing and credential-storage pipeline end-to-end. Not a real completion credential.",
        },
        // OB3 Achievement.image - see the ACHIEVEMENT_IMAGE_PATH/
        // MODULE_ACHIEVEMENTS comments above. `type: "Image"` matches the
        // OB3 spec's Image class. achievementImagePath is resolved against
        // ISSUER_URL here (never hardcoded into the stored module-metadata
        // config itself).
        image: { id: `${ISSUER_URL}${achievementImagePath}`, type: "Image" },
      },
    },
  };
}

export default async (request) => {
  if (request.method !== "POST") {
    return jsonResponse(405, { error: "Method not allowed. Use POST." });
  }

  const privateJwkRaw = process.env.ZETTACARD_SIGNING_PRIVATE_JWK;
  if (!privateJwkRaw) {
    // Missing env var - a deploy/config problem, not a client error. Log
    // server-side (Netlify function logs) but never leak internals to the
    // caller. Same treatment as sign-credential.js.
    console.error("issue-badge: ZETTACARD_SIGNING_PRIVATE_JWK is not set.");
    return jsonResponse(500, { error: "Signing is not configured on this deployment." });
  }

  let payload;
  try {
    payload = await request.json();
  } catch (e) {
    return jsonResponse(400, { error: "Request body must be valid JSON." });
  }

  const validation = validateIssueBadgePayload(payload);
  if (!validation.ok) {
    return jsonResponse(400, { error: validation.error, ...(validation.allowed ? { allowed: validation.allowed } : {}) });
  }
  const { name, email, achievementName, achievementDescription, moduleType, achievementImagePath } = validation.record;

  let privateJwk;
  try {
    privateJwk = JSON.parse(privateJwkRaw);
  } catch (e) {
    console.error("issue-badge: ZETTACARD_SIGNING_PRIVATE_JWK is not valid JSON.");
    return jsonResponse(500, { error: "Signing is not configured correctly on this deployment." });
  }

  // Normalize email to lowercase+trim before hashing - matches the pattern
  // already used on email inputs elsewhere in app/app.js. Hashing is
  // salted and one-way regardless, but normalizing first means the same
  // real-world address always hashes to a *comparable* value if the same
  // normalized string is re-hashed with the same salt elsewhere, rather
  // than "Stefan@Sels.com" and "stefan@sels.com " silently producing
  // unrelated hashes for what's really the same address.
  const normalizedEmail = email.toLowerCase().trim();
  const emailHashResult = hashIdentity(normalizedEmail);
  const nameHashResult = name ? hashIdentity(name) : null;

  const badgeId = crypto.randomUUID();

  try {
    const privateKey = await importJWK(privateJwk, ALG);
    const now = Math.floor(Date.now() / 1000);
    const issuedAt = new Date(now * 1000).toISOString();

    const kid = privateJwk.kid;
    const jwksUrl = `${ISSUER_URL}${JWKS_PATH}`;

    const vc = buildCredentialClaims({
      name,
      achievementName,
      achievementDescription,
      achievementImagePath,
      emailHash: emailHashResult.hash,
      emailSalt: emailHashResult.salt,
      nameHash: nameHashResult ? nameHashResult.hash : undefined,
      nameSalt: nameHashResult ? nameHashResult.salt : undefined,
      issuedAtIso: issuedAt,
      badgeId,
    });

    const jwt = await new SignJWT({ vc })
      // `jku` (JWK Set URL) added 2026-08-16, round 4 - same DN-51 gap as
      // the `vc.id` fix above. Without it, a verifier has no *standard*
      // way to discover this issuer's JWKS from the JWT alone - it would
      // have to already know, out of band, that this project's `kid`
      // convention resolves against jwksUrl. Both 1EdTech's and CertLister's
      // validators flagged exactly this when testing sign-credential.js's
      // output; a third-party importer (e.g. Credly) choking on a badge
      // with an undiscoverable issuer key is the same failure mode.
      .setProtectedHeader({ alg: ALG, kid, typ: "JWT", jku: jwksUrl })
      .setIssuedAt(now)
      .setIssuer(ISSUER_URL)
      .setJti(badgeId)
      .sign(privateKey);

    // The JWT is already validly signed at this point - a storage failure
    // below must NOT fail the whole request, since the caller's actual
    // deliverable (a verifiable credential) already exists and is correct
    // regardless of whether Netlify Blobs happens to be reachable right
    // now. Storage is a nice-to-have retrieval convenience (get-badge.mjs),
    // not a correctness requirement of the signature itself.
    let blobStored = false;
    let blobError;
    try {
      // No explicit siteID/token - see the top-of-file comment. Functions
      // v2 gets these auto-injected by Netlify, confirmed working live for
      // this site's own deploy method via the throwaway blobs-v2-probe.mjs
      // test before this file was converted.
      const store = getStore(BLOBS_STORE_NAME);
      // Only what's already going into the public JWT anyway (the hash,
      // never the raw value) plus non-PII metadata - deliberately NOT the
      // plaintext name or email, even though this is a test-badge-only
      // store, to keep the storage layer held to the same no-plaintext-PII
      // bar as the credential itself. `moduleType` (or null) is persisted
      // alongside the rest so a stored record shows which module (if any)
      // this test badge stands in for.
      await store.setJSON(badgeId, {
        jwt,
        badgeId,
        kid,
        alg: ALG,
        jwksUrl,
        issuedAt,
        achievementName,
        moduleType,
        hasName: !!name,
      });
      blobStored = true;
    } catch (storageErr) {
      console.error("issue-badge: failed to store badge in Netlify Blobs:", storageErr);
      blobError = String((storageErr && storageErr.message) || storageErr);
    }

    // 2026-09-03 PoC fix: the pretty /badges/:id[/credential.json|.jwt]
    // redirects (netlify.toml) still 400 on this deploy after two fix
    // attempts (query-string :id substitution, then a path-shaped
    // destination with force=true) - confirmed live on staging after
    // redeploying both. Root cause not yet found (see BACKLOG.md DN-91/
    // DN-92). Falling back to the DIRECT function-call URL form, which is
    // confirmed working (200) in every format - this is explicitly the
    // documented fallback option (b) from this feature's own design spec,
    // not a workaround invented ad hoc. Swap back to the /badges/:id form
    // once the redirect bug is actually root-caused and fixed; until then
    // every URL this function hands out must actually resolve, since
    // these get pasted into LinkedIn's live "Add to Profile" flow.
    const badgeUrl = `${ISSUER_URL}/.netlify/functions/get-badge?id=${badgeId}&format=html`;
    const credentialJsonUrl = `${ISSUER_URL}/.netlify/functions/get-badge?id=${badgeId}&format=json`;
    const credentialJwtUrl = `${ISSUER_URL}/.netlify/functions/get-badge?id=${badgeId}&format=jwt`;

    return jsonResponse(200, {
      ...(blobError ? { blobError } : {}),
      verified: true,
      jwt,
      badgeId,
      kid,
      alg: ALG,
      jwksUrl,
      issuedAt,
      blobStored,
      // The clean, CDN-shaped public URLs added this round - see
      // netlify.toml's redirect block and get-badge.mjs's top-of-file
      // comment for the full design rationale. badgeUrl is the one to
      // actually hand out/share; the other two are what its download
      // buttons point at, exposed here too so a caller that skips the
      // HTML page (e.g. a curl-based test script) doesn't have to
      // reconstruct them by hand. All three 404 until blobStored is true -
      // they read from the same Blobs record get-badge.mjs looks up.
      badgeUrl,
      credentialJsonUrl,
      credentialJwtUrl,
      // 2026-09-03: LinkedIn's "Add to Profile" certification deep link -
      // see netlify/functions/lib/linkedin.mjs for the full param
      // rationale. Built from the *resolved* achievementName (module
      // metadata or caller-supplied override, whichever won above) and the
      // freshly-minted badgeUrl/badgeId/issuedAt above.
      linkedinAddUrl: buildLinkedInAddUrl({ achievementName, badgeUrl, badgeId, issuedAt }),
    });
  } catch (e) {
    console.error("issue-badge: signing failed:", e);
    return jsonResponse(500, { error: "Failed to sign credential." });
  }
};
