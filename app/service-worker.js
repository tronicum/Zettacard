// drivenow — minimal offline-first service worker (Sprint 1)
// Precaches the app shell so it works after the first load with no network.
//
// DN-39: content is no longer one flat data.json - it's split by module and
// locale under data/<exam_type>/{core.json,locales/<lang>.json}, generated
// by data/build_modules.py. Only the small top-level manifest is precached
// here; the fetch handler below already runtime-caches everything else it
// successfully fetches (module/locale files, sign SVGs), so whichever
// module+locale a visitor actually picks gets cached on first use without
// this list needing to enumerate every module/locale/class combination.
const CACHE_NAME = "drivenow-v4";
const ASSETS = [
  "./",
  "index.html",
  "styles.css",
  "app.js",
  "data/modules.json",
  "manifest.json",
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
