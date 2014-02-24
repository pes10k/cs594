import geoip2.database
import geoip2.errors
import sys
from pprint import pprint

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

ip = sys.stdin.read().strip()
local_geo_info = reader.city(ip)

pprint(dir(local_geo_info))

pprint(local_geo_info)
