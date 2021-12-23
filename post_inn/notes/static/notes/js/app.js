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

defineThemeFromCookies()
tagClassChange()

function defineThemeFromCookies() {
    let html = document.getElementsByTagName('HTML')[0]
    console.log(html)
    let theme = get_cookie("theme")
    if (theme) {
        html.classList.add(theme);
        radioButtonChecked(theme)
    } else {
        radioButtonChecked("light")
        html.classList.add("light");
    }
}

function tagClassChange() {
    document.querySelector('.themes').addEventListener('change', (event) => {
        if (event.target.nodeName === 'INPUT') {
            document.documentElement.classList.remove('dark', 'light');
            let theme = event.target.value
            document.documentElement.classList.add(theme);
            create_cookie(theme)
            radioButtonChecked(theme)
        }
    });
}

function radioButtonChecked(theme) {
    let r1 = document.getElementById("RadioLight")
    let r2 = document.getElementById("RadioDark")
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

// console.log('Установленные куки', get_cookie("theme"))

// Function to get the cookie value
function get_cookie(cookie_name) {
    let results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');
    if (results)
        return (unescape(results[2]));
    else
        return null;
}

function create_cookie(theme) {
    console.log("Будем создавать", theme)

    // If there is a "theme" cookie
    if (get_cookie("theme")) {
        console.log("Есть старые cookie", get_cookie("theme"))
            // Removing old cookies
        deletion_cookie("theme");
    }
    // Overwriting the cookie
    console.log("Нет cookie")
    let current_date = new Date;
    let cookie_year = current_date.getFullYear() + 1;
    let cookie_month = current_date.getMonth();
    let cookie_day = current_date.getDate();
    console.log(cookie_year, cookie_month, cookie_day)
    set_cookie("theme", theme, cookie_year, cookie_month, cookie_day, "/");
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
    console.log("cookie созданы", document.cookie);
}

// Deletion cookies
function deletion_cookie(cookie_name) {
    let cookie_date = new Date(); // Текущая дата и время
    cookie_date.setTime(cookie_date.getTime() - 1); // Срок хранения куки на 1 сек меньше текущего времени
    document.cookie = cookie_name += "=; expires=" + cookie_date.toGMTString();
    console.log("cookie удалены", get_cookie("theme"));
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