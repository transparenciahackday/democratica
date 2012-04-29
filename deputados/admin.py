from deputados.models import *
from django.contrib import admin

class MPAdmin(admin.ModelAdmin):
    list_display = ['shortname', 'name', 'dob', 'occupation']
admin.site.register(MP, MPAdmin)

class PartyAdmin(admin.ModelAdmin):
    list_display = ['abbrev', 'name', 'tendency', 'info']
admin.site.register(Party, PartyAdmin)

class MandateAdmin(admin.ModelAdmin):
    list_display = ['mp', 'constituency', 'date_begin', 'date_end', 'legislature']
admin.site.register(Mandate, MandateAdmin)

class LinkSetAdmin(admin.ModelAdmin):
    list_display = ['mp', 'email', 'website_url', 'twitter_url', 'facebook_url']
admin.site.register(LinkSet, LinkSetAdmin)

class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Constituency, ConstituencyAdmin)
