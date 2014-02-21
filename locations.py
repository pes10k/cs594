#!/usr/bin/env python
import sys
import geoip2.database
import geoip2.errors
import pcappy
from impacket.ImpactDecoder import EthDecoder

decoder = EthDecoder()
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def is_ip_stored(ip):
    rs = locations.find_one({"_id": ip})
    if not rs:
        record = {"_id": ip}
        try:
            geo_info = reader.city(ip)
            record['city'] = geo_info.city.name
            record['country'] = geo_info.country.name
            record['postal'] = geo_info.postal.code
            record['lat'] = geo_info.location.latitude
            record['long'] = geo_info.location.longitude
        except geoip2.errors.AddressNotFoundError:
            pass
        record['count'] = 0
        record['earliest'] = 0
        record['latest'] = 0
        locations.insert(record)
        rs = locations.find_one({"_id": ip})
    return rs

def update_record(ip, ts):
    r = is_ip_stored(ip)
    if r['earliest'] == 0 or r['earliest'] > ts:
        r['earliest'] = ts

    if r['latest'] == 0 or r['latest'] < ts:
        r['latest'] = ts

    r['count'] = r['count'] + 1
    locations.update({"_id": ip}, r)

def got_packet(d, hdr, data):
    packet = decoder.decode(data)
    ip_packet = packet.child()
    src_ip = ip_packet.get_ip_src()
    ts_parts = hdr['ts']
    full_ts = ts_parts['tv_sec'] * 1000000 + ts_parts['tv_usec']
    update_record(src_ip, full_ts)
    # print "{0} at {1}".format(src_ip, full_ts)

if not sys.argv[1:]:
    print 'usage: %s <dump.pcap>' % sys.argv[0]
    sys.exit(-1)

p = pcappy.open_offline(sys.argv[1])
p.filter = 'dst host 137.110.222.70 && icmp'

p.loop(-1, got_packet, {})
