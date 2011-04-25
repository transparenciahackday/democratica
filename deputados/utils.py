#!/usr/bin/env python

def get_tweets_from_url(url):
    import twitter, urllib2
    username = url.strip('/').split('/')[-1]
    c = twitter.Api()
    try:
        tweets = [s for s in c.GetUserTimeline(username, count=5)]
    except urllib2.URLError:
        tweets = []

def get_news_for_mp(mp):
    import feedparser
    import urllib
    # we have more  than 1 query in case the first one doesn't hit anything
    # so the first one is very specific, and from there we broaden the scope till
    # we get something.
    queries = ['"%s" "%s"' % (mp.shortname, mp.current_party.name),
               '"%s" %s' % (mp.shortname, mp.current_party.abbrev), 
               '"%s"' % (mp.shortname), 
               ]
    news = []
    for query in queries:
        values = {'q': query.encode('utf-8'), 'output': 'rss'}
        url = 'http://news.google.com/news?%s&ned=pt-PT_pt' % urllib.urlencode(values)
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
            item = (url, title)
            news.append(item)
            # got enough?
            if len(news) >= 10:
                break
    for n in news:
        index = news.index(n)
        other_news = list(news)
        other_news.pop(index)
        if n in other_news:
            news.pop(index)
    return news



from settings import FEMALE_NAMES_FILE
female_names = open(FEMALE_NAMES_FILE).readlines()

def get_gender_from_name(name):
    if name + '\n' in female_names:
        return 'F'
    else:
        return 'M'

