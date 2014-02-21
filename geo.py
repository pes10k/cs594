#!/usr/bin/env python

import cs594.data
import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True, help="Path to write output to.")
parser.add_argument('--time', default='minute', help="Unit of time to bundle output by")
args = parser.parse_args()

output = open(args.output, 'w')
data_src = os.path.join('..', 'data')
current_state = {"sources": {}}
current_state[args.time] = None

def merge_packet(packet):
    if packet['geo']:
        lat_long = "{0},{1}".format(packet['geo']['lat'], packet['geo']['long'])
        if lat_long not in current_state['sources']:
            current_state['sources'][lat_long] = packet['len']
        else:
            current_state['sources'][lat_long] += packet['len']

def write_state():
    if current_state[args.time] != None:
        output.write(json.dumps(current_state))
        output.write("\n")
    current_state[args.time] = None
    current_state['sources'] = {}

def handle_packet(packet):
    if packet[args.time] != current_state[args.time]:
        write_state()
        current_state[args.time] = packet[args.time]
    merge_packet(packet)

# Iterate over all packet data
cs594.data.pcap_data(data_src, 'dst host 137.110.222.70 && icmp', handle_packet)
write_state()
