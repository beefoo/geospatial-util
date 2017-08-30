# -*- coding: utf-8 -*-

# python h5range.py -in data/co2_m/AIRS.2015.03.01.L3.CO2Std_IR031.v5.9.14.0.IRonly.X15098105512.h5 -dataset "CO2,Data Fields,mole_fraction_of_carbon_dioxide_in_free_troposphere"

import argparse
import h5py
from pprint import pprint
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/co2_m/AIRS.2015.03.01.L3.CO2Std_IR031.v5.9.14.0.IRonly.X15098105512.h5", help="Input file")
parser.add_argument('-dataset', dest="DATASET", default="CO2,Data Fields,mole_fraction_of_carbon_dioxide_in_free_troposphere", help="Dataset")
parser.add_argument('-fill', dest="FILL_VALUE", default=-9999, type=int, help="Fill value")
args = parser.parse_args()

DATASET_PATH = args.DATASET.split(",")

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

    height = len(dataset)
    width = len(dataset[0])
    total = width * height
    print "Dimensions: %s x %s" % (width, height)

    minValue = None
    maxValue = None
    sumValue = 0
    count = 0

    for y in range(height):
        for x in range(width):
            i = y * width + x
            value = dataset[y, x]
            if value != args.FILL_VALUE:
                if minValue is None or value < minValue:
                    minValue = value
                if maxValue is None or value > maxValue:
                    maxValue = value
                sumValue += value
                count += 1

            sys.stdout.write('\r')
            sys.stdout.write("%s%%" % round(1.0*i/total*100,1))
            sys.stdout.flush()

    print "Range: [%s, %s]" % (minValue, maxValue)
    print "Avg: %s" % (1.0*sumValue/count)
