#!/usr/bin/env python
import cs594.data
import os
import sys
import json
import argparse
import boomslang

parser = argparse.ArgumentParser()
parser.add_argument('--input', default=False, help="path to read combined data From. defaults to stdio")
parser.add_argument('--output', required=True, help="path to write resulting graph to.")
args = parser.parse_args()

in_data = open(args.input, 'r') if args.input else sys.stdin

record = json.load(in_data)
values = record.values()
values.sort(reverse=True)


line = boomslang.Line()
line.xValues = range(len(values))
line.yValues = values

plot = boomslang.Plot()
plot.xLabel = "IP Addresses in order of decreasing contribution"
plot.yLabel = "Attack Contribution"

step = float(values[0]) / 10
y_labels = [x * step for x in range(11)]
line.yTickLabelPoints = y_labels
line.yTickLabels = [cs594.data.size_format(v) for v in y_labels]

plot.title = "Contribution to attack by IP"
plot.add(line)
plot.setDimensions(width=12)
plot.save(os.path.join(args.output, "ips_by_contribution.png"))
