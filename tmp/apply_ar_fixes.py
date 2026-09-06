import json, os

base = os.environ["HOME"] + "/mnt/Zettacard/app/data/fuehrerschein"
ar_path = base + "/locales/ar.json"

with open(ar_path, "r", encoding="utf-8") as f:
    ar = json.load(f)

# Fix 1: zeichen-04 wrong sign number 133 -> 136
q = ar["zeichen-04"]["question"]
assert "133" in q, "133 not found in zeichen-04 question: " + q
ar["zeichen-04"]["question"] = q.replace("133", "136")

# Fix 2: zeichen-68 wrong content (was describing an obstacle-passing sign,
# should describe Zeichen 214 mandatory straight-or-right direction sign)
z68 = ar["zeichen-68"]
old_options = dict(z68["options"])
old_explanation = z68["explanation"]

z68["options"]["a"] = "يجب عليك متابعة السير هنا مستقيمًا أو يمينًا."
z68["options"]["b"] = "يجب عليك الانعطاف يمينًا فقط هنا."
z68["options"]["c"] = "يُمنع السير مستقيمًا هنا."
z68["options"]["d"] = "يجوز لك السير هنا في أي اتجاه."
z68["explanation"] = "تُلزم الإشارة رقم 214 هنا باتجاه سير مُحدد: يجوز هنا السير مستقيمًا أو يمينًا فقط، وتُمنع جميع الاتجاهات الأخرى (مثل الانعطاف يسارًا أو الاستدارة)."

with open(ar_path, "w", encoding="utf-8") as f:
    json.dump(ar, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("zeichen-04 new question:", ar["zeichen-04"]["question"])
print()
print("zeichen-68 old options:", old_options)
print("zeichen-68 old explanation:", old_explanation)
print()
print("zeichen-68 new options:", z68["options"])
print("zeichen-68 new explanation:", z68["explanation"])
