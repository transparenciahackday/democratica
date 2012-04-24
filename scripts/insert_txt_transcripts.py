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
import json
import datetime
import dateutil.parser
import logging
logging.basicConfig(level=logging.WARNING)

from democratica.deputados.models import MP, Party, GovernmentPost
from democratica.dar.models import Entry, Day
from democratica.settings import TRANSCRIPTS_DIR

def parse_long_name(speaker):
    # correct cases where names are too long (a sign that parsing didn't catch
    # the separator before)
    logging.error('MP name too long! (%s)' % speaker)
    return speaker[:20]

def insert_entry(speaker, party, text, type, day):
    # make sure the party name is well formatted
    if len(speaker) > 100: 
        speaker = parse_long_name(speaker)
    party = party.strip('-')
    # try to match the speaker name to an MP entry in the database
    matching_mps = MP.objects.filter(shortname=speaker)
    if matching_mps:
        if len(matching_mps) > 1:
            # more than 1 result for this MP's shortname
            # use the party to determine this
            if Party.objects.filter(abbrev=party):
                p = Party.objects.get(abbrev=party)
            else:
                logging.error('Invalid party (%s) for MP %s' % (party, speaker))
                p = None

            # go on with the search
            if MP.objects.filter(shortname=speaker, caucus__party__abbrev=p):
                try:
                    # we got them, woohoo
                    mp = MP.objects.filter(shortname=speaker, caucus__party__abbrev=p).distinct()[0]
                except MP.MultipleObjectsReturned:
                    logging.warning('More than 1 result for name %s in party %s. Assigning first MP instance.' % (speaker, party))
                    Entry.objects.create(speaker=speaker, party=party, text=text, day=day, type=type)
        else:
            # oh, this was easy, we found them quickly
            mp = MP.objects.get(shortname=speaker)
        # finally, create the Entry object assigned to the correct MP
        try:
            Entry.objects.create(mp=mp, party=party, text=text, day=day, type=type)
        except:
            logging.error('Could not create Entry, even though I thought all was going fine...')
            print mp
            print text
            return 1
    else:
        # no MP's found, maybe a minister?
        if speaker and GovernmentPost.objects.filter(person_name=speaker, date_started__lt=day.date, date_ended__gt=day.date):
            try:
                mp = MP.objects.get(governmentpost__person_name=speaker, governmentpost__date_started__lt=day.date, governmentpost__date_ended__gt=day.date)
            except MP.DoesNotExist:
                # couldn't find one
                print 
            except MP.MultipleObjectsReturned:
                print speaker
                print MP.objects.filter(governmentpost__person_name=speaker, governmentpost__date_started__lt=day.date, governmentpost__date_ended__gt=day.date)
                raise

            Entry.objects.create(mp=mp, party=party, text=text, day=day, type=type)
        elif speaker and speaker not in ('Primeiro-Ministro', 'Presidente', u'Secretário', u'Secretária') and not speaker.startswith('Vozes'):
            # Speaker appears to not be in our database, logging a warning
            logging.warning('Speaker %s not found in our database. Creating Entry without speaker link.' % speaker)
            Entry.objects.create(speaker=speaker, party=party, text=text, day=day, type=type)
        else:
            Entry.objects.create(speaker=speaker, party=party, text=text, day=day, type=type)

def import_session(filename, force=False):
    '''Does a check for existing records and, if all is OK, 
    calls the import_csv_session or import_json_session to parse
    the file.'''

    print filename
    # extract date
    slug = os.path.basename(filename).split('.')[0]
    try:
        dar, serie, leg, sess, date = slug.split('_')
        dt = dateutil.parser.parse(date)
    except ValueError:
        print 'Could not parse date from filename %s. Skipping.' % f
        return 1
    if Day.objects.filter(date=dt):
        if force:
            # we're overwriting
            d = Day.objects.get(date=dt)
            d.delete()
        else:
            logging.warning("There's already a record for %s, not overwriting." % str(date))
            return
    # create the Day instance
    day = Day.objects.create(date=dt)

    # check format and call appropriate function
    if filename.endswith('.txt'):
        lines = open(filename).read().split('\n\n')
        # import each row
        position = 100
        for item in lines:
            raw_text = item.strip()
            Entry.objects.create(raw_text=raw_text, position=position, day=day)
            position += 100

    # process raw text
    #for e in day.entry_set.all():
    #        e.parse_raw_text()

    # finally, get this session's top words
    day.calculate_top5words()
        
def insert_favorite_words():
    logging.info('A calcular palavras preferidas...')
    for mp in MP.objects.all():
        mp.calculate_favourite_word()

if __name__ == '__main__':
    import sys
    from ConfigParser import SafeConfigParser

    # analisar as opções da linha de comandos
    import optparse
    # print 'ARGV      :', sys.argv[1:]
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', 
                      dest="input", 
                      default="",
                      help='Input file or directory'
                      )
    parser.add_option('-v', '--verbose',
                      dest="verbose",
                      default=False,
                      action="store_true",
                      help='Print verbose information',
                      )
    parser.add_option('-p', '--picky',
                      dest="picky",
                      default=False,
                      action="store_true",
                      help='Stop batch processing in case an error is found',
                      )
    parser.add_option('-f', '--force',
                      dest="force",
                  default=False,
                  action="store_true",
                  help='Process file even if the output file already exists',
                  )

    options, remainder = parser.parse_args()
    input = options.input
    verbose = options.verbose
    picky = options.picky

    # verificar se input existe
    if not os.path.exists(input):
        print 'Input not found: ' + str(input)
        print 'Did you use the -i flag?'
        sys.exit()
    if not (os.path.isfile(input) or os.path.isdir(input)):
        print 'Input must be a valid file or directory name.'
        sys.exit()
    # há input e não output? gravar como txt no mesmo dir
    if os.path.isfile(input):
        # input é ficheiro
        import_session(input, force=options.force)
    else:
        # input é directório, processar os ficheiros lá dentro
        for root, dirs, files in os.walk(input):
            for f in files:
                result = import_session(os.path.join(input, f), force=options.force)
                if result:
                    logging.error('Errors found while trying to import file %s.' % f)
                    if picky:
                        logging.error('Picky option set, quitting.')
                        sys.exit()

    # tudo acabado, calcular palavras preferidas
    # insert_favorite_words()

