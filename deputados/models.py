# -*- coding: utf-8 -*-

from django.db import models

GENDERS = [('F', 'Feminino'),
           ('M', 'Masculino'),
           ('X', 'Não Definido'),
          ]

class MP(models.Model):
    name = models.CharField('Nome completo', max_length=300)
    gender = models.CharField('Género', choices=GENDERS, max_length=1, default='X')
    shortname = models.CharField('Nome abreviado', max_length=200)
    dob = models.DateField('Data de nascimento', blank=True, null=True)
    occupation = models.CharField('Profissão', max_length=300, blank=True)
    photo = models.ImageField('Fotografia', upload_to='mp-photos', null=True)

    @property
    def current_caucus(self):
        return self.caucus_set.all()[0]
    @property
    def current_party(self):
        return self.current_caucus.party

    def has_facts(self):
        if self.fact_set.exclude(fact_type=FactType.objects.get(name='calculated_Occupation')):
            return True
        return False
    def has_activities(self):
        return bool(self.activity_set.all())

    def facts_by_type(self, verbose_type):
        fact_type = FactType.objects.get(name=verbose_type)
        return self.fact_set.filter(fact_type=fact_type)

    @property
    def article(self):
        if self.gender == 'M':
            return 'o'
        elif self.gender == 'F':
            return 'a'
        elif self.gender == 'X':
            return 'x'
        else:
            return 'XXX'

    @property
    def condecoracoes(self): return self.facts_by_type('Condecoracoes')
    @property
    def cargos_exercidos(self): return self.facts_by_type('CargosExercidos')
    @property
    def cargos_actuais(self): return self.facts_by_type('CargosDesempenha')
    @property
    def habilitacoes(self): return self.facts_by_type('HabilitacoesLiterarias')
    @property
    def comissoes(self): return self.facts_by_type('Comissoes')

    def __unicode__(self): return self.shortname
    class Meta:
        verbose_name = 'deputado'
        ordering = ['shortname']

class Party(models.Model):
    name = models.CharField('Nome', max_length=100, blank=True)
    abbrev = models.CharField('Sigla', max_length=20)
    tendency = models.CharField('Orientação', max_length=50)
    info = models.TextField('Observações', max_length=2000)
    has_mps = models.BooleanField('Tem ou teve deputados?', default=True)

    def __unicode__(self): return self.abbrev
    class Meta:
        verbose_name = 'partido'

class FactType(models.Model):
    name = models.CharField('Nome', max_length=100)

    def __unicode__(self): return self.name
    class Meta:
        verbose_name = 'tipo de facto'
        verbose_name_plural = 'tipos de facto'

class Fact(models.Model):
    mp = models.ForeignKey(MP)
    fact_type = models.ForeignKey(FactType)
    value = models.TextField('Valor', max_length=2000)

    def __unicode__(self): return "%s - %s" % (self.fact_type.name, self.value)
    class Meta:
        verbose_name = 'facto'

class Session(models.Model):
    number = models.PositiveIntegerField('Sessão legislativa')

    def __unicode__(self): 
        from roman import toRoman
        return toRoman(self.number)
    class Meta:
        verbose_name = 'sessão legislativa'
        verbose_name_plural = 'sessões legislativas'

class Constituency(models.Model):
    name = models.CharField('Nome', max_length=100)
    article = models.CharField('Artigo', max_length=3)

    def __unicode__(self): return self.name
    class Meta:
        verbose_name = 'círculo eleitoral'
        verbose_name_plural = 'círculos eleitorais'
        ordering = ['name']

class Caucus(models.Model):
    mp = models.ForeignKey(MP)
    session = models.ForeignKey(Session)
    date_begin = models.DateField('Data início', blank=True, null=True)
    date_end = models.DateField('Data fim', blank=True, null=True)
    constituency = models.ForeignKey(Constituency)
    party = models.ForeignKey(Party)
    has_activity = models.BooleanField('Tem actividades?')
    has_registointeresses = models.BooleanField('Tem registo de interesses?')

    def __unicode__(self): return self.mp.shortname
    class Meta:
        verbose_name = 'caucus'
        verbose_name_plural = 'caucuses'
        ordering = ['-session__number']

class Activity(models.Model):
    mp = models.ForeignKey(MP)
    caucus = models.ForeignKey(Caucus)
    type1 = models.CharField('Tipo 1', max_length=50, blank=True)
    type2 = models.CharField('Tipo 2', max_length=50, blank=True)
    number = models.CharField('Número', max_length=50, blank=True)
    session = models.PositiveIntegerField('Sessão', blank=True)
    content = models.TextField('Conteúdo', max_length=3000)
    external_id = models.IntegerField('ID Externo')

    def __unicode__(self): return self.mp.shortname
    class Meta:
        verbose_name = 'actividade'

class LinkSet(models.Model):
    mp = models.OneToOneField(MP)
    active = models.BooleanField(default=True)
    email = models.EmailField('E-mail', blank=True)
    wikipedia_url = models.URLField('Wikipedia', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    twitter_url = models.URLField('Twitter', blank=True)
    blog_url = models.URLField('Blog', blank=True)
    website_url = models.URLField('Website', blank=True)
    linkedin_url = models.URLField('LinkedIn', blank=True)
    twitica_url = models.URLField('Twitica', blank=True)
    radio_url = models.CharField('Programa de rádio', max_length=200, blank=True)
    tv_url = models.CharField('Programa de televisão', max_length=200, blank=True)
