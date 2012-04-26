#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Set up Django path
import sys, os
projectpath = os.path.abspath('../../')
if projectpath not in sys.path:
    sys.path.append(projectpath)
    sys.path.append(os.path.join(projectpath, 'democratica/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'democratica.settings'

import csv
import json
import datetime
import dateutil.parser
import logging
logging.basicConfig(level=logging.INFO)

from democratica.deputados.models import MP, Party, GovernmentPost
from democratica.dar.models import Entry, Day
from democratica.settings import TRANSCRIPTS_DIR

DATE = sys.argv[1]

if len(sys.argv) != 2:
    print 'Usage: python parse_day_entries.py <yyyy-mm-dd>'
    sys.exit()

d = Day.objects.get(date=dateutil.parser.parse(DATE).date())
entries = d.entry_set.all()
for e in entries:
    e.parse_raw_text()
for e in entries:
    e.calculate_neighbors()


