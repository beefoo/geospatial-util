# -*- coding: utf-8 -*-

# python csvToImgComposite.py -resize 0.2

import argparse
import gzip
from PIL import Image
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILES", default="img/vegetation_index_e/MOD13A2_E_NDVI_2015-01-01.PNG,img/snow_cover_e/MOD10C1_E_SNOW_2015-01-01.PNG", help="Comma-separated input files")
parser.add_argument('-dc', dest="DEFAULT_COLOR", default="#000000", help="Default color")
parser.add_argument('-resizeW', dest="RESIZE_TO_WIDTH", default=2048, type=int, help="Resize to width")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/snow_cover_vegetation_index/2015-01-01.png", help="Output file")
args = parser.parse_args()

INPUT_FILES = args.INPUT_FILES.split(",")
RESIZE_TO_WIDTH = args.RESIZE_TO_WIDTH

def hex2rgb(hex):
  # "#FFFFFF" -> [255,255,255]
  return tuple([int(hex[i:i+2], 16) for i in range(1,6,2)])

def norm(value, a, b):
    n = 1.0 * (value - a) / (b - a)
    n = min(n, 1)
    n = max(n, 0)
    return n

# Convert colors to RGB
emptyColor = hex2rgb(args.DEFAULT_COLOR)
imOut = None
width = 0
height = 0
total = 0
resize = 1.0
pixelsOut = []

for index, filename in enumerate(INPUT_FILES):

    imIn = Image.open(filename)
    imIn = imIn.convert('RGB')
    pixelsIn = imIn.load()

    if index <= 0:
        width, height = imIn.size
        if RESIZE_TO_WIDTH > 0:
            resize = 1.0 * RESIZE_TO_WIDTH / width
            height = int(round(resize * height))
            width = int(round(resize * width))
        total = height * width
        print "Dimensions: %s x %s" % (height, width)
        imOut = Image.new("RGB", (width, height), emptyColor)
        pixelsOut = imOut.load()

    for y in range(height):
        for x in range(width):
            i = y * width + x
            xr = int(round(x/resize))
            yr = int(round(y/resize))
            rgb = pixelsIn[xr, yr]
            if rgb[0] >= 1 and rgb[1] >= 1 and rgb[2] >= 1:
                pixelsOut[x, y] = rgb
            sys.stdout.write('\r')
            sys.stdout.write("%s%%" % round(1.0*i/total*100,1))
            sys.stdout.flush()

imOut.save(args.OUTPUT_FILE)
print "\rSaved %s" % args.OUTPUT_FILE
