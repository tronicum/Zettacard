#!/usr/bin/env python3
"""Minimal, auditable Ollama HTTP client (stdlib only).

SCOPE
-----
Everything this project asks of a local model goes through here: /api/generate
for the judge, /api/embed (or the older /api/embeddings) for the Tier 2
pre-filter, /api/tags for the model digest and /api/version for the runtime.
No streaming, no chat history, no tool calls - a judge call is one prompt in,
one JSON object out.

WHY IT LOOKS LIKE THIS
----------------------
1. **Determinism is the product.** temperature 0, an explicit seed, an explicit
   num_ctx (Ollama's default context is small and would silently truncate a
   bilingual prompt - a truncated prompt that still returns valid JSON is the
   worst possible failure mode) and a JSON-schema `format` are set on every
   call and recorded verbatim in the receipt.
2. **A verdict without provenance is worthless.** Every call returns a `Call`
   carrying the model name, its *full* digest from /api/tags (tags move,
   digests do not), the Ollama version, the sha256 of the exact prompt string
   and the sha256 of the options+schema. That tuple is what makes a verdict
   reproducible six months later - and what tells you which knob moved if it
   is not.
3. **Testability without a model.** All HTTP goes through one injectable
   `transport(method, path, body) -> dict`. test_offline.py passes a stub;
   nothing in this repo's test suite ever needs Ollama running.

NOTE ON PROVENANCE, HONESTLY: this file was written in a Linux VM with no
Ollama and no route to the developer's Mac. The pure logic below is covered by
test_offline.py; the wire format is taken from docs/adr/ADR-ollama-setup.md §4.
If a real response disagrees with an assumption here, the response wins.
"""
import hashlib
import json
import os
import urllib.error
import urllib.request

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")

# Recorded verbatim in every receipt. num_ctx is explicit on purpose (see above).
DEFAULT_OPTIONS = {"temperature": 0, "seed": 42, "num_ctx": 4096, "num_predict": 400}


class OllamaError(RuntimeError):
    """Base class - always carries an actionable message, never a traceback."""


class OllamaUnavailable(OllamaError):
    pass


class OllamaModelMissing(OllamaError):
    pass


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(obj):
    """Stable hash of a JSON-serialisable object (sorted keys, no whitespace)."""
    return sha256_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


class Call(dict):
    """One model call plus everything needed to reproduce or audit it."""


def _http_transport(host, timeout):
    def transport(method, path, body=None):
        url = host.rstrip("/") + path
        data = None if body is None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", "replace")[:400]
            except Exception:
                pass
            if exc.code == 404 and "model" in detail.lower():
                raise OllamaModelMissing(
                    f"Ollama replied 404 for {path}: {detail.strip()}\n"
                    "The model is not in the local store. Pull it first, e.g.\n"
                    "  ollama pull qwen2.5:7b-instruct\n"
                    "and check `ollama list`. If the store is on the external SSD, "
                    "confirm it is mounted and OLLAMA_MODELS points at it "
                    "(docs/adr/ADR-ollama-setup.md §3)."
                ) from None
            raise OllamaError(
                f"Ollama returned HTTP {exc.code} for {method} {path}: {detail.strip()}"
            ) from None
        except urllib.error.URLError as exc:
            raise OllamaUnavailable(
                f"Cannot reach Ollama at {host} ({exc.reason}).\n"
                "Most likely one of:\n"
                "  1. Ollama is not running       -> `ollama serve` (or start Ollama.app), "
                "then `curl -s $OLLAMA_HOST/api/version`\n"
                "  2. It is listening elsewhere   -> set OLLAMA_HOST "
                f"(currently {host}) or pass --ollama\n"
                "  3. The model store is on an unmounted external SSD -> mount it, "
                "then restart `ollama serve` (docs/adr/ADR-ollama-setup.md §3)\n"
                "This tooling never falls back to a hosted API: content must not "
                "leave the machine (ADR-llm-translation-qa, driver D3)."
            ) from None
        except TimeoutError:
            raise OllamaUnavailable(
                f"Ollama at {host} did not answer within {timeout}s. A first call after a "
                "model load from an external SSD can be slow; raise --timeout, and consider "
                "OLLAMA_KEEP_ALIVE=60m so the model is not unloaded between cells."
            ) from None
    return transport


class OllamaClient:
    def __init__(self, host=DEFAULT_HOST, timeout=300, transport=None, options=None):
        self.host = host
        self.timeout = timeout
        self.transport = transport or _http_transport(host, timeout)
        self.options = dict(DEFAULT_OPTIONS)
        if options:
            self.options.update(options)
        self._tags = None
        self._version = None

    # ---- provenance -------------------------------------------------------
    def version(self):
        if self._version is None:
            try:
                self._version = str(self.transport("GET", "/api/version", None).get("version", "?"))
            except OllamaError:
                raise
        return self._version

    def tags(self):
        """{model name -> {digest, size, ...}} from /api/tags."""
        if self._tags is None:
            payload = self.transport("GET", "/api/tags", None)
            self._tags = {m.get("name"): m for m in payload.get("models", [])}
        return self._tags

    def model_digest(self, model):
        """Full sha256 digest of a model tag. Tags move; digests are the pin."""
        tags = self.tags()
        entry = tags.get(model) or tags.get(f"{model}:latest")
        if entry is None and model.endswith(":latest"):
            entry = tags.get(model[: -len(":latest")])
        if entry is None:
            have = ", ".join(sorted(tags)) or "(none)"
            raise OllamaModelMissing(
                f"Model {model!r} is not in the local Ollama store.\n"
                f"  available: {have}\n"
                f"  fix:       ollama pull {model}\n"
                "If `ollama list` shows it but this does not, the daemon answering on "
                f"{self.host} is a different one than your shell talks to."
            )
        digest = entry.get("digest") or ""
        return digest if digest.startswith("sha256:") or not digest else "sha256:" + digest

    # ---- inference --------------------------------------------------------
    def generate_json(self, model, prompt, schema, options=None):
        """One schema-constrained completion. Returns a Call with full provenance.

        The parsed object is NOT validated against the rubric here - that is
        judge.py's job. What is guaranteed is: the response was JSON, or the
        caller gets `parsed=None` and `parse_error` set. A malformed reply is
        never silently turned into an empty (and therefore all-false, or
        all-true) verdict.
        """
        opts = dict(self.options)
        if options:
            opts.update(options)
        body = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": opts,
            "format": schema,
        }
        digest = self.model_digest(model)
        version = self.version()
        payload = self.transport("POST", "/api/generate", body)
        raw = payload.get("response", "")
        parsed, parse_error = None, None
        try:
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                parsed, parse_error = None, f"model returned JSON of type {type(parsed).__name__}, expected object"
        except (ValueError, TypeError) as exc:
            parse_error = f"model reply is not JSON: {exc}"
        return Call(
            model=model,
            model_digest=digest,
            ollama_version=version,
            prompt_sha256=sha256_text(prompt),
            options=opts,
            options_sha256=sha256_obj({"options": opts, "format": schema}),
            raw=raw,
            parsed=parsed,
            parse_error=parse_error,
            eval_count=payload.get("eval_count"),
            eval_duration_ns=payload.get("eval_duration"),
            total_duration_ns=payload.get("total_duration"),
        )

    def embed(self, model, inputs):
        """Embeddings for a list of strings.

        Recent Ollama exposes /api/embed (batch, key "embeddings"); older builds
        only have /api/embeddings (single "prompt", key "embedding"). Both are
        handled because the Mac's version is unknown from here.
        """
        digest = self.model_digest(model)
        try:
            payload = self.transport("POST", "/api/embed", {"model": model, "input": list(inputs)})
            vectors = payload.get("embeddings")
        except OllamaError:
            vectors = None
        if not vectors:
            vectors = []
            for text in inputs:
                payload = self.transport("POST", "/api/embeddings", {"model": model, "prompt": text})
                vec = payload.get("embedding")
                if not vec:
                    raise OllamaError(
                        f"Embedding model {model!r} returned no vector. Check `ollama list` "
                        "and that the tag is an embedding model (e.g. bge-m3)."
                    )
                vectors.append(vec)
        return Call(model=model, model_digest=digest, vectors=vectors)


def preflight(client, models):
    """Human-readable readiness check. Raises OllamaError with advice, or returns a dict."""
    info = {"host": client.host, "ollama_version": client.version(), "models": {}}
    for model in models:
        info["models"][model] = client.model_digest(model)
    return info


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Check that Ollama is reachable and models are pulled.")
    ap.add_argument("--ollama", default=DEFAULT_HOST)
    ap.add_argument("--model", action="append", default=[], help="repeatable; model tag to verify")
    args = ap.parse_args()
    try:
        info = preflight(OllamaClient(host=args.ollama), args.model)
    except OllamaError as exc:
        raise SystemExit(f"NOT READY\n\n{exc}")
    print(json.dumps(info, indent=2))
