#!/usr/bin/env python3
"""Offline tests for the Tier 2/3 tooling. NO OLLAMA, NO NETWORK, NO MODEL.

WHY THIS FILE IS THE IMPORTANT ONE
----------------------------------
The judge itself cannot be tested here - it needs a model on the developer's
Mac. What CAN be tested, and what actually decides whether a verdict means
anything, is everything around the model:

  * the prompt is a pure function of the cell (same input -> byte-identical
    prompt), otherwise a receipt's prompt_sha256 is meaningless;
  * the verdict is derived in Python from the booleans, correctly, over ALL
    2^5 x distractor x evidence combinations - never taken from the model;
  * the distractor rule (a correct-key letter named as "became correct" is
    discarded) holds, because getting that wrong flags hundreds of good cells;
  * a malformed reply is rejected, never silently scored as a pass;
  * receipts round-trip and pin the same source hash Tier 0 computes.

Every model call goes through a stub transport that returns canned JSON.

    python3 scripts/i18n_qa/test_offline.py          # exit 1 on any failure
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import cells  # noqa: E402
import embed_screen  # noqa: E402
import judge  # noqa: E402
import ollama_client  # noqa: E402
import receipts  # noqa: E402
import seed_eval  # noqa: E402
import translation_ledger  # noqa: E402

SCRATCH = os.path.join(cells.REPO, "tmp", "i18n_qa_test")

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def eq(a, b, what=""):
    if a != b:
        raise AssertionError(f"{what}: {a!r} != {b!r}")


def contains(haystack, needle, what=""):
    if needle not in haystack:
        raise AssertionError(f"{what}: {needle!r} not found")


# ---------------------------------------------------------------- fixtures
SOURCE_VIEW = {
    "question": "Was schreibt dieses Verkehrszeichen vor?",
    "options": {"a": "Sie müssen hier geradeaus oder nach rechts weiterfahren.",
                "b": "Sie müssen hier nur nach rechts abbiegen.",
                "c": "Geradeausfahren ist hier verboten.",
                "d": "Sie dürfen hier in jede Richtung fahren."},
    "explanation": "Zeichen 214 schreibt die Fahrtrichtung vor.",
    "correct": ["a"],
}
TARGET_VIEW = {
    "question": "Co nakazuje ten znak drogowy?",
    "options": {"a": "Musisz tutaj jechać dalej na wprost lub w prawo.",
                "b": "Musisz tutaj skręcić tylko w prawo.",
                "c": "Jazda na wprost jest tutaj zabroniona.",
                "d": "Możesz tutaj jechać w dowolnym kierunku."},
    "explanation": "Znak 214 określa obowiązkowy kierunek jazdy.",
    "correct": ["a"],
}
GOOD_REPLY = {
    "stem_equivalent": True, "correct_option_equivalent": True, "polarity_preserved": True,
    "numbers_preserved": True, "distractor_became_correct": [],
    "explanation_facts_preserved": True, "verdict": "pass", "confidence": 0.9, "evidence": "",
}


class StubTransport:
    """Canned Ollama. Records every request so the test can assert on the wire format."""

    def __init__(self, response_text, tags=("qwen2.5:7b-instruct",), version="0.11.0"):
        self.response_text = response_text
        self.tags = tags
        self.version = version
        self.calls = []

    def __call__(self, method, path, body=None):
        self.calls.append((method, path, body))
        if path == "/api/version":
            return {"version": self.version}
        if path == "/api/tags":
            return {"models": [{"name": n, "digest": "sha256:" + ("ab" * 32), "size": 4_700_000_000}
                               for n in self.tags]}
        if path == "/api/generate":
            text = self.response_text
            return {"response": text(body) if callable(text) else text,
                    "eval_count": 120, "eval_duration": 3_000_000_000}
        if path in ("/api/embed", "/api/embeddings"):
            texts = body.get("input") or [body.get("prompt")]
            # deterministic pseudo-embedding: length + character-class counts
            vecs = [[float(len(t)), float(sum(c.isdigit() for c in t)),
                     float(sum(c.isalpha() for c in t))] for t in texts]
            return {"embeddings": vecs}
        raise AssertionError("unexpected path " + path)


def client_with(response, **kw):
    return ollama_client.OllamaClient(host="http://stub", transport=StubTransport(response, **kw))


# ---------------------------------------------------------------- hashing
@test
def test_source_hash_is_the_ledgers_hash():
    """A receipt must pin the same hash Tier 0 pins, or CI cannot check receipts."""
    eq(cells.source_hash, translation_ledger.source_hash, "source_hash must be re-used, not re-implemented")
    q = cells.load_questions("fuehrerschein")["zeichen-68"]
    eq(cells.source_hash(q), translation_ledger.source_hash(q), "hash of zeichen-68")
    eq(len(cells.source_hash(q)), 64, "sha256 hex length")


@test
def test_target_hash_uses_identical_normalisation():
    q = cells.load_questions("fuehrerschein")["zeichen-68"]
    eq(cells.target_hash(q, "de"), cells.source_hash(q), "target_hash('de') must equal source_hash")
    if cells.target_hash(q, "pl") == cells.source_hash(q):
        raise AssertionError("pl and de must not hash the same")
    eq(cells.target_hash(q, "xx"), None, "absent locale")


@test
def test_target_hash_moves_with_the_answer_key():
    """If `correct` moves, every translation's meaning of 'option a' moves with it."""
    q = json.loads(json.dumps(cells.load_questions("fuehrerschein")["zeichen-68"]))
    before = cells.target_hash(q, "pl")
    q["correct"] = ["b"]
    if cells.target_hash(q, "pl") == before:
        raise AssertionError("answer-key change must invalidate the target hash")


# ---------------------------------------------------------------- prompt
@test
def test_prompt_is_deterministic():
    a = judge.build_prompt(SOURCE_VIEW, TARGET_VIEW, "pl")
    b = judge.build_prompt(json.loads(json.dumps(SOURCE_VIEW)),
                           json.loads(json.dumps(TARGET_VIEW)), "pl")
    eq(a, b, "identical input must give a byte-identical prompt")
    eq(ollama_client.sha256_text(a), ollama_client.sha256_text(b), "prompt hash")


@test
def test_prompt_option_order_is_normalised():
    """Dict insertion order must not change the prompt - it would change prompt_sha256."""
    shuffled = dict(TARGET_VIEW)
    shuffled["options"] = {k: TARGET_VIEW["options"][k] for k in ("d", "b", "a", "c")}
    eq(judge.build_prompt(SOURCE_VIEW, shuffled, "pl"),
       judge.build_prompt(SOURCE_VIEW, TARGET_VIEW, "pl"), "option order")


@test
def test_prompt_changes_when_the_cell_changes():
    other = json.loads(json.dumps(TARGET_VIEW))
    other["options"]["a"] = "Musisz przejechać z prawej strony."
    if judge.build_prompt(SOURCE_VIEW, other, "pl") == judge.build_prompt(SOURCE_VIEW, TARGET_VIEW, "pl"):
        raise AssertionError("a changed option must change the prompt")


@test
def test_prompt_carries_both_cells_the_key_and_the_distractor_rule():
    p = judge.build_prompt(SOURCE_VIEW, TARGET_VIEW, "pl")
    contains(p, SOURCE_VIEW["options"]["a"], "German correct option")
    contains(p, TARGET_VIEW["options"]["c"], "target distractor")
    contains(p, SOURCE_VIEW["explanation"], "German explanation")
    contains(p, "marked correct", "answer key marking")
    contains(p, "NOT translations of the German distractors", "the distractor convention")
    contains(p, "(pl)", "locale label")


# ---------------------------------------------------------------- verdicts
@test
def test_derive_verdict_over_every_boolean_combination():
    """Exhaustive: 2^5 booleans x 3 distractor lists x evidence present/absent."""
    fields = judge.BOOL_FIELDS
    checked = 0
    for mask in range(2 ** len(fields)):
        booleans = {f: bool(mask >> i & 1) for i, f in enumerate(fields)}
        for letters in ([], ["b"], ["a"], ["a", "c"]):
            for evidence in ("", "de: 'muss' / pl: 'nie musi'"):
                reply = dict(GOOD_REPLY, **booleans)
                reply["distractor_became_correct"] = letters
                reply["evidence"] = evidence
                verdict, reasons = judge.derive_verdict(reply, correct_letters=["a"])
                surviving = [x for x in letters if x != "a"]
                hard = [f for f in judge.HARD_BOOLS if not booleans[f]]
                soft = [f for f in judge.SOFT_BOOLS if not booleans[f]]
                if hard or surviving:
                    expected = "fail" if evidence else "unsure"
                elif soft:
                    expected = "unsure"
                else:
                    expected = "pass"
                eq(verdict, expected, f"booleans={booleans} letters={letters} evidence={bool(evidence)}")
                if expected == "pass":
                    eq(reasons, [], "a pass carries no reasons")
                else:
                    if not reasons:
                        raise AssertionError("a non-pass must say why")
                checked += 1
    eq(checked, 2 ** len(fields) * 4 * 2, "combinations covered")


@test
def test_the_correct_letter_is_never_a_distractor_defect():
    """THE false-positive guard: 'the correct answer reads as correct' is not a defect."""
    reply = dict(GOOD_REPLY, distractor_became_correct=["a"], evidence="x")
    eq(judge.derive_verdict(reply, correct_letters=["a"])[0], "pass", "correct letter discarded")
    eq(judge.derive_verdict(reply, correct_letters=["b"])[0], "fail", "a real distractor is a fail")
    multi = dict(GOOD_REPLY, distractor_became_correct=["a", "c"], evidence="x")
    v, reasons = judge.derive_verdict(multi, correct_letters=["a", "c"])
    eq(v, "pass", "multi-answer question: both key letters discarded")


@test
def test_a_distractor_that_differs_wildly_is_not_a_defect():
    """The localisation convention: non-literal distractors must not be flagged.

    The judge expresses that by leaving distractor_became_correct empty; nothing
    in the derivation may invent a failure from the distractor texts themselves.
    """
    localised = json.loads(json.dumps(TARGET_VIEW))
    localised["options"]["c"] = "Tutaj obowiązuje zakaz zatrzymywania się w dni robocze."
    reply = dict(GOOD_REPLY)
    eq(judge.derive_verdict(reply, correct_letters=["a"])[0], "pass", "free distractor stays a pass")
    p = judge.build_prompt(SOURCE_VIEW, localised, "pl")
    contains(p, "still clearly a WRONG answer", "the two-question distractor rule is in the prompt")


@test
def test_fail_without_evidence_is_downgraded_not_dropped():
    reply = dict(GOOD_REPLY, polarity_preserved=False, evidence="")
    verdict, reasons = judge.derive_verdict(reply, correct_letters=["a"])
    eq(verdict, "unsure", "unquoted accusation")
    contains(",".join(reasons), "polarity_preserved", "reason kept")
    contains(",".join(reasons), "downgraded_from_fail", "downgrade is visible")


@test
def test_low_confidence_can_only_weaken_a_pass():
    eq(judge.derive_verdict(dict(GOOD_REPLY, confidence=0.4), correct_letters=["a"])[0], "unsure")
    # ... and never strengthen a fail into anything else
    eq(judge.derive_verdict(dict(GOOD_REPLY, confidence=1.0, stem_equivalent=False,
                                 evidence="q"), correct_letters=["a"])[0], "fail")


@test
def test_model_self_verdict_is_ignored():
    """The model may write anything in `verdict`; it never decides."""
    liar = dict(GOOD_REPLY, stem_equivalent=False, evidence="q", verdict="pass")
    eq(judge.derive_verdict(liar, correct_letters=["a"])[0], "fail", "model said pass, booleans said no")
    flatterer = dict(GOOD_REPLY, verdict="fail")
    eq(judge.derive_verdict(flatterer, correct_letters=["a"])[0], "pass", "model said fail, booleans said yes")


# ---------------------------------------------------------------- bad replies
@test
def test_malformed_replies_are_never_a_pass():
    q = cells.load_questions("fuehrerschein")["zeichen-68"]
    bad_replies = {
        "prose": "Sure! The translation looks fine to me.",
        "empty": "",
        "truncated json": '{"stem_equivalent": true, "correct_option_equi',
        "json array": '[{"stem_equivalent": true}]',
        "json string": '"pass"',
        "missing field": json.dumps({k: v for k, v in GOOD_REPLY.items() if k != "polarity_preserved"}),
        "boolean as string": json.dumps(dict(GOOD_REPLY, numbers_preserved="true")),
        "boolean as null": json.dumps(dict(GOOD_REPLY, numbers_preserved=None)),
        "confidence out of range": json.dumps(dict(GOOD_REPLY, confidence=7)),
        "confidence as bool": json.dumps(dict(GOOD_REPLY, confidence=True)),
        "letters not a list": json.dumps(dict(GOOD_REPLY, distractor_became_correct="b")),
        "unknown option letter": json.dumps(dict(GOOD_REPLY, distractor_became_correct=["z"])),
        "markdown fenced": "```json\n" + json.dumps(GOOD_REPLY) + "\n```",
    }
    for label, text in bad_replies.items():
        record, _, _ = judge.judge_cell(client_with(text), "fuehrerschein", "zeichen-68", q, "pl",
                                        "qwen2.5:7b-instruct")
        eq(record["verdict"], "error", f"{label} must be an error")
        if not record.get("error"):
            raise AssertionError(f"{label}: error verdict without a diagnosis")
        if record["verdict"] == "pass":
            raise AssertionError(f"{label} was scored as a pass")


@test
def test_a_wellformed_reply_produces_a_full_receipt():
    q = cells.load_questions("fuehrerschein")["zeichen-68"]
    record, prompt, call = judge.judge_cell(client_with(json.dumps(GOOD_REPLY)),
                                            "fuehrerschein", "zeichen-68", q, "pl",
                                            "qwen2.5:7b-instruct")
    eq(record["verdict"], "pass")
    eq(record["source_hash"], cells.source_hash(q), "receipt pins the ledger hash")
    eq(record["target_hash"], cells.target_hash(q, "pl"))
    eq(record["prompt_sha256"], ollama_client.sha256_text(prompt), "prompt hash is of the real prompt")
    eq(record["model_digest"], "sha256:" + "ab" * 32, "full digest from /api/tags")
    eq(record["ollama_version"], "0.11.0")
    for field in ("prompt_template_sha256", "options_sha256", "options", "at", "elapsed_ms"):
        if not record.get(field) and record.get(field) != 0:
            raise AssertionError("receipt missing " + field)
    receipts.validate(record)


@test
def test_wire_format_pins_determinism_knobs():
    q = cells.load_questions("fuehrerschein")["zeichen-68"]
    stub = StubTransport(json.dumps(GOOD_REPLY))
    client = ollama_client.OllamaClient(host="http://stub", transport=stub)
    judge.judge_cell(client, "fuehrerschein", "zeichen-68", q, "pl", "qwen2.5:7b-instruct")
    gen = [b for m, p, b in stub.calls if p == "/api/generate"][0]
    eq(gen["stream"], False, "streaming would break one-shot JSON")
    eq(gen["options"]["temperature"], 0)
    eq(gen["options"]["seed"], 42)
    if "num_ctx" not in gen["options"]:
        raise AssertionError("num_ctx must be explicit: the default silently truncates")
    eq(gen["format"], judge.VERDICT_SCHEMA, "schema-constrained output")
    eq(gen["format"]["required"], list(judge.VERDICT_SCHEMA["required"]))


# ---------------------------------------------------------------- client errors
@test
def test_unreachable_ollama_gives_advice_not_a_traceback():
    import urllib.error

    def dead(method, path, body=None):
        raise urllib.error.URLError("Connection refused")

    client = ollama_client.OllamaClient(host="http://127.0.0.1:11434", transport=None)
    client.transport = ollama_client._http_transport("http://127.0.0.1:1", 1)
    try:
        client.version()
    except ollama_client.OllamaUnavailable as exc:
        msg = str(exc)
        contains(msg, "ollama serve", "how to start it")
        contains(msg, "OLLAMA_HOST", "how to point it elsewhere")
        contains(msg, "SSD", "the external-store failure mode")
        return
    raise AssertionError("a dead Ollama must raise OllamaUnavailable")


@test
def test_missing_model_names_the_fix():
    client = client_with(json.dumps(GOOD_REPLY), tags=("bge-m3",))
    try:
        client.model_digest("aya-expanse:8b")
    except ollama_client.OllamaModelMissing as exc:
        contains(str(exc), "ollama pull aya-expanse:8b", "the exact command")
        contains(str(exc), "bge-m3", "what is available instead")
        return
    raise AssertionError("a missing model must raise OllamaModelMissing")


@test
def test_latest_tag_is_matched_either_way():
    eq(client_with("{}", tags=("qwen3:8b",)).model_digest("qwen3:8b"), "sha256:" + "ab" * 32)
    eq(client_with("{}", tags=("qwen3:8b:latest",)).model_digest("qwen3:8b"), "sha256:" + "ab" * 32)


# ---------------------------------------------------------------- receipts
@test
def test_receipts_round_trip():
    os.makedirs(SCRATCH, exist_ok=True)
    path = receipts.path_for("roundtrip", SCRATCH)
    open(path, "w").close()  # start from empty; device_bash cannot delete files
    q = cells.load_questions("fuehrerschein")["zeichen-68"]
    first, _, _ = judge.judge_cell(client_with(json.dumps(GOOD_REPLY)), "fuehrerschein",
                                   "zeichen-68", q, "pl", "qwen2.5:7b-instruct")
    receipts.append("roundtrip", first, SCRATCH)
    second, _, _ = judge.judge_cell(
        client_with(json.dumps(dict(GOOD_REPLY, polarity_preserved=False, evidence="de X / pl Y"))),
        "fuehrerschein", "zeichen-68", q, "pl", "qwen2.5:7b-instruct")
    receipts.append("roundtrip", second, SCRATCH)

    loaded, broken = receipts.load("roundtrip", SCRATCH)
    eq(broken, [], "no unreadable lines")
    eq(len(loaded), 2, "append-only: both lines survive")
    eq(loaded[0]["verdict"], "pass")
    eq(loaded[0], json.loads(json.dumps(first)), "round-trips exactly")
    eq(receipts.latest_index("roundtrip", SCRATCH)[("zeichen-68", "pl")]["verdict"], "fail",
       "the newest receipt wins")


@test
def test_a_receipt_without_provenance_is_refused():
    for field in ("model_digest", "prompt_sha256", "source_hash", "at"):
        rec = {f: "x" for f in receipts.REQUIRED_FIELDS}
        rec[field] = ""
        try:
            receipts.validate(rec)
        except ValueError as exc:
            contains(str(exc), field, "names the missing field")
            continue
        raise AssertionError(f"a receipt without {field} must be refused")


@test
def test_corrupt_receipt_lines_are_reported_not_ignored():
    os.makedirs(SCRATCH, exist_ok=True)
    with open(receipts.path_for("corrupt", SCRATCH), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"id": "a", "locale": "pl", "verdict": "pass"}) + "\n")
        fh.write("{not json\n\n")
    loaded, broken = receipts.load("corrupt", SCRATCH)
    eq(len(loaded), 1)
    eq(len(broken), 1, "the bad line is reported")


# ---------------------------------------------------------------- tier 2
@test
def test_embedding_screen_never_sees_distractors():
    text = embed_screen.screen_text(TARGET_VIEW)
    contains(text, TARGET_VIEW["question"], "stem")
    contains(text, TARGET_VIEW["options"]["a"], "correct option")
    for letter in ("b", "c", "d"):
        if TARGET_VIEW["options"][letter] in text:
            raise AssertionError(f"distractor {letter} leaked into the embedded text")
    if TARGET_VIEW["explanation"] in text:
        raise AssertionError("the explanation would dominate the cosine")


@test
def test_cosine_behaves():
    eq(round(embed_screen.cosine([1, 0, 0], [1, 0, 0]), 6), 1.0)
    eq(round(embed_screen.cosine([1, 0, 0], [0, 1, 0]), 6), 0.0)
    eq(embed_screen.cosine([0, 0, 0], [1, 2, 3]), 0.0, "zero vector must not divide by zero")


# ---------------------------------------------------------------- seed set
@test
def test_seed_halves_are_disjoint_and_balanced():
    bad = cells.load_json(seed_eval.KNOWN_BAD)
    good = cells.load_json(seed_eval.KNOWN_GOOD)
    bad_keys = {(b["id"], b["locale"]) for b in bad}
    good_keys = {(g["id"], g["locale"]) for g in good}
    eq(bad_keys & good_keys, set(), "a cell in both halves would be scored twice")
    eq(len(bad), len(good), "the halves must be the same size")
    per = {}
    for entry in bad:
        per.setdefault(entry["locale"], [0, 0])[0] += 1
    for entry in good:
        per.setdefault(entry["locale"], [0, 0])[1] += 1
    for locale, (nb, ng) in sorted(per.items()):
        eq(nb, ng, f"{locale}: per-locale balance")


@test
def test_seed_bad_cells_really_differ_from_todays_text():
    """A 'known bad' cell that equals the shipped text would be scored as a defect wrongly."""
    for entry in cells.load_json(seed_eval.KNOWN_BAD):
        q = cells.load_questions(entry["module"])[entry["id"]]
        current = cells.cell_view(q, entry["locale"])
        spliced = cells.cell_view(seed_eval.materialise(entry), entry["locale"])
        if spliced == current:
            raise AssertionError(f"{entry['id']}/{entry['locale']} ({entry['defect']}) "
                                 "is identical to the shipped text")
        eq(cells.cell_view(seed_eval.materialise(entry), "de"), cells.cell_view(q, "de"),
           "the German half must never be mutated")


@test
def test_known_defects_are_present_in_the_seed():
    defects = {e["defect"] for e in cells.load_json(seed_eval.KNOWN_BAD)}
    for expected in ("wrong_sign_obstacle_vs_214", "wrong_sign_mofa_vs_pedestrian",
                     "wrong_number_133_vs_136", "leaked_high_stakes_token_in_target",
                     "synthetic_swapped_correct_option", "synthetic_foreign_cell",
                     "synthetic_digit_flip"):
        if expected not in defects:
            raise AssertionError("seed set lost the " + expected + " case")
    z68 = [e for e in cells.load_json(seed_eval.KNOWN_BAD)
           if e["id"] == "zeichen-68" and e["locale"] == "es"][0]
    contains(z68["target_override"]["options"]["a"], "Debe pasar por la derecha",
             "the real pre-fix obstacle-passing text")
    z04 = [e for e in cells.load_json(seed_eval.KNOWN_BAD)
           if e["id"] == "zeichen-04" and e["locale"] == "pl"][0]
    contains(z04["target_override"]["question"], "133", "the wrong sign number")


@test
def test_synthetic_swap_actually_breaks_the_answer_key():
    entry = [e for e in cells.load_json(seed_eval.KNOWN_BAD)
             if e["defect"] == "synthetic_swapped_correct_option"][0]
    q = cells.load_questions(entry["module"])[entry["id"]]
    before = cells.cell_view(q, entry["locale"])
    after = cells.cell_view(seed_eval.materialise(entry), entry["locale"])
    key = before["correct"][0]
    if after["options"][key] == before["options"][key]:
        raise AssertionError("the correct option was not actually swapped")
    if sorted(after["options"].values()) != sorted(before["options"].values()):
        raise AssertionError("a swap must permute, not rewrite")


@test
def test_metrics_and_the_viability_gate():
    eq(seed_eval.decide(0.05, 0.9)[:7], "ENABLED", "clean and sensitive")
    eq(seed_eval.decide(0.05, 0.4)[:8], "ADVISORY", "clean but blind")
    eq(seed_eval.decide(0.15, 0.9)[:8], "ADVISORY", "borderline noise")
    eq(seed_eval.decide(0.25, 1.0)[:8], "DISABLED", "flags everything -> worthless")
    eq(seed_eval.decide(0.30, 0.0)[:8], "DISABLED")
    results = [
        {"locale": "pl", "label": "bad", "verdict": "fail", "elapsed_ms": 1000},
        {"locale": "pl", "label": "bad", "verdict": "unsure", "elapsed_ms": 1000},
        {"locale": "pl", "label": "bad", "verdict": "pass", "elapsed_ms": 1000},
        {"locale": "pl", "label": "good", "verdict": "pass", "elapsed_ms": 1000},
        {"locale": "pl", "label": "good", "verdict": "fail", "elapsed_ms": 1000},
        {"locale": "pl", "label": "good", "verdict": "error", "elapsed_ms": 1000},
    ]
    strict = seed_eval.summarise(results, {"fail"})["pl"]
    eq((strict["tp"], strict["fn"], strict["fp"], strict["tn"]), (1, 2, 1, 2), "strict policy")
    eq(strict["err_good"], 1, "an error is counted apart, never as a catch or a false positive")
    loose = seed_eval.summarise(results, {"fail", "unsure"})["pl"]
    eq((loose["tp"], loose["fn"], loose["fp"]), (2, 1, 1), "review-queue policy")


@test
def test_seed_eval_end_to_end_against_a_stub_model():
    """A stub that flags exactly the bad half must produce 100 % recall and 0 % FP."""
    seeds = [e for e in seed_eval.load_seeds(["pl"])]
    bad_ids = {(e["id"], e["locale"]) for e in seeds if e["label"] == "bad"}

    def respond(body):
        # the stub "reads" the prompt: it flags a cell iff the prompt contains a
        # marker only the mutated/pre-fix text carries. Enough to exercise the
        # whole pipeline; it is not a model and proves nothing about a model.
        flag = any(marker in body["prompt"] for marker in ("133", "Mofa", "high_stakes", "ZZZ-mutated"))
        return json.dumps(dict(GOOD_REPLY, stem_equivalent=not flag,
                               evidence="de: X / pl: Y" if flag else "",
                               verdict="fail" if flag else "pass"))

    results = seed_eval.run_eval(seeds, client_with(respond), "qwen2.5:7b-instruct")
    eq(len(results), len(seeds))
    for r in results:
        if r["verdict"] == "error":
            raise AssertionError("stub replies must all parse")
    per = seed_eval.summarise(results, {"fail"})["pl"]
    if per["fp"]:
        raise AssertionError("the stub flagged a known-good cell")
    if per["tp"] < 1:
        raise AssertionError("the stub caught nothing - the harness is not wired up")
    report = seed_eval.build_report(results, "stub")
    contains(report, "Precision on the known-good half is what decides viability", "the headline")
    contains(report, "| locale |", "the per-locale table")
    contains(report, "recall", "recall column")
    for entry in results:
        receipts.validate(entry)


@test
def test_verify_receipts_sees_a_stale_receipt():
    import verify_receipts  # noqa: F401  (imported here so a syntax error surfaces as a test failure)
    q = cells.load_questions("fuehrerschein")["zeichen-68"]
    record, _, _ = judge.judge_cell(client_with(json.dumps(GOOD_REPLY)), "fuehrerschein",
                                    "zeichen-68", q, "pl", "qwen2.5:7b-instruct")
    eq(record["source_hash"], cells.source_hash(q), "current")
    stale = dict(record, source_hash="sha256:old")
    if stale["source_hash"] == cells.source_hash(q):
        raise AssertionError("fixture is not actually stale")


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    failures = []
    for fn in TESTS:
        name = fn.__name__
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - a test runner reports, it does not raise
            failures.append((name, f"{type(exc).__name__}: {exc}"))
            print(f"FAIL  {name}\n        {type(exc).__name__}: {exc}")
        else:
            print(f"ok    {name}")
    print()
    if failures:
        print(f"FAILED: {len(failures)} of {len(TESTS)} test(s)")
        return 1
    print(f"PASSED: {len(TESTS)} test(s), no model and no network involved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
