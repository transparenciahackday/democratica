import datetime
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.db import models
from django.db.models import Max, Avg
from django.template.defaultfilters import slugify

from djutils.dashboard.registry import registry


PANEL_AGGREGATE_MINUTE = 0
PANEL_AGGREGATE_HOUR = 1
PANEL_AGGREGATE_DAY = 2
PANEL_AGGREGATE_CHOICES = (
    (PANEL_AGGREGATE_MINUTE, 'minute'),
    (PANEL_AGGREGATE_HOUR, 'hour'),
    (PANEL_AGGREGATE_DAY, 'day'),
)


class PanelManager(models.Manager):
    def update_panels(self):
        data = []
        shared_now = datetime.datetime.now()
        
        # function to sort the panels by priority
        key = lambda obj: obj.get_priority()
        
        for provider in sorted(registry.get_provider_instances(), key=key):
            # pull the data off the panel and store
            panel_obj = provider.get_panel_instance()
            
            panel_data_obj = PanelData.objects.create(
                panel=panel_obj,
                created_date=shared_now,
                aggregate_type=PANEL_AGGREGATE_MINUTE,
            )
            
            raw_panel_data = provider.get_data()
            
            for key, value in raw_panel_data.items():
                data_set_obj = PanelDataSet.objects.create(
                    panel_data=panel_data_obj,
                    key=key,
                    value=value,
                )
            
            data.append(panel_data_obj)
        
        return data
    
    def _generate_aggregate(self, timedelta, aggregate_type, seed):
        data = []
        shared_now = seed or datetime.datetime.now()
        low_date = shared_now - timedelta
        
        # function to sort the panels by priority
        key = lambda obj: obj.get_priority()
        
        for provider in sorted(registry.get_provider_instances(), key=key):
            # pull the data off the panel and store
            panel_obj = provider.get_panel_instance()
            
            # create a new panel data object to store the aggregates
            panel_data_obj = PanelData.objects.create(
                panel=panel_obj,
                created_date=shared_now,
                aggregate_type=aggregate_type,
            )
            
            # get the panel data queryset for the previous `timedelta`
            data_qs = panel_obj.data.minute_data().filter(created_date__range=(
                low_date, shared_now
            ))
            
            # get what we really want, which are the k/v pairs
            data_sets = PanelDataSet.objects.filter(panel_data__in=data_qs)
            
            # find the unique keys and aggregate over them
            distinct_keys = data_sets.values_list('key', flat=True).distinct()
            
            for key in distinct_keys:
                # calculate the average and store it
                average = data_sets.filter(key=key).aggregate(
                    average=Avg('value')
                )['average']
                
                PanelDataSet.objects.create(
                    panel_data=panel_data_obj,
                    key=key,
                    value=average,
                )
            
            data.append(panel_data_obj)
        
        return data
    
    def generate_hourly_aggregates(self, seed=None):
        self._generate_aggregate(datetime.timedelta(seconds=3600), PANEL_AGGREGATE_HOUR, seed)
    
    def generate_daily_aggregates(self, seed=None):
        self._generate_aggregate(datetime.timedelta(seconds=86400), PANEL_AGGREGATE_DAY, seed)
    
    def get_panels(self):
        """\
        Purpose is to get a queryset of panel models matching the registered 
        panel providers
        """
        return self.filter(title__in=registry.get_titles())
    
    def get_latest(self):
        """\
        Get the latest panel data for the registered panel providers
        """
        return [
            PanelData.objects.minute_data().filter(panel=panel)[0] \
                for panel in self.get_panels()
        ]


class Panel(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(db_index=True)
    
    class Meta:
        ordering = ('title',)

    objects = PanelManager()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Panel, self).save(*args, **kwargs)


class PanelDataManager(models.Manager):
    def minute_data(self):
        return self.filter(aggregate_type=PANEL_AGGREGATE_MINUTE)
    
    def hour_data(self):
        return self.filter(aggregate_type=PANEL_AGGREGATE_HOUR)
    
    def day_data(self):
        return self.filter(aggregate_type=PANEL_AGGREGATE_DAY)
    
    def get_most_recent_update(self):
        return self.minute_data().aggregate(max_date=Max('created_date'))['max_date']


class PanelData(models.Model):
    """
    Preserve historical data from dashboard.  Automatically deleted by the
    periodic command :func:`remove_old_panel_data`
    """
    panel = models.ForeignKey(Panel, related_name='data')
    created_date = models.DateTimeField(db_index=True)
    aggregate_type = models.IntegerField(choices=PANEL_AGGREGATE_CHOICES,
            default=PANEL_AGGREGATE_MINUTE)
    
    objects = PanelDataManager()
    
    class Meta:
        ordering = ('-created_date',)
    
    def __unicode__(self):
        return '%s: %s' % (self.panel.title, self.created_date)
    
    def get_data(self):
        data_dict = {}
        
        for data_set in self.keys.all():
            data_dict[data_set.key] = data_set.value
        
        return data_dict


class PanelDataSet(models.Model):
    panel_data = models.ForeignKey(PanelData, related_name='keys')
    key = models.CharField(max_length=255)
    value = models.FloatField()
