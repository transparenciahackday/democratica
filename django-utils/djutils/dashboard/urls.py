from django.conf.urls.defaults import *

from djutils.dashboard.models import PANEL_AGGREGATE_MINUTE, PANEL_AGGREGATE_HOUR, PANEL_AGGREGATE_DAY


urlpatterns = patterns('djutils.dashboard.views',
    # the main dashboard view
    url(r'^$', 'dashboard', name='djutils_dashboard_dashboard'),
    
    # views that return json encoded data used to update the dashboard
    url(r'^minute/$',
        'dashboard_data_endpoint',
        kwargs={'data_type': PANEL_AGGREGATE_MINUTE},
        name='djutils_dashboard_data_minute'
    ),
    url(r'^hour/$',
        'dashboard_data_endpoint',
        kwargs={'data_type': PANEL_AGGREGATE_HOUR},
        name='djutils_dashboard_data_hour'
    ),
    url(r'^day/$',
        'dashboard_data_endpoint',
        kwargs={'data_type': PANEL_AGGREGATE_DAY},
        name='djutils_dashboard_data_day'
    ),
)
