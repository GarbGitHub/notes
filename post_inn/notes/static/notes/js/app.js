// serviceWorker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
        .register('/sw.js', { scope: '/' })
        .then(function(reg) {
            console.log('Achieng Service worker Registration worked!');
        })
        .catch(function(error) {
            console.log(error);
        });
}

// Cookies
defineThemeFromCookies()
defineSizeFromCookies()
tagClassChange()
setFontSizeForRange()

function defineThemeFromCookies() {
    let html = document.getElementsByTagName('HTML')[0];
    let theme = get_cookie("theme");
    if (theme) {
        html.classList.add(theme);
        radioButtonChecked(theme);
    } else {
        radioButtonChecked("light");
        html.classList.add("light");
    }
}

function defineSizeFromCookies() {
    let lead = document.getElementsByClassName('lead');
    let userFontSize = document.getElementById('sizeRange');
    let cookFs = get_cookie("cookieFs");
    // If there are cookies, set the styles
    if (cookFs) {
        userFontSize.value = cookFs;
        for (let i = 0; i < lead.length; ++i)
            lead[i].style.fontSize = '1.' + cookFs + 'rem';
    }
}

function tagClassChange() {
    document.querySelector('.themes').addEventListener('change', (event) => {
        if (event.target.nodeName === 'INPUT') {
            document.documentElement.classList.remove('dark', 'light');
            let theme = event.target.value;
            document.documentElement.classList.add(theme);
            let output = document.getElementById("sizeValue");
            output.classList.remove('dark', 'light');
            output.classList.add(theme);
            create_cookie("theme", theme);
            radioButtonChecked(theme);
        }
    });
    document.querySelector('.slidecontainer').addEventListener('change', (event) => {

        // If the user chooses the font size
        if (event.target.nodeName === 'INPUT') {
            let lead = document.getElementsByClassName('lead');
            let inputText = document.getElementById("id_text");
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

function radioButtonChecked(theme) {
    let r1 = document.getElementById("RadioLight");
    let r2 = document.getElementById("RadioDark");
    if (theme === 'light') {
        if (r2.checked) {
            r2.removeAttribute("checked");
        }
        r1.setAttribute("checked", "checked");
    } else {
        if (r1.checked) {
            r1.removeAttribute("checked");
        }
        r2.setAttribute("checked", "checked");
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
    console.log("Будем создавать", cookieName, ": ", cookieValue);

    // If there is a "cookieName" cookie
    if (get_cookie(cookieName)) {
        // Removing old cookies
        deletion_cookie(cookieName);
    } else {
        console.log("Нет cookie");
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
    let cookie_date = new Date(); // Текущая дата и время
    cookie_date.setTime(cookie_date.getTime() - 1); // Срок хранения куки на 1 сек меньше текущего времени
    document.cookie = cookie_name += "=; expires=" + cookie_date.toGMTString();
    console.log("cookie", "удалены");
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
    let slider = document.getElementById("sizeRange");
    let output = document.getElementById("sizeValue");
    let inputText = document.getElementById("id_text");
    let lead = document.getElementsByClassName('lead');

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