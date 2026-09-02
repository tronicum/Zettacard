# cka_kubectl_drills.json — schema & matching-engine notes

For whoever wires this content up to the terminal-look UI (a separate,
parallel workstream — this file describes the content side only, not the
frontend). Written alongside `data/cka_kubectl_drills.json` and its
generator `data/gen_cka_kubectl_drills.py`.

## What this is, and isn't

50 "kubectl command-recall drill" tasks. The learner reads a `prompt`,
types one `kubectl` command into a terminal-look widget, and the typed
string gets checked against `accepted_grammar` — a small structured
description of what a correct answer looks like. There is no real
`kubectl` binary, no cluster, no WASM, nothing server-side: matching is a
pure string/token check that can run entirely client-side, offline, per
AGENTS.md constraint 6. This is explicitly *not* an attempt to build a real
grammar/parser for the `kubectl` CLI — see "Deliberately kept simple"
below for what was left out on purpose.

## Locale scope

`en`, `de`, `ja`, `zh` — matches the precedent already set by
`data/cka_course.json` / `data/cka_pilot.json`, not the project's normal
12-locale default (AGENTS.md constraint 5's explicit CKA exception).
`reference_command` and every token inside `accepted_grammar` is
locale-independent (kubectl syntax doesn't get translated); only
`prompt`, `hint`, `success_message` and `explanation` are localized.

## Top-level shape

```
{
  "meta": { ... one _meta-style block, see the file itself ... },
  "tasks": [ { ...task... }, ... ]   // 50 entries
}
```

`meta.legal_review_status` is `"pending"` and `meta.license_ref` is
`"CC-BY-NC-SA-4.0"`, per AGENTS.md constraints 3 and 4 — do not silently
upgrade the review status. `meta.topic_code_counts` and
`meta.difficulty_counts` are computed by the generator script, not
hand-maintained, so they can't drift from the actual task list.

## Per-task fields

- `id` — `kubectl-drill-NNN`, stable, zero-padded, assigned in generation
  order (grouped by topic_code — see the script for the exact grouping).
- `topic_code` — one of the seven values already used by
  `data/cka_course.json`/`data/cka_pilot.json`:
  `core_concepts`, `workloads`, `config_scheduling`, `networking`,
  `storage`, `security_admin`, `troubleshooting`. Confirmed by reading
  both files rather than guessed.
- `difficulty` — `easy` / `medium` / `hard`. Distribution across the 50
  tasks: 21 easy / 21 medium / 8 hard.
- `prompt`, `hint`, `explanation` — localized (`en`/`de`/`ja`/`zh`),
  bespoke per task.
- `success_message` — localized, but deliberately **canned**: five
  rotating variants per language, assigned round-robin by task index, not
  hand-written per task. The card's own spec calls this field "canned
  positive feedback," so this was a deliberate scope-saving choice, not an
  oversight — a bespoke congratulatory line per task would have added
  volume without adding learning value.
- `reference_command` — one fully-correct example string. This is *a*
  correct answer, not *the* only correct answer — several tasks have
  multiple equally valid phrasings (short vs. long flag names, `-n` vs
  `--namespace`, resource short names like `pod`/`po`), all captured in
  `accepted_grammar`, not just the one shown here.
- `accepted_grammar` — see below.

## `accepted_grammar` design

Built for a plain-JS tokenizer + rule matcher — no parser library, no
regex DSL, no grammar generator. The whole thing tokenizes the learner's
input on whitespace (**respecting quotes** — see gotcha #1 below), then
checks a handful of independent rules. Fields, all optional except
`base_tokens`:

- **`base_tokens`** — the leading token sequence that must appear, in
  order, as `kubectl <verb> [<resource>]`. Each **slot** in this array is
  either a plain string (exact match) or an array of strings (any one of
  them matches) — this is how resource short names are handled, e.g.
  `["pods", "pod", "po"]` for a `get pods` task. This same
  string-or-array-of-strings convention is reused everywhere else a
  "slot" appears (`positional_args`, `required_trailing_args`) — one
  mechanism, not three.
- **`positional_args`** — token slots required immediately after
  `base_tokens`, in order (e.g. an object name, or a `KEY=VALUE` pair for
  `kubectl label`). Same string-or-array convention. A couple of tasks
  (e.g. `kubectl-drill-015`, `kubectl-drill-023` rollout tasks) use an
  array slot containing a *multi-word* alternative
  (`"deployment/checkout"` vs `"deployment checkout"`) — when an
  alternative string itself contains a space, the implementer should
  split it into multiple consumed tokens, not treat it as one literal
  token to compare against.
- **`required_flags`** — list of `{forms, value?, value_match?}`. `forms`
  is the array of acceptable spellings for one logical flag (e.g.
  `["-n", "--namespace"]`); at least one of those forms must be present.
  If `value` is set, the flag's value must match it (default
  `value_match: "exact"`, case-sensitive, after stripping any surrounding
  quote characters the learner's shell-style quoting left behind). If
  `value` is absent, the flag is a **presence-only** boolean flag (e.g.
  `--rm`, `--force`, `-f`/`--follow`) — see gotcha #2.
- **`optional_flags`** — informational only. Present or absent, they
  don't affect correctness. Listed mainly so a "here's what else you
  could add" secondary hint could be built later; the matcher can ignore
  this field entirely for pass/fail purposes.
- **`required_trailing_args`** — token slots that must appear, in order,
  immediately after a literal `--` token (kubectl's own separator between
  its own flags and a container's command). Only a few tasks use this
  (Job/CronJob/`kubectl run ... -- <cmd>` tasks).
- **`forbidden_tokens`** — rare; a short list of literal words that, if
  present anywhere in the input, make an otherwise-plausible answer wrong
  for *this specific task* (used once, on `kubectl-drill-008`, to catch a
  learner who reaches for `kubectl create deployment` on a "bare Pod, no
  Deployment" task).
- **`either_base`** — present but unused in this batch (0 of the 50 tasks
  needed it). Reserved for a genuine full-command alternative (two truly
  different verbs that both produce a correct result for the same task).
  Deliberately not manufactured just to exercise the field — see below.
- **`common_wrong_attempts`** — present on a handful of tasks only: a
  `{command, why_key}` pair naming one tempting-but-wrong answer, for a
  richer "here's specifically why that's wrong" hint tier if the frontend
  wants one. `why_key` is a short slug, not localized text — the
  frontend/localization layer would need to map each key to a sentence
  per locale (or these could be promoted to inline localized strings
  later; kept as slugs here to avoid another 4x-locale text field on a
  rarely-used piece of the schema).
- **`notes`** — free-text, English-only, matcher-implementer-facing.
  Used on ~8 tasks for a genuinely tricky point (quoted multi-word flag
  values, colon-joined compound values, etc.) rather than repeated on
  every task.

## Known gotchas for whoever writes the actual matcher

1. **Tokenize with quote-awareness.** A few reference commands contain a
   flag value with spaces in it (`--schedule="0 2 * * *"`,
   `kubectl-drill-012`). A naive `input.split(" ")` would shred that into
   five tokens. Use a shell-like tokenizer (JS has no `shlex` built in —
   a small hand-rolled quote-aware splitter, or a tiny npm-free
   state-machine, is enough; don't reach for a full shell-parsing
   library for this).
2. **Distinguish value flags from boolean/presence-only flags before
   consuming the "next token" as a value.** This was the one real trap
   found while self-testing this file's own grammar against its own
   `reference_command`s: a naive matcher that sees `-f api` and assumes
   `-f` takes `api` as its value will wrongly swallow the Pod name as
   part of a `--follow` flag that actually takes no value at all
   (`kubectl-drill-044`, `kubectl logs -f api -n prod`). The fix is a
   small fixed registry, e.g.:
   `{"-f":false, "--follow":false, "--force":false, "--rm":false,
   "-A":false, "--all-namespaces":false, "--previous":false, "-p":false,
   "--current":false, "--ignore-daemonsets":false, "-it":false, ...}`
   (false = boolean/no value) vs. everything else defaulting to
   "consumes the next token, or an `=`-joined value, as its value." This
   repo's own grammar objects already encode which of a task's
   `required_flags` are boolean (no `value` key) vs. value-taking (has a
   `value` key) — that's exactly the signal to build such a registry
   from; it doesn't need to be guessed at match time.
3. **`--flag=value` and `--flag value` are both valid kubectl syntax and
   both must match.** Every `value` in this file's grammar is written
   without regard to which shell form the learner used — normalize both
   forms to the same (form, value) pair before comparing.
4. **Case-sensitive, exact-string matching on resource names, namespaces,
   labels, and flag values.** `Nginx` ≠ `nginx`, `Web` ≠ `web`. Do not
   add case-folding — kubectl itself is case-sensitive about these, and
   learning that the hard way once in a drill is cheaper than in the
   real exam.
5. **Flag *order* never matters; base-token and positional-arg order
   always does.** `kubectl get pods -n kube-system` and
   `kubectl get pods --namespace kube-system` (or with the flag placed
   before `pods`, e.g. `kubectl -n kube-system get pods` — kubectl itself
   accepts global flags before the verb) are all equally correct.
   Whether to accept a global-flag-before-verb ordering like the last
   example is a judgment call left to the implementer; none of this
   batch's `reference_command`s use that style, but a lenient matcher
   that tokenizes the whole line and only checks *presence*, not
   position, for flags (while still checking strict order for
   `base_tokens`/`positional_args`/`required_trailing_args`) will accept
   it for free without any special-casing.
6. **A resource-name slot like `["pods", "pod", "po"]` only appears
   inside `base_tokens`, immediately after the verb** — it is not a
   general "anywhere in the sentence" alternative-matching mechanism.
   Don't build a more general fuzzy-matcher than the schema actually
   needs.

## Deliberately kept simple / scope cut

- **No full kubectl grammar/parser.** Real `kubectl` accepts an enormous
  surface area (global flags in any position, `-o` with a dozen output
  formats, `--` command-arg passthrough with its own quoting rules,
  server-side vs. client-side dry-run nuances, etc.). This file's
  `accepted_grammar` intentionally covers only the one or two flags that
  actually matter for *that specific task*, plus the well-known spelling
  variants (`-n`/`--namespace`, short resource names). It will not catch
  every conceivable valid `kubectl` invocation for a given task — it
  doesn't need to; it needs to catch the small set of forms a learner
  practicing command recall would plausibly type.
- **No tasks requiring a YAML file as input.** Every task is answerable
  with exactly one `kubectl` command with no external file. Tasks that
  would naturally want `kubectl apply -f something.yaml` (e.g. a
  NetworkPolicy with actual ingress/egress rules, a Pod with a
  volumeMount, anything needing a securityContext) were either dropped
  or reshaped into a `get`/`describe`/`delete` task on the same resource
  kind instead — see e.g. `kubectl-drill-029` (list NetworkPolicies)
  rather than "create a NetworkPolicy that denies all ingress," which
  would need inline heredoc YAML the matcher can't reasonably grade with
  simple token rules.
- **No genuine `either_base` alternates were manufactured.** Several
  candidate tasks (e.g. "create a ClusterIP Service for this Deployment")
  have a *tempting* second command family (`kubectl create service
  clusterip ...`) that looks equivalent but actually behaves differently
  in a way that matters (it doesn't auto-derive a selector from the
  Deployment's Pod template the way `kubectl expose` does) — rather than
  encode a wrong "equivalent," those tasks were written narrowly enough
  that only one command family is actually correct, and the tempting
  wrong one is called out via `common_wrong_attempts` where it seemed
  worth flagging (e.g. `kubectl-drill-008`).
- **`common_wrong_attempts` is sparse, not exhaustive.** Only added where
  a specific, plausible wrong answer was foreseeable and worth a sharper
  hint; not an attempt to enumerate every possible mistake.

## Topic coverage (approximate CKA domain grounding)

Mapped from the public CNCF CKA curriculum's five domains onto this
project's existing seven `topic_code` values (general public knowledge of
the blueprint, not sourced from any paid material — see `meta.
domain_weight_note` in the JSON itself):

| topic_code | tasks | CNCF domain (approx.) |
|---|---|---|
| troubleshooting | 10 | Troubleshooting (heaviest domain) |
| workloads | 8 | Workloads & Scheduling (workload-object half) |
| networking | 8 | Services & Networking |
| core_concepts | 7 | Cluster Architecture, Installation & Configuration |
| config_scheduling | 7 | Workloads & Scheduling (config/scheduling half) |
| security_admin | 6 | Cluster Architecture (RBAC/service-account slice) |
| storage | 4 | Storage (lightest domain) |

## Open questions for the PO

1. **Locale quality bar.** DE/JA/ZH strings here are AI-authored in one
   pass, consistent in *style* with `cka_course.json`'s existing prose but
   not reviewed by a native-speaker domain expert — same caveat that
   already applies to the rest of the `cka` module's content, not a new
   risk this file introduces, but worth a native pass before this ships
   alongside graded content.
2. **`common_wrong_attempts.why_key` localization.** Right now these are
   English-only slugs (`creates_deployment_not_bare_pod`, etc.), not
   localized strings, on the assumption the frontend either doesn't
   surface them yet or will map them to a small localized-string table of
   its own. If the frontend wants inline localized text instead, that's
   a quick follow-up edit to this file, but it changes the field's shape
   (slug → `{en,de,ja,zh}` object) and is worth deciding before the
   matcher is built around one shape or the other.
3. **Difficulty calibration is a first-pass judgment call**, not derived
   from any measured pass-rate data (there is none yet — this is brand
   new content). 21 easy / 21 medium / 8 hard felt right for a first
   batch weighted toward building confidence, but there's no real
   difficulty telemetry yet to check that against.
4. **Two tasks assume tooling that may not exist on every practice
   cluster**: `kubectl-drill-050` (`kubectl top nodes`) needs the
   metrics-server add-on installed, and this is called out in the task's
   own `explanation`, but the drill itself can't detect or warn about
   that the way a real cluster would — worth deciding whether that's
   fine for a pure recall drill (arguably yes, since the *command* is
   still exactly what's being tested) or whether it should be swapped
   for a metrics-server-independent troubleshooting task instead.
5. **Everything else about the single-kubectl-command constraint held up
   without needing to cut a topic** — no task required dropping to a
   YAML-file pattern; see "Deliberately kept simple" above for how the
   handful of naturally-YAML-shaped candidates (NetworkPolicy rules,
   anything needing a volumeMount) were reshaped instead of skipped.
