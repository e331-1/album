const CACHE_NAME="cache v0"
self.addEventListener('install', (event) => {
    console.log('インストール');
});
caches.open(CACHE_NAME).then((cache) => {
    return cache.addAll([
        '/index.html',
        '/index.css',
        '/index.js',
        '/lang.json',
        "/app.webmanifest",
        "/icon/192x192.png",
        "/icon/512x512.png",
        "/icon/icon.svg"
    ]);
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.match(event.request).then((response) => {
                return response || fetch(event.request).then((response) => {
                    return response;
                });
            });
        })
    );
});
