from django.db import models

from djutils.constants import LIVE_STATUS


class PublishedManager(models.Manager):
    """
    Manager that uses the status constants defined in :module:`djutils.constants`
    to add a :func:`published` method to the default manager.
    
    Usage::
    
        objects = PublishedManager('name_of_status_field')
    """
    def __init__(self, status_field='status', *args, **kwargs):
        self.status_field = status_field
        super(PublishedManager, self).__init__(*args, **kwargs)
    
    def published(self):
        return self.filter(**{self.status_field: LIVE_STATUS})
