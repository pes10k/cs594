#!/usr/bin/env python

import sys
import json
import boomslang

records = []
h = open('../computed/stats.txt', 'r')
for l in h.xreadlines():
    r = json.loads(l)
    records.append((r['avg'], r['min'], r['max']))

plot = boomslang.Plot()
line = boomslang.Line()
sorted_records = sorted(records, key=lambda x: x[0])

line.xValues = range(len(sorted_records))
line.yValues = [x[0] for x in sorted_records]
line.yMins = [x[1] for x in sorted_records]
line.yMaxes = [x[2] for x in sorted_records]

line.label = "Asymmetric Errors"
line.color = "red"

plot.add(line)
plot.xLabel = "X Label"
plot.yLabel = "Y Label"
plot.hasLegend()
plot.save("errorbars.png")
