from django.conf.urls.defaults import *

from djutils import dashboard


dashboard.autodiscover()

urlpatterns = patterns('',
    (r'^dashboard/', include('djutils.dashboard.urls')),
)
