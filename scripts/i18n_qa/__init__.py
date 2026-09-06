"""Tier 2/3 translation-QA tooling for Zettacard (see docs/adr/ADR-llm-translation-qa.md).

Tier 0 (staleness ledger) lives in scripts/translation_ledger.py and Tier 1
(deterministic lint) in scripts/check_data_integrity.py. Both are already
implemented, both gate CI, and nothing in this package is allowed to be a
reason to weaken them. This package only adds the two *model-based*, advisory
tiers, plus the receipts that let CI verify they ran without running a model.

Python 3 stdlib only, matching data/build_modules.py and the two existing
checkers. Nothing here needs installing beyond Ollama itself, which runs on the
developer's Mac and is never reachable from CI.
"""
