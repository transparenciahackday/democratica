#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

HONORIFICS = ('O Sr. ', u'A Sr.ª ')
re_separador = (re.compile(ur'\: [\–\–\—\-] ', re.UNICODE), ': - ')

def remove_strings(st, strings_tuple, once=False):
    for s in strings_tuple:
        if once:
            st = st.replace(s, '', 1)
        else:
            st = st.replace(s, '')
    return st

def parse_mp_from_raw_text(text):
    # returns (None, text) if no match
    #         (mp_id, text) if MP match
    #         (speaker, text) if no MP match but separator found
    from democratica.deputados.models import MP, Party
    mp_id = None
    text = text.strip()
    if not text.startswith(HONORIFICS):
        return (None, text)
    text = remove_strings(text, HONORIFICS, once=True).strip()

    # ver se há separador
    has_sep = re.search(re_separador[0], text)
    if not has_sep:
        return (None, text)
    speakerparty, text = re.split(re_separador[0], text, 1)
    speakerparty = speakerparty.strip()
    if speakerparty.startswith(('Presidente', u'Secretári')):
        return (speakerparty, text)
    if '(' in speakerparty:
        speaker, party = speakerparty.split('(', 1)
        party = party.strip(')')
    else:
        return (speakerparty, text)

    # try to match the speaker name to an MP entry in the database
    matching_mps = MP.objects.filter(shortname=speaker)
    if matching_mps:
        if len(matching_mps) > 1:
            # more than 1 result for this MP's shortname
            # use the party to determine this
            if Party.objects.filter(abbrev=party):
                p = Party.objects.get(abbrev=party)
            else:
                pass

            # go on with the search
            if MP.objects.filter(shortname=speaker, caucus__party__abbrev=p):
                try:
                    # we got them, woohoo
                    mp = MP.objects.filter(shortname=speaker, caucus__party__abbrev=p).distinct()[0]
                    mp_id = MP.id
                except MP.MultipleObjectsReturned:
                    logging.warning('More than 1 result for name %s in party %s. Assigning first MP instance.' % (speaker, party))
        else:
            # oh, this was easy, we found them quickly
            mp = MP.objects.get(shortname=speaker)
            mp_id = mp.id
    else:
        # FIXME: no MP's found, maybe a minister?
        pass
    if not mp_id:
        return (None, text)
    else:
        return (int(mp_id), text)
    
def determine_entry_tag(e):
    if e.mp and not e.speaker.startswith('Primeiro-Ministro'):
        if len(e.text) < 60:
            return 'deputado_aparte'
        else:
            return 'deputado_intervencao'
    elif e.speaker:
        if e.speaker.startswith('Primeiro-Ministro'):
            # TODO: fetch prime minister mp id
            from deputados.utils import get_pm_from_date
            from deputados.models import MP
            pm_name = get_pm_from_date(e.day.date)
            e.mp = MP.objects.get(shortname=pm_name)
            e.save()
            return 'pm_intervencao'

        elif e.speaker.startswith('Presidente'):
            return 'presidente'
        elif e.speaker.startswith(u'Secretári'):
            return 'secretario'
    else:
        if e.text.startswith(u'Vozes'):
            has_sep = re.search(re_separador[0], e.text)
            if not has_sep:
                return (None, e.text)
            speaker, text = re.split(re_separador[0], e.text, 1)
            e.speaker = speaker
            e.text = text
            e.save()
            return 'vozes_aparte'
        elif e.text.startswith(u'Aplauso'):
            return 'aplauso'
        elif e.text.startswith(u'Protesto'):
            return 'protesto'
        elif e.text.startswith(u'Risos'):
            return 'riso'

        if e.text.startswith(u'Submetido à votação'):
            return 'voto'

        elif e.text == 'Pausa.':
            return 'pausa'

    return ''


def split_entry(e):
    from democratica.dar.models import Entry
    # splits an entry at '\n\n' and creates a new one after it
    txt = e.raw_text
    chunks = txt.split('\n\n')
    if len(chunks) == 1:
        return
    elif len(chunks) > 2:
        raise "More than 1 split not implemented"

    text1, text2 = chunks

    next_entry = Entry.objects.filter(position__gt=e.position)[0]
    new_position = e.position + (next_entry.position - e.position)/2

    e.raw_text = text1 
    e.save()
    new_e = Entry.objects.create(day=e.day, raw_text=text2, position=new_position)
    return new_e

def get_dates(sess, leg):
    pass

from haystack.utils import Highlighter
from django.utils.html import strip_tags

class MyHighlighter(Highlighter):
    prev_chars = 10

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        start_offset -= self.prev_chars
        end_offset -= self.prev_chars
        return self.render_html(highlight_locations, start_offset, end_offset)



