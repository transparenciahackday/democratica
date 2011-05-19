#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
import datetime
import jsonfield
from democratica.core import text_utils

from deputados.models import MP

class Day(models.Model):
    date = models.DateField()
    top5words = jsonfield.JSONField(null=True)

    def __unicode__(self):
        return str(self.date)
    def get_absolute_url(self):
        return reverse('day_detail', args=[self.date.year, self.date.month, self.date.day])
    def calculate_top5words(self):
        if self.entry_set.all():
             top5words = text_utils.most_frequent_word(self.entry_set.all(), 5)
             print top5words
             #self.save()

class Entry(models.Model):
    day = models.ForeignKey(Day)
    mp = models.ForeignKey(MP, blank=True, null=True)
    speaker = models.CharField('Orador', max_length=100)
    party = models.CharField('Partido', max_length=200, blank=True)
    text = models.TextField('Texto', max_length=10000)
    type = models.CharField('Tipo', max_length=40)

    def text_as_html(self):
        paras = self.text.split('\\n')
        output = ''
        for para in paras:
            output += '<p>%s</p> ' % para 
        return mark_safe(output)

    def text_as_html_plain(self):
        return mark_safe(self.text)

    @property
    def is_applause(self):
        if '*** Aplausos ***' in self.text:
            return True
        return False

    @property
    def is_protest(self):
        if '*** Protestos ***' in self.text:
            return True
        return False

    @property
    def is_interruption(self):
        if self.is_protest or self.is_applause:
            return False
        if 'Muito bem!' in self.text:
            return True
        # see if it's a short intervention
        if len(self.text.split(' ')) < 10:
            return True
        return False

    @property
    def is_regular(self):
        if self.is_applause or self.is_protest or self.is_interruption:
            return False
        return True

    def __unicode__(self):
        if self.mp:
            return '%s (%s)' % (self.mp.shortname, str(self.day.date))
        else:
            return '%s (%s)' % (self.speaker, str(self.day.date))

    def get_absolute_url(self): return '/dar/%d#%d' % (self.day.id, self.id)
