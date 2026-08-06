#!/usr/bin/env node
// Manual round-trip test for netlify/functions/sign-credential.js: invokes
// the function's handler directly (no `netlify dev` needed) with a mock
// event, then verifies the returned JWT against the public JWKS using
// jose's own verify function - proving the whole sign -> publish -> verify
// loop actually works end to end.
//
// Requires ZETTACARD_SIGNING_PRIVATE_JWK to be set - loads it from
// .env.local (repo root) if present, since that's where local/dev testing
// keeps it (gitignored, never a production key in a real deploy).
const fs = require("fs");
const path = require("path");

function loadDotEnvLocal() {
  const envPath = path.join(__dirname, "..", ".env.local");
  if (!fs.existsSync(envPath)) return;
  const lines = fs.readFileSync(envPath, "utf8").split("\n");
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    const value = trimmed.slice(eq + 1).trim();
    if (!process.env[key]) process.env[key] = value;
  }
}

async function main() {
  loadDotEnvLocal();
  if (!process.env.ZETTACARD_SIGNING_PRIVATE_JWK) {
    console.error("ZETTACARD_SIGNING_PRIVATE_JWK not set (expected in .env.local for this test). Run scripts/generate_signing_keypair.mjs first.");
    process.exit(1);
  }
  process.env.URL = process.env.URL || "https://zettacard.netlify.app";

  const { handler } = require("../netlify/functions/sign-credential.js");
  // Dynamic import, not require() - jose is ESM-only and this must keep
  // testing the same code path Netlify's actual (older, non-require(esm))
  // Lambda runtime uses, not just whatever this dev machine's Node version
  // happens to tolerate (see the ERR_REQUIRE_ESM bug this caught live on
  // the first real deploy, 2026-08-06).
  const { importJWK, jwtVerify } = await import("jose");

  const mockRecord = {
    id: "arbeitsschutz-basis-1735000000000",
    examType: "arbeitsschutz",
    scopeCode: "basis",
    moduleLabel: "Arbeitssicherheit",
    scopeLabel: "Basis",
    passedAt: new Date().toISOString(),
    errorPoints: 2,
    wrongHighStakes: 0,
    totalQuestions: 20,
  };

  console.log("--- Test 1: valid payload signs successfully ---");
  const okResult = await handler({ httpMethod: "POST", body: JSON.stringify(mockRecord) });
  console.log("status:", okResult.statusCode);
  const okBody = JSON.parse(okResult.body);
  console.log(JSON.stringify(okBody, null, 2));
  if (okResult.statusCode !== 200 || !okBody.jwt || okBody.verified !== true) {
    console.error("FAIL: expected 200 with a signed jwt and verified:true");
    process.exit(1);
  }

  console.log("\n--- Round-trip verify against app/.well-known/jwks.json ---");
  const jwks = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "app", ".well-known", "jwks.json"), "utf8"));
  const publicJwk = jwks.keys.find((k) => k.kid === okBody.kid);
  if (!publicJwk) {
    console.error("FAIL: no matching kid in JWKS - did you regenerate the keypair without updating jwks.json?");
    process.exit(1);
  }
  const publicKey = await importJWK(publicJwk, okBody.alg);
  const { payload, protectedHeader } = await jwtVerify(okBody.jwt, publicKey);
  console.log("Verified JWT header:", protectedHeader);
  console.log("Verified JWT payload:", JSON.stringify(payload, null, 2));
  if (payload.vc.credentialSubject.achievement.name !== "Arbeitssicherheit - Basis") {
    console.error("FAIL: unexpected claims in verified payload");
    process.exit(1);
  }
  console.log("PASS: JWT verifies successfully against the public JWKS.\n");

  console.log("--- Test 2: tampering with the signature must fail verification ---");
  const tampered = okBody.jwt.slice(0, -4) + "abcd";
  try {
    await jwtVerify(tampered, publicKey);
    console.error("FAIL: tampered JWT unexpectedly verified");
    process.exit(1);
  } catch (e) {
    console.log("PASS: tampered JWT correctly rejected:", e.message);
  }

  console.log("\n--- Test 3: malformed payload is rejected with a clean JSON error ---");
  const badResult = await handler({ httpMethod: "POST", body: JSON.stringify({ examType: "x".repeat(500) }) });
  console.log("status:", badResult.statusCode, "body:", badResult.body);
  if (badResult.statusCode !== 400) {
    console.error("FAIL: expected 400 for malformed payload");
    process.exit(1);
  }
  console.log("PASS: malformed payload rejected cleanly.\n");

  console.log("--- Test 4: missing env var is handled gracefully (not a raw crash) ---");
  const savedKey = process.env.ZETTACARD_SIGNING_PRIVATE_JWK;
  delete process.env.ZETTACARD_SIGNING_PRIVATE_JWK;
  const noKeyResult = await handler({ httpMethod: "POST", body: JSON.stringify(mockRecord) });
  process.env.ZETTACARD_SIGNING_PRIVATE_JWK = savedKey;
  console.log("status:", noKeyResult.statusCode, "body:", noKeyResult.body);
  if (noKeyResult.statusCode !== 500 || !JSON.parse(noKeyResult.body).error) {
    console.error("FAIL: expected a clean 500 JSON error when env var is missing");
    process.exit(1);
  }
  console.log("PASS: missing-env-var case handled gracefully.\n");

  console.log("ALL TESTS PASSED");
}

main().catch((e) => {
  console.error("Unexpected test failure:", e);
  process.exit(1);
});
