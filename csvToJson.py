# -*- coding: utf-8 -*-

# python csvToJson.py -in "data/land_surface_temperature_m/MOD11C1_M_LSTDA_2016-06.CSV.gz,data/sea_surface_temperature_m/MYD28M_2016-06.CSV.gz" -key "surface_temperature_june"
# python csvToJson.py -in "data/vegetation_index_m/MOD13A2_M_NDVI_2015-03.CSV.gz" -key "vegetation_index_march" -grad " #2d2823,#6d6d33,#34ce29" -range " -0.1:0.9"

import argparse
import gzip
import json
import math
import os
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILES", default="data/land_surface_temperature_m/MOD11C1_M_LSTDA_2016-03.CSV.gz,data/sea_surface_temperature_m/MYD28M_2016-03.CSV.gz", help="Comma-separated input files")
parser.add_argument('-grad', dest="GRADIENT", default="#b2dcff,#7548c9,#212121,#7a3465,#ff3838", help="Color gradient")
parser.add_argument('-dc', dest="DEFAULT_COLOR", default="#000000", help="Default color")
parser.add_argument('-range', dest="DATA_RANGES", default="-20:40,-20:40", help="Comma-separated data ranges in celsius")
parser.add_argument('-unit', dest="UNIT", default="Celsius", help="Unit")
parser.add_argument('-scale', dest="SCALING_FACTOR", default=1.0, type=float, help="Data scaling factor")
parser.add_argument('-fill', dest="FILL_VALUE", default=99999.0, type=float, help="Fill value")
parser.add_argument('-degrees', dest="DEGREES", default=2.5, type=float, help="Resolution in degrees")
parser.add_argument('-key', dest="KEY", default="surface_temperature_march", help="Data key")
parser.add_argument('-threshold', dest="SIZE_THRESHOLD", default=0.3, type=float, help="Size threshold")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/globe_data.json", help="Output file")
args = parser.parse_args()

INPUT_FILES = args.INPUT_FILES.split(",")
GRADIENT = args.GRADIENT.split(",")
DEGREES = args.DEGREES
KEY = args.KEY
OUTPUT_FILE = args.OUTPUT_FILE

# parse ranges
DATA_RANGES = args.DATA_RANGES.split(",")
for i,r in enumerate(DATA_RANGES):
    theRange = [float(d) for d in r.split(":")]
    # apply scaling factor
    if args.UNIT == "Kelvin":
        theRange = [(d+273.15)/args.SCALING_FACTOR for d in theRange]
    else:
        theRange = [d/args.SCALING_FACTOR for d in theRange]
    DATA_RANGES[i] = theRange

def hex2rgb(hex):
  # "#FFFFFF" -> [255,255,255]
  return tuple([int(hex[i:i+2], 16) for i in range(1,6,2)])

def rgb2hex(rgb):
  # [255,255,255] -> "0xFFFFFF"
  rgb = [int(x) for x in list(rgb)]
  return "0x"+"".join(["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in rgb]).upper()

def lerpColor(s, f, amount):
    rgb = [
      int(s[j] + amount * (f[j]-s[j]))
      for j in range(3)
    ]
    return tuple(rgb)

def getColor(grad, amount):
    gradLen = len(grad)
    i = (gradLen-1) * amount
    remainder = i % 1
    rgb = (0,0,0)
    if remainder > 0:
        rgb = lerpColor(grad[int(i)], grad[int(i)+1], remainder)
    else:
        rgb = grad[int(i)]
    return int(rgb2hex(rgb), 16)

# Mean of list
def mean(data):
    n = len(data)
    if n < 1:
        return 0
    else:
        return 1.0 * sum(data) / n

def norm(value, a, b):
    n = 1.0 * (value - a) / (b - a)
    n = min(n, 1)
    n = max(n, 0)
    return n

# Convert colors to RGB
GRADIENT = [hex2rgb(g.strip()) for g in GRADIENT]
emptyColor = hex2rgb(args.DEFAULT_COLOR)
width = int(360 / DEGREES)
height = int(180 / DEGREES)
total = width * height
values = [[] for d in range(total)]

for index, filename in enumerate(INPUT_FILES):

    rows = []
    with gzip.open(filename, 'rb') as f:
        for line in f:
            row = [float(value) for value in line.split(",")]
            rows.append(row)

    sHeight = len(rows)
    sWidth = len(rows[0])
    sTotal = sHeight * sWidth

    for y in range(sHeight):
        for x in range(sWidth):
            i = y * sWidth + x
            value = rows[y][x]

            if value != args.FILL_VALUE:
                RANGE = DATA_RANGES[index]
                n = norm(value, RANGE[0], RANGE[1])
                vy = int(round(1.0 * y / (sHeight-1) * (height - 1)))
                vx = int(round(1.0 * x / (sWidth-1) * (width - 1)))
                vi = vy * width + vx
                values[vi].append(n)

            sys.stdout.write('\r')
            sys.stdout.write("%s%%" % round(1.0*i/sTotal*100,1))
            sys.stdout.flush()

# calculate colors
jsonData = []
for i, v in enumerate(values):
    if len(v) > 0:
        value = mean(v)
        color = getColor(GRADIENT, value)
        lat = round(i / width * DEGREES - 90, 2) * -1
        lon = round(i % width * DEGREES - 180, 2)
        # size = round(value, 2)
        size = value
        # adjust size based on latitude
        # adjust = (90-abs(lat)) / 90.0
        # size = round(size * adjust, 2)
        if size > args.SIZE_THRESHOLD:
            jsonData += [lat, lon, size, color]
    sys.stdout.write('\r')
    sys.stdout.write("%s%%" % round(1.0*i/len(values)*100,1))
    sys.stdout.flush()

# Retrieve existing data if exists
jsonOut = {}
if os.path.isfile(OUTPUT_FILE):
    with open(OUTPUT_FILE) as f:
        jsonOut = json.load(f)
jsonOut[KEY] = jsonData

# Write to file
with open(OUTPUT_FILE, 'w') as f:
    json.dump(jsonOut, f)
    print "Wrote %s items to %s" % (len(jsonData)/4, OUTPUT_FILE)
