# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from thumbs import ImageWithThumbsField
from django_extensions.db.fields.json import JSONField
from democratica.core import text_utils

from south.modelsinspector import add_introspection_rules
add_introspection_rules(
    [([ImageWithThumbsField], [], {"sizes": ["sizes", {}]})],
    ["^deputados.thumbs.ImageWithThumbsField"]
)

class MPManager(models.Manager):
     def get_query_set(self):
        return super(MPManager, self).get_query_set().filter(is_active = True)
class MPAllManager(models.Manager):
     def get_query_set(self):
        return super(MPAllManager, self).get_query_set()


GENDERS = [('F', 'Feminino'),
           ('M', 'Masculino'),
           ('X', 'Não Definido'),
          ]

class MP(models.Model):
    name = models.CharField('Nome completo', max_length=300)
    gender = models.CharField('Género', choices=GENDERS, max_length=1, default='X')
    shortname = models.CharField('Nome abreviado', max_length=200)
    aka_1 = models.CharField('Nome abreviado (alternativa)', max_length=200, blank=True, null=True)
    aka_2 = models.CharField('Nome abreviado (2ª alternativa)', max_length=200, blank=True, null=True)
    dob = models.DateField('Data de nascimento', blank=True, null=True)
    occupation = models.CharField('Profissão', max_length=300, blank=True)
    photo = ImageWithThumbsField('Fotografia', upload_to='fotos', sizes=((18,25), (60,79)), null=True)

    commissions = models.TextField('Comissões', blank=True, max_length=5000)
    education = models.TextField('Formação', blank=True, max_length=5000)
    current_jobs = models.TextField('Cargos actuais', blank=True, max_length=5000)
    jobs = models.TextField('Cargos exercidos', blank=True, max_length=5000)
    awards = models.TextField('Condecorações', blank=True, max_length=5000)

    favourite_word = models.CharField('Palavra preferida', max_length=100, blank=True, null=True, editable=False)
    news = JSONField(null=True, editable=False)
    tweets = JSONField(null=True, editable=False)

    is_active = models.BooleanField('Activo', default=True)
    current_party = models.ForeignKey('Party', verbose_name='Último partido', null=True, editable=False)
    current_mandate = models.ForeignKey('Mandate', related_name='current', null=True, editable=False)

    objects = MPManager()
    all_objects = MPAllManager()

    def update_current_mandate(self):
        if self.mandate_set.all():
            self.current_mandate = self.mandate_set.all()[0]
            self.save()

    def update_current_party(self):
        if self.current_mandate:
            p = self.current_mandate.party
            self.current_party = p
            self.save()

    @property
    def has_facts(self):
        if self.fact_set.exclude(fact_type=FactType.objects.get(name='calculated_Occupation')):
            return True
        return False
    @property
    def has_activities(self):
        return bool(self.activity_set.all())

    def facts_by_type(self, verbose_type):
        fact_type = FactType.objects.get(name=verbose_type)
        return self.fact_set.filter(fact_type=fact_type)

    def post_on(self, gov_number):
        if gov_number:
            if self.governmentpost_set.filter(government=Government.objects.get(number=gov_number)):
                return self.governmentpost_set.filter(government=Government.objects.get(number=gov_number))[0]
        return None

    def mandate_on(self, legislature_number):
        return self.mandate_set.get(legislature__number=legislature_number)

    def has_post_on(self, gov_number):
        if gov_number:
            if self.governmentpost_set.filter(government=Government.objects.get(number=gov_number)):
                return True
        return False

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

    def calculate_favourite_word(self):
        # NOTA: Só procura na XII legislatura
        import datetime
        d = datetime.date(day=20, month=6, year=2011)
        if self.entry_set.filter(day__date__gt=d):
             self.favourite_word = text_utils.most_frequent_word(self.entry_set.filter(day__date__gt=d))
             self.save()

    def get_absolute_url(self):
        return reverse('mp_detail', args=[self.id])
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
    #primary_color = models.CharField('Cor principal', max_length=10)
    #secondary_color = models.CharField('Cor principal', max_length=10)

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

class Government(models.Model):
    number = models.PositiveIntegerField('Número', unique=True)
    date_started = models.DateField('Início do mandato', blank=True, null=True)
    date_ended = models.DateField('Fim do mandato', blank=True, null=True)

    def __unicode__(self): 
        from roman import toRoman
        return toRoman(self.number)
    class Meta:
        verbose_name = 'governo'
        ordering = ['number']

class GovernmentPost(models.Model):
    name = models.CharField('Nome', max_length=200, blank=True)
    person_name = models.CharField('Nome da pessoa', max_length=200, blank=True)
    government = models.ForeignKey(Government)
    mp = models.ForeignKey(MP, null=True)
    date_started = models.DateField('Início do mandato')
    date_ended = models.DateField('Fim do mandato', blank=True, null=True)
    
    def __unicode__(self):
        return 'GC%d: %s' % (self.government.number, self.name)
    class Meta:
        ordering = ['government__number']

class Legislature(models.Model):
    number = models.PositiveIntegerField('Sessão legislativa')
    date_start = models.DateField('Data de início', null=True)
    date_end = models.DateField('Data de fim', null=True)

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

class Mandate(models.Model):
    mp = models.ForeignKey(MP)
    legislature = models.ForeignKey(Legislature)
    date_begin = models.DateField('Data início', blank=True, null=True)
    date_end = models.DateField('Data fim', blank=True, null=True)
    constituency = models.ForeignKey(Constituency)
    party = models.ForeignKey(Party)
    has_activity = models.BooleanField('Tem actividades?')
    has_registointeresses = models.BooleanField('Tem registo de interesses?')

    def __unicode__(self): return '%s (%s - %s)' % (self.mp.shortname, self.legislature, self.party.abbrev)
    class Meta:
        verbose_name = 'mandato'
        ordering = ['-legislature__number']

class Activity(models.Model):
    mp = models.ForeignKey(MP)
    mandate = models.ForeignKey(Mandate)
    type1 = models.CharField('Tipo 1', max_length=50, blank=True)
    type2 = models.CharField('Tipo 2', max_length=50, blank=True)
    number = models.CharField('Número', max_length=50, blank=True)
    content = models.TextField('Conteúdo', max_length=3000)
    legislature = models.ForeignKey(Legislature)
    external_id = models.IntegerField('ID Externo')

    def __unicode__(self): return self.mp.shortname
    class Meta:
        verbose_name = 'actividade'

class LinkSet(models.Model):
    mp = models.OneToOneField(MP, verbose_name="Deputado")
    active = models.BooleanField(default=True, editable=False)
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

    class Meta:
        verbose_name = 'conjunto de links'
        verbose_name_plural = 'conjuntos de links'
