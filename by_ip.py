#!/usr/bin/env python

import cs594.data
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True, help="Path to write output to.")
parser.add_argument('--data', required=True, help="Directory to read pcap data from.")
args = parser.parse_args()

output = open(args.output, 'w')
ips = {}

def handle_packet(packet):
    src_ip = packet['src_ip']
    if src_ip not in ips:
        ips[src_ip] = 0
    ips[src_ip] += packet['len']

# Iterate over all packet data
cs594.data.pcap_data(args.data, 'dst host 137.110.222.70 && icmp', handle_packet)

json.dump(ips, output)
