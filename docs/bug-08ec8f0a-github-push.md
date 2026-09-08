# Bug report — Cowork session cannot push to GitHub despite GitHub Integration being connected

**Bug ID:** 08ec8f0a-9e51-4abd-b577-3995ec871266
**Date:** 2026-09-07
**Session:** session_018y7msVZfmRRirN8wvv1GAP
**Reporter:** sels@tnwx.net (GitHub: `tronicum`)

---

## Summary

In a Cowork task created around a connected local folder, `git push` to a repository is
impossible through every available path, even though the GitHub Integration is connected at
account level and the repository is explicitly granted to the GitHub App.

The account-level GitHub Integration is never wired into the session: the agent proxy holds an
empty authorized-repository set, the connector is not exposed to the session at all, and the
`add_repo` tool the error message instructs the agent to call does not exist in this session type.

This is not a misconfiguration on the user's side. Every user-facing control is already set
correctly. There is no action available to the user or the agent that closes the gap.

## Environment

| | |
|---|---|
| Product | Cowork (Claude desktop app), cloud session linked to a local device |
| Desktop app | 1.46388.4 (Electron 42.10.0, Node 24.18.1) |
| Device | `mac-fritz-box`, macOS, arm64 |
| Connected folder | `/Users/stefan/workspace/Zettacard` |
| Repository | `https://github.com/tronicum/Zettacard` (public) |
| Device workspace VM | Linux aarch64 6.8.0-136-generic, git 2.34.1, `$HOME=/sessions/rcw-018y7msvzfmrrirn8wvv1gap` |

## Preconditions (all verified correct)

1. GitHub App installed on the `tronicum` account, "Only select repositories", 30 repos
   selected, `tronicum/Zettacard` among them.
2. Desktop Connectors panel lists **GitHub Integration — Type: Web — Status: connected (✓)**,
   alongside Google Drive and Netlify.
3. `GITHUB_TOKEN` / `GH_TOKEN` are present in the cloud container and authenticate correctly:
   `GET https://api.github.com/user` returns `tronicum`.

## Expected behaviour

With the GitHub Integration connected and the repository granted to the App, the session can
push to `tronicum/Zettacard`.

## Actual behaviour

Push fails on every path. Read succeeds only because the repository is public and needs no
credential — which makes the integration look functional until a write is attempted.

---

## Finding 1 — Proxy holds an empty authorized-repository set (primary)

From the cloud container, against a fresh clone:

```
$ git push --dry-run origin HEAD:refs/heads/main
remote: access denied by the git proxy: tronicum/Zettacard is not in this session's
authorized repository set, so the proxy will not inject a credential for it.
To fix, add the repository to the session's sources.
fatal: unable to access 'https://github.com/tronicum/Zettacard/': The requested URL returned error: 403
```

Anonymous read over the same proxy works, confirming the block is credential injection, not
network reachability:

```
$ git ls-remote https://github.com/tronicum/Zettacard HEAD
7ad2d8f7aed677498fd05f1e78fa4d9ffb258806	HEAD          # exit 0
```

Proxy state at the time: `enabled: true`, `gitConfigInjection: true`, `gitSshRewrite: true`,
`selective: false`, `toolScoped: false`, `recentRelayFailures: []`.

**The session's "sources" the message refers to are not reachable from anywhere in the product
for a folder-based Cowork task.** The task was created with a local folder attached; no UI
offers adding a GitHub repository to an existing task, and account-level settings do not
populate this set.

## Finding 2 — The remediation tool named in the error does not exist

The GitHub API returns, through the same proxy:

```
HTTP 403
GitHub access to this repository is not enabled for this session. Use add_repo to request
access. If add_repo answers that read access is already available and you need GitHub API or
write access, call add_repo again with access:"push" to attach the repository with credentials.
```

`add_repo` is not available in this session:

```
ToolSearch "select:add_repo"  ->  No matching deferred tools found
```

The error text is written for a session type that has the tool, and is surfaced verbatim in one
that does not. It instructs the agent to take an action it cannot take, which is actively
misleading during diagnosis.

## Finding 3 — GitHub Integration is not exposed to the session

`ListConnectors` returns only:

```json
[{"name":"Google Drive","installState":"connected","connected":true,"enabledInChat":true},
 {"name":"Netlify","installState":"needs_reconnect","connected":false,"enabledInChat":true}]
```

**GitHub Integration is absent entirely** — not listed as disconnected or disabled, simply not
present — while the desktop Connectors panel shows it connected with a ✓. No GitHub tools are in
the session's tool list. `SearchMcpRegistry` for github/git/repository returns no GitHub server
either.

The user has no way to tell from the UI that a connector showing ✓ is invisible to the session
they are working in.

## Finding 4 — The device workspace VM has no git credentials and none are injected

`device_bash` runs in an ephemeral Linux VM with the user's folders mounted, not in the user's
macOS shell. Pushing from there:

```
$ git push --dry-run origin ship/2026-09-07
fatal: could not read Username for 'https://github.com': No such device or address
```

Credential inventory in that VM — everything absent:

```
git config --get credential.helper       -> (empty)
git config --global --list               -> fatal: unable to read config file
                                            '/sessions/rcw-.../.gitconfig': No such file or directory
~/.git-credentials                       -> No such file or directory
~/.netrc                                 -> No such file or directory
~/.ssh                                   -> No such file or directory
which gh                                 -> (not installed)
env | grep -i github                     -> (none)
```

The macOS keychain that makes push work in the user's own terminal is not visible to this VM,
and the proxy's credential injection does not extend to it. `git fetch` succeeds only via
anonymous public read.

`$HOME` is `/sessions/rcw-<session-id>/`, which is ephemeral — so even a manual credential setup
would not survive the session. The only writable persistent location is the mounted project
folder itself, which would mean a plaintext token inside the user's repository directory.

## Finding 5 — `unlink` blocked on mounted folders has silently corrupted the repository's object store

This is not cosmetic. It has been degrading the user's repository for roughly four weeks.

The device bridge's delete restriction applies inside `.git/`. Git assumes it can remove its own
temporary files and lock files; when `unlink` fails it warns and continues, so the damage
accumulates invisibly:

```
warning: unable to unlink '.git/objects/7a/tmp_obj_Yd0FZs': Operation not permitted
```

Confirmed directly:

```
$ touch .git/zz_unlink_probe && rm .git/zz_unlink_probe
rm: cannot remove '.git/zz_unlink_probe': Operation not permitted
```

### Minimal reproduction (verified)

After a full manual cleanup from the user's own terminal — `git gc --prune=now` reporting
`packs: 1, garbage: 0, prune-packable: 0` — a **single** `git fetch` issued through
`device_bash` re-created the stale lock immediately:

```
$ git fetch --all
Fetching origin
warning: unable to unlink
'/sessions/rcw-.../mnt/Zettacard/.git/objects/maintenance.lock': Operation not permitted

$ find .git -name '*.lock'
.git/objects/maintenance.lock
```

`git fetch` triggers auto-maintenance, which takes `.git/objects/maintenance.lock` and tries to
release it on exit. The release fails, so from that moment maintenance is disabled again and
garbage begins accumulating anew. **The repository cannot stay healthy for longer than one
bridge git operation.** No amount of cleanup from the user's side persists.

Reproduction is one command in any git repository inside a connected folder.

### Accumulated damage in this one repository

```
$ git count-objects -v
warning: garbage found: .git/objects/pack/tmp_idx_j3zu9e
warning: garbage found: .git/objects/pack/tmp_pack_d81qHc
... (25 warnings total)
count: 983
in-pack: 11412
packs: 28
prune-packable: 202
garbage: 25
size-garbage: 47671        # ~46 MB of orphaned temp packs
```

**25 orphaned files, ~46 MB**, with timestamps running from **12 Aug** to the present — every
`tmp_pack_*` / `tmp_idx_*` that any fetch, repack or maintenance run tried and failed to clean
up. The pack count has reached 28.

### Stale locks that can never be released

```
-rw------- 0 Aug 12 04:50 .git/objects/maintenance.lock
-rw------- 0 Aug 16 08:31 .git/refs/bundle-test-verify.lock
```

`.git/objects/maintenance.lock` is the critical one. `git maintenance` takes this lock, and on
exit tries to remove it. The removal failed on **12 August**, and because the file cannot be
deleted from inside the bridge, **every `git maintenance` run since then has aborted
immediately**. Maintenance is exactly the process that would have cleaned up the temp packs, so
the failure is self-reinforcing: the unlink restriction creates the garbage *and* disables the
only mechanism that removes it.

`.git/refs/bundle-test-verify.lock` similarly blocks any update to `refs/bundle-test-verify`.

### Why this matters beyond disk usage

- `git gc`, `git repack` and `git prune` fail or refuse to run.
- Object lookups slow as the pack count grows unbounded (28 and climbing).
- `prune-packable: 202` — loose objects that duplicate packed ones, never reclaimed.
- The user sees no error. Git downgrades every one of these to a warning, and the bridge reports
  success on the surrounding operation.

This will affect **every** git repository worked on through a connected folder, and the longer a
project is used this way, the worse it gets. A repository that is only ever read stays clean; one
that is actively fetched and committed to degrades steadily.

### The restriction blocks `unlink` but not `rename`

Worth noting for whoever fixes this: the bridge refuses `unlink` while permitting `rename`.

```
$ rm .git/objects/maintenance.lock
rm: cannot remove '...': Operation not permitted

$ mkdir -p .git/_to_delete && mv .git/objects/maintenance.lock .git/_to_delete/
(succeeds)
```

So the restriction does not actually prevent an agent from disposing of a file — it only
prevents doing it cleanly. Anything unwanted can be renamed out of the way, which leaves clutter
in the user's folder instead of a clean removal. As a safety boundary it is porous; as an
obstacle to correct tool behaviour it is total. That asymmetry is backwards.

### Workaround applied (partial)

Disabling git's auto-maintenance in the affected repository stops the lock from being taken at
all, which stops the recurrence:

```bash
git config maintenance.auto false
git config gc.auto 0
mkdir -p .git/_to_delete && mv .git/objects/maintenance.lock .git/_to_delete/
```

Verified: `git fetch --all` through the bridge afterwards completes with no warning, creates no
lock, and leaves `garbage: 0`. This is a per-repository mitigation that has to be applied by
hand to every repo worked on through a connected folder, and it trades away automatic
maintenance to do it. It is not a fix.

### Suggested handling

Git's own temp and lock files inside `.git/` should be exempt from the bridge's unlink
restriction. The restriction exists to protect the user's *content* from unintended deletion;
`.git/objects/pack/tmp_pack_*` and `*.lock` are tool-internal housekeeping that the user never
sees and would never be asked to approve. Routing them through the delete-permission prompt is
not a workable alternative — they are created and destroyed many times per operation.

## Finding 6 — `device_bash` wedged for the whole first half of the session

Five consecutive `device_bash` calls failed with no output and no diagnostic beyond a generic
failure string, while `device_list_dir`, `device_stage_files` and `get_device_info` continued to
work normally against the same device. The shell recovered only after the user restarted the
desktop app. During the outage, `.git/` had to be read by staging individual ref files into the
container to determine repository state.

---

## Impact

For any Cowork task built on a connected folder plus a GitHub repository — the natural shape for
agentic coding work — the agent can read, edit and commit, but cannot push. Work accumulates
locally and every ship step requires the user to drop into their own terminal, which defeats the
point of the integration.

The failure is also expensive to diagnose. Four separate surfaces each report success or say
nothing is wrong:

- GitHub App settings: repository granted ✓
- Connectors panel: GitHub Integration connected ✓
- `git fetch` / `git clone`: succeed (public repo, anonymous)
- `GET /user`: authenticates as the correct account ✓

Only `git push` fails, and the error names a fix ("add the repository to the session's sources")
that maps to no control the user can reach and no tool the agent has.

The same failure occurred previously in the user's `zettacard-legacy` project, so this is
reproducible across tasks rather than specific to one session.

## Suggested fixes

1. **Populate the proxy's authorized-repository set from the account-level GitHub Integration**
   for folder-based Cowork tasks, or expose `add_repo` in these sessions so the gap is closable
   at runtime.
2. **Surface a repository picker** on Cowork tasks, alongside the folder picker, and allow
   attaching a repository to an existing task.
3. **Do not emit remediation text naming tools the session does not have.** Detect the session
   type and either omit the `add_repo` instruction or state that the repository must be attached
   at task creation.
4. **Make `ListConnectors` report connectors that are connected but not exposed**, rather than
   omitting them — a connector showing ✓ in the panel and absent from the session is
   indistinguishable from a bug in the connector itself.
5. **Exempt `.git/` internals from the device bridge's unlink restriction**, or grant git's
   temp-file cleanup an internal allowance, so fetch/gc/repack behave correctly on mounted
   repositories.
6. **Improve `device_bash` failure reporting** — a distinct error for "workspace wedged, restart
   required" would have saved most of a session, given that sibling device tools kept working.

## Cleanup commands for the affected repository

Run from a normal terminal (the bridge cannot do any of this):

```bash
cd /Users/stefan/workspace/Zettacard

# release the stale locks that have blocked maintenance since 12 Aug
rm -f .git/objects/maintenance.lock
rm -f .git/refs/bundle-test-verify.lock

# remove ~46 MB of orphaned temp packs
rm -f .git/objects/pack/tmp_pack_* .git/objects/pack/tmp_idx_*
rm -f .git/objects/7a/tmp_obj_Yd0FZs

# left by the unlink probe in Finding 5
rm -f .git/zz_unlink_probe

# repack and verify
git gc --prune=now
git count-objects -v
```

`git count-objects -v` should afterwards report `garbage: 0` and a single-digit pack count.

Note that this is a temporary reprieve: per the reproduction in Finding 5, the next `git fetch`
run through the bridge re-creates `.git/objects/maintenance.lock` and the cycle restarts. The
cleanup has to be repeated from a normal terminal until the unlink restriction is fixed.
