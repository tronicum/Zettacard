# Ideas — spark file

Raw, early-stage product ideas from the PO, captured as they come up mid-conversation,
on purpose *before* any research or scoping happens to them. This is deliberately not
`BACKLOG.md`'s "Backlog" section (which holds work that's already been scoped and is
just waiting its turn) and not `TODO.md` (a working list for one specific active arc,
currently the boating-licence integration). An idea lives here exactly as loosely as
the PO gave it - a name, a one-line pitch, whatever it obviously connects to in the
existing codebase - with no commitment implied by writing it down.

**Lifecycle**: spark here → (when the PO wants to move on it) a dossier/scoping doc in
`docs/` + a `BACKLOG.md` entry, same as every other module/feature in this project got →
this file gets a one-line "promoted, see BACKLOG DN-NN" note next to the entry rather
than deleting it, so the origin of an idea stays traceable.

---

## Open sparks

### Zettacard Badgify (or similar name) — scan-to-badge for external certificates
**2026-08-17.** PO's framing, lightly paraphrased: a tool you can scan a paper or PDF
external certificate into, that turns it into an encrypted PDF you can keep and share
easily as a digital badge for your skills - possibly with a mobile/PWA-style "wallet"
view across all your certs/badges, not just Zettacard-issued ones.

Worth noting for whenever this gets picked up, without scoping it now: there are two
quite different products hiding under one name, and they weren't disambiguated -
(a) **pure convenience wrapper**: OCR/scan a document, encrypt it, generate a clean
shareable link/QR - no claim about the document's authenticity beyond "here's what was
scanned," or (b) **attestation layer**: Zettacard actually vouches for the scanned
credential somehow (verifies against the issuing body? just timestamps the scan?) before
wrapping it - a materially bigger trust/liability question than (a). This project
already has a working OB3/Verifiable-Credential signing pipeline for badges it issues
itself (`netlify/functions/issue-badge.mjs`/`get-badge.mjs`, JWKS at
`app/.well-known/jwks.json`, the `/badges/:id` URL scheme) - a "wallet" view that also
displays those alongside imported third-party certs is a natural fit for (a), but (b)
would need a genuinely new verification story this repo doesn't have yet. Encryption-at-
rest for a scanned personal document (someone's actual name, actual employer, actual
cert number) is also a real privacy/GDPR-relevant decision, not just an implementation
detail, given this project already treats identity data carefully elsewhere (see
`netlify/functions/lib/identity-hash.mjs`'s salted one-way hashing for its own badges).

### Cheaper Okta-alternative for social login (incl. LinkedIn)
**2026-08-17.** PO's own words: "we will need something like octa (but cheaper) for our
social logins (linkedin too for the badges, and as login source) so we can manage all
that. but this is an much later milestone." LinkedIn specifically for two roles: as a
login/identity source, and as a badge-sharing surface (LinkedIn profiles already support
adding certifications). Explicitly deferred by the PO - no vendor comparison, no
scoping, not connected to anything else yet. Likely relevant once the whitelabel course
line (`docs/whitelabel-regulatory-training-scoping-2026-08-17.md`, BACKLOG DN-77) or any
paywall/access-gating work gets real, since both would need real identity, but that
connection hasn't been confirmed by the PO - noted here as a hypothesis, not a decision.

---

## Promoted (kept for the trail)

*(none yet)*
