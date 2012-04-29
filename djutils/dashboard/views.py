try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.conf import settings
from django.db.models import Max
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.views.generic.simple import direct_to_template

from djutils.dashboard.models import Panel, PanelData, PANEL_AGGREGATE_MINUTE
from djutils.decorators import staff_required
from djutils.utils.http import json_response


DASHBOARD_DEFAULT_LIMIT = getattr(settings, 'DASHBOARD_DEFAULT_LIMIT', 60)


def serialize_panel_data(panels_and_data):
    payload = []
    
    for panel, panel_data_qs in panels_and_data.items():
        for obj in panel_data_qs:
            payload.append(dict(
                panel_id=panel.pk,
                point_id=obj.id,
                data=obj.get_data()
            ))
    
    return payload

def dashboard_security(func):
    if getattr(settings, 'DASHBOARD_NO_SECURITY', False):
        return func
    else:
        return staff_required(func)

@dashboard_security
def dashboard_data_endpoint(request, data_type=PANEL_AGGREGATE_MINUTE):
    panels = Panel.objects.get_panels()
    
    max_id = int(request.GET.get('max_id') or 0)
    limit = int(request.GET.get('limit') or DASHBOARD_DEFAULT_LIMIT)
    
    panels_and_data = {}
    
    for panel in panels:
        panels_and_data[panel] = panel.data.filter(
            aggregate_type=data_type,
            pk__gt=max_id
        )[:limit]
    
    payload = serialize_panel_data(panels_and_data)
    
    return json_response(payload)

@dashboard_security
def dashboard(request):    
    return direct_to_template(request, 'dashboard/dashboard_index.html', {
        'panel_list': Panel.objects.get_panels(),
    })
