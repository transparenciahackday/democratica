from django.conf.urls.defaults import url

from tastypie import fields
from tastypie.resources import ModelResource
from deputados.models import MP, LinkSet

from django.core.serializers import json
from django.utils import simplejson
from tastypie.serializers import Serializer

class PrettyJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                                sort_keys=True, ensure_ascii=False, indent=self.json_indent)

class LinkResource(ModelResource):
    # mp = fields.ForeignKey('deputados.api.resources.MPResource', 'mp', related_name="links")
    class Meta:
        queryset = LinkSet.objects.all()
        resource_name = 'links'
        allowed_methods = ['get']

class MPResource(ModelResource):
    linkset = fields.ToOneField(LinkResource, "linkset", null=True)
    class Meta:
        queryset = MP.objects.all()
        resource_name = 'deputado'
        excludes = ['aka_1', 'aka_2', 'favourite_word', 'is_active', 'tweets', 'news']
        allowed_methods = ['get']

    def prepend_urls(self):
        return [
            url(ur"^(?P<resource_name>%s)/(?P<shortname>[\w ]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
