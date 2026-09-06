// Netlify Function: public retrieval/verify endpoint for test badges
// issued by issue-badge.mjs. Reached through three stable public paths
// (see netlify.toml's redirect block right above the SPA catch-all, and
// its own comment on why they're deliberately CDN-shaped/implementation-
// decoupled) rather than being linked to directly:
//   GET /badges/:id                    -> format=html (this file's default
//                                          when no ?format is given, since
//                                          that's also how a raw function
//                                          URL with only ?id= behaves)
//   GET /badges/:id/credential.json    -> format=json (the full stored
//                                          record, incl. the signed JWT)
//   GET /badges/:id/credential.jwt     -> format=jwt (just the compact
//                                          JWS string, text/plain - the
//                                          exact bytes a wallet/importer
//                                          like Credly wants as an upload)
// A clean 404 (in whichever format was requested) if nothing was ever
// stored under that id - e.g. the badge was issued while Netlify Blobs
// was unreachable, see issue-badge.mjs's `blobStored: false` fallback.
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
//
// 2026-08-17, round 4: added the format=html/jwt paths above (previously
// this only ever returned the raw JSON record, at the raw function URL
// with no clean public path in front of it at all).
//
// 2026-09-03, round 5: netlify.toml's :id-in-query-string redirects
// (`to = "/.netlify/functions/get-badge?id=:id&format=json"` etc.) were
// found to NOT actually substitute :id into the destination on this
// deploy method - every one of /badges/:id, /badges/:id/credential.json
// and /badges/:id/credential.jwt came back 400 "Invalid or missing 'id'
// query parameter", while the direct function-call form
// (/.netlify/functions/get-badge?id=<id>&format=<format>) worked fine.
// Netlify's placeholder substitution into a PATH segment is the
// documented/well-supported form; substitution into a query-string value
// is the part that wasn't working here. Fix: netlify.toml's three rules
// now rewrite to a path-shaped destination
// (/.netlify/functions/get-badge/:id/:format) with force = true instead,
// and this function now ALSO parses id/format from the trailing path
// segments of the incoming request URL, added below, falling back to the
// original ?id=&format= query-string parsing when no path segments are
// present - so a direct function call using the old query-string form
// (still how a caller might reach this without going through the
// netlify.toml redirects at all) keeps working exactly as before.
// -----------------------------------------------------------------------
import { getStore } from "@netlify/blobs";

const BLOBS_STORE_NAME = "test-badges";

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

// Renders the human-facing verification page for a found badge. Deliberately
// plain/self-contained (inline <style>, no external CSS/JS/fonts) - matches
// how app/legal/*.html are built, and means this page has no dependency on
// anything else deploying correctly to render. Not trying to match the
// full app chrome; this is a verification/share page, not app UI.
function renderFoundHtml(record, badgeId) {
  const issuedAt = escapeHtml(record.issuedAt || "");
  const achievementName = escapeHtml(record.achievementName || "Zettacard credential");
  const kid = escapeHtml(record.kid || "");
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex,nofollow" />
<title>${achievementName} — Zettacard credential</title>
<style>
  body { font-family: -apple-system, system-ui, sans-serif; max-width: 40rem; margin: 3rem auto; padding: 0 1.25rem; background: #0b1220; color: #e8ecf4; line-height: 1.5; }
  .badge { background: #131b2e; border: 1px solid #263250; border-radius: 12px; padding: 1.5rem; }
  h1 { font-size: 1.3rem; margin: 0 0 .25rem; }
  .verified { color: #5fd08a; font-weight: 600; font-size: .9rem; }
  dl { display: grid; grid-template-columns: auto 1fr; gap: .35rem 1rem; margin: 1.25rem 0; font-size: .9rem; }
  dt { color: #93a1c2; }
  dd { margin: 0; word-break: break-all; }
  .downloads { margin-top: 1.25rem; display: flex; gap: .75rem; flex-wrap: wrap; }
  .downloads a { background: #263250; color: #e8ecf4; text-decoration: none; padding: .5rem .9rem; border-radius: 8px; font-size: .85rem; }
  .downloads a:hover { background: #33436a; }
  .note { margin-top: 1.5rem; font-size: .8rem; color: #93a1c2; }
</style>
</head>
<body>
  <div class="badge">
    <div class="verified">&#10003; Verified Zettacard credential</div>
    <h1>${achievementName}</h1>
    <dl>
      <dt>Issued</dt><dd>${issuedAt}</dd>
      <dt>Key ID</dt><dd>${kid}</dd>
      <dt>Badge ID</dt><dd>${escapeHtml(badgeId)}</dd>
    </dl>
    <div class="downloads">
      <!-- 2026-09-03: these used to point at the pretty /badges/:id/... form,
           which still 400s (see the top-of-file comment on the routing bug -
           not yet root-caused). Switched to the direct function-call form,
           which is the confirmed-working fallback issue-badge.mjs's own
           response fields already use - a PO hit exactly this "Download"
           button returning the 400 error before this fix. Revert once the
           pretty-URL redirect bug is actually fixed. -->
      <a href="/.netlify/functions/get-badge?id=${encodeURIComponent(badgeId)}&format=json&download=1">Download credential.json</a>
      <a href="/.netlify/functions/get-badge?id=${encodeURIComponent(badgeId)}&format=jwt&download=1">Download credential.jwt</a>
    </div>
    <p class="note">This is a signed Open Badges 3.0 / Verifiable Credential. To import into a wallet like Credly, download one of the files above and upload it there directly - most importers (Credly included) accept a file upload only, not a URL.</p>
  </div>
</body>
</html>`;
}

function renderNotFoundHtml(badgeId) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex,nofollow" />
<title>Credential not found — Zettacard</title>
<style>body { font-family: -apple-system, system-ui, sans-serif; max-width: 32rem; margin: 4rem auto; padding: 0 1.25rem; background: #0b1220; color: #e8ecf4; }</style>
</head>
<body>
  <h1>Credential not found</h1>
  <p>No badge is stored under id <code>${escapeHtml(badgeId)}</code>. It may have been issued while storage was unreachable, or the id is wrong.</p>
</body>
</html>`;
}

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

// "json" is the default so a bare `?id=...` call (the raw function URL,
// still reachable directly, and how every caller before this round used
// it) keeps returning exactly what it always has - no behavior change for
// anything that already depends on this endpoint. "html"/"jwt" are only
// ever requested via the netlify.toml rewrites, which append &format=...
// explicitly, but validating the value here regardless means a stray or
// malformed ?format on the raw function URL fails closed rather than
// falling through to something unexpected.
const VALID_FORMATS = new Set(["json", "html", "jwt"]);

// 2026-09-03: parses id/format from the trailing path segments of the
// incoming request, e.g. /.netlify/functions/get-badge/<id>/<format> (the
// destination shape netlify.toml's rewrites now use - see top-of-file
// comment). Returns { id, format } (format may be null if only one
// trailing segment was present) or null if the path doesn't end in
// anything path-shaped at all, in which case the caller falls back to
// query-string parsing.
function parsePathSegments(pathname) {
  const segments = pathname.split("/").filter(Boolean);
  // The function's own mount path is always at least
  // ["", ".netlify", "functions", "get-badge"] worth of segments before
  // anything path-shaped we added ourselves - a bare call to the function
  // (no extra segments) still ends in "get-badge" itself, so requiring at
  // least one segment *after* "get-badge" is what distinguishes "path form
  // used" from "query-string form used, nothing extra in the path".
  const fnIndex = segments.lastIndexOf("get-badge");
  if (fnIndex === -1 || fnIndex === segments.length - 1) {
    return null;
  }
  const extra = segments.slice(fnIndex + 1);
  const id = extra[0];
  const format = extra.length > 1 ? extra[1] : null;
  return { id, format };
}

export default async (request) => {
  if (request.method !== "GET") {
    return jsonResponse(405, { error: "Method not allowed. Use GET." });
  }

  const url = new URL(request.url);

  // Path segments first (the netlify.toml-rewritten public paths), falling
  // back to the original ?id=&format= query-string form - see top-of-file
  // comment. This keeps a direct function call
  // (/.netlify/functions/get-badge?id=...&format=...) working exactly as
  // it always has.
  const fromPath = parsePathSegments(url.pathname);
  const id = fromPath ? fromPath.id : url.searchParams.get("id");
  if (typeof id !== "string" || !SAFE_BADGE_ID_RE.test(id)) {
    return jsonResponse(400, { error: "Invalid or missing 'id' query parameter." });
  }

  const formatParam = (fromPath && fromPath.format) || url.searchParams.get("format") || "json";
  if (!VALID_FORMATS.has(formatParam)) {
    return jsonResponse(400, { error: "Invalid 'format' - must be json, html, or jwt." });
  }
  // ?download=1 (set by the html page's own download links) adds
  // Content-Disposition: attachment so the browser saves a file instead of
  // rendering it inline - this is what actually turns "visit a link" into
  // "get a file to upload to Credly", since Credly itself still only
  // accepts a file upload, never a URL (checked directly against Credly's
  // own support docs earlier this session - that hasn't changed, this
  // just makes getting the file a one-click action from a shareable link
  // instead of a manual curl/save-as).
  const wantsDownload = url.searchParams.get("download") === "1";

  let record;
  try {
    // No explicit siteID/token - see the top-of-file comment. Automatic
    // Blobs credential injection for Functions v2.
    const store = getStore(BLOBS_STORE_NAME);
    record = await store.get(id, { type: "json" });
  } catch (e) {
    console.error("get-badge: lookup failed:", e);
    if (formatParam === "html") {
      return new Response(renderNotFoundHtml(id), {
        status: 500,
        headers: { "content-type": "text/html; charset=utf-8" },
      });
    }
    return jsonResponse(500, { error: "Failed to retrieve badge." });
  }

  if (!record) {
    if (formatParam === "html") {
      return new Response(renderNotFoundHtml(id), {
        status: 404,
        headers: { "content-type": "text/html; charset=utf-8" },
      });
    }
    if (formatParam === "jwt") {
      return new Response("Badge not found.", {
        status: 404,
        headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    return jsonResponse(404, { error: "Badge not found." });
  }

  if (formatParam === "html") {
    return new Response(renderFoundHtml(record, id), {
      status: 200,
      headers: { "content-type": "text/html; charset=utf-8" },
    });
  }

  if (formatParam === "jwt") {
    const headers = { "content-type": "text/plain; charset=utf-8" };
    if (wantsDownload) {
      headers["content-disposition"] = `attachment; filename="zettacard-badge-${id}.jwt"`;
    }
    return new Response(record.jwt || "", { status: 200, headers });
  }

  // format === "json"
  const headers = { "content-type": "application/json" };
  if (wantsDownload) {
    headers["content-disposition"] = `attachment; filename="zettacard-badge-${id}.json"`;
  }
  return new Response(JSON.stringify(record, null, 2), { status: 200, headers });
};
