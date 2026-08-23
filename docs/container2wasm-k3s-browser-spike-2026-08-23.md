# Spike: Can a real Kubernetes control plane run client-side via container2wasm?

**Date:** 2026-08-23 · **Duration:** ~2h wall clock · **Author:** Zettacard feasibility spike
**Verdict: 🟡 YELLOW** — it genuinely works, but ~11 minutes and ~1.1 GB to first `kubectl` response.

---

## TL;DR

A real `kube-apiserver` + `etcd` + `kubectl` stack **does** boot and serve a real Kubernetes API
response inside a WebAssembly module, with no server backend, running only x86_64 emulation
(Bochs) compiled to WASM. `kubectl` printed a genuine `Server Version: v1.32.0` from an API server
running entirely inside the WASM sandbox.

But it is worse than that headline suggests. It took **569–650 seconds (9.5–10.8 min)** and
**936–1,130 MB** peak host RSS to reach that first response — roughly **125–295× slower** than the
same container natively (2.2–5.2 s). It only worked at all after switching the API server's TLS
keys from RSA-2048 to ECDSA P-256; with stock RSA the control plane **never became ready**, because
emulated crypto cannot finish a handshake inside Kubernetes' hard-coded 10-second timeout.

**And the API server then died within seconds of that first response.** `kubectl get nodes`,
`kubectl get ns`, and a server-side dry-run create — every actual resource operation — failed with
`connection refused`. **No real Kubernetes resource query ever succeeded in WASM.**

Real k3s is separately and independently blocked: the Linux kernel container2wasm ships has
**no netfilter/iptables, no bridge, no veth, no VXLAN, and no SMP**, so kube-proxy and CNI pod
networking cannot run at all without forking and maintaining a custom kernel config.

**Recommendation: do not invest further engineering time. Ship the Killercoda-scenario approach.**

---

## 1. Environment

| Item | Value |
|---|---|
| OS | Ubuntu 24.04.4 LTS, kernel 6.18.44 (Firecracker microVM) |
| CPU / RAM | 2 vCPU / 8 GB |
| Docker | 29.4.3 (buildx v0.33.0), started manually via `dockerd` |
| Go | 1.24.7 |
| container2wasm | release binary **v0.8.4**; repo HEAD `ecb4caa` (2026-06-30) |
| wasmtime | **33.0.2** (the version container2wasm's own CI pins). 29.0.1 also tried. |
| Target | **WASI build target** (`c2w` default), run under wasmtime — **not** the browser target. See §7. |
| Guest arch | amd64 → **Bochs** x86_64 emulator compiled to WASM |

Scratch dir: `/tmp/container2wasm-spike/` (standalone, not a Zettacard repo change).

---

## 2. Step 1 — reproduce the documented happy path

### 2.1 Four blockers had to be cleared first

This is a reportable finding in itself: **the documented happy path does not work out of the box
in a typical sandboxed Linux environment.** Four separate problems, in the order hit:

**(a) GitHub API is gated; direct release downloads are fine.**
`https://api.github.com/repos/container2wasm/container2wasm/releases/latest` → **HTTP 403**.
The official `wasmtime.dev/install.sh` installer depends on that API and fails with a mangled URL
(`.../releases/download/{/wasmtime-{-x86_64-linux.tar.xz`). Workaround: fetch pinned release URLs
directly, which return 200.

**(b) TLS trust is not propagated into BuildKit stages.** `c2w` shells out to `docker buildx`,
and the ~100-stage embedded Dockerfile clones from GitHub inside build containers. First failure,
91 s in:

```
#23 [runc-amd64-dev 2/2] RUN git clone https://github.com/opencontainers/runc.git ...
#23 1.065 fatal: unable to access 'https://github.com/opencontainers/runc.git/':
          server certificate verification failed. CAfile: none CRLfile: none
```

Fixed by generating the Dockerfile with `c2w --show-dockerfile`, programmatically injecting a CA
copy + cert env vars into all **23** registry-based `FROM` stages, and passing the bundle as a
named build context:

```
c2w --dockerfile Dockerfile.ca \
    --extra-flag=--build-context=cacerts=/tmp/container2wasm-spike/ca ...
```

**(c) The v0.8.4 release binary's embedded Dockerfile points at a dead repo.** Second failure:

```
#38 [assets-base 5/5] RUN git clone -b v0.8.4 https://github.com/ktock/container2wasm /assets
#38 1.211 fatal: Remote branch v0.8.4 not found in upstream origin
```

The project moved from `ktock/container2wasm` to the `container2wasm/container2wasm` org, but the
shipped v0.8.4 binary still hard-codes the old path, and the old repo no longer carries that tag.
**The released converter cannot build anything until you override this.** Fixed with
`--build-arg SOURCE_REPO=https://github.com/container2wasm/container2wasm`.

**(d) The generated WASM image requires a TTY, and dies silently without one.** With stdin not a
pty, the module runs, allocates ~4 GB of virtual address space, burns 6–21 s of CPU, then calls
`proc_exit(1)` with **zero bytes written to stdout or stderr** — no trap message, no diagnostic,
nothing. Confirmed via `strace`:

```
17335 mmap(NULL, 4362076160, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_NORESERVE, -1, 0) = 0x7f2558000000
17335 exit_group(1)
```

Also note `c2w` **always** passes `--build-arg LINUX_LOGLEVEL=0 --build-arg INIT_DEBUG=false`
unless you pass `--debug-image`, so there is no kernel output to diagnose with by default. With
`--debug-image` the boot is visible and `runc` is seen reaching
`init: about to wait on exec fifo` before dying. Running under a pty makes it work. This cost the
single largest chunk of debugging time in the spike and is essentially undocumented.

### 2.2 Result: the happy path works

Exact command:

```
c2w --dockerfile Dockerfile.ca \
    --extra-flag=--build-context=cacerts=/tmp/container2wasm-spike/ca \
    --build-arg SOURCE_REPO=https://github.com/container2wasm/container2wasm \
    alpine:3.20 /tmp/container2wasm-spike/alpine.wasm
```

| Metric | wizer (default) | non-wizer (`OPTIMIZATION_MODE=native`) |
|---|---|---|
| First (cold) build | **1651 s / 27.5 min** | — |
| Incremental rebuild (warm cache) | 330 s | **158 s** |
| Artifact size | **104.3 MiB** | 42.2 MiB |
| Boot → interactive shell echoing a marker | **4.8 s** | 23.9 s |
| Peak host RSS | 349 MB | 206 MB |

Verified interactively: a real `/ #` busybox shell, `runc` creating a real container, cgroup2 and
overlayfs mounted, kernel boot to init in ~4.3 s of guest time.

**Step 1: PASS.** A real Linux container really does run in WASM in under 5 seconds. The cold
build cost (27.5 min) is a one-time toolchain cost; warm rebuilds are 2.5–5.5 min.

---

## 3. Step 2 — the actual Kubernetes target

### 3.1 Why not real k3s: the shipped kernel forecloses it

Before spending emulation time, I inspected the guest kernel config container2wasm ships for the
Bochs/amd64 path (`config/bochs/linux_x86_config`):

| Kubernetes prerequisite | Status |
|---|---|
| `CONFIG_NETFILTER` | ❌ **not set** |
| `CONFIG_NF_TABLES` / `CONFIG_IP_NF_IPTABLES` | ❌ absent |
| `CONFIG_BRIDGE` | ❌ **not set** |
| `CONFIG_VETH` | ❌ **not set** |
| `CONFIG_VXLAN` | ❌ **not set** |
| `CONFIG_IPV6` | ❌ **not set** |
| `CONFIG_TUN` | ❌ **not set** |
| `CONFIG_SMP` | ❌ **not set** (uniprocessor only) |
| `CONFIG_CPUSETS` | ❌ absent |
| `CONFIG_SYSVIPC` | ❌ **not set** |
| `CONFIG_CGROUPS`, `MEMCG`, `CGROUP_PIDS/DEVICE/FREEZER` | ✅ set |
| `CONFIG_OVERLAY_FS`, `NAMESPACES`, `USER_NS`, `SECCOMP`, `EXT4_FS` | ✅ set |

Without netfilter there is no `kube-proxy` and no Service VIPs. Without bridge/veth there is no CNI
and no pod networking. Without VXLAN there is no flannel backend. This is not a
"k3s is heavy" problem — **k3s is architecturally blocked** on the kernel container2wasm ships.
Changing it means forking the kernel config and owning that fork.

So I pivoted, as the brief permits, to the smaller **KWOK-like target: `kube-apiserver` + `etcd`
only**, no kubelet, no container runtime, no CNI — which needs none of the missing features.

Also relevant: the guest VM defaults to **`ARG VM_MEMORY_SIZE_MB=128`**, far too small for an API
server. I raised it to 1024 via `--build-arg VM_MEMORY_SIZE_MB=1024`.

### 3.2 The image, and its native baseline

A single Alpine-based image containing statically-linked `kube-apiserver` v1.32.0, `kubectl`
v1.32.0, and `etcd` v3.5.17, all talking over **loopback inside the guest** — so no host
networking, no `c2w-net`, nothing outside the WASM sandbox. This matches the Zettacard model,
where the learner's `kubectl` runs in the same browser terminal as the cluster.

Certs and service-account keys are pre-generated **at image build time**, not at runtime, to avoid
spending emulated CPU on key generation.

Native baseline (plain `docker run`, same image, same script):

| Metric | Value |
|---|---|
| Time to first `kubectl` response (RSA-2048) | **5.2 s** |
| Time to first `kubectl` response (ECDSA P-256) | **2.2 s** |
| `kube-apiserver` RSS | **197 MB** |
| `etcd` RSS | **36 MB** |
| Whole-container memory | **162.6 MiB** |

Full native output, confirming a genuinely functional control plane:

```
Client Version: v1.32.0
Server Version: v1.32.0
--- kubectl get nodes ---   No resources found
--- kubectl get ns ---
NAME              STATUS   AGE
default           Active   3s
kube-node-lease   Active   3s
kube-public       Active   3s
kube-system       Active   3s
--- kubectl create deployment (dry-run=server) ---
deployment.apps/demo
```

One config note worth recording: Kubernetes **silently disables anonymous auth when
`--authorization-mode=AlwaysAllow`**, so `kubectl` gets a 401 and prompts `Please enter Username:`.
Fixed by using `--authorization-mode=RBAC` with a static token file mapping to `system:masters`.

### 3.3 Attempt 1 — RSA-2048: FAILED

Build: `k8s.wasm`, **207.0 MiB**, 239 s (warm cache), non-wizer + `--debug-image`, 1 GB guest.

The guest booted fine and both services started:

```
[spike] guest-start uptime=10.70s
[spike] starting etcd...
[spike] starting kube-apiserver...
[spike] polling apiserver /healthz ...
```

Then it ran for **21.5 minutes of wall clock / 1183 s of guest uptime** and never became ready.
**Zero** successful `kubectl` responses. The failure was completely consistent — 23 occurrences of
exactly one error:

```
E0823 11:36:54 reflector.go:166] "Unhandled Error" err="Failed to watch *v1.Lease:
  failed to list *v1.Lease: Get \"https://127.0.0.1:6443/apis/coordination.k8s.io/v1/
  namespaces/kube-system/leases?...\": net/http: TLS handshake timeout"
```

**The API server could not complete a TLS handshake with itself inside 10 seconds** — the timeout
hard-coded in Kubernetes' client-go transport. Nothing was broken; RSA-2048 under Bochs-in-WASM is
simply too slow. Memory was never the constraint: the guest held steady at **856 MB free of
1024 MB** (~170 MB used) the entire time.

### 3.4 Attempt 2 — ECDSA P-256: SUCCEEDED

ECDSA P-256 handshakes are roughly an order of magnitude cheaper than RSA-2048. I regenerated all
certs and SA keys as ECDSA, pinned
`--tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256`, and rebuilt with the **fast default
config** (wizer, no debug logging) to be fair to the tool.

Build: `k8s-ec.wasm`, **283.8 MiB**, 327 s.

**Result: a real `kubectl` response from a real `kube-apiserver` running entirely in WASM —
followed immediately by the API server dying.**

I ran this twice. Run 1 stopped at the success marker; run 2 continued to capture the full
evidence.

| Metric | Run 1 | Run 2 |
|---|---|---|
| **Wall clock → first `kubectl` response** | **650.2 s (10.8 min)** | **~423 s guest / 569.0 s wall to completion** |
| Guest uptime at first success | 579.0 s | 423.5 s |
| **Peak host RSS** | **1,130 MB** | **936 MB** |
| WASM artifact size | 283.8 MiB | 283.8 MiB |
| Native equivalent | 2.2 s / 162.6 MiB | — |
| **Slowdown vs native** | **~125–295×** | — |

Guest boot itself is fast — 10.7 s to userspace. Essentially all the remaining time is `etcd` +
`kube-apiserver` initialisation and TLS under emulation. Each `kubectl` invocation alone costs
~30 s of guest time (a 57 MB Go binary starting under an interpreting emulator).

**The full captured evidence from run 2 — this is the honest result:**

```
[spike] SUCCESS first-kubectl-response guest-uptime=423.46s (start was 10.73s)
Client Version: v1.32.0
Kustomize Version: v5.5.0
Server Version: v1.32.0                     <-- REAL response from the in-WASM API server
[spike] --- kubectl get nodes ---
Get "https://127.0.0.1:6443/api/v1/nodes?limit=500": dial tcp 127.0.0.1:6443:
  connect: connection refused - error from a previous attempt: unexpected EOF
[spike] --- kubectl get ns ---
The connection to the server 127.0.0.1:6443 was refused - did you specify the right host or port?
[spike] --- kubectl create deployment (dry-run=server) ---
error: failed to create deployment: Post ".../deployments?dryRun=All": connect: connection refused
[spike] --- guest meminfo ---
MemTotal:        1017068 kB
MemFree:          693008 kB
```

So: `kubectl version` — the lightest, earliest-available endpoint — returned a genuine
`Server Version: v1.32.0`. Then the API server was gone. **Every operation that touches actual
Kubernetes resources failed.**

The last API server output captured before it died shows it was still mid-startup, loading API
groups:

```
I0823 12:27:53 cacher.go:463] cacher (serviceaccounts): initialized
I0823 12:27:53 apis.go:119] Enabling API group "".
I0823 12:28:24 handler.go:286] Adding GroupVersion apiregistration.k8s.io v1 to ResourceManager
```

**Most likely cause: the guest OOM-killed it.** `MemFree` jumped to 693 MB *after* the process
died, and the API server's memory peaks during exactly this API-group-registration phase. This is a
**hypothesis, not a confirmed fact** — the non-debug build runs with `LINUX_LOGLEVEL=0`, which
suppresses the kernel's OOM-kill message, so there is no direct evidence in the log. If correct, it
means 1 GB of guest RAM is *not* enough, and the memory picture is worse than the mid-run
"~170 MB used" sample suggested — that sample was taken while the server was still early in
startup.

---

## 4. Scorecard against the pre-agreed criteria

| Light | Criteria | Met? |
|---|---|---|
| 🟢 Green | k3s or equivalent boots in a few minutes, <1–2 GB, real kubectl responses | ❌ — not k3s; 10.8 min is not "a few minutes" |
| 🟡 **Yellow** | Something boots and responds but is too slow/heavy for a browser tab, **or only the smaller etcd+apiserver target works, not real k3s** | ✅ **both clauses matched exactly** |
| 🔴 Red | Nothing beyond hello-world works, or apiserver never responds | ❌ — it did respond |

**Landed on 🟡 YELLOW — but a weak one, sitting right on the Yellow/Red boundary.** Both yellow
conditions are satisfied literally: only the reduced apiserver+etcd target works, and it is far too
slow for a browser tab. It is not Red by the agreed definition, because the API server *did* boot
and *did* return a real response within the attempt budget.

Three honest caveats that all push toward Red:

1. **With the default RSA certs any normal person would use, this is Red** — the control plane
   never becomes ready at all. It is only Yellow because I applied a non-obvious crypto workaround.
2. **Only the trivial `/version` endpoint ever answered.** `get nodes`, `get ns`, and a dry-run
   create all failed. If the bar is "a learner can actually do something," nothing here clears it.
3. **The API server did not stay up.** Whatever the cause, an unstable control plane is not a lab.

Memory (0.94–1.13 GB) sits inside the "1–2 GB" gut-check band, and may in fact have been the thing
that killed the process. **Time is what fails most clearly, and stability fails right behind it.**

---

## 5. Where the time and memory actually go

- **Memory: probably not the main wall, but not clearly safe either.** Mid-run samples showed the
  guest using only ~170–245 MB of its 1 GB, which looks comfortable. But the API server died during
  its memory-hungriest startup phase, and `MemFree` jumped by ~300 MB when it did — so a
  startup-peak OOM at 1 GB is a live possibility (unproven; `LINUX_LOGLEVEL=0` hid the evidence).
  The 0.94–1.13 GB host RSS is dominated by the WASM linear memory holding the emulated guest's RAM
  plus wasmtime's JIT output for a 283 MiB module. Raising the guest above ~1.5–2 GB to be safe
  would push the browser memory ceiling (§7) from "plausible" to "unrealistic".
- **Emulated CPU throughput is the wall.** Bochs is an interpreting x86 emulator; the bochsrc
  claims `cpu: ips=40000000` (40 MIPS) against a modern core's billions. Everything
  crypto-heavy or Go-runtime-heavy pays that tax.
- **Kubernetes has hard-coded timeouts that assume real hardware.** The 10 s
  `TLSHandshakeTimeout` is the specific thing that turned "slow" into "never ready". Other such
  timeouts exist throughout the control plane and would surface next.
- Uniprocessor only (`CONFIG_SMP` unset) — no parallelism to recover any of it.

---

## 6. Artifacts and timings summary

| Artifact | Config | Size | Build time |
|---|---|---|---|
| `alpine.wasm` | wizer, default | 104.3 MiB | 1651 s (cold, full toolchain) |
| `alpine-native.wasm` | non-wizer | 42.2 MiB | 158 s (warm) |
| `alpine-dbg.wasm` | non-wizer + debug | 42.5 MiB | 373 s (warm) |
| `k8s.wasm` | non-wizer + debug, RSA, 1 GB | 207.0 MiB | 239 s (warm) |
| `k8s-fast.wasm` | wizer, RSA, 1 GB | 283.8 MiB | 330 s (warm) |
| `k8s-ec.wasm` | wizer, **ECDSA**, 1 GB | 283.8 MiB | 327 s (warm) |

For Zettacard's PWA the relevant number is **283.8 MiB of WASM that a learner must download**,
before any of Zettacard's own assets. That alone is disqualifying for an offline-first mobile PWA
even if performance were acceptable.

---

## 7. ⚠️ Scope limitation: this was WASI/wasmtime, NOT a browser tab

**This must not be over-read.** Everything above ran server-side under **wasmtime (WASI)**, not
inside a browser's WASM engine (V8/SpiderMonkey). Setting up a headless-browser WASM harness was
deliberately out of scope for a one-day spike.

`c2w` distinguishes two build targets: the **WASI** target (default, what I tested) and an
**emscripten/browser** target (`--to-js`). The project does document running the *WASI* artifact in
a browser via `browser_wasi_shim` + `xterm-pty`, so the same `.wasm` is nominally browser-runnable.

**A positive WASI result is necessary-but-not-sufficient evidence for "works in a browser tab."**
Specifically, the browser would be **worse, not better**:

1. **Speed.** wasmtime's Cranelift JIT is generally faster than browser WASM for this workload, and
   the browser path adds **Asyncify** overhead (the Dockerfile compiles with `-sASYNCIFY=1`), which
   imposes a large additional slowdown on exactly this kind of emulator inner loop. 650 s under
   wasmtime should be read as a **lower bound** for the browser.
2. **Memory ceiling.** wasm32 has a hard 4 GB address space; my run reserved ~4.06 GB virtual and
   used 1.13 GB resident. Browsers cap WASM memory well below the theoretical maximum, and mobile
   Safari/Chrome far below that. Tellingly, container2wasm's own emscripten builds hard-code
   `-sTOTAL_MEMORY=2300MB` / `3000MB` — the project is already fighting this ceiling.
3. **Primitives.** Browsers have no WASI filesystem/socket primitives; they are shimmed in JS.
   *This one is actually favourable here* — my design used only guest-internal loopback, so no host
   networking was needed.
4. **Tab lifecycle.** A 10-minute foreground boot with a 283 MiB download, on a tab the OS may
   suspend or reclaim, is not a viable UX.

**Conclusion on the gap:** a browser run would very likely be slower than 650 s and closer to the
memory ceiling. The spike's negative performance conclusion therefore **strengthens** in a browser;
it does not need re-testing to be trusted for a go/no-go decision.

---

## 8. Licensing check

container2wasm's converter is **Apache 2.0**. The **generated image** bundles third-party software.
Per the README, and confirmed against the stages my build actually executed, an **amd64/Bochs WASI
image** contains:

| Component | License | Copyleft? |
|---|---|---|
| **Bochs** (patched, `ktock/Bochs`) | **LGPL v2.1** | ✅ weak copyleft |
| **GRUB** | **GPL v3** | ✅ strong copyleft |
| **Linux kernel** | **GPL v2** | ✅ strong copyleft |
| **BusyBox** | **GPL v2** | ✅ strong copyleft |
| tini | MIT | — |
| runc | Apache 2.0 | — |
| binfmt | MIT | — |
| *(riscv64/QEMU paths only)* TinyEMU (MIT), BBL, QEMU, vmtouch | mixed | — |
| Browser extras | xterm-pty (MIT), `browser_wasi_shim` (MIT/Apache-2.0), `gvisor-tap-vsock` (Apache-2.0) | — |
| **Plus my payload** | kube-apiserver / kubectl / etcd — all **Apache 2.0** | — |

**Is source-availability enough?** Broadly yes, but **it is not automatic — there are real
obligations Zettacard would have to actively satisfy:**

1. **Shipping the `.wasm` to a browser is distribution of a binary.** Serving it from the PWA
   triggers GPL/LGPL distribution obligations exactly as shipping a binary would. "It's just a web
   page" is not a defence.
2. **GPL v2 (Linux, BusyBox) + GPL v3 (GRUB) → corresponding-source obligation.** Zettacard must
   provide the complete corresponding source for those components at the exact versions built, or a
   valid written offer. In practice: publish the pinned build inputs (container2wasm's Dockerfile
   pins every version) and host a source mirror. Pointing at upstream URLs is a common practice but
   is **not** strictly compliant on its own for GPLv2 §3(a)/(b).
3. **GPL v3 (GRUB) adds Installation Information / anti-tivoization terms.** Low practical risk for
   a web-delivered artifact, but it is the strictest licence in the bundle and warrants a
   deliberate look rather than an assumption.
4. **LGPL v2.1 (Bochs) requires the ability to relink.** Everything here is statically linked into
   one WASM module, so the §6 relinking obligation is live — satisfied most simply by shipping the
   object/source needed to rebuild, which the GPL obligations already force.
5. **Notices.** All licence texts and copyright notices must be reproduced and shipped with, or
   clearly linked from, the artifact.

**Bottom line:** nothing here is a licence *blocker* — every component is open source and Zettacard
would not be modifying any of it. But it is **not free**: it means a source-mirror obligation, a
notices page, and a compliance process to keep them in sync with every rebuild. For a *rejected*
approach this is moot; if the approach were ever revived, budget real legal-review time. This is a
genuine cost that should count against the option, not a footnote.

---

## 9. Recommendation

**Drop this direction. Proceed with the already-recommended Killercoda-scenario approach.**

Reasons, in priority order:

1. **~9.5–11 minutes to first `kubectl` response, and that is the optimistic lower bound.** A
   browser tab would be slower. No CKA learner will wait 10 minutes for a lab to start, and
   Zettacard's value proposition is quick drilling.
2. **No actual Kubernetes operation ever succeeded.** Only `kubectl version` answered; `get nodes`,
   `get ns` and a dry-run create all got `connection refused` because the API server died seconds
   after coming up. Even setting speed aside, we do not have a working lab — we have a 10-minute
   boot that yields one version string.
3. **283.8 MiB WASM download** before any Zettacard content — incompatible with an offline-first
   PWA, especially on mobile.
4. **It only worked after a non-obvious crypto workaround.** With stock RSA certs the control plane
   never becomes ready. Kubernetes is full of hard-coded timeouts calibrated to real hardware;
   having hit one, we should expect to hit more, each needing bespoke work.
5. **Real k3s is off the table entirely** without forking and maintaining container2wasm's kernel
   config (no netfilter, bridge, veth, VXLAN, SMP). And the reduced apiserver-only target can never
   demonstrate the things CKA actually tests — pod scheduling, kube-proxy/Services, CNI,
   troubleshooting a kubelet. **This is the decisive point: even a fast, stable version of what I
   built would teach the wrong subset of CKA.**
6. **The toolchain is fragile.** The shipped v0.8.4 binary cannot build anything without a
   `SOURCE_REPO` override; the artifact dies silently without a TTY; the project self-describes as
   experimental. That is real ongoing maintenance risk for a core learning feature.
7. **Ongoing GPL/LGPL compliance overhead** (§8) for a feature that would still underperform.

### What is worth keeping from this spike

- The finding that **container2wasm genuinely works** — a real Linux container boots in WASM in
  **4.8 s** at **104 MiB**. If Zettacard ever wants an offline **Linux shell** lab (bash, grep,
  awk, sed, systemd-less filesystem drills, `Linux Essentials`-style content), this is a viable,
  genuinely-offline option worth revisiting. That is a real, positive, reusable result.
- The kernel-config table in §3.1 is the reusable artifact: it tells you in advance which
  container-based labs can and cannot work under container2wasm, without re-running any of this.

---

## Appendix: exact command sequence

```bash
# Toolchain
git clone https://github.com/container2wasm/container2wasm.git
curl -sSL -o c2w.tar.gz https://github.com/container2wasm/container2wasm/releases/download/v0.8.4/container2wasm-v0.8.4-linux-amd64.tar.gz
curl -sSL -o wasmtime.tar.xz https://github.com/bytecodealliance/wasmtime/releases/download/v33.0.2/wasmtime-v33.0.2-x86_64-linux.tar.xz
sudo dockerd &

# Patch the embedded Dockerfile to trust the sandbox CA (23 stages)
./c2w --show-dockerfile > Dockerfile.orig
python3 patch.py   # injects COPY --from=cacerts + SSL_CERT_FILE/GIT_SSL_CAINFO/... per stage

C2W_ARGS="--dockerfile Dockerfile.ca \
  --extra-flag=--build-context=cacerts=/tmp/container2wasm-spike/ca \
  --build-arg SOURCE_REPO=https://github.com/container2wasm/container2wasm"

# Step 1: basic demo
./c2w $C2W_ARGS alpine:3.20 alpine.wasm                       # 1651 s, 104.3 MiB
python3 harness.py alpine.wasm sh --send-on '/ #' \
  --send 'echo ALPINE_MARKER_OK; exit\n' --marker ALPINE_MARKER_OK
# -> 4.8 s to shell, peak RSS 349 MB

# Step 2: Kubernetes (kube-apiserver + etcd + kubectl, ECDSA certs)
docker build -f Dockerfile.ec -t k8s-mini:ec .
./c2w $C2W_ARGS --build-arg VM_MEMORY_SIZE_MB=1024 k8s-mini:ec k8s-ec.wasm   # 327 s, 283.8 MiB
python3 harness.py k8s-ec.wasm --timeout 2100 --marker 'spike\] (SUCCESS|TIMEOUT)'
# -> run 1: SUCCESS at 650.2 s wall, peak RSS 1130 MB
python3 harness.py k8s-ec.wasm --timeout 2100 --marker 'spike\] (DONE|TIMEOUT)'
# -> run 2: SUCCESS at 423 s guest, DONE at 569.0 s wall, peak RSS 936 MB
#    kubectl version OK; get nodes / get ns / dry-run create all "connection refused"
```

Full logs retained in `/tmp/container2wasm-spike/`: `build-*.log` (converter builds),
`k8s-ec-run2.log` (the definitive Kubernetes run), `native-k8s.log` / `native-ec.log`
(native baselines), `harness.py` (pty measurement harness).

Note: every WASM run must be under a **pty**; without one the module exits 1 silently.
