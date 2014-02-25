#!/usr/bin/env python
import sys
import json
import argparse
import boomslang
import datetime
import cs594.data

parser = argparse.ArgumentParser()
parser.add_argument('--input', default=False, help="path to read combined data From. defaults to stdio")
parser.add_argument('--ip', required=True)
args = parser.parse_args()

in_data = open(args.input, 'r') if args.input else sys.stdin
for a_line in in_data.xreadlines():
    record = json.loads(a_line)
    sources = record['sources']
    for s in sources:
        if s['ip'] == args.ip:
            print s['len']
            break
