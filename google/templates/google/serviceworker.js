// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

const staticCacheName = "django-pwa-v" + new Date().getTime();
const filesToCache = [ 'map', 'offline'];
const self = this;
// Cache on install
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                console.log('Opened Cache');
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    const cacheWhitelist = [];
    cacheWhitelist.push(staticCacheName);
    event.waitUntil(
        caches.keys().then(cacheNames => Promise.all(
                cacheNames.map((cacheName) => {
                    if(!cacheWhitelist.includes(cacheName)){
                        return caches.delete(cacheName)
                    }
                })
        ))
    )
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(() => {
                return fetch(event.request)
                    .catch(() => caches.match('offline.html'))
            })
    )
});