# -*- coding: utf-8 -*-

from dptd.deputados.models import MP
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

def index(request):
    return direct_to_template('index.html')

def mp_list(request):
    queryset = MP.objects.all()
    return object_list(request, queryset) 

def mp_detail(request, object_id):
    queryset = MP.objects.all()

    # get Google News feed
    import feedparser

    url = 'http://news.google.com/news?q="António Guterres"&output=rss'
    channels = feedparser.parse(url)
    url = ''
    summary = ''
    title = ''

    for entry in channels.entries:
        try:
            url = unicode(entry.link, channels.encoding)
            summary = unicode(entry.description, channels.encoding)
            title = unicode(entry.title, channels.encoding)
        except:
            url = entry.link
            summary = entry.description
            title = entry.title

            print "URL: ", url
            print "Summary: ", summary
            print "Title: ", title

    return object_detail(request, queryset, object_id)


