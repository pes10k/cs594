from __future__ import division
import os
import pcapy
from impacket.ImpactDecoder import EthDecoder
import geoip2.database
import geoip2.errors

decoder = EthDecoder()
reader = geoip2.database.Reader('GeoLite2-City.mmdb')
_geodata = {}

def formatted_y_labels(datas, num=10):
  # find the max value
  max_value = max([sum(row) for row in datas])
  step = float(max_value)/num
  return [step * i for i in range(num + 1)]

def _sort_key(k):
    index = k.replace("ddostrace.070804.pcap", "")
    return int(index) if index else 0

def pcap_data(path, a_filter, callback):

    def extract_packet(hdr, data):
        packet = decoder.decode(data)
        ip_packet = packet.child()
        src_ip = ip_packet.get_ip_src()
        ts_sec, ts_usec = hdr.getts()
        full_ts = ts_sec * 1000000 + ts_usec
        parsed_packet = {
            "full_ts": full_ts,
            "sec": ts_sec,
            "minute": ts_sec - (ts_sec % 60),
            "hour": ts_sec - (ts_sec % 3600),
            "src_ip": src_ip,
            "len": hdr.getlen()
        }

        if src_ip not in _geodata:
            try:
                local_geo_info = reader.city(src_ip)
                local_rec = {
                    'city': local_geo_info.city.name,
                    'country': local_geo_info.country.iso_code,
                    'region': local_geo_info.subdivisions.most_specific.iso_code,
                    'lat': local_geo_info.location.latitude,
                    'long': local_geo_info.location.longitude
                }
                _geodata[src_ip] = local_rec
            except geoip2.errors.AddressNotFoundError:
                _geodata[src_ip] = None
        parsed_packet['geo'] = _geodata[src_ip]
        callback(parsed_packet)

    for root, dirs, files in os.walk(path):
        for f in sorted(files, key=_sort_key):
            print "parsing " + f
            full_path = os.path.join(path, f)
            p = pcapy.open_offline(full_path)
            p.setfilter(a_filter)
            p.loop(0, extract_packet)

def size_format(b):
    if b < 1000:
        return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'
