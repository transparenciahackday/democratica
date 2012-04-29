import datetime

from django.db import models
from django.template.defaultfilters import slugify

from djutils import constants


class StatusField(models.IntegerField):
    """
    Field to store status of model instance, i.e. "LIVE", "DRAFT", "DELETED".
    Used by the :class:`djutils.db.managers.PublishedManager`
    """
    def __init__(self, *args, **kwargs):
        defaults = {
            'choices': constants.STATUS_CHOICES,
            'default': constants.LIVE_STATUS,
            'db_index': True
        }
        defaults.update(kwargs)
        super(StatusField, self).__init__(*args, **defaults)
    
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.IntegerField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class SmartSlugField(models.SlugField):
    """
    Field that generates unique slugs in the event of collisions, optionally
    accepting a date-field.
    
    Example usage::
    
        title = models.CharField(max_length=255)
        pub_date = models.DateTimeField(auto_now_add=True)
        slug = SmartSlugField(
            source_field='title',
            date_field='pub_date',
            split_on_words=True
        )
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        :param source_field: optional string field to use as source for the slug, i.e. 'title'
        :param date_field: optional date field on which to enforce slug unique-ness,
        :param split_on_words: boolean whether to only break up slug on spaces
        :param underscores: whether to append underscores to generated slug to
            enforce unique-ness, if False will append numbers, i.e. slug-1, slug-2
        """
        self.source_field = kwargs.pop('source_field', None)
        self.date_field = kwargs.pop('date_field', None)
        self.split_on_words = kwargs.pop('split_on_words', False)
        self.underscores = kwargs.pop('underscores', True)
        kwargs['unique'] = self.date_field is None
        kwargs['editable'] = self.source_field is None
        super(SmartSlugField, self).__init__(*args, **kwargs)

    def _generate_date_query(self, dt):
        return {
            '%s__year' % self.date_field: dt.year,
            '%s__month' % self.date_field: dt.month,
            '%s__day' % self.date_field: dt.day
        }

    def pre_save(self, instance, add):
        potential_slug = getattr(instance, self.attname)

        if self.source_field:
            potential_slug = slugify(getattr(instance, self.source_field))
        
        model = instance.__class__

        if self.date_field:
            query = self._generate_date_query(getattr(instance, self.date_field))
        else:
            query = {}
        base_qs = model._default_manager.filter(**query)

        if self.split_on_words and len(potential_slug) > self.max_length:
            pos = potential_slug[:self.max_length + 1].rfind('-')
            if pos > 0:
                potential_slug = potential_slug[:pos]

        potential_slug = slug = potential_slug[:self.max_length]
                
        if instance.pk is not None:
            base_qs = base_qs.exclude(pk=instance.pk)

        i = 0
        while base_qs.filter(**{self.attname: potential_slug}).count() > 0:
            i += 1
            if self.underscores:
                suffix = '_' * i
            else:
                suffix = '-%s' % i
            potential_slug = '%s%s' % (slug[:self.max_length - len(suffix)], suffix)

        setattr(instance, self.attname, potential_slug)
        return potential_slug
        
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.SlugField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
