from django.db import models

from djutils.decorators import async, memoize, throttle, cached_for_model
from djutils.db.fields import SmartSlugField, StatusField
from djutils.db.managers import PublishedManager


class Simple(models.Model):
    slug = SmartSlugField(max_length=5)
    
    class FakeTagManager(object):
        def most_common(self):
            return ['apple', 'orange']
    
    class Meta:
        ordering = ('id',)
    
    tags = FakeTagManager()
    
    @cached_for_model(60)
    def get_cached_data(self, some_arg):
        return self.slug


class Complex(models.Model):
    title = models.CharField(max_length=100)
    slug = SmartSlugField(
        source_field='title',
        date_field='pub_date',
        split_on_words=True,
        max_length=10)
    pub_date = models.DateTimeField()


class UnderscoresNumerals(models.Model):
    slug_underscores = SmartSlugField(max_length=10)
    slug_numerals = SmartSlugField(underscores=False, max_length=10)


class StatusModel(models.Model):
    status = StatusField()
    
    objects = PublishedManager('status')


class BaseNote(models.Model):
    message = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    status = StatusField()
    
    objects = PublishedManager()
    
    class Meta:
        abstract = True


class Note1(BaseNote):
    pass

class Note2(BaseNote):
    pass

class Note3(BaseNote):
    pass
