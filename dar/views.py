from models import Day, Entry
from django.views.generic.list_detail import object_list, object_detail

def day_detail(request, object_id):
    day = Day.objects.get(id=object_id)
    entries = Entry.objects.filter(day=day).order_by('id')[30:]

    return object_detail(request, Day.objects.all(), object_id,
            template_object_name = 'day',
            extra_context={'entries': entries,
                })
