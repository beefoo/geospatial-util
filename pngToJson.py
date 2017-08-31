# -*- coding: utf-8 -*-

# python pngToJson.py -in "img/net_radiation_m/CERES_NETFLUX_M_2015-06.PNG" -key "net_radiation_june"

import argparse
import colorsys
import json
import math
import os
from PIL import Image
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="img/net_radiation_m/CERES_NETFLUX_M_2015-03.PNG", help="Input file")
parser.add_argument('-hue', dest="HUE_GRADIENT", default="165,58,15", help="Hue gradient")
parser.add_argument('-grad', dest="GRADIENT", default="#212121,#3d2d29,#593931,#ffe877", help="Color gradient")
parser.add_argument('-degrees', dest="DEGREES", default=2.5, type=float, help="Resolution in degrees")
parser.add_argument('-key', dest="KEY", default="net_radiation_march", help="Data key")
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
GRADIENT = [hex2rgb(g.strip()) for g in args.GRADIENT.strip().split(",")]
HUE_GRADIENT = [float(g) for g in args.HUE_GRADIENT.strip().split(",")]
DEGREES = args.DEGREES
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
    # n = min(n, 1)
    # n = max(n, 0)
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

def getValue(grad, value):
    step = 1.0 / (len(grad)-1)
    returnValue = None

    for i,g in enumerate(grad):
        if i > 0:
            v = norm(value, grad[i-1], g)
            if 0 <= v <= 1:
                returnValue = (i-1) * step + v * step
                break

    if returnValue is None:
        g0 = grad[0]
        g1 = grad[-1]
        returnValue = 1
        if g1 > g0:
            if value < g0 or g0+(360-value) < value-g1:
                returnValue = 0
        else:
            if not (value < g1 or g1+(360-value) < value-g0):
                returnValue = 0

    return returnValue

width = int(360 / DEGREES)
height = int(180 / DEGREES)
total = width * height
values = [[] for d in range(total)]

im = Image.open(INPUT_FILE)
imW, imH = im.size
im = im.convert('HSV')
pixels = im.load()

scaleW = 1.0 * imW / width
scaleH = 1.0 * imH / height

values = [[] for d in range(total)]

for y in range(height):
    for x in range(width):
        i = y * width + x
        imX = int(x * scaleW)
        imY = int(y * scaleH)
        hsv = pixels[imX, imY]
        hue = hsv[0]
        value = getValue(HUE_GRADIENT, hue)
        values[i].append(value)

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
        adjust = (90-abs(lat)) / 90.0
        size = round(size * adjust, 2)
        color = getColor(GRADIENT, value)

        if size > 0:
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
