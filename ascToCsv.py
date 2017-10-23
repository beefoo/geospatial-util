# -*- coding: utf-8 -*-

# python ascToCsv.py -in geotiff/water_vapor_m/MYDAL2_M_SKY_WV_2016-01.asc -out data/water_vapor_m/MYDAL2_M_SKY_WV_2016-01.csv

import argparse
import csv
import os
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="path/to/file.asc", help="Input file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="path/to/file.csv", help="Output file")
args = parser.parse_args()

print "Converting ASCII to CSV..."
data = []
with open(args.INPUT_FILE) as f:
    lines = [l.strip() for l in f.readlines()]
    for line in lines[5:]:
        row = [value for value in line.split(" ")]
        data.append(row)

with open(args.OUTPUT_FILE, 'wb') as f:
    w = csv.writer(f, delimiter=',')
    w.writerows(data)
    print "Successfully converted to %s" % args.OUTPUT_FILE
