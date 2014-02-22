(function () {

    // Set up simple skelleton for expected "namespaces"
    window.cs594 = {
        data: {},
    };

    var bytesToSize;

    bytesToSize = function (bytes, precision) {
        var kilobyte = 1024;
        var megabyte = kilobyte * 1024;
        var gigabyte = megabyte * 1024;
        var terabyte = gigabyte * 1024;

        if ((bytes >= 0) && (bytes < kilobyte)) {
            return bytes + ' B';

        } else if ((bytes >= kilobyte) && (bytes < megabyte)) {
            return (bytes / kilobyte).toFixed(precision) + ' KB';

        } else if ((bytes >= megabyte) && (bytes < gigabyte)) {
            return (bytes / megabyte).toFixed(precision) + ' MB';

        } else if ((bytes >= gigabyte) && (bytes < terabyte)) {
            return (bytes / gigabyte).toFixed(precision) + ' GB';

        } else if (bytes >= terabyte) {
            return (bytes / terabyte).toFixed(precision) + ' TB';

        } else {
            return bytes + ' B';
        }
    };

    google.load('visualization', '1', {'packages': ['geochart']});
    google.setOnLoadCallback(function () {

        var toggleButtonElm = document.getElementById('toggle-button'),
            $toggleButton = jQuery(toggleButtonElm),
            timeSelectorElm = document.getElementById('time-slider'),
            timeElm = document.getElementById("google-map-time"),
            mapElm = document.getElementById('google-sec-map'),
            bandwithElm = document.getElementById("google-map-bandwidth"),
            chart = new google.visualization.GeoChart(mapElm),
            data = window.cs594.data.minData,
            shape = data.shape,
            options = {
                displayMode: 'markers',
                // region: "US",
                colorAxis: {
                    colors: ['green', 'red'],
                    minValue: shape.min,
                    maxValue: shape.max
                }
            },
            timerId = null,
            stepSize = (data.type === "sec") ? 1 : 60,
            dataTable = new google.visualization.DataTable(data.table),
            currentTime = shape.first - stepSize,
            toggleStop = false,
            updateToggleButton = function () {
                if (timeSelectorElm.max == timeSelectorElm.value) {
                    toggleButtonElm.innerHTML = "Restart!";
                    $toggleButton.removeClass("btn-primary");
                    $toggleButton.removeClass("btn-warning");
                    $toggleButton.addClass("btn-success");
                } else if (timerId) {
                    $toggleButton.removeClass("btn-primary");
                    $toggleButton.addClass("btn-warning");
                    $toggleButton.removeClass("btn-success");
                    toggleButtonElm.innerHTML = "Stop";
                } else {
                    $toggleButton.addClass("btn-primary");
                    $toggleButton.removeClass("btn-warning");
                    $toggleButton.removeClass("btn-success");
                    toggleButtonElm.innerHTML = "Start";
                }
            },
            progressView = function () {

                var dataView = new google.visualization.DataView(dataTable),
                    totalBits = 0,
                    aDate;

                if (toggleStop) {
                    toggleStop = false;
                    timerId = null;
                    updateToggleButton();
                    return;
                }

                currentTime += stepSize;
                timeSelectorElm.value = currentTime;

                aDate = new Date(currentTime * 1000);
                timeElm.innerHTML = aDate.toLocaleString();
                rowIndexes = dataView.getFilteredRows([{column: 5, value: currentTime}]);

                rowIndexes.forEach(function (val, index) {
                    totalBits += parseInt(dataView.getValue(val, 2), 10);
                });

                bandwithElm.innerHTML = bytesToSize(totalBits, 1);

                dataView.setRows(rowIndexes);
                dataView.setColumns([0, 1, 2]);
                chart.draw(dataView, options);

                if (currentTime < shape.last) {
                    timerId = setTimeout(progressView, 1000);
                } else {
                    timerId = null;
                    updateToggleButton();
                }
            };

        timeSelectorElm.min = shape.first;
        timeSelectorElm.max = shape.last;
        timeSelectorElm.step = stepSize;

        progressView();

        timeSelectorElm.addEventListener("change", function (e) {
            currentTime = parseInt(timeSelectorElm.value, 10);
            if (timerId === null) {
                progressView();
            }
        }, false);

        toggleButtonElm.addEventListener("click", function (e) {
            if ($toggleButton.hasClass("btn-primary")) {
                progressView();
            } else if ($toggleButton.hasClass("btn-warning")) {
                toggleStop = true;
            } else {
                currentTime = shape.first - stepSize;
                timeSelectorElm.value = 0;
                progressView();
            }
            updateToggleButton();
        }, false);
    });
}());
