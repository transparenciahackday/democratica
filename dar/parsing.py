#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from utils import remove_strings
from dar.models import Entry

HONORIFICS = ('O Sr. ', u'A Sr.ª ')
re_separador = (re.compile(ur'\: [\–\–\—\-] ', re.UNICODE), ': - ')

re_concluir = re.compile(ur'(tempo esgotou-se)|(esgotou-se o( seu)? tempo)|((tem (mesmo )?de|queira) (terminar|concluir))|((ultrapassou|esgotou|terminou)[\w ,]* o( seu)? tempo)|((peço|solicito)(-lhe)? que (termine|conclua))|(atenção ao tempo)|(remate o seu pensamento)|(atenção para o tempo de que dispõe)|(peço desculpa mas quero inform)|(deixem ouvir o orador)|(faça favor de prosseguir( a sua)?)|(favor de (concluir|terminar))|(poder prosseguir a sua intervenção)|(faça( o)? favor de continuar|(queira[\w ,]* concluir))', re.UNICODE|re.IGNORECASE)

re_voto = re.compile(ur'^Submetid[oa]s? à votação', re.UNICODE)

def parse_mp_from_raw_text(text):
    # returns (None, text) if no match
    #         (mp_id, text) if MP match
    #         (speaker, text) if no MP match but separator found
    from democratica.deputados.models import MP, Party
    mp_id = None
    text = text.strip()
    if not text.startswith(HONORIFICS):
        if text.startswith(('O Orador:','A Oradora:')):
            speaker, text = re.split(re_separador[0], text, 1)
            return (speaker, text)
        if text.startswith(('Vozes', 'Uma voz d')):
            speaker, text = re.split(re_separador[0], text, 1)
            return (speaker, text)
        return (None, text)
    # ver se há separador
    has_sep = re.search(re_separador[0], text)
    if not has_sep:
        return (None, text)
    speakerparty, text = re.split(re_separador[0], text, 1)
    speakerparty = remove_strings(speakerparty, HONORIFICS, once=True).strip()

    if speakerparty.startswith('Presidente'):
        return (speakerparty, text)
    elif speakerparty.startswith(u'Secretári') and not "Estado" in speakerparty:
        return (speakerparty, text)

    # ugly but works
    if '(' in speakerparty:
        speaker, party = speakerparty.split('(', 1)
        party = party.strip(')')
    else:
        if 'Primeiro' in speakerparty:
            return ('pm', text)
        if 'Ministr' in speakerparty or speakerparty.startswith('Ministr'):
            return ('ministro: ' + speakerparty, text)
        elif u'Secretári' in speakerparty or speakerparty.startswith(u'Secretári'):
            return ('secestado: ' + speakerparty, text)
        return (speakerparty, text)

    if 'Primeiro' in speaker:
        return ('pm', text)
    elif 'Ministr' in speaker or speaker.startswith('Ministr'):
        return ('ministro: ' + speaker, text)
    # já excluímos as entradas dos secretários antes
    elif u'Secretári' in speaker or speaker.startswith(u'Secretári'):
        return ('secestado: ' + speaker, text)

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
        if MP.objects.filter(aka_1=speaker).exists():
            mp = MP.objects.get(aka_1=speaker)
            mp_id = mp.id
        elif MP.objects.filter(aka_2=speaker).exists():
            mp = MP.objects.get(aka_2=speaker)
            mp_id = mp.id
            
    if not mp_id:
        return (speaker, text)
    else:
        return (int(mp_id), text)
    
def determine_entry_tag(e):

    if e.mp and not e.speaker.startswith('Primeiro-Ministro') and not e.speaker.startswith('Ministr') and not (e.speaker.startswith(u'Secretári') and "Estado" in e.speaker) :
        if len(e.text) < 60:
            return 'deputado_aparte'
        else:
            return 'deputado_intervencao'
    elif e.speaker:
        if e.speaker in ('O Orador', 'A Oradora'):
            find_cont_speaker(e)
            return 'continuacao'
        if e.speaker.startswith('Primeiro-Ministro'):
            from deputados.utils import get_pm_from_date
            from deputados.models import MP
            pm_name = get_pm_from_date(e.day.date)
            e.mp = MP.objects.get(shortname=pm_name)
            e.save()
            if len(e.text) < 30:
                return 'pm_aparte'
            else:
                return 'pm_intervencao'
        elif e.speaker.startswith(u'Secretári') and "Estado" in e.speaker:
            if len(e.text) < 30:
                return 'secestado_aparte'
            else:
                return 'secestado_intervencao'
        elif e.speaker.startswith('Ministr'):
            if len(e.text) < 30:
                return 'ministro_aparte'
            else:
                return 'ministro_intervencao'
        elif e.speaker.startswith('Presidente'):
            if re_concluir.search(e.text):
                return 'presidente_aparte'
            return 'presidente'
        elif e.speaker.startswith(u'Secretári') and not "Estado" in e.speaker:
            return 'secretario'
        elif e.speaker.startswith(('Vozes', 'Uma voz d')):
            return 'vozes_aparte'
    else:
        if e.text.startswith(u'Aplauso'):
            return 'aplauso'
        elif e.text.startswith(u'Protesto'):
            return 'protesto'
        elif e.text.startswith(u'Risos'):
            return 'riso'
        elif re_voto.search(e.text):
            return 'voto'
        elif e.text.strip() == 'Pausa.':
            return 'pausa'
        elif not e.speaker and e.text.startswith('Entretanto, assumiu'):
            return 'nota'
        elif e.text.startswith((u'SUMÁRIO', u'S U M Á R I O')):
            return 'sumario'
        elif e.text.startswith(('ORDEM DO DIA', 'ANTES DA ORDEM DO DIA')):
            return 'nota'
        elif e.text.startswith('Eram ') and e.text.strip().endswith('minutos.'):
            return 'hora'
        elif e.text.strip(' :.').endswith((u'presentes à sessão', )) or e.text.startswith('Estavam presentes os seguintes Srs. Deputados:'):
            return 'chamada_presentes'
        elif e.text.endswith((u'faltaram à sessão:', )):
            return 'chamada_ausentes'
        elif e.text.endswith((u'por se encontrarem em missões internacionais:', )):
            return 'chamada_missao'

    return ''

def find_cont_speaker(e):
    '''Quando temos uma intervenção com o speaker "Orador" ou "Oradora", é preciso saber quem é.
    Esta função tenta descobrir andando para trás até chegar a uma intervenção.'''
    counter = 0
    # olha que queryset mai lindo, as entries anteriores ordenadas inversamente
    for prev_entry in Entry.objects.filter(day=e.day, position__lt=e.position).order_by('-position'):
        if (prev_entry.type in ['deputado_intervencao', 'pm_intervencao', 'ministro_intervencao', 'secestado_intervencao', 'presidente_intervencao', 'presidente']) or \
           (prev_entry.type == 'continuacao' and prev_entry.mp):
            # há casos em que o presidente interrompe
            if not counter and prev_entry.type in ('presidente', 'presidente_intervencao'):
                continue
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
    
def guess_if_continuation(e):
    if e.type not in ('deputado_intervencao', 'pm_intervencao', 'ministro_intervencao', 'secestado_intervencao'):
        return False
    prev_e = e.get_previous()
    if prev_e.type in ('deputado_aparte', 'presidente_aparte', 'pm_aparte', 'ministro_aparte', 'secestado_aparte', 'vozes_aparte', 'aplauso', 'protesto', 'riso'):
        return True
    return False



        
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

