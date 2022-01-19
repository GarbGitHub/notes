//This is the service worker with the Advanced caching

importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

const HTML_CACHE = "html";
const JS_CACHE = "javascript";
const STYLE_CACHE = "stylesheets";
const IMAGE_CACHE = "images";
const FONT_CACHE = "fonts";

addEventListener('install', installEvent => {
    installEvent.waitUntil(
        caches.open('Johnny')
        .then(JohnnyCache => {
            JohnnyCache.addAll([
                '/offline.html'
            ]); // конец addAll
        }) // конец open.then
    ); // конец waitUntil
}); // конец addEventListener

// Всегда, когда файл запрашивается
addEventListener('fetch', fetchEvent => {
    const request = fetchEvent.request;
    fetchEvent.respondWith(
        // Сначала попытка запросить его из Сети
        fetch(request)
        .then(responseFromFetch => {
            return responseFromFetch;
        }) // конец fetch.then
        // Если не сработало, то...
        .catch(fetchError => {
            // пытаемся найти в кеше
            caches.match(request)
                .then(responseFromCache => {
                    if (responseFromCache) {
                        return responseFromCache;
                        // если не сработало и...
                    } else {
                        // это запрос к веб-странице, то...
                        if (request.headers.get('Accept').includes('text/html')) {
                            // покажите вашу офлайн-страницу
                            return caches.match('/offline.html');
                        } // 1конец if
                    } // конец if/else
                }) // конец match.then
        }) // конец fetch.catch
    ); // конец respondWith
}); // конец addEventListener

self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
  });

workbox.routing.registerRoute(
  ({event}) => event.request.destination === 'document',
  new workbox.strategies.NetworkFirst({
    cacheName: HTML_CACHE,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 10,
      }),
    ],
  })
);

workbox.routing.registerRoute(
  ({event}) => event.request.destination === 'script',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: JS_CACHE,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 15,
      }),
    ],
  })
);

workbox.routing.registerRoute(
  ({event}) => event.request.destination === 'style',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: STYLE_CACHE,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 15,
      }),
    ],
  })
);

workbox.routing.registerRoute(
  ({event}) => event.request.destination === 'image',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: IMAGE_CACHE,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 15,
      }),
    ],
  })
);

workbox.routing.registerRoute(
  ({event}) => event.request.destination === 'font',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: FONT_CACHE,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 15,
      }),
    ],
  })
);
