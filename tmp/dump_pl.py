import json, sys

mod = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
path = "/sessions/rcw-01dljkimnrnap8ldte7prwra/mnt/Zettacard/data/" + mod + ".json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
qs = data["questions"]
for q in qs[start:end]:
    de = q["text"]["de"]
    pl = q["text"].get("pl", {})
    print("="*80)
    print("ID:", q["id"], "CORRECT:", q.get("correct"))
    print("-- DE Q:", de["question"])
    print("-- PL Q:", pl.get("question"))
    for k in ["a","b","c","d"]:
        if k in de.get("options", {}):
            print(f"  DE[{k}]:", de["options"][k])
            print(f"  PL[{k}]:", pl.get("options", {}).get(k))
    print("-- DE EXPL:", q["explanation"].get("de"))
    print("-- PL EXPL:", q["explanation"].get("pl"))
