import json

root = "/sessions/rcw-01dljkimnrnap8ldte7prwra/mnt/Zettacard/app/data/fuehrerschein"
path = f"{root}/locales/hi.json"

with open(path, encoding="utf-8") as f:
    hi = json.load(f)

changes = []

# zeichen-04: wrong sign number in question text
old = hi["zeichen-04"]["question"]
new = old.replace("साइन 133", "साइन 136")
if new != old:
    hi["zeichen-04"]["question"] = new
    changes.append(("zeichen-04", "question", old, new))

# zeichen-122 and zeichen-123 option d: mistranslated "supplementary plate without meaning"
old_d = "बिना अपने किसी अर्थ वाली एक सहायक प्लेट।"
new_d = "अगले विश्राम स्थल की ओर एक दिशा-सूचक।"
for qid in ["zeichen-122", "zeichen-123"]:
    cur = hi[qid]["options"]["d"]
    if old_d in cur:
        replaced = cur.replace(old_d, new_d)
        hi[qid]["options"]["d"] = replaced
        changes.append((qid, "options.d", cur, replaced))

with open(path, "w", encoding="utf-8") as f:
    json.dump(hi, f, ensure_ascii=False, indent=2)
    f.write("\n")

for c in changes:
    print(c[0], c[1])
    print(" OLD:", c[2])
    print(" NEW:", c[3])
    print()

print("done, total changes:", len(changes))
