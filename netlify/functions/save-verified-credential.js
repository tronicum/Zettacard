// Netlify Function: persists an ALREADY-SIGNED completion record (see
// sign-credential.js) to Netlify Blobs under a random public slug, so it
// can be shown at a permanent, shareable /verify/<slug> page (see
// verify-credential.js) - the actual DN-49 deliverable: a link a DGUV
// auditor or new employer can just open, not a JSON file only a
// technical person could check.
//
// -----------------------------------------------------------------------
// SCOPE, DELIBERATE (see docs/paid-verifiable-certificates-scoping.md):
// - Only the 4 workplace-compliance modules (datenschutz, arbeitssicherheit,
//   ki_act, it_sicherheit) may get a permanent link - driving/fishing
//   modules are out of scope for this feature entirely, by PO decision.
// - MVP ships at 0€ - no payment gate here at all. Every passed compliance
//   Exam Simulation may request a permanent link, for free, for now.
// - Only records that carry a REAL signature (verified:true + a signedJwt
//   that actually verifies against the live JWKS) may be persisted here -
//   this function independently re-verifies the signature itself rather
//   than trusting the client's claim, exactly like sign-credential.js
//   never trusts client-computed exam results for anything that matters.
//   A self-issued/unverified record is NOT eligible for a permanent link;
//   that would undermine the whole point of the feature (a link that's
//   supposed to mean "cryptographically real" showing up for something
//   that isn't).
// -----------------------------------------------------------------------

let _josePromise;
function loadJose() {
  if (!_josePromise) _josePromise = import("jose");
  return _josePromise;
}
let _blobsPromise;
function loadBlobs() {
  if (!_blobsPromise) _blobsPromise = import("@netlify/blobs");
  return _blobsPromise;
}

const ALG = "ES256";
const ISSUER_URL = process.env.URL || "https://zettacard.netlify.app";
const JWKS_PATH = "/.well-known/jwks.json";
const STORE_NAME = "verified-credentials";

const COMPLIANCE_EXAM_TYPES = new Set(["datenschutz", "arbeitssicherheit", "ki_act", "it_sicherheit"]);
const MAX_LABEL_LEN = 200;
const MAX_NAME_LEN = 100;
const SAFE_CODE_RE = /^[a-zA-Z0-9_-]{1,64}$/;

function jsonResponse(statusCode, body) {
  return { statusCode, headers: { "content-type": "application/json" }, body: JSON.stringify(body) };
}

// Strips control characters only - stored as plain data. The actual
// HTML-safety boundary is enforced on the OUTPUT side (verify-credential.js
// escapes it when rendering, the same discipline certificateHtmlDoc() in
// app.js already uses for user-adjacent text) - escaping on render is the
// correct place for that, not mangling the stored value here. Purely a
// display label, never used as an identifier or compared against anything.
function sanitizeName(raw) {
  if (typeof raw !== "string") return null;
  const controlCharsRe = new RegExp("[\\x00-\\x1f\\x7f]", "g");
  const cleaned = raw.replace(controlCharsRe, "").trim();
  if (!cleaned) return null;
  return cleaned.slice(0, MAX_NAME_LEN);
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return jsonResponse(405, { error: "Method not allowed. Use POST." });
  }

  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch (e) {
    return jsonResponse(400, { error: "Request body must be valid JSON." });
  }

  const {
    id, examType, scopeCode, moduleLabel, scopeLabel, passedAt,
    errorPoints, wrongHighStakes, totalQuestions,
    signedJwt, signedKid, signedAlg, participantName,
  } = payload;

  if (typeof examType !== "string" || !COMPLIANCE_EXAM_TYPES.has(examType)) {
    return jsonResponse(400, { error: "Permanent verification links are only available for the compliance modules (datenschutz, arbeitssicherheit, ki_act, it_sicherheit)." });
  }
  if (typeof id !== "string" || id.length < 1 || id.length > MAX_LABEL_LEN) {
    return jsonResponse(400, { error: "Invalid or missing 'id'." });
  }
  if (typeof scopeCode !== "string" || !SAFE_CODE_RE.test(scopeCode)) {
    return jsonResponse(400, { error: "Invalid or missing 'scopeCode'." });
  }
  if (typeof moduleLabel !== "string" || !moduleLabel || moduleLabel.length > MAX_LABEL_LEN) {
    return jsonResponse(400, { error: "Invalid or missing 'moduleLabel'." });
  }
  if (typeof scopeLabel !== "string" || !scopeLabel || scopeLabel.length > MAX_LABEL_LEN) {
    return jsonResponse(400, { error: "Invalid or missing 'scopeLabel'." });
  }
  if (typeof passedAt !== "string" || Number.isNaN(new Date(passedAt).getTime())) {
    return jsonResponse(400, { error: "Invalid or missing 'passedAt'." });
  }
  if (!Number.isInteger(totalQuestions) || totalQuestions < 1) {
    return jsonResponse(400, { error: "Invalid or missing 'totalQuestions'." });
  }
  if (!Number.isInteger(errorPoints) || errorPoints < 0) {
    return jsonResponse(400, { error: "Invalid or missing 'errorPoints'." });
  }
  if (!Number.isInteger(wrongHighStakes) || wrongHighStakes < 0) {
    return jsonResponse(400, { error: "Invalid or missing 'wrongHighStakes'." });
  }
  if (typeof signedJwt !== "string" || !signedJwt) {
    return jsonResponse(400, { error: "A permanent link requires an already-signed credential (signedJwt missing) - self-issued/unverified completions are not eligible." });
  }

  // Independently re-verify the signature ourselves - never trust the
  // client's "this is signed" claim, same discipline sign-credential.js
  // already applies to exam results.
  try {
    const jwksRaw = await fetch(`${ISSUER_URL}${JWKS_PATH}`).then((r) => r.json());
    const jwk = (jwksRaw.keys || []).find((k) => k.kid === signedKid) || jwksRaw.keys?.[0];
    if (!jwk) throw new Error("No matching key in JWKS.");
    const { importJWK, jwtVerify } = await loadJose();
    const publicKey = await importJWK(jwk, signedAlg || ALG);
    await jwtVerify(signedJwt, publicKey, { issuer: ISSUER_URL });
  } catch (e) {
    console.error("save-verified-credential: signature re-verification failed:", e);
    return jsonResponse(400, { error: "The provided signature could not be independently verified - a permanent link cannot be created for it." });
  }

  const slug = crypto.randomUUID();
  const record = {
    slug, id, examType, scopeCode, moduleLabel, scopeLabel, passedAt,
    errorPoints, wrongHighStakes, totalQuestions,
    signedJwt, signedKid: signedKid || null, signedAlg: signedAlg || ALG,
    participantName: sanitizeName(participantName),
    createdAt: new Date().toISOString(),
  };

  try {
    const { getStore } = await loadBlobs();
    const store = getStore(STORE_NAME);
    await store.setJSON(slug, record);
  } catch (e) {
    console.error("save-verified-credential: Blobs write failed:", e);
    return jsonResponse(500, { error: "Could not save the permanent verification record on this deployment." });
  }

  return jsonResponse(200, { slug, verifyUrl: `${ISSUER_URL}/verify/${slug}` });
};
