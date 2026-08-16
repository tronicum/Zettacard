// Netlify Function: manually issues a signed, salted-hash-identity TEST
// badge, used to verify the identity-hashing + signing + Blobs-storage
// pipeline end-to-end (crypto.randomUUID() badge id -> hashed identity ->
// ES256-signed JWT -> Netlify Blobs -> get-badge.js retrieval), NOT for
// real exam-completion credentials.
//
// -----------------------------------------------------------------------
// Why this is a SEPARATE function from sign-credential.js, not a mode/flag
// on it:
//
// sign-credential.js is already live in production signing real exam-
// completion credentials (see its own top-of-file comment for the full
// trust-boundary discussion). Bolting a "test badge" branch onto that
// file's request handling would risk regressing the one thing it must
// never do - sign or mis-shape a real completion credential - for the sake
// of a feature that has nothing to do with exam completions. Keeping this
// entirely separate means a bug here (bad validation, a hashing mistake, a
// Blobs outage) cannot touch the live exam-signing path at all. The two
// functions do share the same signing key/JWKS (there is only one
// Zettacard issuer identity to verify against) and the same jose-loading
// and ES256/JWT conventions, mirrored deliberately for consistency - see
// sign-credential.js for the canonical version of those conventions.
// -----------------------------------------------------------------------

// jose v6 ships as an ESM-only package - a top-level `require("jose")`
// crashes Netlify's bundled CommonJS function at runtime with a raw
// ERR_REQUIRE_ESM stack trace (confirmed live on sign-credential.js's first
// real deploy, 2026-08-06 - see that file's comment for the full story). A
// dynamic import() works from CommonJS and is cached after the first call
// within a given function instance, so this has no real per-request cost
// beyond the first invocation. Mirrored here exactly for the same reason.
let _josePromise;
function loadJose() {
  if (!_josePromise) _josePromise = import("jose");
  return _josePromise;
}

// @netlify/blobs actually ships a dual CJS/ESM build (unlike jose, which is
// ESM-only), so a top-level require() would probably work today - but
// "probably works with this particular bundler" is exactly the assumption
// that already broke sign-credential.js's first real deploy for jose, and
// this project isn't interested in re-learning that lesson a second time
// for a different package. Same lazy-import-with-cache treatment, for
// consistency and safety, whether or not it's strictly required.
let _blobsPromise;
function loadBlobs() {
  if (!_blobsPromise) _blobsPromise = import("@netlify/blobs");
  return _blobsPromise;
}

const crypto = require("crypto");
const { hashIdentity } = require("./lib/identity-hash");

const ALG = "ES256";
// Same issuer identity/JWKS as sign-credential.js - see that file's
// comment for the full reasoning. Duplicated here rather than factored
// into a shared constants module so this file stays a single self-
// contained unit and sign-credential.js's live behavior is never at risk
// of being affected by a change made for this file's sake.
const ISSUER_URL = process.env.URL || "https://zettacard.netlify.app";
const JWKS_PATH = "/.well-known/jwks.json";

const BLOBS_STORE_NAME = "test-badges";

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
  return {
    statusCode,
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  };
}

// Validates shape/types/plausibility of the client-submitted test-badge
// request. Returns { ok: true, record } or { ok: false, error }. Mirrors
// validateCompletionPayload's style in sign-credential.js: explicit,
// individually-messaged 400 rejections, no silent coercion of bad input
// into "close enough" values.
function validateIssueBadgePayload(payload) {
  if (!payload || typeof payload !== "object") {
    return { ok: false, error: "Request body must be a JSON object." };
  }
  const { name, email, achievementName, achievementDescription, test } = payload;

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

  if (typeof achievementName !== "string" || achievementName.length < 1 || achievementName.length > MAX_ACHIEVEMENT_NAME_LEN) {
    return { ok: false, error: "Invalid or missing 'achievementName'." };
  }

  if (typeof achievementDescription !== "string" || achievementDescription.length < 1 || achievementDescription.length > MAX_ACHIEVEMENT_DESC_LEN) {
    return { ok: false, error: "Invalid or missing 'achievementDescription'." };
  }

  return {
    ok: true,
    record: {
      name: normalizedName,
      email,
      achievementName,
      achievementDescription,
    },
  };
}

// Builds the VC/OB3 claims for a manually-issued test badge. Follows the
// exact same @context/type/issuer conventions as sign-credential.js's
// buildCredentialClaims() (same ISSUER_URL, same @context array, same
// type: ["VerifiableCredential", "OpenBadgeCredential"]), but with a
// credentialSubject shaped for a hashed, privacy-preserving identity
// rather than sign-credential.js's fully anonymous default.
function buildCredentialClaims({ name, achievementName, achievementDescription, emailHash, emailSalt, nameHash, nameSalt, issuedAtIso }) {
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
      },
    },
  };
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
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
    payload = JSON.parse(event.body || "{}");
  } catch (e) {
    return jsonResponse(400, { error: "Request body must be valid JSON." });
  }

  const validation = validateIssueBadgePayload(payload);
  if (!validation.ok) {
    return jsonResponse(400, { error: validation.error });
  }
  const { name, email, achievementName, achievementDescription } = validation.record;

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
    const { importJWK, SignJWT } = await loadJose();
    const privateKey = await importJWK(privateJwk, ALG);
    const now = Math.floor(Date.now() / 1000);
    const issuedAt = new Date(now * 1000).toISOString();

    const vc = buildCredentialClaims({
      name,
      achievementName,
      achievementDescription,
      emailHash: emailHashResult.hash,
      emailSalt: emailHashResult.salt,
      nameHash: nameHashResult ? nameHashResult.hash : undefined,
      nameSalt: nameHashResult ? nameHashResult.salt : undefined,
      issuedAtIso: issuedAt,
    });

    const jwt = await new SignJWT({ vc })
      .setProtectedHeader({ alg: ALG, kid: privateJwk.kid, typ: "JWT" })
      .setIssuedAt(now)
      .setIssuer(ISSUER_URL)
      .setJti(badgeId)
      .sign(privateKey);

    const kid = privateJwk.kid;
    const jwksUrl = `${ISSUER_URL}${JWKS_PATH}`;

    // The JWT is already validly signed at this point - a storage failure
    // below must NOT fail the whole request, since the caller's actual
    // deliverable (a verifiable credential) already exists and is correct
    // regardless of whether Netlify Blobs happens to be reachable right
    // now. Storage is a nice-to-have retrieval convenience (get-badge.js),
    // not a correctness requirement of the signature itself.
    let blobStored = false;
    // TEMP DEBUG (2026-08-16): surfacing the actual storage error in the
    // response body, not just server logs, since this sandbox has no way
    // to read Netlify's live function logs directly. Remove blobError from
    // the response once the real cause is found and fixed - this endpoint
    // should never leak internal error detail to callers long-term, same
    // as sign-credential.js's existing "log server-side, stay generic to
    // the caller" convention.
    let blobError;
    try {
      const { getStore } = await loadBlobs();
      const store = getStore(BLOBS_STORE_NAME);
      // Only what's already going into the public JWT anyway (the hash,
      // never the raw value) plus non-PII metadata - deliberately NOT the
      // plaintext name or email, even though this is a test-badge-only
      // store, to keep the storage layer held to the same no-plaintext-PII
      // bar as the credential itself.
      await store.setJSON(badgeId, {
        jwt,
        badgeId,
        kid,
        alg: ALG,
        jwksUrl,
        issuedAt,
        achievementName,
        hasName: !!name,
      });
      blobStored = true;
    } catch (storageErr) {
      console.error("issue-badge: failed to store badge in Netlify Blobs:", storageErr);
      blobError = String((storageErr && storageErr.stack) || storageErr);
    }

    return jsonResponse(200, {
      verified: true,
      jwt,
      badgeId,
      kid,
      alg: ALG,
      jwksUrl,
      issuedAt,
      blobStored,
      ...(blobError ? { blobError } : {}),
    });
  } catch (e) {
    console.error("issue-badge: signing failed:", e);
    return jsonResponse(500, { error: "Failed to sign credential." });
  }
};
