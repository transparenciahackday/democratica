from django.db import models

# Create your models here.
class Election(models.Model):
    date = models.DateField()
    type = models.CharField('Tipo', max_length=100)

    def __unicode__(self):
        return '%s - %d-%d-%d' % (self.type, self.date.year, self.date.month, self.date.day)
