import json, os

base = os.environ["HOME"] + "/mnt/Zettacard/app/data/fuehrerschein"
path = base + "/locales/it.json"

with open(path, "r", encoding="utf-8") as f:
    it = json.load(f)

changes = []

# --- Fix 1: zeichen-68 (Zeichen 214 mandatory direction straight-or-right) ---
old = dict(it["zeichen-68"])
it["zeichen-68"] = {
    "question": "Cosa prescrive questo segnale stradale?",
    "options": {
        "a": "Dovete proseguire qui dritto o svoltare a destra.",
        "b": "Dovete svoltare qui solo a destra.",
        "c": "Qui è vietato proseguire dritto.",
        "d": "Qui potete procedere in qualsiasi direzione."
    },
    "explanation": "Il segnale 214 è un segnale di obbligo per la direzione di marcia prescritta: in questo punto si può proseguire solo dritto o svoltare a destra; tutte le altre direzioni (ad es. svoltare a sinistra o invertire il senso di marcia) sono vietate."
}
changes.append(("zeichen-68", old, it["zeichen-68"]))

# --- Fix 2: zeichen-132 (Zusatzzeichen "Fußgänger") ---
old = dict(it["zeichen-132"])
it["zeichen-132"] = {
    "question": "Sotto un segnale stradale si trova un pannello integrativo bianco con la scritta «Fußgänger» (pedoni). Cosa significa?",
    "options": {
        "a": "Il pannello integrativo indica che il segnale principale si riferisce (anche) ai pedoni.",
        "b": "I pedoni sono in linea di principio esclusi da qualsiasi regolamentazione del segnale principale.",
        "c": "Si tratta di un'indicazione di una zona pedonale.",
        "d": "Il pannello integrativo vale solo per gli utenti di sedia a rotelle, non per gli altri pedoni."
    },
    "explanation": "Il pannello integrativo 1010-53 «Fußgänger» precisa l'ambito di validità del segnale principale sovrastante: chiarisce che la regolamentazione include anche i pedoni, invece di riferirsi soltanto ai veicoli, come spesso si presume in assenza del pannello integrativo."
}
changes.append(("zeichen-132", old, it["zeichen-132"]))

# --- Fix 3: zeichen-118 option c (distractor mismatched meaning) ---
old_c = it["zeichen-118"]["options"]["c"]
new_c = "Indica al contempo anche la fine di una strada riservata ai veicoli a motore."
it["zeichen-118"]["options"]["c"] = new_c
changes.append(("zeichen-118.options.c", old_c, new_c))

with open(path, "w", encoding="utf-8") as f:
    json.dump(it, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("Applied", len(changes), "changes")
for c in changes:
    print("---", c[0])
    print("OLD:", c[1])
    print("NEW:", c[2])
