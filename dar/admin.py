from dar.models import Day, Entry
from django.contrib import admin

class EntryInline(admin.TabularInline):
    model = Entry
    fields = ['position', 'speaker']
class DayAdmin(admin.ModelAdmin):
    list_display = ['date', 'diary_series', 'diary_number']
    inlines = [EntryInline]
admin.site.register(Day, DayAdmin)

'''
class EntryAdmin(admin.ModelAdmin):
    list_display = ['day', 'position', 'mp', 'speaker', 'text']
admin.site.register(Entry, EntryAdmin)
'''

