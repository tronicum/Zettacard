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
// This exact scheme (`sha256$` prefix, crypto.randomBytes(16) salt) was
// already the documented design intent for this project - see BACKLOG.md's
// "Optional multi-email identity binding for wallet-import badges" entry -
// but that entry's implementation was never actually committed anywhere in
// this repo (there is no prior hashing code to reuse; grep the repo before
// assuming otherwise). This module is a fresh, from-scratch implementation
// of the same convention, factored out here so netlify/functions/issue-
// badge.js (and any future function needing the same hashed-identity
// shape) doesn't have to duplicate it.
//
// Plain Node built-in `crypto` only - no external dependency, no ESM
// concerns, safe to `require()` normally at the top of a file (unlike
// `jose` or `@netlify/blobs`, which need the lazy-import-with-cache
// pattern documented at the top of sign-credential.js and issue-badge.js).
const crypto = require("crypto");

// Hashes a single identity value (an email address, a display name, etc.)
// with a fresh random salt. Returns { hash, salt } where `hash` is already
// in the `sha256$<hex>` storage/transport format and `salt` is the raw hex
// salt string that must be stored alongside it - the hash is meaningless
// for matching purposes without the salt that produced it.
//
// Note this intentionally does NOT normalize/trim the input - callers
// (e.g. issue-badge.js) are responsible for normalizing a value (such as
// lowercasing + trimming an email address) *before* calling this, so the
// normalization policy lives with the caller who knows the field's
// semantics, not buried in a generic hashing helper.
function hashIdentity(value) {
  const salt = crypto.randomBytes(16).toString("hex");
  const digest = crypto.createHash("sha256").update(value + salt).digest("hex");
  return { hash: `sha256$${digest}`, salt };
}

module.exports = { hashIdentity };
