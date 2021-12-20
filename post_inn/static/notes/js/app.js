if ('serviceWorker' in navigator) {
    navigator.serviceWorker
        .register('sw.js', { scope: '/' })
        .then(function(reg) {
            console.log('Achieng Service worker Registration worked!');
        })
        .catch(function(error) {
            console.log(error);
        });

}