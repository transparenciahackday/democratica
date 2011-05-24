from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from democratica import settings
from democratica.deputados.models import MP, Party, Caucus, LinkSet, Session, Fact, FactType, Activity
import democratica.deputados.views as views
import democratica.dar.views as darviews

# Enable admin interface
from django.contrib import admin
admin.autodiscover()

# Enable Databrowse
'''
from django.contrib import databrowse
databrowse.site.register(MP)
databrowse.site.register(Party)
databrowse.site.register(Caucus)
databrowse.site.register(LinkSet)
databrowse.site.register(Fact)
databrowse.site.register(FactType)
databrowse.site.register(Activity)
databrowse.site.register(Session)
'''
urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^acerca/$', 'django.views.generic.simple.direct_to_template', {'template': 'acerca.html'}),

    url(r'^deputados/$', views.mp_list, name='mp_list'),
    url(r'^deputados/(?P<object_id>\d+)/$', views.mp_detail, name='mp_detail'),
    url(r'^deputados/(?P<object_id>\d+)/stats$', views.mp_statistics, name='mp_stats'),

    url(r'^sessoes/$', darviews.day_list, name='calendar'),
    url(r'^sessoes/(?P<year>\d+)/$', darviews.day_list, name='calendar_year'),
    url(r'^sessoes/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', darviews.day_detail, name='day_detail'),
    url(r'^sessoes/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/stats$', darviews.day_statistics, name='day_stats'),

    (r'^pesquisa/', include('dar.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    # (r'^databrowse/(.*)', databrowse.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^ie6/$', direct_to_template, {'template': 'browser-update.html'}),
    (r'^404/$', direct_to_template, {'template': '404.html'}),
    (r'^500/$', direct_to_template, {'template': '500.html'}),
    (r'^502/$', direct_to_template, {'template': '502.html'}),

)
