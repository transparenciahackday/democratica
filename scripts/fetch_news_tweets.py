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
import datetime
import dateutil.parser
import logging

from democratica.deputados import utils

from democratica.deputados.models import MP, Party, GovernmentPost
from democratica.dar.models import Entry, Day
from democratica.settings import TRANSCRIPTS_DIR
'''
print '--------------------'
print 'A importar tweets...'
print '--------------------'
print 
for mp in MP.objects.filter(linkset__twitter_url__contains='twitter'):
    print 'Tweets: %s' % mp.shortname
    tweets =  utils.get_tweets_for_mp(mp)
    if not tweets:
        print '...Não há tweets!'
    mp.news = tweets
    mp.save()
'''
print '----------------------'
print 'A importar notícias...'
print '----------------------'
print 
# só queremos deputados que estejam nas transcrições
# FIXME: alargar isto a todos!!

for id in frozenset(Entry.objects.values_list('mp', flat=True)):
    if id:
        mp = MP.objects.get(id=id)
        print mp.shortname
        mp.news = utils.get_news_for_mp(mp)
        mp.save()
    
