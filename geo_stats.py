#!/usr/bin/env python

import json
import pprint
from cs594.data import size_format

countries_by_contient = {
  "AD": "EU",
  "AE": "AS",
  "AF": "AS",
  "AG": "NA",
  "AI": "NA",
  "AL": "EU",
  "AM": "AS",
  "AN": "NA",
  "AO": "AF",
  "AP": "AS",
  "AQ": "AN",
  "AR": "SA",
  "AS": "OC",
  "AT": "EU",
  "AU": "OC",
  "AW": "NA",
  "AX": "EU",
  "AZ": "AS",
  "BA": "EU",
  "BB": "NA",
  "BD": "AS",
  "BE": "EU",
  "BF": "AF",
  "BG": "EU",
  "BH": "AS",
  "BI": "AF",
  "BJ": "AF",
  "BL": "NA",
  "BM": "NA",
  "BN": "AS",
  "BO": "SA",
  "BR": "SA",
  "BS": "NA",
  "BT": "AS",
  "BV": "AN",
  "BW": "AF",
  "BY": "EU",
  "BZ": "NA",
  "CA": "NA",
  "CC": "AS",
  "CD": "AF",
  "CF": "AF",
  "CG": "AF",
  "CH": "EU",
  "CI": "AF",
  "CK": "OC",
  "CL": "SA",
  "CM": "AF",
  "CN": "AS",
  "CO": "SA",
  "CR": "NA",
  "CU": "NA",
  "CV": "AF",
  "CX": "AS",
  "CY": "AS",
  "CZ": "EU",
  "DE": "EU",
  "DJ": "AF",
  "DK": "EU",
  "DM": "NA",
  "DO": "NA",
  "DZ": "AF",
  "EC": "SA",
  "EE": "EU",
  "EG": "AF",
  "EH": "AF",
  "ER": "AF",
  "ES": "EU",
  "ET": "AF",
  "EU": "EU",
  "FI": "EU",
  "FJ": "OC",
  "FK": "SA",
  "FM": "OC",
  "FO": "EU",
  "FR": "EU",
  "FX": "EU",
  "GA": "AF",
  "GB": "EU",
  "GD": "NA",
  "GE": "AS",
  "GF": "SA",
  "GG": "EU",
  "GH": "AF",
  "GI": "EU",
  "GL": "NA",
  "GM": "AF",
  "GN": "AF",
  "GP": "NA",
  "GQ": "AF",
  "GR": "EU",
  "GS": "AN",
  "GT": "NA",
  "GU": "OC",
  "GW": "AF",
  "GY": "SA",
  "HK": "AS",
  "HM": "AN",
  "HN": "NA",
  "HR": "EU",
  "HT": "NA",
  "HU": "EU",
  "ID": "AS",
  "IE": "EU",
  "IL": "AS",
  "IM": "EU",
  "IN": "AS",
  "IO": "AS",
  "IQ": "AS",
  "IR": "AS",
  "IS": "EU",
  "IT": "EU",
  "JE": "EU",
  "JM": "NA",
  "JO": "AS",
  "JP": "AS",
  "KE": "AF",
  "KG": "AS",
  "KH": "AS",
  "KI": "OC",
  "KM": "AF",
  "KN": "NA",
  "KP": "AS",
  "KR": "AS",
  "KW": "AS",
  "KY": "NA",
  "KZ": "AS",
  "LA": "AS",
  "LB": "AS",
  "LC": "NA",
  "LI": "EU",
  "LK": "AS",
  "LR": "AF",
  "LS": "AF",
  "LT": "EU",
  "LU": "EU",
  "LV": "EU",
  "LY": "AF",
  "MA": "AF",
  "MC": "EU",
  "MD": "EU",
  "ME": "EU",
  "MF": "NA",
  "MG": "AF",
  "MH": "OC",
  "MK": "EU",
  "ML": "AF",
  "MM": "AS",
  "MN": "AS",
  "MO": "AS",
  "MP": "OC",
  "MQ": "NA",
  "MR": "AF",
  "MS": "NA",
  "MT": "EU",
  "MU": "AF",
  "MV": "AS",
  "MW": "AF",
  "MX": "NA",
  "MY": "AS",
  "MZ": "AF",
  "NA": "AF",
  "NC": "OC",
  "NE": "AF",
  "NF": "OC",
  "NG": "AF",
  "NI": "NA",
  "NL": "EU",
  "NO": "EU",
  "NP": "AS",
  "NR": "OC",
  "NU": "OC",
  "NZ": "OC",
  "O1": "--",
  "OM": "AS",
  "PA": "NA",
  "PE": "SA",
  "PF": "OC",
  "PG": "OC",
  "PH": "AS",
  "PK": "AS",
  "PL": "EU",
  "PM": "NA",
  "PN": "OC",
  "PR": "NA",
  "PS": "AS",
  "PT": "EU",
  "PW": "OC",
  "PY": "SA",
  "QA": "AS",
  "RE": "AF",
  "RO": "EU",
  "RS": "EU",
  "RU": "EU",
  "RW": "AF",
  "SA": "AS",
  "SB": "OC",
  "SC": "AF",
  "SD": "AF",
  "SE": "EU",
  "SG": "AS",
  "SH": "AF",
  "SI": "EU",
  "SJ": "EU",
  "SK": "EU",
  "SL": "AF",
  "SM": "EU",
  "SN": "AF",
  "SO": "AF",
  "SR": "SA",
  "ST": "AF",
  "SV": "NA",
  "SY": "AS",
  "SZ": "AF",
  "TC": "NA",
  "TD": "AF",
  "TF": "AN",
  "TG": "AF",
  "TH": "AS",
  "TJ": "AS",
  "TK": "OC",
  "TL": "AS",
  "TM": "AS",
  "TN": "AF",
  "TO": "OC",
  "TR": "EU",
  "TT": "NA",
  "TV": "OC",
  "TW": "AS",
  "TZ": "AF",
  "UA": "EU",
  "UG": "AF",
  "UM": "OC",
  "US": "NA",
  "UY": "SA",
  "UZ": "AS",
  "VA": "EU",
  "VC": "NA",
  "VE": "SA",
  "VG": "NA",
  "VI": "NA",
  "VN": "AS",
  "VU": "OC",
  "WF": "OC",
  "WS": "OC",
  "YE": "AS",
  "YT": "AF",
  "ZA": "AF",
  "ZM": "AF",
  "ZW": "AF",
  'Unknown': 'Unknown'
}

country_indexes = ['NA', 'EU', 'AS', 'SA', 'AF', 'OC', 'Unknown']
country_names = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Oceania', 'Unknown']

countries = set()
cities = set()
continents = set()
ips = set()
continent_traffic = {}
countries_traffic = {}
total_traffic = 0


h = open("../computed/sec_combined.txt", 'r')
for l in h.xreadlines():
    r = json.loads(l)
    for s in r['sources']:

        continent = countries_by_contient.get(s['country'], 'Unknown')
        if continent not in continent_traffic:
            continent_traffic[continent] = 0
        continent_traffic[continent] += s['len']

        if s['country'] not in countries_traffic:
            countries_traffic[s['country']] = 0
        countries_traffic[s['country']] += s['len']

        total_traffic += s['len']

        continents.add(continent)
        countries.add(s['country'])
        ips.add(s['ip'])
        if s['country'] and s['city']:
            cities.add(s['city'] + s['country'])
h.close()

continent_traffic_values = []
for key in continent_traffic:
    continent_traffic_values.append((key, "%.2f" % (continent_traffic[key]/float(total_traffic),), continent_traffic[key], size_format(continent_traffic[key])))
continent_traffic_values = sorted(continent_traffic_values, key=lambda x: x[2])

countries_traffic_values = []
for key in countries_traffic:
    countries_traffic_values.append((key, "%.2f" % (countries_traffic[key]/float(total_traffic),), countries_traffic[key], size_format(countries_traffic[key])))
countries_traffic_values = sorted(countries_traffic_values, key=lambda x: x[2])


results = []
results.append(" * Continents: {0}".format(len(continents)))
results.append(" * Countries: {0}".format(len(countries)))
results.append(" * Cities: {0}".format(len(cities)))
results.append(" * IPs: {0}".format(len(ips)))

print "\n".join(results)

pprint.pprint(continent_traffic_values)
pprint.pprint(countries_traffic_values)
