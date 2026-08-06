// Netlify Function: signs a completed exam-simulation record as a real,
// third-party-verifiable JWT credential.
//
// This is the "smallest viable version of the recommended step" from
// docs/open-badges-signing-scoping.md (section 4): a single serverless
// function holding an issuer private key, signing plain JWTs against a
// static JWKS (app/.well-known/jwks.json) - not a full did:web/JSON-LD
// Data Integrity setup. See that doc for the full reasoning.
//
// -----------------------------------------------------------------------
// IMPORTANT, HONEST TRUST-BOUNDARY NOTE (read before assuming this is more
// than it is):
//
// This app's exam-simulation logic (questions, correct answers, pass/fail
// threshold) lives ENTIRELY client-side (see app/app.js computeExamResults()
// and friends) - there is no server-side answer key, question bank, or
// grading logic anywhere in this repo or this function. That means this
// function can validate that the SHAPE of a completion record is
// well-formed and internally consistent (see validateCompletionPayload
// below), but it CANNOT independently re-grade the exam or truly prove the
// user actually answered the underlying questions correctly - it is
// trusting the client's computed results the same way the current
// self-issued/unverified flow does.
//
// What this signature DOES prove to a third-party verifier: "Zettacard's
// signing key attests that a completion record with exactly these claims
// was submitted and accepted." What it does NOT prove: "the exam engine
// itself was tamper-proof end-to-end" - a sufficiently motivated user could
// still forge a plausible-looking payload client-side before it reaches
// this function, same as they always could edit localStorage today. Closing
// that gap fully would require moving the entire question bank and grading
// logic server-side, which is a real architecture change, not something to
// fake here. This function's real value-add is narrower and still genuine:
// it converts "a JSON file typed in a text editor could look identical to
// a real one" (true of today's client-only unverified credential) into "a
// forged credential must also have a valid signature from a key that never
// leaves Netlify's environment-variable store" - a meaningfully higher bar,
// just not a perfect one.
// -----------------------------------------------------------------------

const { importJWK, SignJWT } = require("jose");

const ALG = "ES256";
// Public, stable identity for the issuer - this is what a verifier will see
// in the JWT's `iss` claim and should match wherever the JWKS is actually
// reachable so a verifier can find the right key.
const ISSUER_URL = process.env.URL || "https://drivenow-fahrschule.netlify.app";
const JWKS_PATH = "/.well-known/jwks.json";

// Reasonable sanity bounds - not a re-grade, just rejecting shapes that
// couldn't possibly correspond to a real exam-simulation pass produced by
// this app's own recordCompletion() (see app/app.js).
const MAX_QUESTIONS = 500;
const MAX_LABEL_LEN = 200;
const SAFE_CODE_RE = /^[a-zA-Z0-9_-]{1,64}$/;
// How far in the past/future a submitted passedAt may reasonably be. Wide
// enough to tolerate clock skew and offline users signing later after
// reconnecting, without accepting arbitrarily old/replayed or
// future-dated timestamps.
const MAX_AGE_MS = 1000 * 60 * 60 * 24 * 30; // 30 days
const MAX_FUTURE_SKEW_MS = 1000 * 60 * 10; // 10 minutes

function jsonResponse(statusCode, body) {
  return {
    statusCode,
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  };
}

// Validates shape/types/plausibility of the client-submitted completion
// record. Returns { ok: true, record } or { ok: false, error }.
function validateCompletionPayload(payload) {
  if (!payload || typeof payload !== "object") {
    return { ok: false, error: "Request body must be a JSON object." };
  }
  const { id, examType, scopeCode, moduleLabel, scopeLabel, passedAt, errorPoints, wrongHighStakes, totalQuestions } = payload;

  if (typeof id !== "string" || id.length < 1 || id.length > MAX_LABEL_LEN) {
    return { ok: false, error: "Invalid or missing 'id'." };
  }
  if (typeof examType !== "string" || !SAFE_CODE_RE.test(examType)) {
    return { ok: false, error: "Invalid or missing 'examType'." };
  }
  if (typeof scopeCode !== "string" || !SAFE_CODE_RE.test(scopeCode)) {
    return { ok: false, error: "Invalid or missing 'scopeCode'." };
  }
  if (typeof moduleLabel !== "string" || moduleLabel.length < 1 || moduleLabel.length > MAX_LABEL_LEN) {
    return { ok: false, error: "Invalid or missing 'moduleLabel'." };
  }
  if (typeof scopeLabel !== "string" || scopeLabel.length < 1 || scopeLabel.length > MAX_LABEL_LEN) {
    return { ok: false, error: "Invalid or missing 'scopeLabel'." };
  }
  const passedAtDate = new Date(passedAt);
  if (typeof passedAt !== "string" || Number.isNaN(passedAtDate.getTime())) {
    return { ok: false, error: "Invalid or missing 'passedAt' (must be an ISO date string)." };
  }
  const now = Date.now();
  const passedAtMs = passedAtDate.getTime();
  if (passedAtMs > now + MAX_FUTURE_SKEW_MS) {
    return { ok: false, error: "'passedAt' is implausibly in the future." };
  }
  if (now - passedAtMs > MAX_AGE_MS) {
    return { ok: false, error: "'passedAt' is too old to sign (exceeds max allowed age)." };
  }
  if (!Number.isInteger(totalQuestions) || totalQuestions < 1 || totalQuestions > MAX_QUESTIONS) {
    return { ok: false, error: "Invalid or missing 'totalQuestions'." };
  }
  if (!Number.isInteger(errorPoints) || errorPoints < 0 || errorPoints > totalQuestions * 10) {
    return { ok: false, error: "Invalid or missing 'errorPoints'." };
  }
  if (!Number.isInteger(wrongHighStakes) || wrongHighStakes < 0 || wrongHighStakes > totalQuestions) {
    return { ok: false, error: "Invalid or missing 'wrongHighStakes'." };
  }

  return {
    ok: true,
    record: { id, examType, scopeCode, moduleLabel, scopeLabel, passedAt, errorPoints, wrongHighStakes, totalQuestions },
  };
}

// Mirrors app/app.js credentialJsonDoc()'s achievement shape, extended with
// real issuer/proof-carrying claims instead of unverified/unverifiedReason.
function buildCredentialClaims(record) {
  return {
    "@context": ["https://www.w3.org/ns/credentials/v2", "https://purl.imsglobal.org/spec/ob/v3p0/context.json"],
    type: ["VerifiableCredential", "OpenBadgeCredential"],
    issuer: { type: "Profile", id: ISSUER_URL, name: "Zettacard" },
    validFrom: record.passedAt,
    credentialSubject: {
      type: "AchievementSubject",
      achievement: {
        type: "Achievement",
        name: `${record.moduleLabel} - ${record.scopeLabel}`,
        description: `Passed an Exam Simulation for ${record.moduleLabel} (${record.scopeLabel}) in the Zettacard app.`,
        criteria: {
          narrative: `${record.totalQuestions}-question simulated exam, ${record.errorPoints} error points, ${record.wrongHighStakes} wrong safety-critical answer(s).`,
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
    // caller.
    console.error("sign-credential: ZETTACARD_SIGNING_PRIVATE_JWK is not set.");
    return jsonResponse(500, { error: "Signing is not configured on this deployment." });
  }

  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch (e) {
    return jsonResponse(400, { error: "Request body must be valid JSON." });
  }

  const validation = validateCompletionPayload(payload);
  if (!validation.ok) {
    return jsonResponse(400, { error: validation.error });
  }
  const record = validation.record;

  let privateJwk;
  try {
    privateJwk = JSON.parse(privateJwkRaw);
  } catch (e) {
    console.error("sign-credential: ZETTACARD_SIGNING_PRIVATE_JWK is not valid JSON.");
    return jsonResponse(500, { error: "Signing is not configured correctly on this deployment." });
  }

  try {
    const privateKey = await importJWK(privateJwk, ALG);
    const vc = buildCredentialClaims(record);
    const now = Math.floor(Date.now() / 1000);

    const jwt = await new SignJWT({ vc })
      .setProtectedHeader({ alg: ALG, kid: privateJwk.kid, typ: "JWT" })
      .setIssuedAt(now)
      .setIssuer(ISSUER_URL)
      .setJti(record.id)
      .sign(privateKey);

    return jsonResponse(200, {
      verified: true,
      jwt,
      kid: privateJwk.kid,
      alg: ALG,
      jwksUrl: `${ISSUER_URL}${JWKS_PATH}`,
      issuedAt: new Date(now * 1000).toISOString(),
    });
  } catch (e) {
    console.error("sign-credential: signing failed:", e);
    return jsonResponse(500, { error: "Failed to sign credential." });
  }
};
