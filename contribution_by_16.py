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
ips_in_16_blocks = {}

for key in record:
    ip_by_16 = ".".join(key.split(".")[0:2])
    if ip_by_16 not in ips_in_16_blocks:
        ips_in_16_blocks[ip_by_16] = 0
    ips_in_16_blocks[ip_by_16] += record[key]

ips_sorted = sorted(ips_in_16_blocks, key=ips_in_16_blocks.__getitem__, reverse=True)

values = ips_in_16_blocks.values()
values.sort(reverse=True)

line = boomslang.Line()
line.xValues = range(len(values))
line.yValues = values

plot = boomslang.Plot()
plot.xLabel = "IP Addresses in order of decreasing contribution by /16"
plot.yLabel = "Attack Contribution"

step = float(values[0]) / 10
y_labels = [x * step for x in range(11)]
line.yTickLabelPoints = y_labels
line.yTickLabels = [cs594.data.size_format(v) for v in y_labels]

line.xTickLabelPoints = [x for x in range(0, len(values), 100)]
line.xTickLabels = [ips_sorted[x] for x in line.xTickLabelPoints]


line.xTickLabelProperties = {
    'rotation': 45
}

plot.title = "Contribution to attack by /16 IP"
plot.add(line)
plot.setDimensions(width=12)
plot.save(os.path.join(args.output, "ips_by_16_contribution.png"))
