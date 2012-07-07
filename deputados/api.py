# myapp/api.py
from tastypie.resources import ModelResource
from deputados.models import MP

class MPResource(ModelResource):
    class Meta:
        queryset = MP.objects.all()
        resource_name = 'deputado'
