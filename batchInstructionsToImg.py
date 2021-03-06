# -*- coding: utf-8 -*-

# python batchInstructionsToImg.py -keys sea_surface_temperature

import argparse
from datetime import datetime
import json
import os
from pprint import pprint
import re
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="data/instructions.json", help="Path to instruction file")
parser.add_argument('-keys', dest="KEYS", default="land_sea_surface_temperature", help="Comma-separated list of keys to process")
args = parser.parse_args()

KEYS = args.KEYS.split(",")

def dateToSeconds(dateString):
    parts = dateString.split('-')
    year = int(parts[0])
    month = int(parts[1])
    day = 14
    if len(parts) > 2:
        day = int(parts[2])
    dt = datetime(year, month, day)
    unix = datetime(1970,1,1)
    return (dt - unix).total_seconds()

data = {}
with open(args.INPUT_FILE) as f:
    data = json.load(f)

for key in data:
    if key in KEYS or KEYS=="all":
        entry = data[key]
        matches = []
        for path in entry["in"]:
            # Read files and find matches
            pathParts = path.split("/")
            fileDir = "/".join(pathParts[0:-1])
            pattern = pathParts[-1]
            pattern = re.compile(pattern)
            fileMatches = []

            filenames = os.listdir(fileDir)
            for filename in filenames:
                m = pattern.match(filename)
                if m:
                    match = m.group(1)
                    filePath = os.path.join(fileDir, filename)
                    fileMatches.append({
                        "match": match,
                        "filePath": filePath
                    })
            fileMatches = sorted(fileMatches, key=lambda k: k['filePath'])
            matches.append(fileMatches)

        temp = matches[:]
        temp.sort(key=len, reverse=True)
        target = temp[0]
        targetLen = len(temp[0])
        print "Target length: %s" % targetLen

        # build batch
        batch = [[] for i in range(targetLen)]
        for fmatches in matches:
            # same length as target, just add
            if len(fmatches)==targetLen:
                for i, f in enumerate(fmatches):
                     batch[i].append(f["filePath"])

            # otherwise try to find a match yyyy-mm to yyyy-mm-dd
            else:
                # for each yyyy-mm-dd
                for i, f in enumerate(target):
                    found = False
                    # for each yyyy-mm
                    for j, ff in enumerate(fmatches):
                        if ff["match"] in f["match"]:
                            batch[i].append(ff["filePath"])
                            found = True
                            break
                    # if could not find, add the closest
                    if not found:
                        fdate = dateToSeconds(f["match"])
                        closest = fmatches[0]["filePath"]
                        closestDelta = sys.maxint
                        for j, ff in enumerate(fmatches):
                            ffdate = dateToSeconds(ff["match"])
                            delta = abs(ffdate-fdate)
                            if delta < closestDelta:
                                closest = ff["filePath"]
                        batch[i].append(closest)

        # Make commands
        for i, filenames in enumerate(batch):

            inFilename = ",".join(filenames)
            filename = str(i+1).zfill(len(str(targetLen))+1)
            outFilename = entry["out"].replace("*", filename)

            command = ['python', entry["command"]]

            for key in entry["options"]:
                command.append("-"+key)
                command.append(entry["options"][key])

            command.append('-in')
            command.append(inFilename)
            command.append('-out')
            command.append(outFilename)

            print " ".join(command)
            subprocess.call(command)
