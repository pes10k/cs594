#!/usr/bin/env python

from cs594.stats import Stats
import os
import sys
import json
import argparse
import boomslang

parser = argparse.ArgumentParser()
parser.add_argument('--input', default=False, help="path to read combined data From. defaults to stdio")
parser.add_argument('--output', required=True, help="path to write resulting graph to.")
args = parser.parse_args()


ip_contributions = {}
step = 0
total = 0
in_data = open(args.input, 'r') if args.input else sys.stdin

def backfill_ip_steps(record):
    last_recorded_step = record['step']
    steps_to_add = step - 1 - last_recorded_step
    added = steps_to_add
    while steps_to_add > 0:
        record['amounts'].append(0)
        steps_to_add -= 1
    return added


for a_line in in_data.xreadlines():
    r = json.loads(a_line)
    time = r['time']
    for e in r['sources']:
        ip = e['ip']
        amount = e['len']
        total += amount
        if ip not in ip_contributions:
            ip_contributions[ip] = {"amounts": [amount], "step": step}
        else:
            backfill_ip_steps(ip_contributions[ip])
            ip_contributions[ip]['step'] = step
            ip_contributions[ip]['amounts'].append(amount)
    step += 1

print total

stat_collections = [Stats(ip_contributions[ip]['amounts'], ip) for ip in ip_contributions]

out_h = open(args.output, 'w')
for s in stat_collections:
    out_h.write(s.toJSON() + "\n")
out_h.close()
