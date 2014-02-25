#!/usr/bin/env python
import geoip2
import cs594.data
import os
import sys
import json
import argparse
import boomslang

in_h = open('../computed/ip.json', 'r')
out_h = open('../computed/ips.dump.txt', 'w')

record = json.load(in_h)
ips = record.keys()

for ip in ips:
    out_h.write(ip + "\n")
out_h.close()
