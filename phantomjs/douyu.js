/**
 * 测试网页JS渲染速度,网络监听
 */
var page = require('webpage').create(),
    system = require('system'),
    t, address;

if (system.args.length === 1) {
    console.log('Usage: loadspeed.js <some URL>');
    phantom.exit();
}

//接收到资源请求监听
page.onResourceRequested = function (request) {
    // console.log('Request' + JSON.stringify(request, undefined, 4));
};
//接收资源接受完毕监听
page.onResourceReceived = function (response) {
    // console.log('Receive ' + JSON.stringify(response, undefined, 4));
};

t = Date.now();
address = system.args[1];
page.open(address, function (status) {
    if (status !== 'success') {
        console.log('FAIL to load the address');
    } else {
        t = Date.now() - t;
        console.log('Loading ' + system.args[1]);
        console.log('Loading time ' + t + ' msec');
    }
    phantom.exit();
});