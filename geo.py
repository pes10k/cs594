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
    src_ip = packet['src_ip']
    if packet['geo'] and packet['geo']['lat']:
        if src_ip not in current_state['sources']:
            current_state['sources'][src_ip] = {
                'len': packet['len'],
                'lat': packet['geo']['lat'],
                'lon': packet['geo']['long'],
                'ip': src_ip
            }
        else:
            current_state['sources'][src_ip]['len'] += packet['len']

def write_state():
    if current_state[args.time] != None:
        to_write = {}
        to_write['type'] = args.time
        to_write['time'] = current_state[args.time]
        to_write['sources'] = sorted(current_state['sources'].iteritems(), key=lambda x: x['len'], reverse=True)
        output.write(json.dumps(to_write))
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
