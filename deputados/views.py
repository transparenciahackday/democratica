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
    mp = MP.objects.get(id=object.id)

    # get Google News feed
    import feedparser
    import urllib
    name = "Francisco Louçã"
    values = {'q': name, 'output': 'rss'}

    url = 'http://news.google.com/news?%s' % urllib.urlencode(values)
    channels = feedparser.parse(url)

    for entry in channels.entries:
        try:
            url = unicode(entry.link, channels.encoding)
            # summary = unicode(entry.description, channels.encoding)
            # pubdate does not work yet
            # pubdate = unicode(entry.pubdate, channels.encoding)
            title = unicode(entry.title, channels.encoding)
        except:
            url = entry.link
            summary = entry.description
            title = entry.title

            print title
            print url

    return object_detail(request, queryset, object_id)


