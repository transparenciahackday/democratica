#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict
from django.core.urlresolvers import reverse
from django_extensions.db.fields.json import JSONField
from django.shortcuts import redirect
from democratica.core import text_utils
from deputados.models import MP

class Day(models.Model):
    date = models.DateField()
    top5words = JSONField(null=True)
    parsed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.date)
    def get_absolute_url(self):
        return reverse('day_detail', args=[self.date.year, self.date.month, self.date.day])
    def calculate_top5words(self):
        if self.entry_set.all():
             top5words = text_utils.most_frequent_word(self.entry_set.all(), 5)
             words = []
             for word, count in top5words:
                 words.append({word: count})
             wordict = {'words': words}
             self.top5words = wordict
             self.save()
             output = u""
             for w in self.get_5words_list:
                 output += ' ' + w
             print output
    @property
    def get_5words_list(self):
        return [d.keys()[0] for d in self.top5words['words']]

    def parse_entries(self):
        entries = Entry.objects.filter(day=self)
        for e in entries:
            e.parse_raw_text()
        for e in entries:
            e.calculate_neighbors()
        self.parsed = True
        self.save()

    class Meta:
        ordering = ['date'] 

class Entry(models.Model):
    day = models.ForeignKey(Day)
    position = models.PositiveIntegerField(default=0)
    raw_text = models.TextField('Texto original', max_length=100000)
    html = models.TextField('Texto formatado em HTML', max_length=300000, blank=True)
    
    data = JSONField(null=True)
    mp = models.ForeignKey(MP, blank=True, null=True)
    speaker = models.CharField('Orador', max_length=200, blank=True)
    party = models.CharField('Partido', max_length=200, blank=True)
    text = models.TextField('Texto', max_length=10000, blank=True)
    type = models.CharField('Tipo', max_length=40, blank=True)

    next_id = models.PositiveIntegerField(blank=True, null=True)
    prev_id = models.PositiveIntegerField(blank=True, null=True)

    def extract_data(self):
        pass

    def __unicode__(self):
        if len(self.raw_text) > 30:
            return "<Entry: %s...>" % self.raw_text[:30]
        else:
            return "<Entry: %s>" % self.raw_text

    def get_absolute_url(self): 
        return '/sessoes/%d/%d/%d/%d' % (self.day.date.year, self.day.date.month, self.day.date.day, self.position)

    def calculate_neighbors(self):
        previous = self.get_previous()
        next = self.get_next()
        if previous:
            self.prev_id = previous.id
        if next:
            self.next_id = next.id
        self.save()

    def get_previous(self):
        try:
            return self.__class__.objects.filter(day=self.day, position__lt=self.position).order_by('-position')[0]
        except IndexError:
            return None
    def get_next(self):
        try:
            return self.__class__.objects.filter(day=self.day, position__gt=self.position).order_by('position')[0]
        except IndexError:
            return None

    def parse_raw_text(self):
        if not self.raw_text:
            return None
        from parsing import parse_mp_from_raw_text, find_cont_speaker
        speaker, text = parse_mp_from_raw_text(self.raw_text)
        self.normalize_text()

        if isinstance(speaker, int):
            self.mp = MP.objects.get(id=speaker)
            self.text = text
            self.save()
        elif speaker:
            if speaker == 'pm':
                from deputados.utils import get_pm_from_date
                self.mp = get_pm_from_date(self.day.date)
                self.speaker = 'Primeiro-Ministro'
                self.party = self.mp.current_party
                if self.type == 'deputado_intervencao':
                    self.type = 'pm_intervencao'
                self.save()
            elif speaker.startswith('ministro: '):
                from deputados.utils import get_minister
                speaker = speaker.replace('ministro: ', '').strip()
                if '(' in speaker:
                    speaker = speaker.split('(')[1].rstrip(')')
                    govpost = get_minister(self.day.date, shortname=speaker)
                else:
                    govpost = get_minister(self.day.date, post=speaker)
                if govpost:
                    if govpost.mp:
                        self.mp = govpost.mp
                    else:
                        self.speaker = govpost.person_name
                    self.party = govpost.name
                else:
                    self.speaker = speaker
                self.type = 'ministro_intervencao'
            elif speaker.startswith('secestado: '):
                from deputados.utils import get_minister
                speaker = speaker.replace('secestado: ', '').strip()
                if '(' in speaker:
                    speaker = speaker.split('(')[1].rstrip(')')
                    govpost = get_minister(self.day.date, shortname=speaker)
                else:
                    govpost = get_minister(self.day.date, post=speaker)
                if govpost:
                    if govpost.mp:
                        self.mp = govpost.mp
                    else:
                        self.speaker = govpost.person_name
                    self.party = govpost.name
                else:
                    self.speaker = speaker
                self.type = 'secestado_intervencao'

            elif len(speaker) > 100:
                speaker = speaker[:100]
            else:
                self.speaker = speaker
            self.text = text
            self.save()
        else:
            self.text = self.raw_text
            self.save()
        # special case
        if not self.type in ('continuacao', 'pm_intervencao', 'ministro_intervencao', 'secestado_intervencao'):
            self.determine_type()

        from parsing import guess_if_continuation
        if guess_if_continuation(self):
            self.type = 'continuacao'
            self.save()
            if not self.mp:
                find_cont_speaker(self)

    def determine_type(self):
        from parsing import determine_entry_tag
        self.type = determine_entry_tag(self)
        self.save()
    def normalize_text(self):
        self.text = self.text.replace(u' - ', u' — ')
        if self.text.startswith(u'»'):
            self.text = self.text.replace(u'»', '...', 1)

        self.text = self.text.replace('Primeiro- Ministro', 'Primeiro-Ministro')

        self.save()

    @property
    def raw_text_as_html(self):
        paras = self.raw_text.split('\n')
        output = ''
        for para in paras:
            if self.is_interruption:
                output += '<p class="Mini">%s</p> ' % para 
            else:
                output += '<p>%s</p> ' % para 
        return mark_safe(output)
    @property
    def text_as_html(self):
        if not self.text:
            txt = self.raw_text
        else:
            txt = self.text
        paras = txt.split('\n')
        output = ''
        for para in paras:
            output += '<p>%s</p> ' % para 
        return mark_safe(output)

    @property
    def is_interruption(self):
        if self.type in ('aplauso', 'protesto', 'risos', 'vozes'):
            return True
        return False

    class Meta:
        ordering = ['day', 'position'] 

