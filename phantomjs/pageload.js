/**
 * 屏幕捕获,将网页保存为图片
 */
// var url = "http://baidu.com";
var url = "https://www.douyu.com/2206496";
var page = require('webpage').create();
//viewportSize being the actual size of the headless browser(viewportSize 是视区的大小，你可以理解为你打开了一个浏览器，然后把浏览器窗口拖到了多大。)
page.viewportSize = {width: 1024, height: 768}
//the clipRect is the portion of the page you are taking a screenshot of(clipRect 是裁切矩形的大小，需要四个参数，前两个是基准点，后两个参数是宽高。)
page.clipRect = {top: 0, left: 0, width: 1024, height: 768}
page.open(url, function (status) {
    console.log("Status: " + status);
    if (status === "success") {
        page.render('example.png');
    }
    phantom.exit();
});