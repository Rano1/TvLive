/**
 * 使用附加库，在1.6版本之后允许添加外部的JS库，比如下面的例子添加了jQuery，然后执行了jQuery代码。
 */
var url = "http://family.yizhibo.com/account/login/init";
var jquery = "http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js";
var page = require('webpage').create();
page.open(url, function () {
    page.includeJs(jquery, function () {
        page.evaluate(function () {
            $("go").click();
        });
    });
    phantom.exit();
});

