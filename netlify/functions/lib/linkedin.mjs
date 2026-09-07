// Builds LinkedIn's "Add to Profile" certification deep link for a signed
// Zettacard badge. Factored out of issue-badge.mjs (rather than inlined
// there) so a future real "Share to LinkedIn" button elsewhere in the app
// can import this same function later instead of re-deriving the same
// query-string shape in a second place.
//
// See LinkedIn's own documented deep-link contract for "Add to Profile"
// certifications: https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&...
// - startTask=CERTIFICATION_NAME is a required literal (not a real value to
//   fill in, it tells LinkedIn which profile section's "add" form to open).
// - organizationName is used as-is (free-text fallback) since Zettacard has
//   no registered LinkedIn Organization page to reference by
//   organizationId instead.
// - issueYear/issueMonth are the current UTC year/month AT ISSUANCE (not
//   the exam-completion date - see issue-badge.mjs's own validFrom comment
//   for why a manually-issued test badge has no equivalent earned-date).
//   issueMonth is 1-12, no zero-padding (LinkedIn's own form fields expect
//   plain integers, not zero-padded strings).
// - No expiration params - these credentials don't expire.
export function buildLinkedInAddUrl({ achievementName, badgeUrl, badgeId, issuedAt }) {
  const d = new Date(issuedAt);
  const params = new URLSearchParams({
    startTask: "CERTIFICATION_NAME",
    name: achievementName,
    organizationName: "Zettacard",
    issueYear: String(d.getUTCFullYear()),
    issueMonth: String(d.getUTCMonth() + 1),
    certUrl: badgeUrl,
    certId: badgeId,
  });
  return `https://www.linkedin.com/profile/add?${params.toString()}`;
}
