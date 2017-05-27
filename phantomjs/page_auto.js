/**
 * 页面自动化处理
 */
var url = "http://www.httpuseragent.org";
// var url = "https://www.douyu.com/2206496";
var page = require('webpage').create();
console.log('The default user agent is ' + page.settings.userAgent);
page.settings.userAgent = 'SpecicalAgent';
page.open(url, function (status) {
    if (status !== 'success') {
        console.log('Unable to access netword');
    } else {
        var ua = page.evaluate(function () {
            return document.getElementById('qua').textContent;
        });
        console.log("Your Http User Agent string is: " + ua);
    }
    phantom.exit();
});