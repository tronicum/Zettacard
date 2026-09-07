import json

path = 'locales/fr.json'
with open(path, encoding='utf-8') as f:
    fr = json.load(f)

# --- zeichen-68: fully stale (French described a different sign entirely) ---
fr['zeichen-68'] = {
    "question": "Qu'indique ce panneau de signalisation ?",
    "options": {
        "a": "Vous devez continuer tout droit ou tourner à droite ici.",
        "b": "Vous ne devez tourner qu'à droite ici.",
        "c": "Il est interdit d'aller tout droit ici.",
        "d": "Vous pouvez circuler dans n'importe quelle direction ici."
    },
    "explanation": "Le Zeichen 214 est un panneau de prescription indiquant la direction obligatoire : à cet endroit, seule la direction tout droit ou à droite est autorisée ; toutes les autres directions (par exemple tourner à gauche ou faire demi-tour) sont interdites."
}

# --- zeichen-132: fully stale (French described "Mofa frei" instead of "Fussgaenger") ---
fr['zeichen-132'] = {
    "question": "Un panonceau blanc portant la mention « Piétons » se trouve sous un panneau de signalisation. Que signifie-t-il ?",
    "options": {
        "a": "Le panonceau indique que le panneau principal s'applique (aussi) aux piétons.",
        "b": "Les piétons sont par principe exemptés de toute règle imposée par le panneau principal.",
        "c": "Il s'agit d'une indication signalant une zone piétonne.",
        "d": "Le panonceau ne s'applique qu'aux utilisateurs de fauteuil roulant, et non aux autres piétons."
    },
    "explanation": "Le panonceau 1010-53 « Piétons » précise le champ d'application du panneau principal placé au-dessus : il indique clairement que la règle concerne aussi les piétons, et non uniquement les véhicules, comme on pourrait le supposer en l'absence de ce panonceau."
}

# --- zeichen-14: distractors described unrelated signs (rest area, roadworks) ---
fr['zeichen-14']['options']['c'] = "L'autoroute ne commence qu'après la prochaine sortie"
fr['zeichen-14']['options']['d'] = "Une bretelle d'accès vers l'autoroute, mais pas encore l'autoroute elle-même"

# --- zeichen-15: distractors described unrelated signs (interchange, higher speed limit) ---
fr['zeichen-15']['options']['c'] = "Une aire de repos dans 300 mètres"
fr['zeichen-15']['options']['d'] = "L'autoroute devient une voie express"

# --- vorfahrt-17: distractors described unrelated rules (hand signals, dismounting) ---
fr['vorfahrt-17']['options']['c'] = "Le cycliste doit d'abord vous laisser passer, car vous êtes en voiture"
fr['vorfahrt-17']['options']['d'] = "Le cycliste n'est prioritaire que si la piste cyclable n'est pas à usage obligatoire"

# --- zeichen-118: distractor c described an unrelated meaning ---
fr['zeichen-118']['options']['c'] = "Il indique en même temps la fin d'une voie express"

with open(path, 'w', encoding='utf-8') as f:
    json.dump(fr, f, ensure_ascii=False, indent=2)

print("done")
