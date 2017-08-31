# -*- coding: utf-8 -*-

# python h5ToJson.py -in "data/co2_m/AIRS.2015.06.01.L3.CO2Std_IR030.v5.9.14.0.IRonly.X15194072600.h5" -key "co2_june"

import argparse
import h5py
import json
import math
import os
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/co2_m/AIRS.2015.03.01.L3.CO2Std_IR031.v5.9.14.0.IRonly.X15098105512.h5", help="Input file")
parser.add_argument('-dataset', dest="DATASET", default="CO2,Data Fields,mole_fraction_of_carbon_dioxide_in_free_troposphere", help="Dataset")
parser.add_argument('-grad', dest="GRADIENT", default="#212121,#212121,#3c253f,#c13838,#ff8484", help="Color gradient")
parser.add_argument('-degrees', dest="DEGREES", default=2.5, type=float, help="Resolution in degrees")
parser.add_argument('-key', dest="KEY", default="co2_march", help="Data key")
parser.add_argument('-range', dest="DATA_RANGE", default="0.00039,0.00041", help="Data range")
parser.add_argument('-scale', dest="SCALING_FACTOR", default=1.0, type=float, help="Data scaling factor")
parser.add_argument('-fill', dest="FILL_VALUE", default=-9999, type=int, help="Fill value")
parser.add_argument('-threshold', dest="SIZE_THRESHOLD", default=0.3, type=float, help="Size threshold")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/globe_data.json", help="Output file")
args = parser.parse_args()

def hex2rgb(hex):
  # "#FFFFFF" -> [255,255,255]
  return tuple([int(hex[i:i+2], 16) for i in range(1,6,2)])

def rgb2hex(rgb):
  # [255,255,255] -> "0xFFFFFF"
  rgb = [int(x) for x in list(rgb)]
  return "0x"+"".join(["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in rgb]).upper()

INPUT_FILE = args.INPUT_FILE
DATASET_PATH = args.DATASET.split(",")
GRADIENT = [hex2rgb(g.strip()) for g in args.GRADIENT.strip().split(",")]
DEGREES = args.DEGREES
RANGE = [float(d) for d in args.DATA_RANGE.split(",")]
KEY = args.KEY
OUTPUT_FILE = args.OUTPUT_FILE

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

width = int(360 / DEGREES)
height = int(180 / DEGREES)
total = width * height
values = [[] for d in range(total)]

dataset = None

with h5py.File(args.INPUT_FILE,'r') as f:
    for p in DATASET_PATH:
        if dataset is None:
            dataset = f[p]
        else:
            dataset = dataset[p]

    if not dataset:
        print "Could not find dataset in file"
        sys.exit(0)

    dHeight = len(dataset)
    dWidth = len(dataset[0])

    scaleW = 1.0 * dWidth / width
    scaleH = 1.0 * dHeight / height

    for y in range(height):
        for x in range(width):
            i = y * width + x
            dX = int(x * scaleW)
            dY = int(y * scaleH)
            value = dataset[dY, dX]
            if value != args.FILL_VALUE:
                n = norm(value, RANGE[0], RANGE[1])
                values[i].append(n)

            sys.stdout.write('\r')
            sys.stdout.write("%s%%" % round(1.0*i/total*100,1))
            sys.stdout.flush()

# calculate colors
jsonData = []
for i, v in enumerate(values):
    if len(v) > 0:
        lat = round(i / width * DEGREES - 90, 2) * -1
        lon = round(i % width * DEGREES - 180, 2)
        value = mean(v)
        size = value
        # adjust size based on latitude
        # adjust = (90-abs(lat)) / 90.0
        # size = round(size * adjust, 2)
        color = getColor(GRADIENT, value)

        if size > args.SIZE_THRESHOLD:
            jsonData += [lat, lon, size, color]

        sys.stdout.write('\r')
        sys.stdout.write("%s%%" % round(1.0*i/total*100,1))
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
