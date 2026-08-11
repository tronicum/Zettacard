// Zettacard — minimal offline-first service worker (Sprint 1)
// Precaches the app shell so it works after the first load with no network.
//
// DN-39: content is no longer one flat data.json - it's split by module and
// locale under data/<exam_type>/{core.json,locales/<lang>.json}, generated
// by data/build_modules.py. Only the small top-level manifest is precached
// here; the fetch handler below already runtime-caches everything else it
// successfully fetches (module/locale files, sign SVGs), so whichever
// module+locale a visitor actually picks gets cached on first use without
// this list needing to enumerate every module/locale/class combination.
//
// User-reported bug (2026-08-05): "I can reselect LKW but not get back to
// the Datenschutz stuff" after already having the app open before. Root
// cause found by investigation: this file itself had never changed since
// the very first commit (CACHE_NAME had been "drivenow-v4" through every
// deploy since, including DN-42/43/45 and the DN-44 Datenschutz/
// Arbeitssicherheit/KI-Act/IT-Sicherheit rollout). Browsers only re-run a
// service worker's install/activate lifecycle when the SW *script's bytes*
// change - if service-worker.js is byte-identical to what a visitor's
// browser already has registered, nothing re-installs, no new cache is
// opened, and the visitor keeps being served whatever ASSETS content
// (notably data/modules.json and app.js) their browser fetched and cached
// on their very first visit, forever - even though every subsequent fetch
// against this same cache name was previously cache-first with no
// expiry/refresh path. A visitor who first opened the app before DN-44
// shipped would have a permanently stale data/modules.json missing the 4
// new modules, with no way to ever see them short of manually clearing
// site data. Confirmed locally: seeding an old cached modules.json under
// this cache name and reloading (without clearing storage, i.e. exactly
// what a real returning visitor experiences) kept serving the stale
// 4-module list even though the server had the real 8-module one the whole
// time.
//
// Two-part fix:
//  1. CACHE_NAME bumped below - this alone changes the SW script's bytes,
//     forcing every existing visitor's browser to notice the update, run
//     install/activate again, and drop the old (possibly stale-forever)
//     cache. This unblocks everyone stuck on pre-DN-44 content right now.
//  2. The fetch handler no longer serves the app shell (ASSETS below)
//     cache-first unconditionally - that was the actual structural gap:
//     it required a human to remember to bump CACHE_NAME on every deploy
//     that changes shell/data content, and four+ real deploys since launch
//     (DN-42 index.html/styles.css changes, DN-43, this DN-44 round) prove
//     that discipline doesn't hold up in practice. Shell/manifest requests
//     are now network-first with cache fallback (for true offline use), so
//     a visitor who's online always gets the current index.html/app.js/
//     modules.json regardless of whether anyone remembered to bump the
//     cache name - the manual version bump is now a defense-in-depth
//     backstop, not the only thing standing between visitors and stale
//     content. Runtime-cached module/locale/sign content (fetched via the
//     final else-branch below) is untouched - that content is genuinely
//     immutable per filename once published, so cache-first there is still
//     correct and keeps the app usable offline.
// v7: root index.html is now the marketing landing page (see AGENTS.md /
// BACKLOG.md rebrand entry) and the actual app moved to app.html. Both are
// precached: app.html for the obvious offline-app reason, and the landing
// page too since it's cheap (one small static file) and keeps this a fully
// installable-and-offline PWA even for the splash page a fresh visitor
// hits before ever opening the app. logo.svg is the new favicon/app-icon
// source and is small/static, so it's precached alongside the PNGs it was
// rendered from.
// v8 (DN-56): added vendor/qrcode.js (the certificate-embedded verify-link
// QR encoder, loaded via a <script> tag in app.html right before app.js) -
// a genuine new app-shell dependency, not just runtime-cached content, so
// it's precached here and the cache name is bumped per this file's own
// documented discipline (see the v7 comment above for why that discipline
// exists and what breaks without it).
const CACHE_NAME = "zettacard-v8";
const ASSETS = [
  "./",
  "index.html",
  "app.html",
  "styles.css",
  "app.js",
  "vendor/qrcode.js",
  "data/modules.json",
  "manifest.json",
  "icons/logo.svg",
  "icons/icon-192.png",
  "icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  const isShellAsset = ASSETS.some((a) => url.pathname.endsWith(a.replace(/^\.\//, "")) || (a === "./" && url.pathname.endsWith("/")));

  if (isShellAsset) {
    // Network-first for the app shell / manifest: always prefer whatever
    // the server has right now (so real deploys are visible immediately to
    // an already-open or returning tab without depending on CACHE_NAME
    // having been bumped), falling back to the cached copy only when
    // offline. See the top-of-file comment for why this replaced the old
    // unconditional cache-first behavior.
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          }
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).then((response) => {
        // Runtime-cache anything else we successfully fetch (in practice:
        // the sign/diagram SVGs under assets/, added incrementally as
        // content grows, without needing every filename hardcoded above).
        if (response && response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        }
        return response;
      });
    })
  );
});
