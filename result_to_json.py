#!/usr/bin/env python
#
#Convert intermediate results into google-chart-able-json-data

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True, help="Path to write Google friendly json to.")
parser.add_argument('--input', required=True, help="Path to read intermediate json from.")
parser.add_argument('--bin', default="minute", help="The unit of time bin to look for in data")
parser.add_argument('--name', default="window.map", help="Global property to store resulting table in.")
args = parser.parse_args()

out_h = open(args.output, 'w')
boiler_plate = args.name + " = {};\n"
boiler_plate += args.name + ".type = '" + args.bin + "';\n";
boiler_plate += args.name + """.table = {
    cols: [{id: 'lat', label: 'Latitude', type: 'number'},
           {id: 'long', label: 'Longitude', type: 'number'},
           {id: 'bits', label: 'Bits', type: 'number'},
           {id: 'size', label: 'Size', type: 'number'},
           {id: 'ip', label: 'IP Address', type: 'string'},
           {id: 'time', label: 'Time Bin', type: 'number'}],
    rows: ["""
boiler_plate_end = "]};"
out_h.write(boiler_plate)

min_bin, max_bin = None, None
min_value, max_value = None, None

with open(args.input, 'r') as in_h:
    for a_line in in_h.xreadlines():
        record = json.loads(a_line)
        time = record[args.bin]
        for source, amount in record['sources'].items():
            if min_bin is None or time < min_bin:
                min_bin = time
            if max_bin is None or time > max_bin:
                max_bin = time
            if min_value is None or amount < min_value:
                min_value = amount
            if max_bin is None or amount > max_value:
                max_value = amount
in_h.close()

with open(args.input, 'r') as in_h:
    for a_line in in_h.xreadlines():
        record = json.loads(a_line)
        time = record[args.bin]
        for source_ip, values in record['sources'].items():
            if not values['lat']:
                continue
            lat = values['lat']
            lon = values['lon']
            color = amount
            size = float(amount) / max_value
            lat, lon = [float(v) for v in source.split(",")]
            row_string = "{c: [" + ",".join(["{v: '" + str(f) + "'}" for f in [lat, lon, color, size, source_ip, time]]) + "]},\n"
            out_h.write(row_string)

out_h.write(boiler_plate_end)
out_h.write("\n")
out_h.write(args.name + ".shape = {first: " + str(min_bin) + ", last: " + str(max_bin) + ", min: " + str(min_value) + ", max: " + str(max_value) + "};\n")
