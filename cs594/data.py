import os
import pcapy
from impacket.ImpactDecoder import EthDecoder
import geoip2.database
import geoip2.errors

decoder = EthDecoder()
reader = geoip2.database.Reader('GeoLite2-City.mmdb')
_geodata = {}

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
            "src_ip": src_ip,
            "len": hdr.getlen()
        }

        if src_ip not in _geodata:
            try:
                local_geo_info = reader.city(src_ip)
                local_rec = {
                    'city': local_geo_info.city.name,
                    'country': local_geo_info.country.name,
                    'postal': local_geo_info.postal.code,
                    'lat': local_geo_info.location.latitude,
                    'long': local_geo_info.location.longitude
                }
                _geodata[src_ip] = local_rec
            except geoip2.errors.AddressNotFoundError:
                _geodata[src_ip] = None
        parsed_packet['geo'] = _geodata[src_ip]
        callback(parsed_packet)

    for root, dirs, files in os.walk(path):
        for f in files:
            full_path = os.path.join(path, f)
            p = pcapy.open_offline(full_path)
            p.setfilter(a_filter)
            p.loop(0, extract_packet)
