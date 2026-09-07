// Per-module achievement metadata for badges issued via issue-badge.mjs's
// optional `moduleType` field. Added 2026-09-03 so a caller issuing a
// badge for one of the four workplace-compliance modules (see
// data/modules_manifest.json for the modules themselves - not edited by
// this change) doesn't have to pass achievementName/achievementDescription
// by hand every time; those two fields stay supported directly and take
// precedence when supplied (see issue-badge.mjs's resolution order).
//
// `image` here is a BARE FILENAME, not a URL - deliberately, so this
// object never hardcodes a domain. issue-badge.mjs resolves it against
// its own ISSUER_URL at request time
// (`${ISSUER_URL}/assets/badges/${MODULE_ACHIEVEMENTS[moduleType].image}`),
// the same way it already does for ACHIEVEMENT_IMAGE_PATH.
export const MODULE_ACHIEVEMENTS = {
  datenschutz: {
    name: "Datenschutz DSGVO/BDSG – Grundlagenzertifikat",
    description: "Bestätigt Grundkenntnisse im betrieblichen Datenschutz nach DSGVO und BDSG: Rechtsgrundlagen der Verarbeitung, Betroffenenrechte, Auftragsverarbeitung, technisch-organisatorische Maßnahmen und Meldepflichten bei Datenschutzverletzungen. Nachgewiesen durch eine bestandene Prüfungssimulation.",
    image: "datenschutz.svg",
  },
  arbeitssicherheit: {
    name: "Arbeitssicherheit & Arbeitsschutz – Grundlagenzertifikat",
    description: "Bestätigt Grundkenntnisse im Arbeitsschutz nach ArbSchG und DGUV-Vorschriften: Gefährdungsbeurteilung, Unterweisungspflichten, persönliche Schutzausrüstung, Verhalten im Notfall sowie Melde- und Dokumentationspflichten bei Arbeitsunfällen.",
    image: "arbeitssicherheit.svg",
  },
  ki_act: {
    name: "EU KI-Verordnung (AI Act) – KI-Kompetenz Grundlagenzertifikat",
    description: "Bestätigt die nach Art. 4 der Verordnung (EU) 2024/1689 geforderte KI-Kompetenz: Risikostufen des AI Act, verbotene Praktiken, Pflichten von Anbietern und Betreibern, Transparenzanforderungen und sicherer Einsatz von KI-Systemen am Arbeitsplatz.",
    image: "ki_act.svg",
  },
  it_sicherheit: {
    name: "IT-Sicherheit am Arbeitsplatz – Grundlagenzertifikat",
    description: "Bestätigt Grundkenntnisse der IT-Sicherheit im Arbeitsalltag: Zugriffsschutz und Passworthygiene, Erkennen von Phishing und Social Engineering, Datensicherung und Geräteumgang, mobiles Arbeiten und Homeoffice sowie Meldepflichten bei IT-Sicherheitsvorfällen.",
    image: "it_sicherheit.svg",
  },
};
