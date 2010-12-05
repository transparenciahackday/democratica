# -*- coding: utf-8 -*-

from dptd.deputados.models import MP, LinkSet
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

def index(request):
    return direct_to_template('index.html')

def mp_list(request):
    queryset = MP.objects.all()
    return object_list(request, queryset,
                       paginate_by=60,
                       ) 

def mp_detail(request, object_id):
    queryset = MP.objects.all()
    mp = MP.objects.get(id=object_id)

    # get Google News feed
    import feedparser
    import urllib
    name = mp.shortname
    values = {'q': name, 'output': 'rss'}
    url = 'http://news.google.com/news?%s' % urllib.urlencode(values)
    channels = feedparser.parse(url)
    news = []
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
        item = (url, title)
        news.append(item)

    # get Twitter posts
    try:
        if mp.linkset.twitter_url:
            username = mp.linkset.twitter_url.strip('/').split('/')[-1]
            import twitter
            c = twitter.Api()
            tweets = [s for s in c.GetUserTimeline(username, count=5)]
        else:
            tweets = []
    except LinkSet.DoesNotExist:
            tweets = []


    return object_detail(request, queryset, object_id,
            extra_context={'news': news, 'tweets': tweets,
                })


