#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from deputados.models import MP

class Session(models.Model):
    date = models.DateField()

class Entry(models.Model):
    session = models.ForeignKey(Session)
    mp = models.ForeignKey(MP, blank=True, null=True)
    speaker = models.CharField('Orador', max_length=100)
    party = models.CharField('Partido', max_length=200, blank=True)
    text = models.TextField('Texto', max_length=10000)


