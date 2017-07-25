# -*- coding: utf-8 -*-

# python batchCsvToImg.py -dir "data/vegetation_index" -pattern "MOD13A2_E_NDVI_([0-9\-]+)\.CSV\.gz" -out "output/vegetation_index/*.png" -grad " #ece0d7,#8b8c35,#132d02" -range " -0.1,0.9" -resize 0.5

import argparse
import os
import re
import subprocess
import sys

argValues = [
    ['-grad', "GRADIENT", "#b2dcff,#7548c9,#212121,#7a3465,#ff3838", "Color gradient"],
    ['-dc', "DEFAULT_COLOR", "#000000", "Default color"],
    ['-range', "DATA_RANGE", ' -20,40', "Data range in celsius"],
    ['-unit', "UNIT", "Celsius", "Unit"],
    ['-scale', "SCALING_FACTOR", "1.0", "Data scaling factor"],
    ['-fill', "FILL_VALUE", "99999.0", "Fill value"],
    ['-resize', "RESIZE", "1.0", "Resize to"]
]

# input
parser = argparse.ArgumentParser()
for v in argValues:
    parser.add_argument(v[0], dest=v[1], default=v[2], help=v[3])
parser.add_argument('-dir', dest="INPUT_DIR", default="data/land_surface_temperature", help="Input directory")
parser.add_argument('-pattern', dest="FILE_PATTERN", default="MOD11C1_E_LSTDA_([0-9\-]+)\.CSV\.gz", help="Input file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/land_surface_temperature/*.png", help="Output file")
args = parser.parse_args()
argv = vars(args)

FILE_PATTERN = re.compile(args.FILE_PATTERN)

for f in os.listdir(args.INPUT_DIR):
    matches = FILE_PATTERN.match(f)

    if matches:
        inFilename = os.path.join(args.INPUT_DIR, f)
        outFilename = args.OUTPUT_FILE.replace("*", matches.group(1))
        command = ['python', 'csvToImg.py']

        for v in argValues:
            command.append(v[0])
            command.append(argv[v[1]])

        command.append('-in')
        command.append(inFilename)
        command.append('-out')
        command.append(outFilename)

        print " ".join(command)
        subprocess.call(command)
