from django.db import models

# Create your models here.
class Election(models.Model):
    date = models.DateField()
    type = models.CharField('Tipo', max_length=100)
