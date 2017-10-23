# -*- coding: utf-8 -*-

# Uses command-line utility `gdal_translate` to batch convert GeoTIFF files to Gzipped CSV files
# e.g. python geotiffToCsv.py -in geotiff/water_vapor_m -out data/water_vapor_m

import argparse
import gzip
import os
import shutil
import subprocess
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_DIR", default="data", help="Input dir")
parser.add_argument('-out', dest="OUTPUT_DIR", default="data", help="Input dir")
args = parser.parse_args()

# Recursively walk through directory
for root, dirs, files in os.walk(args.INPUT_DIR):
    for f in files:
        if f.endswith(".TIFF"):
            tiff = os.path.join(root, f)
            asc = tiff[:-4] + "asc"
            csv = args.OUTPUT_DIR + "/" + f[:-4] + "csv"
            print csv
            # csv file not found, create it
            if not os.path.isfile(csv + '.gz'):
                print "Converting %s to ASCII..." % f
                command = ['gdal_translate', '-of', 'AAIGrid', tiff, asc]
                # subprocess.call(command)
                finished = subprocess.check_call(command)
                command = ['python', 'ascToCsv.py', '-in', asc, '-out', csv]
                finished = subprocess.check_call(command)
                # compress file
                print "Compressing CSV file..."
                with open(csv, 'rb') as f_in, gzip.open(csv + '.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                # delete temp file
                os.remove(csv)
                os.remove(asc)
                os.remove(asc + ".aux.xml")
                os.remove(tiff[:-4] + "prj")

print "Done."
