#!/usr/bin/env node
// One-off tool: generates the ES256 (P-256) issuer keypair used by
// netlify/functions/sign-credential.js.
//
// This script is a *generator*, not something the app or the function ever
// imports. Run it once (or whenever rotating keys per the plan in
// docs/open-badges-signing-setup.md), then:
//   1. Copy the printed private JWK into the Netlify env var
//      ZETTACARD_SIGNING_PRIVATE_JWK (see setup doc - never commit it).
//   2. Copy the printed public JWKS into app/.well-known/jwks.json,
//      replacing its contents (this file IS committed - it's public key
//      material only).
//
// Why ES256/P-256 instead of RSA-2048 or EdDSA/Ed25519:
// - Much smaller keys/signatures than RSA-2048 (cheaper JWKS, cheaper JWTs),
//   while still being universally supported by every mainstream JWT
//   library and validator (unlike EdDSA, which some older/JS-based OB3
//   validator stacks still don't handle consistently as of this writing).
// - `jose` supports ES256 natively with no extra dependencies.
// - This app's own scoping doc (docs/open-badges-signing-scoping.md)
//   favors Ed25519 only in the context of a *did:web + JSON-LD Data
//   Integrity* proof suite, which this implementation deliberately does
//   NOT use (it uses plain signed JWTs per that doc's own recommendation);
//   ES256 is the more broadly interoperable choice for the JWT/JWKS path.
import { generateKeyPair, exportJWK } from "jose";
import { randomUUID } from "node:crypto";

const { publicKey, privateKey } = await generateKeyPair("ES256", { extractable: true });

const kid = randomUUID();

const publicJwk = await exportJWK(publicKey);
publicJwk.kid = kid;
publicJwk.alg = "ES256";
publicJwk.use = "sig";

const privateJwk = await exportJWK(privateKey);
privateJwk.kid = kid;
privateJwk.alg = "ES256";
privateJwk.use = "sig";

console.log("=== Public JWKS (commit this to app/.well-known/jwks.json) ===");
console.log(JSON.stringify({ keys: [publicJwk] }, null, 2));

console.log("\n=== Private JWK (set as Netlify env var ZETTACARD_SIGNING_PRIVATE_JWK - NEVER commit) ===");
console.log(JSON.stringify(privateJwk));

console.log(`\nkid: ${kid}`);
