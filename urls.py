from django.conf.urls.defaults import *
from dptd import settings
from dptd.deputados.models import MP
import dptd.deputados.views as views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

info_dict = { 'queryset': MP.objects.all(), }


urlpatterns = patterns('',
    (r'^$', 
        'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),

    (r'^deputados/$', views.mp_list),
    (r'^deputados/(?P<object_id>\d+)/$', views.mp_detail),

    # url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/results.html'), 'poll_results'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
