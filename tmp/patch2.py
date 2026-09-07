import json, os
root = os.path.expanduser("~/mnt/Zettacard/app/data/fuehrerschein")
path = f"{root}/locales/hi.json"
with open(path, encoding="utf-8") as f:
    hi = json.load(f)

# zeichen-68: Zeichen 214 (mandatory direction: straight or right) - HI content was mismatched (talked about passing an obstacle left or right)
hi["zeichen-68"]["question"] = "यह ट्रैफिक साइन क्या निर्देशित करता है?"
hi["zeichen-68"]["options"]["a"] = "आपको यहां सीधे या दाईं ओर आगे बढ़ना होगा।"
hi["zeichen-68"]["options"]["b"] = "आपको यहां केवल दाईं ओर मुड़ना होगा।"
hi["zeichen-68"]["options"]["c"] = "यहां सीधे जाना मना है।"
hi["zeichen-68"]["options"]["d"] = "आप यहां किसी भी दिशा में जा सकते हैं।"
hi["zeichen-68"]["explanation"] = "Zeichen 214 अनिवार्य दिशा साइन है: यहां से केवल सीधे या दाईं ओर आगे बढ़ा जा सकता है, अन्य सभी दिशाएं (जैसे बाईं ओर मुड़ना या यू-टर्न लेना) प्रतिबंधित हैं।"

# zeichen-132: Zusatzzeichen "Fußgänger" (pedestrian) under a sign - HI content was wrongly about "Mofa frei"
hi["zeichen-132"]["question"] = "एक ट्रैफिक साइन के नीचे 'Fußgänger' (पैदल यात्री) लिखा एक सफ़ेद सहायक साइन लगा है। इसका क्या अर्थ है?"
hi["zeichen-132"]["options"]["a"] = "यह सहायक साइन बताता है कि मुख्य साइन पैदल यात्रियों पर भी (साथ ही) लागू होता है।"
hi["zeichen-132"]["options"]["b"] = "पैदल यात्री मुख्य साइन के किसी भी नियम से मूल रूप से मुक्त हैं।"
hi["zeichen-132"]["options"]["c"] = "यह पैदल यात्री क्षेत्र (Fußgängerzone) की ओर संकेत है।"
hi["zeichen-132"]["options"]["d"] = "यह सहायक साइन केवल व्हीलचेयर उपयोगकर्ताओं पर लागू होता है, अन्य पैदल यात्रियों पर नहीं।"
hi["zeichen-132"]["explanation"] = "सहायक साइन 1010-53 'Fußgänger' ऊपर लगे मुख्य साइन के दायरे को स्पष्ट करता है: यह दर्शाता है कि नियम पैदल यात्रियों पर भी लागू होता है, न कि (जैसा सहायक साइन के बिना अक्सर माना जाता है) केवल वाहनों पर।"

with open(path, "w", encoding="utf-8") as f:
    json.dump(hi, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("patched zeichen-68 and zeichen-132")
