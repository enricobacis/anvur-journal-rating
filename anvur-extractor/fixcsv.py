#!/usr/bin/env pypthon
import csv
import sys
import re

filename = sys.argv[1]
outfilename = filename + '.out.csv'
pattern = re.compile(r'\s+')

with open(filename) as fp:
    with open(outfilename, 'w') as ofp:
        csvreader = csv.reader(fp)
        csvwriter = csv.writer(ofp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for rowid, row in enumerate(csvreader):
            csvwriter.writerow([pattern.sub(' ', cell) for cell in row])
