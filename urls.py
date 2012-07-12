from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from democratica import settings
from democratica.deputados.models import MP, Party, Mandate, LinkSet, Legislature, Fact, FactType, Activity
import democratica.deputados.views as views
import democratica.dar.views as darviews
import django.contrib.auth.views as authviews

# Enable admin interface
from django.contrib import admin
admin.autodiscover()
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory
sqs = SearchQuerySet().filter(order_by='-day')

# Enable API's
from tastypie.api import Api
from deputados.api import *
v1_api = Api(api_name='v1')
v1_api.register(MPResource())
v1_api.register(PartyResource())
v1_api.register(ConstituencyResource())


urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^acerca/$', 'django.views.generic.simple.direct_to_template', {'template': 'acerca.html'}),

    url(r'^deputados/$', views.mp_list, name='mp_list'),
    url(r'^deputados/(?P<object_id>\d+)/$', views.mp_detail, name='mp_detail'),
    url(r'^deputados/(?P<object_id>\d+)/stats$', views.mp_statistics, name='mp_stats'),

    url(r'^sessoes/$', darviews.day_list, name='calendar'),
    url(r'^sessoes/(?P<year>\d+)/$', darviews.day_list, name='calendar_year'),
    url(r'^sessoes/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', darviews.day_detail, name='day_detail'),
    url(r'^sessoes/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<position>\d+)$', darviews.entry_detail, name='entry_detail'),
    url(r'^sessoes/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/edicoes/$', darviews.day_revisions, name='day_revisions'),
    url(r'^sessoes/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/stats$', darviews.day_statistics, name='day_stats'),
    # url(r'^sessoes/intervencao/(?P<id>\d+)/$', darviews.statement_detail, name='statement_detail'),

    url(r'^sessoes/marcar/(?P<id>\d+)/$', darviews.mark_as_cont, name='mark_as_cont'),
    url(r'^sessoes/marcar_aparte/(?P<id>\d+)/$', darviews.mark_as_aside, name='mark_as_aside'),
    url(r'^sessoes/marcar_intervencao/(?P<id>\d+)/$', darviews.mark_as_main, name='mark_as_main'),
    url(r'^sessoes/desmarcar/(?P<id>\d+)/$', darviews.unmark_as_cont, name='unmark_as_cont'),
    url(r'^sessoes/juntar/(?P<id>\d+)/$', darviews.join_entry_with_previous, name='join_entry_with_previous'),
    url(r'^sessoes/newlines/(?P<id>\d+)/$', darviews.correct_newlines, name='correct_newlines'),

    url(ur'^sessoes/catalogar/(?P<id>\d+)/$', darviews.parse_session_entries, name='parse_session_entries'),

    (ur'^sessoes/gravar/$', darviews.entry_save),
    (ur'^sessoes/raw/$', darviews.fetch_raw_entry),
    (ur'^sessoes/reprocessar/(?P<id>\d+)/$', darviews.refresh),

    (r'^pesquisa/', include('haystack.urls')),

    url(r'^login/', authviews.login, name='login'),
    url(r'^logout/', authviews.logout, name='logout'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    # (r'^databrowse/(.*)', databrowse.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^labs/$', direct_to_template, {'template': 'labs/labs_list.html'}),
    (ur'^labs/doquesefalou/$', darviews.wordlist),

    (r'^api/', include(v1_api.urls)),

    (r'^ie6/$', direct_to_template, {'template': 'browser-update.html'}),
    (r'^404/$', direct_to_template, {'template': '404.html'}),
    (r'^500/$', direct_to_template, {'template': '500.html'}),
    (r'^502/$', direct_to_template, {'template': '502.html'}),

    url(r'^$', search_view_factory(
            searchqueryset=sqs,
        ), name='haystack_search'),
)

# Enable Databrowse
'''
from django.contrib import databrowse
databrowse.site.register(MP)
databrowse.site.register(Party)
databrowse.site.register(Mandate)
databrowse.site.register(LinkSet)
databrowse.site.register(Fact)
databrowse.site.register(FactType)
databrowse.site.register(Activity)
databrowse.site.register(Legislature)
'''
