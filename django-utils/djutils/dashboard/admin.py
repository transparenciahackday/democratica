from django.contrib import admin

from djutils.dashboard.models import Panel, PanelData


class PanelAdmin(admin.ModelAdmin):
    list_display = ('title',)


class PanelDataAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_filter = ('panel', 'aggregate_type',)


admin.site.register(Panel, PanelAdmin)
admin.site.register(PanelData, PanelDataAdmin)
