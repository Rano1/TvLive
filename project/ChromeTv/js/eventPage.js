/**
 * Created by Will on 2017/6/12.
 */
chrome.runtime.onStartup.addListener(function () {
    console.log("zhanyutv started")
    onInit()
})

function onInit() {
    // 5 分钟查一次是否有新的账号
    // chrome.alarms.create("zhihuMessage", {when: Date.now(), periodInMinutes: 1});
}

function showDialog() {
    alert("showDialog");
}

function DownloadPage(url, callback) {
    var content = "";
    // 下载代码，可以跨域请求
    // .......
    callback(content);
};