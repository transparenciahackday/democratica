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

    def extract_data(self):
        pass

    def __unicode__(self):
        if len(self.raw_text) > 30:
            return "<Entry: %s...>" % self.raw_text[:30]
        else:
            return "<Entry: %s>" % self.raw_text

    def get_absolute_url(self): 
        return '/sessoes/intervencao/%d' % (self.id)

    def get_previous(self):
        return self.objects.filter(day=self.day, position__lt=self.position).order_by('-position')[0]
    def get_next(self):
        return self.objects.filter(day=self.day, position__gt=self.position).order_by('position')[0]

    def parse_raw_text(self):
        if not self.raw_text:
            return None
        from utils import parse_mp_from_raw_text
        speaker, text = parse_mp_from_raw_text(self.raw_text)
        self.determine_type()
        self.normalize_text()

        if isinstance(speaker, int):
            self.mp = MP.objects.get(id=speaker)
            self.text = text
            self.save()
            return self.mp
        elif speaker:
            if len(speaker) > 100:
                speaker = speaker[:100]
            self.speaker = speaker
            self.text = text
            self.save()
            return self.speaker
        else:
            self.text = self.raw_text
            self.save()
            return None

    def determine_type(self):
        from utils import determine_entry_tag
        self.type = determine_entry_tag(self)
        self.save()
    def normalize_text(self):
        self.text = self.text.replace(' - ', u' — ')
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
            if self.is_interruption:
                output += '<p class="mini">%s</p> ' % para 
            else:
                output += '<p>%s</p> ' % para 
        return mark_safe(output)

    @property
    def is_interruption(self):
        if self.type in ('aplauso', 'protesto', 'risos', 'vozes'):
            return True
        return False

    class Meta:
        ordering = ['day', 'position'] 

