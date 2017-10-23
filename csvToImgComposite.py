# -*- coding: utf-8 -*-

# python csvToImgComposite.py -resize 0.2

import argparse
import gzip
from PIL import Image
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILES", default="data/land_surface_temperature/MOD11C1_E_LSTDA_2016-01-01.CSV.gz,data/sea_surface_temperature/MYD28W_2016-01-01.CSV.gz", help="Comma-separated input files")
parser.add_argument('-grad', dest="GRADIENT", default="#b2dcff,#7548c9,#212121,#7a3465,#ff3838", help="Color gradient")
parser.add_argument('-dc', dest="DEFAULT_COLOR", default="#000000", help="Default color")
parser.add_argument('-range', dest="DATA_RANGES", default="-20:40,-20:40", help="Comma-separated data ranges in celsius")
parser.add_argument('-unit', dest="UNIT", default="Celsius", help="Unit")
parser.add_argument('-scale', dest="SCALING_FACTOR", default=1.0, type=float, help="Data scaling factor")
parser.add_argument('-fill', dest="FILL_VALUE", default=99999.0, type=float, help="Fill value")
parser.add_argument('-resize', dest="RESIZE", default=1.0, type=float, help="Resize to")
parser.add_argument('-resizeW', dest="RESIZE_TO_WIDTH", default=0, type=int, help="Resize to width")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/land_sea_surface_temperature/2016-01-01.png", help="Output file")
args = parser.parse_args()

INPUT_FILES = args.INPUT_FILES.split(",")
GRADIENT = args.GRADIENT.split(",")
RESIZE = args.RESIZE
RESIZE_TO_WIDTH = args.RESIZE_TO_WIDTH

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
    return rgb

def norm(value, a, b):
    n = 1.0 * (value - a) / (b - a)
    n = min(n, 1)
    n = max(n, 0)
    return n

# Convert colors to RGB
GRADIENT = [hex2rgb(g.strip()) for g in GRADIENT]
emptyColor = hex2rgb(args.DEFAULT_COLOR)
width = None
height = None
total = 0
im = None
pixels = []

for index, filename in enumerate(INPUT_FILES):
    print "Processing %s" % filename

    rows = []
    with gzip.open(filename, 'rb') as f:
        for line in f:
            row = [float(value) for value in line.split(",")]
            rows.append(row)

    if im is None:
        height = len(rows)
        width = len(rows[0])
        if RESIZE_TO_WIDTH > 0:
            RESIZE = 1.0 * RESIZE_TO_WIDTH / width
        if RESIZE != 1.0:
            height = int(round(RESIZE * height))
            width = int(round(RESIZE * width))
        total = height * width
        print "Dimensions: %s x %s" % (height, width)
        im = Image.new("RGB", (width, height), emptyColor)
        pixels = im.load()

    for y in range(height):
        for x in range(width):
            i = y * width + x
            value = 0
            if RESIZE != 1.0:
                value = rows[int(round(y/RESIZE))][int(round(x/RESIZE))]
            else:
                value = rows[y][x]
            if value != args.FILL_VALUE:
                RANGE = DATA_RANGES[index]
                n = norm(value, RANGE[0], RANGE[1])
                color = getColor(GRADIENT, n)
                pixels[x, y] = color
            sys.stdout.write('\r')
            sys.stdout.write("%s%%" % round(1.0*i/total*100,1))
            sys.stdout.flush()

im.save(args.OUTPUT_FILE)
print "\rSaved %s" % args.OUTPUT_FILE
