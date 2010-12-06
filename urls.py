from django.conf.urls.defaults import *
from dptd import settings
from dptd.deputados.models import MP, Party, Caucus, LinkSet, Session, Fact, FactType, Activity
import dptd.deputados.views as views

# Enable admin interface
from django.contrib import admin
admin.autodiscover()

# Enable Databrowse
from django.contrib import databrowse
databrowse.site.register(MP)
databrowse.site.register(Party)
databrowse.site.register(Caucus)
databrowse.site.register(LinkSet)
databrowse.site.register(Fact)
databrowse.site.register(FactType)
databrowse.site.register(Activity)
databrowse.site.register(Session)




urlpatterns = patterns('',
    (r'^$', 
        'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^about/$', 
        'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    (r'^datasets/$', 
        'django.views.generic.simple.direct_to_template', {'template': 'datasets.html'}),

    (r'^deputados/$', views.mp_list),
    (r'^deputados/(?P<object_id>\d+)/$', views.mp_detail),

    # url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/results.html'), 'poll_results'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
