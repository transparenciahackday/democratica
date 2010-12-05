# -*- coding: utf-8 -*-
import feedparser
import urllib


# get Google News feed
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



