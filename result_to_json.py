#!/usr/bin/env python
#
#Convert intermediate results into google-chart-able-json-data

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True, help="Path to write Google friendly json to.")
parser.add_argument('--input', required=True, help="Path to read intermediate json from.")
parser.add_argument('--name', default="window.map", help="Global property to store resulting table in.")
parser.add_argument('--group', default='city', help="Sets how to group similarly located data.  Can be be 'city', 'region', 'country', or 'ip'.")
args = parser.parse_args()

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

ip_mapping = {}
def bin_for_record(r):
    if args.group == "ip":
        key = r['ip']
    elif args.group == "city":
        key = "-".join([r['city'] or '', r['region'] or '', r['country'] or ''])
    elif args.group == "region":
        key = "-".join([r['region'] or '', r['country'] or ''])
    elif args.group == "country":
        key = r['country'] or ''

    if key in ip_mapping:
        ip_mapping[key]['len'] += int(r['len'])
    else:
        ip_mapping[key] = {
            'len': r['len'],
            'lat': r['lat'],
            'lon': r['lon']
        }

time_bin = None
min_bin, max_bin = None, None
min_value, max_value = None, None

with open(args.input, 'r') as in_h:
    for a_line in in_h.xreadlines():
        record = json.loads(a_line)
        if not time_bin:
           time_bin = record['type']
        time = record['time']

        ip_mapping = {}

        for r in record['sources']:
            if not r['lat']:
                continue
            bin_for_record(r)

        for bin, values in ip_mapping.items():
            amount = int(values['len'])
            if min_bin is None or time < min_bin:
                min_bin = time
            if max_bin is None or time > max_bin:
                max_bin = time
            if min_value is None or amount < min_value:
                min_value = amount
            if max_value is None or amount > max_value:
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
        ip_mapping = {}
        record = json.loads(a_line)
        time = record['time']

        for r in record['sources']:
            if not r['lat']:
                continue
            bin_for_record(r)

        for bin, values in ip_mapping.items():
            lat = values['lat']
            lon = values['lon']
            amount = values['len']
            size = min(float(amount) / max_value, .1)
            params = {
                "lat": lat,
                "lon": lon,
                "bits": amount,
                "size": size,
                "time": time,
                "format": sizeof_fmt(amount)
            }
            row_string = "{{c: [{{v: {lat}}}, {{v: {lon}}}, {{v: {bits}, f: '{format}'}}, {{v: {size}}}, {{v: {time}}}]}},\n".format(**params)
            out_h.write(row_string)

out_h.write(boiler_plate_end)
out_h.write("\n")
out_h.write(args.name + ".shape = {first: " + str(min_bin) + ", last: " + str(max_bin) + ", min: " + str(min_value) + ", max: " + str(max_value) + "};\n")
