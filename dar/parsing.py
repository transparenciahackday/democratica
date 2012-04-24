#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from utils import remove_strings
from dar.models import Entry

HONORIFICS = ('O Sr. ', u'A Sr.ª ')
re_separador = (re.compile(ur'\: [\–\–\—\-] ', re.UNICODE), ': - ')

def parse_mp_from_raw_text(text):
    # returns (None, text) if no match
    #         (mp_id, text) if MP match
    #         (speaker, text) if no MP match but separator found
    from democratica.deputados.models import MP, Party
    mp_id = None
    text = text.strip()
    if not text.startswith(HONORIFICS):
        return (None, text)
    # ver se há separador
    has_sep = re.search(re_separador[0], text)
    if not has_sep:
        return (None, text)
    speakerparty, text = re.split(re_separador[0], text, 1)
    speakerparty = remove_strings(speakerparty, HONORIFICS, once=True).strip()
    # FIXME: SECRETARIO DE ESTADO
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
            if MP.objects.filter(shortname=speaker, mandate__party__abbrev=p):
                try:
                    # we got them, woohoo
                    mp = MP.objects.filter(shortname=speaker, mandate__party__abbrev=p).distinct()[0]
                    mp_id = mp.id
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
        if e.speaker in ('O Orador' or 'A Oradora'):
            find_cont_speaker(e)
            return 'continuacao'
        if e.speaker.startswith('Primeiro-Ministro'):
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
        if e.text.startswith((u'Vozes', u'Uma voz d')):
            has_sep = re.search(re_separador[0], e.text)
            if not has_sep:
                return 'vozes_aparte'
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
        elif e.text.startswith(u'Submetido à votação'):
            return 'voto'
        elif e.text.strip() == 'Pausa.':
            return 'pausa'
    return ''

def find_cont_speaker(e):
    '''Quando temos uma intervenção com o speaker "Orador" ou "Oradora", é preciso saber quem é.
    Esta função tenta descobrir andando para trás até chegar a uma intervenção.'''
    counter = 0
    # olha que queryset mai lindo, as entries anteriores ordenadas inversamente
    for prev_entry in Entry.objects.filter(day=e.day, position__lt=e.position).order_by('-position'):
        if (prev_entry.type in ['deputado_intervencao', 'pm_intervencao', 'presidente_intervencao', 'presidente']) or \
           (prev_entry.type == 'continuacao' and prev_entry.mp):
            e.speaker = prev_entry.speaker
            e.type = 'continuacao'
            if prev_entry.mp:
                e.mp = prev_entry.mp
            e.save()
            return
        counter += 1
        # se chegámos a 8 intervenções sem encontrar nada, desistimos
        if counter > 8:
            return

def find_continuations(entries):
    # Depois de vozes, aplauso, protesto, riso ou aparte
    # se é deputado-intervenção, mudar pra continauação
    # se é sem tipo identificado, mudar pra continuação e meter MP?
    pass
    


        
def split_entry(e):
    from democratica.dar.models import Entry
    # splits an entry at '\n\n\n' and creates a new one after it
    txt = e.raw_text
    chunks = txt.split('\n\n\n')
    if len(chunks) == 1:
        return
    elif len(chunks) > 2:
        raise "More than 1 split not implemented"

    for c in chunks:
        # remove double newlines
        c = c.replace('\n\n', '\n')

    text1, text2 = chunks

    next_entry = e.get_next()
    new_position = e.position + (next_entry.position - e.position) / 2

    e.raw_text = text1 
    e.save()
    new_e = Entry.objects.create(day=e.day, raw_text=text2, position=new_position)
    return new_e.id

