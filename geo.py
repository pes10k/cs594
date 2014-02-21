import cs594.data
import os
import sys
import json

data_src = os.path.join('..', 'data')
current_state = {
    "sec": None,
    "sources": {}
}

def merge_packet(packet):
    if packet['geo']:
        lat_long = "{0},{1}".format(packet['geo']['lat'], packet['geo']['long'])
        if lat_long not in current_state['sources']:
            current_state['sources'][lat_long] = packet['len']
        else:
            current_state['sources'][lat_long] += packet['len']

def write_state():
    if current_state['sec'] != None:
        print json.dumps(current_state)
    current_state['sec'] = None
    current_state['sources'] = {}

def handle_packet(packet):
    if packet['sec'] != current_state['sec']:
        write_state()
        current_state['sec'] = packet['sec']
    merge_packet(packet)

# Iterate over all packet data
cs594.data.pcap_data(data_src, 'dst host 137.110.222.70 && icmp', handle_packet)
write_state()
