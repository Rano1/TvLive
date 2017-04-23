/**
 * 获取网页源码，标题
 */
var url = "http://www.baidu.com";
var page = require('webpage').create();
page.onConsoleMessage = function (msg) {
    console.log(msg);
};
page.open(url, function (status) {
    var title = page.evaluate(function () {
        return document.title;
    });
    console.log('Page title is ' + title);
    page.evaluate(function () {
        console.log(document.title);
    });
    phantom.exit();
});
