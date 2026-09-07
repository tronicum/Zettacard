import json

base = "app/data/fuehrerschein/locales/zh.json"
zh = json.load(open(base, encoding="utf-8"))

fixes = {}

fixes["zeichen-68"] = {
    "question": "这个交通标志表示什么?",
    "options": {
        "a": "此处必须直行或向右继续行驶。",
        "b": "此处只能向右转弯。",
        "c": "此处禁止直行。",
        "d": "此处可以朝任意方向行驶。"
    },
    "explanation": "Zeichen 214 是规定行驶方向的指令标志:在此处只能直行或向右继续行驶,其他所有方向(例如向左转弯或掉头)均被禁止。"
}

fixes["zeichen-132"] = {
    "question": "在某个交通标志下方有一个白色附加标志,上面写着“Fußgänger”(行人)字样。这是什么意思?",
    "options": {
        "a": "该附加标志说明,上方的主标志(也)适用于行人。",
        "b": "行人原则上不受主标志所规定内容的约束。",
        "c": "这是指示行人专用区的标志。",
        "d": "该附加标志仅适用于轮椅使用者,不适用于其他行人。"
    },
    "explanation": "附加标志1010-53“Fußgänger”(行人)明确了上方主标志的适用范围:它表明该规定也包括行人在内,而不是像没有该附加标志时人们通常以为的那样只针对车辆。"
}

fixes["zeichen-04"] = {
    "question": "一个三角形警示标志,画有正在玩耍的儿童(标志136),提示什么?",
    "options": {
        "a": "附近有学校,但无需特别小心",
        "b": "儿童可能突然出现在车道上",
        "c": "禁止设置游乐场",
        "d": "强制限速30公里/小时"
    },
    "explanation": "该标志警示附近有儿童出现的可能,例如靠近学校或游乐场;应格外小心并做好随时刹车的准备。"
}

fixes["zeichen-118"] = {
    "question": "这个标有地名的黄色地名标志是什么意思?",
    "options": {
        "a": "从此处起进入建成区(市区);市区内原则上限速50公里/小时。",
        "b": "从此处起建成区(市区)结束。",
        "c": "它同时表示机动车专用道路(Kraftfahrstraße)的终点。",
        "d": "从此处起适用30公里/小时限速。"
    },
    "explanation": "Zeichen 310(地名标志正面)标示建成区(市区)的起点;若无其他标志规定,自此处起适用50公里/小时的一般限速。"
}

for qid, val in fixes.items():
    zh[qid] = val

json.dump(zh, open(base, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("done", list(fixes.keys()))
