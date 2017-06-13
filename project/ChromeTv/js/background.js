console.log("Starting background")


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