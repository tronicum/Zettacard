# Killercoda scenarios for the CKA course

Three gradable hands-on labs, one per "lab" lesson in Zettacard's `cka`
module (`data/cka_course.json`), authored against Killercoda's real
scenario format:

- `cka-l2-cluster-setup/` — lesson `cka-l2`: `kubeadm init` a control plane
  from a bare Ubuntu VM, verify it, then break and recover the API server.
- `cka-l5-rollout-scheduling/` — lesson `cka-l5`: rolling update, rollback,
  a broken rollout that doesn't take the service down, then three
  deliberately-Pending Pods (insufficient CPU, untolerated taint, unmatched
  label).
- `cka-l9-networking-storage-rbac/` — lesson `cka-l9`: a broken Service
  selector with vanishing endpoints, a PersistentVolumeClaim that survives a
  Pod delete/recreate, and RBAC least-privilege verified in both directions.

Each directory is a complete, self-contained Killercoda scenario:
`index.json` (the manifest), one markdown file per step plus intro/finish,
and a `verify.sh` per step that Killercoda runs when the learner clicks
**Check** — exit code `0` passes, non-zero fails and the learner sees the
script's own stderr/stdout as the reason. This is the actual grading
upgrade over the old prose-only lessons: a script checks the cluster's real
state (Pods actually Running, endpoints actually empty, `kubectl auth can-i`
actually answering the right way), not just "trust me, I did it."

Each scenario also carries a `METADATA.md` (authorship, license, and CNCF
curriculum grounding — see there for detail; this mirrors the
`license_ref`/`review_status`/`generator` metadata Zettacard already
attaches to every authored content section).

## What we verified about Killercoda's real format before writing any of this

Confirmed directly from Killercoda's own official examples repo
(`github.com/killercoda/scenario-examples`, fetched 2026-08-23), not
assumed:

- `index.json` shape: `{ "title", "description", "details": { "intro":
  {"text"}, "steps": [{"title","text","verify","foreground","background"}],
  "finish": {"text"}, "assets": {"host01": [{"file","target","chmod"}]} },
  "backend": {"imageid"}, "interface": {"layout"} }`.
- `verify` is a shell script; Killercoda runs it when the learner clicks
  **Check** and treats exit code `0` as pass, non-zero as fail. That's the
  entire grading contract — no separate assertion DSL.
- `backend.imageid` selects the environment: plain `ubuntu` (nothing
  pre-installed — what we used for `cka-l2`, since that lesson's whole point
  is running `kubeadm init` yourself) vs. pre-built Kubernetes clusters
  (`kubernetes-kubeadm-1node`, `kubernetes-kubeadm-2nodes` — what we used for
  `cka-l5`/`cka-l9`, which assume a cluster already exists).
- Step markdown supports inline exec/copy annotations —
  `` `cmd`{{exec}} ``, `` `cmd`{{}} `` (copy disabled), `` `cmd`{{exec
  interrupt}} `` (send Ctrl+C before running), and `<details><summary>` for
  collapsible hints/solutions.
- We did **not** find evidence of a raw multi-VM `ubuntu` backend that
  splits into named worker/control-plane hosts in the public examples we
  could reach (only the two-node *pre-built Kubernetes* image,
  `kubernetes-kubeadm-2nodes` — a different thing, since the cluster there
  already exists rather than being built by the learner). If a true 2-VM
  `kubeadm init` experience matching Zettacard's original prose more closely
  is available, it's configured through Killercoda's scenario dashboard at
  publish time, not through anything in this public examples repo — check
  there when you publish, and adjust `cka-l2-cluster-setup/index.json`'s
  `backend` block if a better option exists.

## What still has to happen — a human, not this session

These scenarios are **not live**. Authoring them here does not create a
`killercoda.com/<username>/scenario/<name>` URL — that only happens once a
real Killercoda account publishes them, and Killercoda authentication +
publishing is not something this session can do. To make them real:

1. **Create a Killercoda account** at killercoda.com (their creator
   onboarding is at `killercoda.com/creators` — sign in, there's a
   "Content" / "New Scenario" flow from your creator dashboard).
2. **Get these three directories into a git repo Killercoda can read.**
   Either point Killercoda's scenario importer at this Zettacard repo
   directly (if it's public, or via their git-integration flow — check
   `killercoda.com/creators` for the current "import from git" option), or
   copy each `hands-on-labs/cka-l*/` directory's contents into
   whatever repo/location their dashboard asks for per scenario. Killercoda
   scenarios are one-directory-per-scenario, which is exactly how these are
   laid out already.
3. **Set the backend/environment per scenario** in the Killercoda dashboard
   if it asks for anything beyond `index.json`'s `backend` block (e.g. a
   time limit, tags, or the multi-VM option noted above for `cka-l2`).
4. **Publish each scenario** and copy its real URL — it will look like
   `killercoda.com/<your-username>/scenario/cka-l2-cluster-setup` (or
   whatever slug Killercoda assigns).
5. **Paste each real URL into `data/cka_course.json`.** Each lab lesson's
   `practice_ref` currently has a placeholder `scenario_path` pointing at
   the directory in this repo (see below) — replace it with (or add
   alongside it) the live URL once you have it, then re-run
   `cd data && python3 build_modules.py` per `AGENTS.md`'s deploy section
   before the change is live in the app.

Until step 5 happens, `data/cka_course.json`'s prose `body` for each lab
still stands on its own as a complete, no-Killercoda-required fallback —
nothing about the app breaks if these never get published; it just keeps
working the way it always has.
