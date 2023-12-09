function load_css(path) {
    let ele = document.createElement('link');
    ele.type = 'text/css';
    ele.href = path;
    ele.rel = 'stylesheet';
    document.head.appendChild(ele);
    return ele;
}

function load_js(path) {
    let ele = document.createElement('script');
    ele.src = path;
    document.head.appendChild(ele);
    return ele;
}

load_css('css/cirrus.min.css');
load_css('css/default.css');
load_css('css/sweetalert.css');

let swal_js = load_js("js/sweetalert-dev.js");

let _url = new URL(window.location.href).origin.toString();
console.log("Base Url: ", _url);

let loadingClassList = ['animated', 'loading', 'loading-right'];

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i ++) {
        let c = ca[i].trim();
        if (c.indexOf(name) === 0) return c.substring(name.length, c.length);
    }
    return "";
}

function handleFetch(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject('something went wrong');
    }
}

function check_room_id(room_id) {
    if (!room_id || room_id.length !== 4) return false;
    let url = new URL(`${_url}/api/check_room_id`);
    fetch(url.toString(), {method: 'get'}).then(handleFetch)
        .then(data => {
            // console.log(data);
            if (data['success'] === false) {
                swal('Invalid Room ID', 'Please Try to Connect Again!', 'error');
                setTimeout(function () {
                    window.location.href = new URL(`${_url}/join`).toString();
                }, 5000);
            }
        });
}

function check_session() {
    fetch(new URL(`${_url}/api/check_session`)).then(handleFetch)
        .then(data => {
            // console.log(data);
            if (data['success'] === false) {
                swal('Invalid Session', 'Please Try to Connect Again!', 'error');
                setTimeout(function () {
                    window.location.href = _url;
                }, 5000);
            }
        });
}

// main
function mainloop() {
    check_session();
    check_room_id();

    setTimeout(
        mainloop,
        2000
    );
}

swal_js.onload = (e) => {
    try {
        if (root !== true) {
            mainloop();
        }
    } catch (e) {
        mainloop();
    }
}
