# -*- coding: utf-8 -*-

# Uses command-line utility `h4toh5` to batch convert hdf4 files to hdf5 files
# For UNIX, run this before use: chmod u+x h4toh5

import argparse
import os
import subprocess
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-dir', dest="DIR", default="data", help="Input dir")
args = parser.parse_args()

# Recursively walk through directory
for root, dirs, files in os.walk(args.DIR):
    for f in files:
        if f.endswith(".hdf"):
            h4 = os.path.join(root, f)
            h5 = h4[:-3] + "h5"
            # h5 file not found, create it
            if not os.path.isfile(h5):
                print "Converting %s" % f
                command = ['./h4toh5', h4]
                subprocess.call(command)

print "Done."
