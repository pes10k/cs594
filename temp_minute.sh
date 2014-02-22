#!/bin/bash

head -n -1 ../computed/minute_combined.txt > ../computed/minute_tmp.txt
python -O result_to_json.py --output html/js/cs594/data/minutedata.js --input ../computed/minute_tmp.txt --name window.cs594.data.minData --group region 
