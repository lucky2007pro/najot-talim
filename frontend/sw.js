const CACHE_NAME = 'space-edu-v8';
const ASSETS = [
    './',
    './index.html',
    './explorer.html',
    './style.css',
    './app.js',
    './assets/sun.png',
    './assets/earth.png',
    './assets/mars.png',
    './assets/astronaut.png',
    './assets/trophy.png',
    './assets/space_bg.png',
    'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap'
];

self.addEventListener('install', event => {
    self.skipWaiting(); // Immediately activate new SW
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', event => {
    // Only cache GET requests
    if (event.request.method !== 'GET') return;
    
    // For API requests, let them go to network. We handle API offline in app.js
    if (event.request.url.includes('/api/')) {
        return;
    }

    // Network-first strategy: try network, fallback to cache
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Cache the fresh response
                const responseClone = response.clone();
                caches.open(CACHE_NAME).then(cache => {
                    cache.put(event.request, responseClone);
                });
                return response;
            })
            .catch(() => {
                return caches.match(event.request);
            })
    );
});

self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
