#!/usr/bin/env python

import json
import datetime

totals = []
h = open('../computed/stats.txt', 'r')
for l in h.xreadlines():
    r = json.loads(l)
    totals.append(r['sum'])
h.close()

min_time = None
max_time = 0
h = open("../computed/sec_combined.txt", 'r')
for l in h.xreadlines():
    r = json.loads(l)
    min_time = min(min_time, r['time']) if min_time else r['time']
    max_time = max(max_time, r['time']) if max_time else r['time']
h.close()

start_datetime = datetime.datetime.fromtimestamp(min_time)
end_datetime = datetime.datetime.fromtimestamp(max_time)

records = []
records.append(" * Total Attackers: {0}".format(len(totals)))
records.append(" * Total Bytes: {0}".format(sum(totals)))
records.append(" * Start time: {0}".format(start_datetime))
records.append(" * End time: {0}".format(end_datetime))
records.append(" * Duration: {0}".format(end_datetime - start_datetime))

print "\n".join(records)
