var page = require('webpage').create(),
    system = require('system'),
    fname;

page.viewportSize = {
    width: 1024,
    height: 768
};

page.open("http://localhost:8080/", function () {

    var takeImage,
        lastTime,
        identicalCount = 0;

    takeImage = function () {

        var currentTime = page.evaluate(function () {
                return document.getElementById("google-map-time").innerHTML;
            });

        if (currentTime !== lastTime) {
            identicalCount = 0;
            page.render(currentTime + ".png");
        } else {
            identicalCount += 1;
            if (identicalCount === 600) {
                phantom.exit();
            }
        }

        window.setTimeout(takeImage, 100);
    };

    takeImage();
});
