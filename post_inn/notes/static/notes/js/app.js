// Cookies
const html = document.getElementsByTagName('HTML')[0];
const lead = document.getElementsByClassName('lead');
const slider = document.getElementById("sizeRange");
const output = document.getElementById("sizeValue");
const inputText = document.getElementById("id_text");
const userFontSize = document.getElementById('sizeRange');

// Local datetime
const datetimeField = document.getElementById("id_created");

// Button install PWA
const buttonInstall = document.getElementById('btnPwaInstall');

// Functions
defineThemeFromCookies()
tagClassChange()
setFontSizeForRange()
ThemeTagClassChange()
addClassForImg()
pwaInstall()

if (datetimeField != null) {
    localDateTimeNow();
}

function addClassForImg() {
    if (lead) {
        for (let i = 0; i < lead.length; ++i) {
            let img = lead[i].getElementsByTagName("img");
            for (let i = 0; i < img.length; ++i) {
                img[i].classList.add("img-fluid");
            }
        }
    }
}

function defineThemeFromCookies() {
    let fontFamily = get_cookie("theme");
    let bgtheme = get_cookie("background");
    let cookFs = get_cookie("cookieFs");

    if (fontFamily) {
        html.classList.add(fontFamily);
        radioButtonChecked(fontFamily);
    } else {
        radioButtonChecked("light");
        html.classList.add("light");
    }
    if (bgtheme) {
        html.classList.add(bgtheme);
        checkButtonChecked(bgtheme);
    } else {
        checkButtonChecked("over");
        html.classList.add("over");
    }
    if (cookFs) {
        userFontSize.value = cookFs;
        for (let i = 0; i < lead.length; ++i)
            lead[i].style.fontSize = '1.' + cookFs + 'rem';
    }
}

function ThemeTagClassChange() {
    document.querySelector('.bgthemes').addEventListener('change', (event) => {
        if (event.target.nodeName === 'INPUT') {
            let background = event.target.value;
            html.classList.remove('bgcolor', 'over');
            html.classList.add(background);
            create_cookie("background", background);
            checkButtonChecked(background);
        }
    });
}

function tagClassChange() {
    document.querySelector('.themes').addEventListener('change', (event) => {
        if (event.target.nodeName === 'INPUT') {
            document.documentElement.classList.remove('dark', 'light');
            let theme = event.target.value;
            document.documentElement.classList.add(theme);
            output.classList.remove('dark', 'light');
            output.classList.add(theme);
            create_cookie("theme", theme);
            radioButtonChecked(theme);
        }
    });
    document.querySelector('.slidecontainer').addEventListener('change', (event) => {
        // If the user chooses the font size
        if (event.target.nodeName === 'INPUT') {
            let sizeValue = event.target.value;
            // Remove existing styles and install new ones
            if (inputText) {
                inputText.style.removeProperty('font-size');
                inputText.style.fontSize = '1.' + sizeValue + 'rem';
            }
            for (let i = 0; i < lead.length; ++i) {
                lead[i].style.removeProperty('font-size');
                lead[i].style.fontSize = "1." + sizeValue + 'rem';
            }
            create_cookie("cookieFs", sizeValue);
        }
    });
}

function checkButtonChecked(theme) {
    let inputBgColor = document.getElementById("backgroundColor");
    let inputBgImage = document.getElementById("backgroundImage");
    if (theme === 'over') {
        inputBgColor.removeAttribute("disabled");
        inputBgImage.setAttribute("disabled", "disabled");
    } else {
        inputBgImage.removeAttribute("disabled");
        inputBgColor.setAttribute("disabled", "disabled");
    }
}

function radioButtonChecked(theme) {
    let inpurLight = document.getElementById("RadioLight");
    let inputDark = document.getElementById("RadioDark");
    if (theme === 'light') {
        if (inputDark.checked) {
            inputDark.removeAttribute("checked");
        }
        inpurLight.setAttribute("checked", "checked");
    } else {
        if (inpurLight.checked) {
            inpurLight.removeAttribute("checked");
        }
        inputDark.setAttribute("checked", "checked");
    }
}

// Function to get the cookie value
function get_cookie(cookie_name) {
    let results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');
    if (results)
        return (unescape(results[2]));
    else
        return null;
}

function create_cookie(cookieName, cookieValue) {
    // If there is a "cookieName" cookie
    if (get_cookie(cookieName)) {
        // Removing old cookies
        deletion_cookie(cookieName);
    }
    let current_date = new Date;
    let cookie_year = current_date.getFullYear() + 1;
    let cookie_month = current_date.getMonth();
    let cookie_day = current_date.getDate();
    console.log(cookie_year, cookie_month, cookie_day);
    set_cookie(cookieName, cookieValue, cookie_year, cookie_month, cookie_day, "/");
}

// Function for setting cookies
function set_cookie(name, value, exp_y, exp_m, exp_d, path, domain, secure) {
    let cookie_string = name + "=" + escape(value);
    if (exp_y) {
        let expires = new Date(exp_y, exp_m, exp_d);
        cookie_string += "; expires=" + expires.toGMTString();
    }
    if (path)
        cookie_string += "; path=" + escape(path);
    if (domain)
        cookie_string += "; domain=" + escape(domain);
    if (secure)
        cookie_string += "; secure";
    document.cookie = cookie_string;
    console.log("All cookies:", document.cookie);
}

// Deletion cookies
function deletion_cookie(cookie_name) {
    let cookie_date = new Date(); // Current date and time
    cookie_date.setTime(cookie_date.getTime() - 1); // Cookie expiration is 1 second less than the current time
    document.cookie = cookie_name += "=; expires=" + cookie_date.toGMTString();
    console.log("deleted cookies");
}

// Activating an additional field in an encryption form
function definingKeyType() {
    let rad = document.getElementsByName('flexRadioDefault');
    let typeKey = document.getElementById("FormControlTypeKey");
    for (let i = 0; i < rad.length; i++) {
        if (rad[i].checked) {
            if (i === 0) {
                typeKey.removeAttribute("disabled");
                typeKey.setAttribute("disabled", "disabled");
                typeKey.value = "";
            } else {
                typeKey.removeAttribute("disabled");
                typeKey.value = "";
            }
        }
    }
}

function setFontSizeForRange() {
    output.style.fontSize = '1.' + slider.value + 'rem';
    if (inputText) {
        inputText.style.fontSize = '1.' + slider.value + 'rem';
    }
    slider.oninput = function() {
        if (inputText) {
            inputText.style.fontSize = '1.' + slider.value + 'rem';
        }
        output.style.fontSize = '1.' + slider.value + 'rem';
        updateStyleValue(lead, slider.value)
    }
}

function updateStyleValue(element, styleValue) {
    for (let i = 0; i < element.length; ++i) {
        element[i].style.removeProperty('font-size');
        element[i].style.fontSize = '1.' + styleValue + 'rem';
    }
}

// Local datetime
function localDateTimeNow() {
    let now = new Date();
    let utcString = now.toISOString().substring(0, 19);
    let year = now.getFullYear();
    let month = now.getMonth() + 1;
    let day = now.getDate();
    let hour = now.getHours();
    let minute = now.getMinutes();
    let localDatetime = year + "-" +
        (month < 10 ? "0" + month.toString() : month) + "-" +
        (day < 10 ? "0" + day.toString() : day) + "T" +
        (hour < 10 ? "0" + hour.toString() : hour) + ":" +
        (minute < 10 ? "0" + minute.toString() : minute);
    datetimeField.value = localDatetime;
    console.log(datetimeField.value);
}

// PWA Install
let deferredPrompt;

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

// Textarea size

// Textarea size
if (inputText != null) {
    $("#id_text").keyup(function(e) {
        autoheight(this);
    });

    function autoheight(a) {
        if (!$(a).prop('scrollTop')) {
            do {
                var b = $(a).prop('scrollHeight');
                var h = $(a).height();
                $(a).height(h - 5);
            }
            while (b && (b != $(a).prop('scrollHeight')));
        };
        $(a).height($(a).prop('scrollHeight') + 20);
    }

    autoheight($("#id_text"));
}