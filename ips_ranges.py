#!/usr/bin/env python

import json
import boomslang

max_values = []
h = open('../computed/stats.txt', 'r')
for l in h.xreadlines():
    r = json.loads(l)
    max_values.append(int(r['max']))

max_max = max(max_values)
num_records = len(max_values)
y_values = [float(sum([1 if x > sub_x else 0 for sub_x in max_values])) / num_records for x in range(max_max)]
max_y_value = float(max(y_values))

plot = boomslang.Plot()
line = boomslang.Line()

all_y_labels = ["%.1f" % (y/max_y_value) for y in y_values]

line.yLabels = []
line.xValues = range(max_max)
line.yValues = y_values
line.color = "red"

plot.add(line)
plot.title = "CDF of max network use by IP"
plot.xLabel = "Max observered bandwith in bytes/sec"
plot.yLabel = "% of observed IPs"
plot.save("../computed/cdf_max_network_use.png")
