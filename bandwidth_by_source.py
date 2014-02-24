#!/usr/bin/env python
import sys
import json
import argparse
import boomslang
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--input', default=False, help="path to read combined data From. defaults to stdio")
parser.add_argument('--output', required=True, help="path to write resulting graph to.")
args = parser.parse_args()

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
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'grey', 'purple']
x_points = []
country_data = []

in_data = open(args.input, 'r') if args.input else sys.stdin
for a_line in in_data.xreadlines():
    record = json.loads(a_line)
    country_data_in_record = {}
    for entry in record['sources']:
        continent = countries_by_contient.get(entry['country'], 'Unknown')
        if continent not in country_data_in_record:
            country_data_in_record[continent] = 0
        country_data_in_record[continent] += entry['len']
    country_data.append([country_data_in_record.get(cc, 0) for cc in country_indexes])
    x_points.append(datetime.datetime.fromtimestamp(record['time']).strftime('%H:%M'))

stack = boomslang.StackedBars()
index = 0
for country in country_indexes:
    bar = boomslang.Bar()
    bar.xValues = range(len(x_points))
    bar.yValues = [data[index] for data in country_data]
    bar.color = colors[index]
    bar.label = country_names[index]
    stack.add(bar)
    index += 1

stack.xTickLabels = x_points
stack.xTickLabelProperties = {
    'rotation': 90
}
plot = boomslang.Plot()
plot.add(stack)
plot.hasLegend()
plot.setDimensions(width=1000, height=700)
plot.save("stackedbar.png")
