// Salted SHA-256 hashing for Open Badges 2.0/3.0 "hashed identity" claims
// (credentialSubject.identifier[].identityHash).
//
// Convention: `sha256$` + hex digest of (plaintext value + random salt),
// with the salt generated fresh via crypto.randomBytes(16).toString("hex")
// for every hash. This is the standard OB2/OB3 hashed-identity format (an
// unsalted hash of a common value like an email address would be trivially
// reversible via a rainbow table, which defeats the point of hashing it in
// the first place - the salt is what makes that infeasible).
//
// ESM version of the original identity-hash.js (CommonJS), created
// 2026-08-16 when issue-badge.js was converted to a Functions v2 (.mjs)
// module - see issue-badge.mjs's top-of-file comment for why. Logic is
// byte-for-byte identical to the retired .js version; only the
// require()/module.exports wrapper changed to import/export.
import crypto from "node:crypto";

// Hashes a single identity value (an email address, a display name, etc.)
// with a fresh random salt. Returns { hash, salt } where `hash` is already
// in the `sha256$<hex>` storage/transport format and `salt` is the raw hex
// salt string that must be stored alongside it - the hash is meaningless
// for matching purposes without the salt that produced it.
//
// Note this intentionally does NOT normalize/trim the input - callers
// (e.g. issue-badge.mjs) are responsible for normalizing a value (such as
// lowercasing + trimming an email address) *before* calling this, so the
// normalization policy lives with the caller who knows the field's
// semantics, not buried in a generic hashing helper.
export function hashIdentity(value) {
  const salt = crypto.randomBytes(16).toString("hex");
  const digest = crypto.createHash("sha256").update(value + salt).digest("hex");
  return { hash: `sha256$${digest}`, salt };
}
