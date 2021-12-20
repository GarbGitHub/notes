window.addEventListener('load', async() => {
    if ('serviceWorker' in navigator) {
        try {
            const reg = await navigator.serviceWorker.register(sworker)
            console.log('Service worker register success', reg)
        } catch (e) {
            console.log('Service worker register fail')
        }
    }
})

function sworker() {
    self.addEventListener('install', event => {
        console.log('[SW]: install')
    })

    self.addEventListener('activate', event => {
        console.log('[SW]: activate')
    })
}