const staticCacheName = 's-app-v3'
const dynamicCacheName = 'd-app-v3'


const assetUrls = [
    "/media/apple-touch-icon.png",
    "/media/favicon-32x32.png",
    "/media/android-chrome-192x192.png",
    "/media/favicon-16x16.png",
    "/media/safari-pinned-tab.svg",
    "/media/browserconfig.xml",
    "/static/notes/css/forms-style.css",
    "/static/accounts/css/sing.css",
    "/static/accounts/images/bg-cover.jpg",
    "/static/accounts/images/logo-f.svg",
    "/media/undraw_add_notes_re_ln36.svg",
    "/media/undraw_bookmarks_re_mq1u.svg",
    "/media/undraw_web_search_re_efla.svg",
    "/media/undraw_noted_pc-9-f.svg",
    "/media/undraw_personal_information_re_vw8a.svg",
    "/media/undraw_throw_away_re_x60k.svg",
    "/media/undraw_notes_re_pxhw.svg"
]

self.addEventListener('install', async event => {
    const cache = await caches.open(staticCacheName)
    await cache.addAll(assetUrls)
})

self.addEventListener('activate', async event => {
    const cacheNames = await caches.keys()
    await Promise.all(
        cacheNames
        .filter(name => name !== staticCacheName)
        .filter(name => name !== dynamicCacheName)
        .map(name => caches.delete(name))
    )
})

self.addEventListener('fetch', event => {
    const { request } = event

    const url = new URL(request.url)
    if (url.origin === location.origin) {
        event.respondWith(cacheFirst(request))
    } else {
        event.respondWith(networkFirst(request))
    }
})


async function cacheFirst(request) {
    const cached = await caches.match(request)
    return cached ?? await fetch(request)
}

async function networkFirst(request) {
    const cache = await caches.open(dynamicCacheName)
    try {
        const response = await fetch(request)
        await cache.put(request, response.clone())
        return response
    } catch (e) {
        const cached = await cache.match(request)
        return cached ?? await caches.match('/offline/')
    }
}