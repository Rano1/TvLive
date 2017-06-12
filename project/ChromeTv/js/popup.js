/**
 * Created by Will on 2017/6/12.
 */
// document.write('<script src="https://unpkg.com/axios/dist/axios.min.js"></script>');
$(document).ready(getNotice)

$("#douyu").bind("click", function () {
    var createProperties = new Object();
    // createProperties.url = "https://passport.douyu.com";
    // chrome.tabs.create(createProperties);
    // document.getElementsByName("username")[0].value = "hacker_ma@163.com";
    // document.getElementsByName("password")[0].value = "123456";
    // chrome.tabs.executeScript(null, {
    // }, function(){
    //     alert("xx")
    //     chrome.tabs.executeScript(null, {
    //         file:"js/douyu_script.js"
    //     });
    // });
    // get_cookies();
    // update_account_ui();
    // _showDataOnPage("11");
    set_account();
})

function set_account() {
    var code = 'document.getElementsByName("username")[0].value = "hacker_ma@163.com"'
    // chrome.tabs.executeScript(null,{code:code})
    chrome.tabs.executeScript(null, {file: "js/douyu_script.js"});
}

function getNotice() {
    // get_user_account();
}

//获取用户账号密码
// function get_user_account() {
//     var ajaxURL = "http://10.200.1.203:8009/game/config?ccode=86&os=1&uid=10142&ver=7"
//     $.get(ajaxURL, function (result) {
//         var result_data = JSON.parse(result);
//         if (result_data.code == 0) {
//             alert("success")
//             // document.getElementsByName("username")[0].value = "hacker_ma@163.com";
//             // document.getElementsByName("password")[0].value = "123456";
//         } else {
//             alert("success")
//         }
//     });
// }

//获取用户的账号密码
function get_user_account() {
    var ajaxURL = "http://10.200.1.203:8009/game/config?ccode=86&os=1&uid=10142&ver=7"
    // $.ajax({
    //     type:'GET',
    //     url:ajaxURL,
    //     async:false
    // }).success(function (data) {
    //    
    // });
    $.get(ajaxURL, function (result) {
        var result_data = JSON.parse(result);
        if (result_data.code == 0) {
            alert("success")
            // document.getElementsByName("username")[0].value = "hacker_ma@163.com";
            // document.getElementsByName("password")[0].value = "123456";
        } else {
            alert("success")
        }
    });
}

//上传用户的cookies
function upload_user_cookies() {
    $.ajax({
        type: 'POST',
        url: ajaxURL,
        data: '',
        async: false
    }).success(function (data) {
        console.log(data);
    });
}


function update_account_ui() {
    var bgPage = chrome.extension.getBackgroundPage();
    // bgPage.showDialog();
    // bgPage.someFunc();
    bgPage.DownloadPage("", function (content) {

    });
}
//将data数据以桌面通知的方式显示给用户
function _showDataOnPage(data) {

    //显示一个桌面通知
    if (window.webkitNotifications) {
        var notification = window.webkitNotifications.createNotification(
            'images/icon.png',  // icon url - can be relative
            '通知的title!',  // notification title
            data  // notification body text
        );
        notification.show();
        // 设置3秒后，将桌面通知dismiss
        setTimeout(function () {
            notification.cancel();
        }, 3000);

    } else if (chrome.notifications) {
        var opt = {
            type: 'basic',
            title: '通知的title!',
            message: data,
            iconUrl: 'img/icon.png',
        }
        chrome.notifications.create('', opt, function (id) {
            setTimeout(function () {
                chrome.notifications.clear(id, function () {
                });
            }, 3000);
        });

    } else {
        alert('亲，你的浏览器不支持啊！');
    }

}

var cookieList = new Array();
function get_cookies() {
    // console.log(document.cookie)

    var filteredCookies = [];
    var filterURL = {}
    filterURL.url = "https://passport.douyu.com/";
    filterURL.domain = "passport.douyu.com";

    var cookies = chrome.cookies.getAll(filterURL, function (cks) {
        var currentC;
        for (var i = 0; i < cks.length; i++) {
            currentC = cks[i];

            if (filters.name != undefined && currentC.name.toLowerCase().indexOf(filters.name.toLowerCase()) == -1)
                continue;
            if (filters.domain != undefined && currentC.domain.toLowerCase().indexOf(filters.domain.toLowerCase()) == -1)
                continue;
            if (filters.secure != undefined && currentC.secure.toLowerCase().indexOf(filters.secure.toLowerCase()) == -1)
                continue;
            if (filters.session != undefined && currentC.session.toLowerCase().indexOf(filters.session.toLowerCase()) == -1)
                continue;

            for (var x = 0; x < data.readOnly.length; x++) {
                try {
                    var lock = data.readOnly[x];
                    if (lock.name == currentC.name && lock.domain == currentC.domain) {
                        currentC.isProtected = true;
                        break;
                    }
                } catch (e) {
                    console.error(e.message);
                    delete data.readOnly[x];
                }
            }
            filteredCookies.push(currentC);
        }
        cookieList = filteredCookies;

        if (cookieList.length == 0) {
            swithLayout();
            setEvents();
            setLoaderVisible(false);
            return;
        }

        cookieList.sort(function (a, b) {
            if (preferences.sortCookiesType == "domain_alpha") {
                var compDomain = a.domain.toLowerCase().localeCompare(b.domain.toLowerCase());
                if (compDomain)
                    return compDomain;
            }
            return a.name.toLowerCase().localeCompare(b.name.toLowerCase())
        });
        console.log(cookieList)
    });
}
