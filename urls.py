from django.conf.urls.defaults import *
from democratica import settings
from democratica.deputados.models import MP, Party, Caucus, LinkSet, Session, Fact, FactType, Activity
import democratica.deputados.views as views
import democratica.dar.views as darviews

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

    (r'^deputados/$', views.mp_list),
    (r'^deputados/(?P<object_id>\d+)/$', views.mp_detail),
    
    (r'^dar/$', darviews.day_list),
    (r'^dar/(?P<object_id>\d+)/$', darviews.day_detail),

    (r'^pesquisa/', include('dar.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
