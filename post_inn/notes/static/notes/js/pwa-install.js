// PWA Install

// Button install PWA
const buttonInstall = document.getElementById('btnPwaInstall');

let deferredPrompt;
pwaInstall()

function pwaInstall() {
    if (!localStorage.getItem('pwa')) {
        if (buttonInstall != null) {
            visibleBtnInstallPwa();
        }
    }
    window.addEventListener('beforeinstallprompt', (e) => {
        console.log('beforeinstallprompt Event fired');
        deferredPrompt = e;
        localStorage.removeItem('pwa');
        return false;
    });

    buttonInstall.addEventListener('click', function() {
        if (deferredPrompt !== undefined) {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then(function(choiceResult) {
                console.log(choiceResult.outcome);
                if (choiceResult.outcome == 'dismissed') {
                    console.log('User cancelled home screen install');
                } else {
                    localStorage.setItem('pwa', 'install');
                    hideBtnInstallPwa();
                    console.log('User added to home screen');
                }
                deferredPrompt = null;
            });
        }
    });
}

function visibleBtnInstallPwa() {
    buttonInstall.classList.remove('d-none');
    buttonInstall.classList.add('d-block');
}

function hideBtnInstallPwa() {
    buttonInstall.classList.remove('d-block');
    buttonInstall.classList.add('d-none');
}