Database utils
==============

Fields
------

.. py:module:: djutils.db.fields

This library includes several subclasses of django model fields.


StatusField
^^^^^^^^^^^

.. py:class:: StatusField(models.IntegerField)

    Field to store status of model instance, i.e. "LIVE", "DRAFT", "DELETED".
    Used by the :class:`djutils.db.managers.PublishedManager` to expose the
    :func:`published` method.
    
    Example::
    
        from django.db import models
        
        from djutils.db.fields import StatusField
        from djutils.db.managers import PublishedManager
    
        class BlogEntry(models.Model):
            title = models.CharField(max_length=255)
            body = models.TextField()
            status = StatusField()
            
            objects = PublishedManager('status') # use the status field
    
    To return only those blog entries whose status is LIVE, we can query
    the manager::
    
        >>> published_blogs = BlogEntry.objects.published()


SmartSlugField
^^^^^^^^^^^^^^

.. py:class:: SmartSlugField(models.SlugField)

    Field that generates unique slugs in the event of collisions, optionally
    accepting a date-field.
    
    It attempts to automate several of the pain-points with SlugFields:
        
        * collisions:
            if a slug is specified as unique, a collision can cause you to get
            IntegrityErrors in your database -- if you're using your slug fields
            with a date_field (i.e. /news/2010/mar/5/some-headline/) then you
            will want to validate uniqueness for that day only.
        
        * autopopulation:
            a slug is generally a URL-friendly representation of another field,
            such as a headline or title
        
        * truncation:
            slugs can be truncated in such a way as to not break up a word, so
            instead of "some-interesting-headli" you'd get "some-interesting"
        
        * underscores or numbers:
            if a collision is encountered, you can either append underscores
            or use a number::
            
                underscores: "slug", "slug_", "slug__", "slug___"
                numbers: "slug", "slug-1", "slug-2", "slug-3"
    
    .. py:method:: __init__(self, source_field=None, date_field=None, split_on_words=False, underscores=True, *args, **kwargs)
    
        :param source_field: name of the field to use for autopopulation
        :param date_field: if provided, the date to use for validating unique-ness.  if
            not specified, the slug field will be marked as "unique" in the database.
        :param split_on_words: if True, slug will be truncated at the nearest word-boundary
            instead of cutting off at the character limit
        :param underscores: if True, underscores will be appended to generate a unique
            slug - otherwise, numbers will be used (slug, slug-1, slug-2, etc)


Managers
--------

This library contains the :class:PublishedManager class

.. py:module:: djutils.db.managers

PublishedManager
^^^^^^^^^^^^^^^^

.. py:class:: PublishedManager(models.Manager)

    .. py:method:: __init__(self, status_field='status')
    
        :param status_field: the name of the :class:`StatusField` to use to
            determine the status of the model instances
    
    .. py:method:: published(self)
        
        returns a queryset of model instances whose status is `LIVE_STATUS`.


Utils
-----

A collection of miscellaneous database helpers.

.. py:module:: djutils.db.utils

.. py:function:: extract_rel_field(model, related_to)

    returns the name of the field on `model` that contains a relation to the
    `related_to` model::
    
        >>> extract_rel_field(User, Group)
        'groups'
