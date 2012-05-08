from dar.models import Day, Entry
from django.contrib import admin
import reversion

class EntryInline(admin.TabularInline):
    model = Entry
    fields = ['position', 'speaker']

class EntryAdmin(reversion.VersionAdmin):
    # exclude = ['html']
    pass
admin.site.register(Entry, EntryAdmin)
class DayAdmin(admin.ModelAdmin):
    list_display = ['date', 'diary_series', 'diary_number']
    inlines = [EntryInline]
admin.site.register(Day, DayAdmin)

'''
class EntryAdmin(admin.ModelAdmin):
    list_display = ['day', 'position', 'mp', 'speaker', 'text']
admin.site.register(Entry, EntryAdmin)
'''

