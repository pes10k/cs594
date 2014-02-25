#!/usr/bin/env python

import pprint
import sys
from cs594.data import size_format
import os
import json
import argparse
import boomslang

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=False, help="Read um data.")
parser.add_argument('--output', required=True, help="Path to write output to.")
parser.add_argument('--secs', default=10, help="Dividing line betwen initial and later data sets")
args = parser.parse_args()

initial_ips = {}
all_ips = {}
initial_set_totals = []
all_totals = []

in_data = open(args.input, 'r') if args.input else sys.stdin
steps = 0
for a_line in in_data.xreadlines():
    r = json.loads(a_line)
    time = r['time']
    all_total = 0
    initial_set_total = 0;
    for s in r['sources']:
        ip = s['ip']
        if steps < args.secs:
            initial_ips[ip] = True
        if ip not in all_ips:
            all_ips[ip] = True
        if ip in initial_ips:
            initial_set_total += s['len']
        all_total += s['len']
    steps += 1
    initial_set_totals.append(initial_set_total)
    all_totals.append(all_total)

num_all_ips = len(all_ips)
all_totals_avged = [float(t) / num_all_ips for t in all_totals]

num_initial_ips = len(initial_ips)
initial_totals_avged = [float(t) / num_initial_ips for t in initial_set_totals]

combined = [(all_totals_avged[i], initial_totals_avged[i]) for i in range(len(all_totals))]

plot = boomslang.Plot()
all_line = boomslang.Line()
all_line.yValues = all_totals_avged
all_line.xValues = range(len(all_line.yValues))
all_line.color = "red"
all_line.label = "Average traffic of all IPs ({0} IPs)".format(num_all_ips)

initial_line = boomslang.Line()
initial_line.yValues = initial_totals_avged
initial_line.xValues = all_line.xValues
initial_line.color = "blue"
initial_line.label = "Average traffic of seed IPs ({0} IPs)".format(num_initial_ips)


max_y_value = max([x for x in initial_totals_avged + all_totals_avged])
step = float(max_y_value) / 10
y_points = [x * step for x in range(11)]
y_labels = ["{0}/sec".format(size_format(y)) for y in y_points]
for a_line in (all_line, initial_line):
    a_line.yTickLabelPoints = y_points
    a_line.yTickLabels = y_labels
    plot.add(a_line)

plot.xLabel = "Seconds elapsed"
plot.yLabel = "Average network use (in bytes)"
plot.title = "Comparison of bots appearing early versus all bots"
plot.hasLegend()
plot.setDimensions(width=12)


plot.save(os.path.join(args.output, "early_vs_general_contribution.png"))
