/**
 * Created by Will on 2017/6/12.
 */
// document.write('<script src="https://unpkg.com/axios/dist/axios.min.js"></script>');
$(document).ready(getNotice)

$("#douyu_tab").bind("click", function () {
    // var createProperties = new Object();
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
    // _showDataOnPage("你有新的认证任务");
    // get_user_account();
    // showToast();
    getCookiesAll();
});


$("#btn-refresh").bind("click", function () {
    get_user_account();
});

function set_account(account, password) {
    var username_code = 'document.getElementsByName("username")[0].value = "' + account + '"'
    var password_code = 'document.getElementsByName("password")[0].value = "' + password + '"'
    chrome.tabs.executeScript(null, {code: username_code})
    chrome.tabs.executeScript(null, {code: password_code})
    document.getElementsByName("username")[0].value = "hacker_ma@163.com";
    // chrome.tabs.executeScript(null, {file: "js/douyu_script.js"});
}

function getNotice() {
    // get_user_account();
}

function getCookiesAll() {
    var url = "https://www.douyu.com";
    console.log("Looking for cookies on: " + url);
    var cookiesStr = "";
    chrome.cookies.getAll({
        url: url
    }, function (cookieL) {
        console.log("I have " + cookieL.length + " cookies");
        for (var x = 0; x < cookieL.length; x++) {
            var cCookie = cookieL[x];
            cookiesStr = cookiesStr + cCookie['name'] + "=" + cCookie['value'] + ";"
            console.log(cCookie);
            // if(filterMatchesCookie(filterURL,cCookie.name,cCookie.domain,cCookie.value)){
            //     var cUrl = (cCookie.secure)?"https://":"http://"+cCookie.domain+cCookie.path;
            //     deleteCookie(cUrl,cCookie.name,cCookie.storeId,cCookie)
            // }
        }
        console.log(cookiesStr);
        document.getElementById("cookieContent").value = cookiesStr;
        // port.postMessage({
        //     action : "getall",
        //     url : url,
        //     cks : cks
        // });
    });
}

function createCookiesList() {
    // var cookie = $(".cookie_details_template").clone().removeClass("cookie_details_template");
}
// function getCookiesAll() {
//     var url = "https://passport.douyu.com/";
//     console.log("Looking for cookies on: " + url);
//     chrome.cookies.getAll({
//         url : url
//     }, function(cks) {
//         console.log("I have " + cks.length + " cookies");
//         port.postMessage({
//             action : "getall",
//             url : url,
//             cks : cks
//         });
//     });
// }

function showToast(showText) {
    document.getElementById('toast').innerHTML = showText;
    $("#toast").fadeIn(function () {
        setTimeout(function () {
            $("#toast").fadeOut();
        }, 2500);

    });
    $(this).animate({backgroundColor: "#B3FFBD"}, 300, function () {
        $(this).animate({backgroundColor: "#EDEDED"}, 500);
    });
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
            showToast("获取成功");
            set_account("hacker_ma@163.com", "123456");
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
//将data数据以桌面通知的方式显示给用户（用于通知用户有新的任务进来了）
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