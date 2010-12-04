from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from dptd.models import MP

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'index'),
    (r'^deputados/$',
           ListView.as_view(model=MP,
                            context_object_name='mp_list',
                            template_name='deputados/mp_list.html')),
    (r'^deputados/(?P<pk>\d+)/$',
           DetailView.as_view(model=MP,
                              template_name='deputados/mp_detail.html')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
