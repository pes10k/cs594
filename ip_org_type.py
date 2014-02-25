#!/usr/bin/env python
import cs594.data
import os
import sys
import json
import boomslang
from pprint import pprint

ip_type_counts = {}
ip_type_counts_continent = {}

type_amounts = {}
continent_types_amounts = {}

type_bundles = {
    'hosting': 'commercial',
    'business': 'commercial',
    'cellular': 'residential',
    'college': 'educational',
    'dialup': 'residential',
    'government': 'government',
    'residential': 'residential',
    'content_delivery_network': 'commercial',
    'library': 'educational',
    'school': 'educational',
    'military': 'government',
    'traveler': 'commercial'
}

type_order = ['commercial', 'residential', 'educational', 'government']
type_colors = {
    'commercial': 'blue',
    'residential': 'green',
    'educational': 'orange',
    'government': 'red'
}

continent_order = []
continent_name_order = []

h = open("../computed/sec_combined.txt", 'r')
for l in h.xreadlines():
    r = json.loads(l)
    for s in r['sources']:
        ip = s['ip']
        ip_data = cs594.data.ip_info(ip, 'batch-lookup.json')
        amount = s['len']

        try:
            as_type = ip_data['traits']['user_type']
            continent = ip_data['continent']['code']
            continent_name = ip_data['continent']['names']['en']
        except:
            continue

        new_type = type_bundles[as_type]

        if ip not in ip_type_counts:
            ip_type_counts[ip] = new_type

        if continent not in ip_type_counts_continent:
            ip_type_counts_continent[continent] = {}
            continent_order.append(continent)
            continent_name_order.append(continent_name)

        if ip not in ip_type_counts_continent[continent]:
            ip_type_counts_continent[continent][ip] = new_type

        if new_type not in type_amounts:
            type_amounts[new_type] = 0

        if continent not in continent_types_amounts:
            continent_types_amounts[continent] = {}

        if new_type not in continent_types_amounts[continent]:
            continent_types_amounts[continent][new_type] = 0

        type_amounts[new_type] += amount
        continent_types_amounts[continent][new_type] += amount
h.close()

ip_type_counts_transformed = {}
for ip in ip_type_counts:
    ip_type = ip_type_counts[ip]
    if ip_type not in ip_type_counts_transformed:
        ip_type_counts_transformed[ip_type] = 0
    ip_type_counts_transformed[ip_type] += 1
pprint(ip_type_counts_transformed)


ip_type_counts_continent_transformed = {}
for country in ip_type_counts_continent:
    ip_type_counts_continent_transformed[country] = {}
    for ip in ip_type_counts_continent[country]:
        ip_type = ip_type_counts_continent[country][ip]
        if ip_type not in ip_type_counts_continent_transformed[country]:
            ip_type_counts_continent_transformed[country][ip_type] = 0
        ip_type_counts_continent_transformed[country][ip_type] += 1
pprint(ip_type_counts_continent_transformed)

pprint(type_amounts)
pprint(continent_types_amounts)

ip_type_count_bar = boomslang.Bar()
ip_type_count_bar.xValues = range(len(type_order))
ip_type_count_bar.yValues = [ip_type_counts_transformed[t] for t in type_order]
ip_type_count_bar.xTickLabels = type_order

ip_type_count_plot = boomslang.Plot()
ip_type_count_plot.title = "IPs by Type"
ip_type_count_plot.xLabel = "IP Owner Type"
ip_type_count_plot.yLabel = "# of IPs"
ip_type_count_plot.add(ip_type_count_bar)
ip_type_count_plot.setDimensions(width=12)
ip_type_count_plot.save(os.path.join('..', "computed", "ip_type_count_plot.png"))


traffic_by_type_bar = boomslang.Bar()
traffic_by_type_bar.xValues = range(len(type_order))
traffic_by_type_bar.yValues = [type_amounts[t] for t in type_order]
traffic_by_type_bar.xTickLabels = type_order

traffic_by_type_bar_max_y = max(traffic_by_type_bar.yValues) * 1.1
traffic_by_type_bar_step = traffic_by_type_bar_max_y * .1
traffic_by_type_bar.yTickLabelPoints = [i * traffic_by_type_bar_step for i in range(11)]
traffic_by_type_bar.yTickLabels = [cs594.data.size_format(y) for y in traffic_by_type_bar.yTickLabelPoints]

traffic_by_type_plot = boomslang.Plot()
traffic_by_type_plot.title = "Traffic by Type"
traffic_by_type_plot.xLabel = "IP Owner Type"
traffic_by_type_plot.yLabel = "Amount of Traffic (in Bytes)"
traffic_by_type_plot.add(traffic_by_type_bar)
traffic_by_type_plot.setDimensions(width=12)
traffic_by_type_plot.save(os.path.join('..', "computed", "traffic_by_type_plot.png"))




ip_type_country_cluster = boomslang.ClusteredBars()
for a_type in type_order:
    bar = boomslang.Bar()
    bar.xValues = range(len(continent_order))
    bar.yValues = [ip_type_counts_continent_transformed[c].get(a_type, 0) for c in continent_order]
    bar.color = type_colors[a_type]
    bar.label = a_type
    ip_type_country_cluster.add(bar)

ip_type_country_cluster.spacing = 0.5
ip_type_country_cluster.xTickLabels = continent_name_order

ip_type_country_cluster_plot = boomslang.Plot()
ip_type_country_cluster_plot.title = "IPs by Continents and Type"
ip_type_country_cluster_plot.xLabel = "Continents"
ip_type_country_cluster_plot.yLabel = "# of IPs"
ip_type_country_cluster_plot.add(ip_type_country_cluster)
ip_type_country_cluster_plot.hasLegend()
ip_type_country_cluster_plot.setDimensions(width=12)
ip_type_country_cluster_plot.save(os.path.join('..', "computed", "ip_type_country_cluster.png"))



traffic_country_cluster = boomslang.ClusteredBars()
traffic_country_cluster_max_y = 0
for a_type in type_order:
    bar = boomslang.Bar()
    bar.xValues = range(len(continent_order))
    bar.yValues = [continent_types_amounts[c].get(a_type, 0) for c in continent_order]
    traffic_country_cluster_max_y = max(traffic_country_cluster_max_y, max(bar.yValues))
    bar.color = type_colors[a_type]
    bar.label = a_type
    traffic_country_cluster.add(bar)

traffic_country_cluster.spacing = 0.5
traffic_country_cluster.xTickLabels = continent_name_order


traffic_country_cluster_plot = boomslang.Plot()

traffic_country_cluster_plot.title = "Traffic by Continent and Type (in Bytes)"
traffic_country_cluster_plot.xLabel = "Continents"
traffic_country_cluster_plot.yLabel = "Amount of Traffic (in Bytes)"
traffic_country_cluster_plot.add(traffic_country_cluster)

traffic_country_cluster_max_y *= 1.1
traffic_country_cluster_step = traffic_country_cluster_max_y * .1
traffic_country_cluster_plot.yTickLabelPoints = [i * traffic_country_cluster_step for i in range(11)]
traffic_country_cluster_plot.yTickLabels = [cs594.data.size_format(y) for y in traffic_country_cluster_plot.yTickLabelPoints]

traffic_country_cluster_plot.hasLegend()
traffic_country_cluster_plot.setDimensions(width=12)
traffic_country_cluster_plot.save(os.path.join('..', "computed", "traffic_country_cluster.png"))
