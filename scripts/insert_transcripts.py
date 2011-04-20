#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script para criar os modelos do Django a partir das transcrições do DAR
Copyright 2010-2011 Ricardo Lafuente <r@sollec.org>

Licenciado segundo a GPL v3
http://www.gnu.org/licenses/gpl.html
'''


### Set up Django path
import sys, os
projectpath = os.path.abspath('../../')
if projectpath not in sys.path:
    sys.path.append(projectpath)
    sys.path.append(os.path.join(projectpath, 'democratica/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'democratica.settings'

import csv
import datetime, time
import dateutil.parser
import logging


from democratica.deputados.models import MP, Party, GovernmentPost
from democratica.dar.models import Entry, Day
from democratica.settings import TRANSCRIPTS_DIR

print 'A importar transcrições...'
d = os.path.join(projectpath, 'democratica', TRANSCRIPTS_DIR)
for root, dirs, files in os.walk(d):
    for f in files:
        print f
        if not f.endswith('csv'):
            continue
        
        slug = f.split('.')[0]
        dar, serie, leg, sess, date = slug.split('_')

        try:
            dt = dateutil.parser.parse(date)
        except ValueError:
            dt = None

        if not dt:
            print 'File %s has a strange date format. Ignoring.' % f
            continue

        if Day.objects.filter(date=date):
            s = Day.objects.get(date=date)
        else:
            s = Day.objects.create(date=date)

        filename = os.path.join(d, f)

        lines = csv.reader(open(filename), delimiter='|', quotechar='"')

        for item in lines:
            if len(item) != 4:
                logging.error('Illegal row -- %d cols instead of 4!' % len(item))
                continue
            mpname, party, text, type = item

            #print mpname
            #print party
            # make sure the party name is well formatted
            if len(mpname) > 100: 
                print 'MP name too long! (%s)' % mpname
                mpname = 'LONG_NAME_ERROR'
            party = party.strip('-')
            matching_mps = MP.objects.filter(shortname=mpname)
            if matching_mps:
                if len(matching_mps) > 1:
                    # more than 1 result for this MP's shortname
                    # use the party to determine this
                    if Party.objects.filter(abbrev=party):
                        p = Party.objects.get(abbrev=party)
                    else:
                        print 'Invalid party (%s)' % party
                        p = None

                    try:
                        mp = MP.objects.filter(shortname=mpname, caucus__party__abbrev=p).distinct()[0]
                    except MP.MultipleObjectsReturned:
                        print 'More than 1 result for name %s in party %s. Assigning first MP instance.' % (mpname, party)
                        Entry.objects.create(speaker=mpname, party=party, text=text, day=s, type=type)
                else:
                    mp = MP.objects.get(shortname=mpname)
                Entry.objects.create(mp=mp, party=party, text=text, day=s, type=type)
            else:
                if GovernmentPost.objects.filter(name=mpname):
                    mp = MP.objects.get(governmentpost__name=mpname)
                    Entry.objects.create(mp=mp, party=party, text=text, day=s, type=type)
                else:
                    Entry.objects.create(speaker=mpname, party=party, text=text, day=s, type=type)

print 'A calcular palavras preferidas...'
for mp in MP.objects.all():
    mp.calculate_favourite_word()
