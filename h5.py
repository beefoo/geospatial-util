# -*- coding: utf-8 -*-

# chmod u+x h5dump

import argparse
import h5py

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/land_surface_temperature/MOD11C3.A2016001.006.2016234032549.h5", help="Input file")
args = parser.parse_args()

with h5py.File(args.INPUT_FILE,'r') as f:

    for key, group in f.items():
        print "\n----\nGROUP: %s" % key
        # for name, value in group.attrs.items():
        #     print "%s: %s" % (name, value)
        data = list(f[key])
        print "Data size: %s" % len(data)
        if len(data) > 0:
            # print "Sample: %s" % data[0]
            # print type(data[0])

            if type(data[0]) is unicode:
                for d in data:
                    dataset = group[d]
                    print "Datasets: %s" % len(dataset)
                    for dkey, ditem in dataset.items():
                        print "  %s (%s x %s)" % (dkey, len(ditem), len(ditem[0]))
