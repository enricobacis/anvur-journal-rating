#!/usr/bin/env python
import scraperwiki
import stdnum.issn
import itertools
import requests
import csv
import re

# configuration
areas = (8, 10, 11, 12, 13, 14)
types = ('SCIE', 'CLA')
base_url = 'http://www.anvur.org/attachments/article/254/AREA%d_%s.pdf'
base_filename = 'AREA%d_%s.txt'
fixups_filename = 'fixups.csv'


class ISSN_Extractor:

    def __init__(self, fixups=None):
        self._fixups = self._get_fixups(fixups) if fixups else dict()

    def validate_issn(self, ISSN):
        try:
            stdnum.issn.validate(ISSN)
            return ISSN
        except:
            if ISSN in self._fixups: return self._fixups[ISSN]
            else: print('ignore invalid ISSN: %s' % ISSN)

    def extract_issns(self, data):
        xml = scraperwiki.pdftoxml(data)
        pattern = re.compile(r'\b\d\d\d\d-\d\d\d[\dxX]\b')
        return list(filter(None, map(self.validate_issn, pattern.findall(xml))))

    def get_issns_from_url(self, url):
        response = requests.get(url)
        return self.extract_issns(response.content)

    @staticmethod
    def _get_fixups(filename):
        with open(filename) as csvfile:
            return dict(csv.reader(csvfile))


extractor = ISSN_Extractor(fixups=fixups_filename)
for area, type in itertools.product(areas, types):
    url = base_url % (area, type)
    outfile = base_filename % (area, type)
    print('extracting data from %s ...' % url)

    ISSNs = extractor.get_issns_from_url(url)
    with open(outfile, 'w') as fp:
        for ISSN in ISSNs:
            fp.write('%s\n' % ISSN)

    print('%d ISSNs extracted and saved to %s\n' % (len(ISSNs), outfile))
