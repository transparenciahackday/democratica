from django.conf.urls.defaults import url

from tastypie import fields
from tastypie.resources import ModelResource
from deputados.models import MP, LinkSet, Mandate, Legislature, GovernmentPost, Party, Constituency

from django.core.serializers import json
from django.utils import simplejson
from tastypie.serializers import Serializer

class PrettyJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder, 
                                sort_keys=True, ensure_ascii=False, 
                                indent=self.json_indent)

class LegislatureResource(ModelResource):
    class Meta:
        queryset = Mandate.objects.all()
        resource_name = 'legislature'
        allowed_methods = ['get']

class ConstituencyResource(ModelResource):
    class Meta:
        queryset = Constituency.objects.all()
        resource_name = 'constituency'
        allowed_methods = ['get']

class MandateResource(ModelResource):
    class Meta:
        queryset = Mandate.objects.all()
        resource_name = 'mandates'
        allowed_methods = ['get']
        excludes = ['has_registointeresses', 'has_activity']

class GovPostResource(ModelResource):
    class Meta:
        queryset = GovernmentPost.objects.all()
        resource_name = 'govpost'
        allowed_methods = ['get']

class LinkResource(ModelResource):
    class Meta:
        queryset = LinkSet.objects.all()
        resource_name = 'links'
        allowed_methods = ['get']

class MPResource(ModelResource):
    linkset = fields.ToOneField(LinkResource, "linkset", null=True, full=True)
    mandates = fields.ToManyField(MandateResource, "mandate_set", full=True)
    gov_posts = fields.ToManyField(GovPostResource, "governmentpost_set", full=True)
    class Meta:
        queryset = MP.objects.all()
        resource_name = 'mp'
        excludes = ['aka_1', 'aka_2', 'favourite_word', 'is_active', 'tweets', 'news']
        allowed_methods = ['get']

    def prepend_urls(self):
        return [
            url(ur"^deputados/(?P<id>\d+)/$", self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            # FIXME: o url seguinte não é reconhecido
            url(ur"^deputados/(?P<shortname>[\w ]+)/$", self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class PartyResource(ModelResource):
    class Meta:
        queryset = Party.objects.all()
        resource_name = 'party'
        allowed_methods = ['get']

    def prepend_urls(self):
        return [
            url(ur"^(?P<resource_name>%s)/(?P<abbrev>[\w]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
