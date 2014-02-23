(function () {

    // Set up simple skelleton for expected "namespaces"
    window.cs594 = {
        data: {},
        repainted: false
    };

    var bytesToSize,
        relativeTime;

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

    relativeTime = function (secs) {

        var numDays,
            numHours,
            numMinutes,
            numSeconds,
            output = [];

        if (secs > 86400) {
            numDays = Math.floor(secs / 86400);
            secs -= (numDays * 86400);
            output.push(numDays + "days");
        }

        if (secs > 3600) {
            numHours = Math.floor(secs / 3600);
            secs -= (numHours * 3600);
            output.push(numHours + " hours");
        }

        if (secs > 60) {
            numMinutes = Math.floor(secs / 60);
            secs -= (numMinutes * 60);
            output.push(numMinutes + " minutes");
        }

        if (secs) {
            numSeconds = secs;
            secs -= numSeconds;
            output.push(numSeconds + " seconds");
        }

        return output.join(", ");
    };

    google.load('visualization', '1', {'packages': ['geochart']});
    google.setOnLoadCallback(function () {

        var totalBandwidthElm = document.getElementById('total-bandwidth'),
            numPointsElm = document.getElementById('num-points'),
            maxPointsInputElm = document.getElementById('max-points'),
            toggleButtonElm = document.getElementById('toggle-button'),
            $toggleButton = jQuery(toggleButtonElm),
            timeSelectorElm = document.getElementById('time-slider'),
            timeElm = document.getElementById("google-map-time"),
            mapElm = document.getElementById('google-sec-map'),
            bandwithElm = document.getElementById("google-map-bandwidth"),
            timeElapsedElm = document.getElementById('time-elapsed'),
            chart = new google.visualization.GeoChart(mapElm),
            data = window.cs594.data.minData,
            shape = data.shape,
            totals = data.totals,
            options = {
                displayMode: 'markers',
                // region: "US",
                colorAxis: {
                    colors: ['green', 'red'],
                    minValue: shape.min,
                    maxValue: shape.max,
                    markerOpacity: 0.5
                },
                sizeAxis: {
                    minSize: 2,
                    maxSize: 10,
                    minValue: 0,
                    maxValue: 1
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
                    rowIndexes,
                    aDate,
                    currentTotal,
                    runningTotal;

                if (toggleStop) {
                    toggleStop = false;
                    timerId = null;
                    updateToggleButton();
                    return;
                }

                window.cs594.repainted = false;
                currentTime += stepSize;

                currentTotal = totals[currentTime][0];
                runningTotal = totals[currentTime][1];

                timeSelectorElm.value = currentTime;
                timeElapsedElm.innerHTML = relativeTime(currentTime - shape.first);

                aDate = new Date(currentTime * 1000);
                timeElm.innerHTML = aDate.toLocaleString();
                rowIndexes = dataView.getFilteredRows([{column: 4, value: currentTime}]);

                totalBandwidthElm.innerHTML = bytesToSize(runningTotal, 2);
                bandwithElm.innerHTML = bytesToSize(currentTotal, 2);

                numPointsElm.innerHTML = rowIndexes.length;
                if (maxPointsInputElm.value < rowIndexes.length) {
                    rowIndexes = rowIndexes.slice(0, maxPointsInputElm.value);
                }

                dataView.setRows(rowIndexes);
                dataView.setColumns([0, 1, 2, 3]);
                chart.draw(dataView, options);

                $("circle[r!=2]").each(function () {
                    var circleElm = this,
                        rElm = this.parentNode;
                    rElm.parentNode.appendChild(rElm.parentNode.removeChild(rElm));
                });

                window.cs594.repainted = true;

                if (currentTime < shape.last) {
                    timerId = setTimeout(progressView, 500);
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
