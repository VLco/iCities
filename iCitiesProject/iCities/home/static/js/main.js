let name = "id_cities";

window.onload = loadBth;

function loadBth() {
    let btnCompare = document.getElementsByName("btnCompare")[0];
    if (btnCompare !== undefined && getCookie(name) !== undefined) {
        if (getCookie(name).split(',').indexOf(btnCompare.value) !== -1) {
            btnCompare.innerText = 'Удалить из сравнения';
        }
        if (getCookie(name).split(',').length === 2) {
            toCom = document.getElementById("toCompare");
            toCom.style.display = 'block';
            i = getCookie(name).split(',');
            toCom.href = "../../city/" + i[0] + "vs" + i[1];
        } else {
            toCom = document.getElementById("toCompare");
            toCom.style.display = 'none';
        }
        console.log(btnCompare);
    }

}


function hideBlock(btn) {
    let block = document.getElementById(btn.value);
    if (block.style.display === 'none') {
        block.style.display = 'flex';
        btn.className += " text-secondary"
    } else {
        block.style.display = 'none';
        let style = [btn.className.split(" ").indexOf("text-secondary"), btn.className.split(" ")];
        style[1][style[0]] = "";
        console.log(style[1]);
        btn.className = style[1].join(" ");
        console.log(btn.className)

    }

}


function deleteCookieValue(btn) {
    val = getCookie(name).split(',');
    i = val.indexOf(btn.value) === 1 ? 0 : 1;
    deleteCookie(name);
    setCookie(name, val[i]);
    btn.innerText = 'Добавить к сравнению';
    loadBth()
}


function clickBth(btn) {
    if (getCookie(name) === undefined) {
        setCookie(name, btn.value);
        btn.innerText = 'Удалить из сравнения';
    } else if (getCookie(name).split(',').length < 2) {
        console.log(getCookie(name).split(','));
        if (getCookie(name).split(',').indexOf(btn.value) === -1) {
            setCookie(name, btn.value);
        } else {
            deleteCookie(name);
            btn.innerText = 'Добавить к сравнению';
        }
    } else {
        if (getCookie(name).split(',').indexOf(btn.value) !== -1) {
            deleteCookieValue(btn)
        } else {
            alert("Нельзя добавлять больше 2 городов для сравнения");

        }
        return;
    }
    loadBth();
    console.log(getCookie("id_cities"));
    console.log(document.cookie);

}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, aoptions = {}) {

    let options = {
        path: '/',
    };

    Object.assign(options, options, aoptions);

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }
    let updatedCookie = "";
    if (getCookie(name) !== undefined) {
        updatedCookie = encodeURIComponent(name) + "=" + getCookie(name) + "," + encodeURIComponent(value);
    } else {
        updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
    }

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
}

function deleteCookie(name) {
    setCookie(name, '', {'max-age': -1})
}