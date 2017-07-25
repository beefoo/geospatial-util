# -*- coding: utf-8 -*-

# python batchCsvToImgComposite.py -resize 0.5

import argparse
import os
import re
import subprocess
import sys

argValues = [
    ['-grad', "GRADIENT", "#b2dcff,#7548c9,#212121,#7a3465,#ff3838", "Color gradient"],
    ['-dc', "DEFAULT_COLOR", "#000000", "Default color"],
    ['-range', "DATA_RANGES", " -20:40,-20:40", "Comma-separated data ranges in celsius"],
    ['-unit', "UNIT", "Celsius", "Unit"],
    ['-scale', "SCALING_FACTOR", "1.0", "Data scaling factor"],
    ['-fill', "FILL_VALUE", "99999.0", "Fill value"],
    ['-resize', "RESIZE", "1.0", "Resize to"]
]

# input
parser = argparse.ArgumentParser()
for v in argValues:
    parser.add_argument(v[0], dest=v[1], default=v[2], help=v[3])
parser.add_argument('-dirs', dest="INPUT_DIRS", default="data/land_surface_temperature,data/sea_surface_temperature", help="Input directories")
parser.add_argument('-patterns', dest="FILE_PATTERNS", default="MOD11C1_E_LSTDA_([0-9\-]+)\.CSV\.gz,MYD28W_([0-9\-]+)\.CSV\.gz", help="Input file patterns")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/land_sea_surface_temperature/frame*.png", help="Output file")
args = parser.parse_args()
argv = vars(args)

INPUT_DIRS = args.INPUT_DIRS.split(",")
FILE_PATTERNS = [re.compile(p) for p in args.FILE_PATTERNS.split(",")]

INPUT_DIR_FILES = [os.listdir(d)for d in INPUT_DIRS]

matches = []
for i, files in enumerate(INPUT_DIR_FILES):
    matchIndex = 0
    for f in files:
        m = FILE_PATTERNS[i].match(f)
        if m:
            match = m.group(1)
            inFilename = os.path.join(INPUT_DIRS[i], f)

            if i <= 0:
                matches.append([inFilename])
            elif matchIndex >= len(matches):
                print "Mismatch in number of files!"
                sys.exit(1)
            else:
                matches[matchIndex].append(inFilename)
                matchIndex += 1

if len(matches[-1]) < len(INPUT_DIRS):
    print "Mismatch in number of files!"
    sys.exit(1)

for i, inFilenames in enumerate(matches):

    inFilename = ",".join(inFilenames)
    filename = str(i+1).zfill(len(str(len(matches)))+1)
    outFilename = args.OUTPUT_FILE.replace("*", filename)

    command = ['python', 'csvToImgComposite.py']

    for v in argValues:
        command.append(v[0])
        command.append(argv[v[1]])

    command.append('-in')
    command.append(inFilename)
    command.append('-out')
    command.append(outFilename)

    print " ".join(command)
    subprocess.call(command)
