// Netlify Function: the actual public-facing deliverable of DN-49. Renders
// a plain, no-JS-required HTML page for a permanent /verify/<slug> link
// (routed here via the netlify.toml redirect, which must stay ABOVE the
// catch-all SPA-fallback redirect for /verify/* to ever reach this
// function instead of the marketing landing page) so a non-technical
// verifier (a DGUV auditor, a new employer) can just open a link and see
// whether a completion is real - not parse a JSON credential or run a
// signature check themselves.
//
// Re-verifies the stored signature against the LIVE JWKS at request time
// (not just trusting whatever was true when save-verified-credential.js
// wrote the record) - belt-and-suspenders in case of a future key
// rotation, and because this is the one honest place to actually show
// "yes, right now, this still checks out."
//
// Access model: this is a public, unauthenticated GET endpoint. The only
// thing gating access is knowing the random UUID slug - nobody can browse
// or guess other people's certificates, but anyone holding the specific
// link can view it. Same trust model as sharing a Google Docs link - a
// deliberate, simple choice for the MVP, not an oversight (see
// docs/paid-verifiable-certificates-scoping.md, "Open questions").

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

function escapeHtml(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function htmlPage({ title, bodyHtml, statusOk }) {
  return `<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background: #f5f7fb; color: #1a2233; margin: 0; padding: 40px 16px; }
  .card { max-width: 560px; margin: 0 auto; background: #fff; border: 1px solid #d7deec; border-radius: 14px; padding: 32px; }
  .brand { font-weight: 700; font-size: 0.85rem; color: #5b6478; letter-spacing: 0.02em; margin-bottom: 18px; }
  h1 { font-size: 1.3rem; margin: 0 0 6px; }
  .status { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; padding: 6px 14px; border-radius: 999px; font-size: 0.9rem; margin-bottom: 18px; }
  .status.ok { background: #e5f7ed; color: #0f6b3d; }
  .status.bad { background: #fbe8e3; color: #b8402a; }
  .row { margin: 10px 0; font-size: 0.95rem; }
  .row .label { color: #5b6478; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.03em; display: block; margin-bottom: 2px; }
  .disclaimer { margin-top: 28px; padding-top: 18px; border-top: 1px solid #d7deec; font-size: 0.78rem; color: #5b6478; }
  code { background: #eef2fb; padding: 1px 5px; border-radius: 4px; font-size: 0.85em; word-break: break-all; }
</style></head>
<body>
  <div class="card">
    <div class="brand">ZETTACARD</div>
    ${bodyHtml}
  </div>
</body></html>`;
}

exports.handler = async (event) => {
  if (event.httpMethod !== "GET") {
    return { statusCode: 405, headers: { "content-type": "text/plain" }, body: "Method not allowed." };
  }

  // The redirect (netlify.toml) forwards the path segment as
  // /.netlify/functions/verify-credential/<slug> - pull the last segment.
  const parts = event.path.split("/").filter(Boolean);
  const slug = parts[parts.length - 1];
  const slugRe = /^[0-9a-f-]{8,64}$/i;
  if (!slug || !slugRe.test(slug)) {
    return {
      statusCode: 400,
      headers: { "content-type": "text/html; charset=utf-8" },
      body: htmlPage({ title: "Ungültiger Link", bodyHtml: `<h1>Ungültiger Link</h1><p>Dieser Verifizierungslink ist nicht gültig.</p>` }),
    };
  }

  let record;
  try {
    const { getStore } = await loadBlobs();
    const store = getStore(STORE_NAME);
    record = await store.get(slug, { type: "json" });
  } catch (e) {
    console.error("verify-credential: Blobs read failed:", e);
    record = null;
  }

  if (!record) {
    return {
      statusCode: 404,
      headers: { "content-type": "text/html; charset=utf-8" },
      body: htmlPage({
        title: "Zertifikat nicht gefunden",
        bodyHtml: `<h1>Zertifikat nicht gefunden</h1><p>Unter diesem Link ist kein Zertifikat hinterlegt. Der Link könnte falsch kopiert oder das Zertifikat entfernt worden sein.</p>`,
      }),
    };
  }

  // Re-verify RIGHT NOW against the live JWKS, not just trusting that the
  // signature was valid when this record was first saved.
  let signatureValid = false;
  try {
    const jwksRaw = await fetch(`${ISSUER_URL}${JWKS_PATH}`).then((r) => r.json());
    const jwk = (jwksRaw.keys || []).find((k) => k.kid === record.signedKid) || jwksRaw.keys?.[0];
    if (jwk) {
      const { importJWK, jwtVerify } = await loadJose();
      const publicKey = await importJWK(jwk, record.signedAlg || ALG);
      await jwtVerify(record.signedJwt, publicKey, { issuer: ISSUER_URL });
      signatureValid = true;
    }
  } catch (e) {
    console.error("verify-credential: live re-verification failed:", e);
    signatureValid = false;
  }

  const dateStr = new Date(record.passedAt).toLocaleDateString("de-DE");
  const statusHtml = signatureValid
    ? `<div class="status ok">✅ Signatur gültig</div>`
    : `<div class="status bad">⚠️ Signatur konnte nicht bestätigt werden</div>`;

  const bodyHtml = `
    ${statusHtml}
    <h1>${escapeHtml(record.moduleLabel)} · ${escapeHtml(record.scopeLabel)}</h1>
    ${record.participantName ? `<div class="row"><span class="label">Name</span>${escapeHtml(record.participantName)}</div>` : ""}
    <div class="row"><span class="label">Bestanden am</span>${escapeHtml(dateStr)}</div>
    <div class="row"><span class="label">Prüfungssimulation</span>${record.totalQuestions} Fragen · ${record.errorPoints} Fehlerpunkt(e) · ${record.wrongHighStakes} sicherheitsrelevante Fehler</div>
    <div class="row"><span class="label">Ausgestellt von</span>Zettacard (${escapeHtml(ISSUER_URL)})</div>
    <div class="row"><span class="label">Schlüssel-ID</span><code>${escapeHtml(record.signedKid || "—")}</code></div>
    <div class="disclaimer">
      Diese Seite bestätigt: ein Zertifikat mit genau diesen Angaben wurde signiert und unter diesem Link hinterlegt, und die Signatur ist gerade jetzt gegen den öffentlichen Schlüssel unter
      <code>${escapeHtml(ISSUER_URL)}/.well-known/jwks.json</code> geprüft worden. Das ist eine ehrliche Einschränkung, kein Kleingedrucktes: die Prüfungssimulation selbst läuft clientseitig, diese Seite bezeugt die eingereichte Punktzahl, nicht dass die Person die Fragen unter Aufsicht beantwortet hat.
    </div>
  `;

  return {
    statusCode: 200,
    headers: { "content-type": "text/html; charset=utf-8" },
    body: htmlPage({ title: `Zettacard – ${record.moduleLabel} Zertifikat`, bodyHtml }),
  };
};
