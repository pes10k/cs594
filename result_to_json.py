#!/usr/bin/env python
#
#Convert intermediate results into google-chart-able-json-data

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True, help="Path to write Google friendly json to.")
parser.add_argument('--input', required=True, help="Path to read intermediate json from.")
parser.add_argument('--name', default="window.map", help="Global property to store resulting table in.")
args = parser.parse_args()

time_bin = None
min_bin, max_bin = None, None
min_value, max_value = None, None

with open(args.input, 'r') as in_h:
    for a_line in in_h.xreadlines():
        record = json.loads(a_line)
        if not time_bin:
           time_bin = record['type']
        time = record['time']
        for s in record['sources']:
            amount = s['len']
            if min_bin is None or time < min_bin:
                min_bin = time
            if max_bin is None or time > max_bin:
                max_bin = time
            if min_value is None or amount < min_value:
                min_value = amount
            if max_bin is None or amount > max_value:
                max_value = amount
in_h.close()

out_h = open(args.output, 'w')
boiler_plate = args.name + " = {};\n"
boiler_plate += args.name + ".type = '" + time_bin + "';\n";
boiler_plate += args.name + """.table = {
    cols: [{id: 'lat', label: 'Latitude', type: 'number'},
           {id: 'long', label: 'Longitude', type: 'number'},
           {id: 'bits', label: 'Bits', type: 'number'},
           {id: 'size', label: 'Size', type: 'number'},
           {id: 'time', label: 'Time Bin', type: 'number'}],
    rows: ["""
boiler_plate_end = "]};"
out_h.write(boiler_plate)

with open(args.input, 'r') as in_h:
    for a_line in in_h.xreadlines():
        record = json.loads(a_line)
        time = record['time']
        for source in record['sources']:
            if not source['lat']:
                continue
            ip = source['ip']
            lat = source['lat']
            lon = source['lon']
            amount = source['len']
            size = float(amount) / max_value
            params = {
                "lat": lat,
                "lon": lon,
                "bits": amount,
                "ip": ip,
                "size": size,
                "time": time
            }
            row_string = "{{c: [{{v: {lat}, f: '{ip}'}}, {{v: {lon}}}, {{v: {bits}}}, {{v: {size}}}, {{v: {time}}}]}},\n".format(**params)
            out_h.write(row_string)

out_h.write(boiler_plate_end)
out_h.write("\n")
out_h.write(args.name + ".shape = {first: " + str(min_bin) + ", last: " + str(max_bin) + ", min: " + str(min_value) + ", max: " + str(max_value) + "};\n")
