from deputados.models import *
from django.contrib import admin

class MPAdmin(admin.ModelAdmin):
    list_display = ['shortname', 'name', 'dob', 'occupation']
admin.site.register(MP, MPAdmin)

class PartyAdmin(admin.ModelAdmin):
    list_display = ['abbrev', 'name', 'tendency', 'info']
admin.site.register(Party, PartyAdmin)

class FactTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(FactType, FactTypeAdmin)

class FactAdmin(admin.ModelAdmin):
    list_display = ['mp', 'fact_type', 'value']
admin.site.register(Fact, FactAdmin)

class CaucusAdmin(admin.ModelAdmin):
    list_display = ['mp', 'constituency', 'date_begin', 'date_end', 'session']
admin.site.register(Caucus, CaucusAdmin)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['mp', 'caucus', 'type1', 'type2', 'number', 'session', 'content']
admin.site.register(Activity, ActivityAdmin)

class LinkSetAdmin(admin.ModelAdmin):
    list_display = ['mp', 'email', 'website_url', 'twitter_url', 'facebook_url']
admin.site.register(LinkSet, LinkSetAdmin)

class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Constituency, ConstituencyAdmin)
