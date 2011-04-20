#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe

from deputados.models import MP

class Day(models.Model):
    date = models.DateField()
    def __unicode__(self):
        return str(self.date)
    def get_absolute_url(self):
        return '/dar/%d' % self.id

class Entry(models.Model):
    day = models.ForeignKey(Day)
    mp = models.ForeignKey(MP, blank=True, null=True)
    speaker = models.CharField('Orador', max_length=100)
    party = models.CharField('Partido', max_length=200, blank=True)
    text = models.TextField('Texto', max_length=10000)

    def text_as_html(self):
        paras = self.text.split('\\n')
        output = ''
        for para in paras:
            output += '<p>%s</p> ' % para 
        return mark_safe(output)

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
