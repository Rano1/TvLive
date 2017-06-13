console.log("Starting background")


chrome.runtime.onLaunched.addListener(function () {
    chrome.app.window.create('index.html', {
        id: 'wechat_web',
        width: 1000,
        height: 700,
        maxWidth: 1000,
        maxHeight: 1000,
        minWidth: 700,
        minHeight: 700
    });
});

chrome.runtime.onConnect.addListener(function () {

})

function getCookiesAll(port, message) {
    chrome.tabs.get(message.tabId, function (tab) {
        var url = tab.url;
        console.log("Looking for cookies on: " + url);
        chrome.cookies.getAll({
            url: url
        }, function (cks) {
            console.log("I have " + cks.length + " cookies");
            port.postMessage({
                action: "getall",
                url: url,
                cks: cks
            });
        });
    });
}