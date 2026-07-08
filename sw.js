/* 1xCasino PWA service worker (repo root -> scope '/'). Minimal: satisfies install eligibility,
   keeps the landing fresh online (network-first navigations), caches shell + assets as fallback. */
var V = "1xc-pwa-v1";
var SHELL = ["/"];

self.addEventListener("install", function (e) {
  self.skipWaiting();
  e.waitUntil(caches.open(V).then(function (c) { return c.addAll(SHELL).catch(function () {}); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== V; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;

  // Navigations: network-first (fresh landing online), cached shell only when offline.
  if (req.mode === "navigate") {
    e.respondWith(
      fetch(req).then(function (r) {
        var cp = r.clone();
        caches.open(V).then(function (c) { c.put("/", cp); });
        return r;
      }).catch(function () { return caches.match("/"); })
    );
    return;
  }

  // Static assets: cache-first with background fill.
  e.respondWith(
    caches.match(req).then(function (cached) {
      return cached || fetch(req).then(function (r) {
        if (r && r.ok && req.url.indexOf("/assets/") !== -1) {
          var cp = r.clone();
          caches.open(V).then(function (c) { c.put(req, cp); });
        }
        return r;
      }).catch(function () { return cached; });
    })
  );
});
