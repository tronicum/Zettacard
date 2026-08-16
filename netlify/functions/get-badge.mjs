// Netlify Function: public retrieval/verify endpoint for test badges
// issued by issue-badge.mjs. GET /.netlify/functions/get-badge?id=<badgeId>
// returns the stored badge record (which includes the signed JWT itself)
// as JSON, or a clean 404 if nothing was ever stored under that id (e.g.
// the badge was issued while Netlify Blobs was unreachable - see
// issue-badge.mjs's `blobStored: false` fallback).
//
// Intentionally NO AUTH - same trust model as sign-credential.js's public
// signing endpoint and the public JWKS at app/.well-known/jwks.json. The
// stored record's only "secret-shaped" fields are salted, one-way identity
// hashes (see netlify/functions/lib/identity-hash.mjs) - not the plaintext
// name/email that produced them, and not anything that could be turned
// back into them - so there is nothing here that requires gating who can
// look up a badge id. A badge id (crypto.randomUUID()) is itself the only
// thing that has to be known to look one up, the same way a `jti` in a
// JWT is a public-but-unguessable-in-practice identifier, not a secret.
//
// -----------------------------------------------------------------------
// 2026-08-16, round 3: converted from Functions v1 to Functions v2 for the
// exact same reason as issue-badge.mjs - see that file's top-of-file
// comment for the full root-cause writeup (secret-flagged env vars don't
// reach v1 function runtimes on this site's deploy method; v2 gets
// automatic, zero-config Blobs credentials instead, confirmed working live
// via a throwaway probe function before converting either real endpoint).
// -----------------------------------------------------------------------
import { getStore } from "@netlify/blobs";

const BLOBS_STORE_NAME = "test-badges";

// crypto.randomUUID() output shape: 8-4-4-4-12 lowercase hex, hyphen-
// separated (e.g. "3fa85f64-5717-4562-b3fc-2c963f66afa6"). Validating
// against this specific shape - rather than just "any non-empty string" -
// means a malformed/junk `id` query param is rejected with a clean 400
// before it ever reaches the Blobs store lookup, in the same spirit as
// sign-credential.js's SAFE_CODE_RE guard on its own string inputs.
const SAFE_BADGE_ID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function jsonResponse(statusCode, body) {
  return new Response(JSON.stringify(body), {
    status: statusCode,
    headers: { "content-type": "application/json" },
  });
}

export default async (request) => {
  if (request.method !== "GET") {
    return jsonResponse(405, { error: "Method not allowed. Use GET." });
  }

  const url = new URL(request.url);
  const id = url.searchParams.get("id");
  if (typeof id !== "string" || !SAFE_BADGE_ID_RE.test(id)) {
    return jsonResponse(400, { error: "Invalid or missing 'id' query parameter." });
  }

  try {
    // No explicit siteID/token - see the top-of-file comment. Automatic
    // Blobs credential injection for Functions v2.
    const store = getStore(BLOBS_STORE_NAME);
    const record = await store.get(id, { type: "json" });

    if (!record) {
      return jsonResponse(404, { error: "Badge not found." });
    }

    return jsonResponse(200, record);
  } catch (e) {
    console.error("get-badge: lookup failed:", e);
    return jsonResponse(500, { error: "Failed to retrieve badge." });
  }
};
