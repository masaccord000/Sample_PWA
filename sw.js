const CACHE_NAME = "stlite-cache-v1";
const urlsToCache = [
  "/index.html",
  "/main.py",
  "/Home.py",
  "/ResizeImages.py",
  "/About.py",
  "/manifest.json",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
  "/assets/stlite.js",
  "https://cdn.jsdelivr.net/npm/@stlite/mountable@0.75.0/build/stlite.css"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(key => {
        if (key !== CACHE_NAME) return caches.delete(key);
      }))
    )
  );
  return self.clients.claim();
});

self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});





