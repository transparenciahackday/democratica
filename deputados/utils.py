#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_tweets_for_mp(mp):
    import urllib2, twitter
    from models import LinkSet

    try:
        url = mp.linkset.twitter_url
    except (LinkSet.DoesNotExist, urllib2.HTTPError):
        return []

    if not url:
        return []
    username = url.strip('/').split('/')[-1]
    c = twitter.Api()
    try:
        tweets = []
        for s in c.GetUserTimeline(username, count=5):
            tweets.append({ 'id': s.id, 'text': s.text, 
                           'created_at': s.created_at,})
        return tweets
    except urllib2.URLError:
        return []

def get_news_for_mp(mp):
    import json
    import urllib
    # we have more  than 1 query in case the first one doesn't hit anything
    # so the first one is very specific, and from there we broaden the scope till
    # we get something.
    if not mp:
        return
    queries = [
               # '"%s" "%s"' % (mp.shortname, mp.current_party.name),
               '"%s" %s' % (mp.shortname, mp.current_party.abbrev), 
               '"%s"' % (mp.shortname), 
               ]
    news = []
    for query in queries:
        values = {'q': query.encode('utf-8'), 'format': 'json',
                  'sort': 'date', 'match': 'phrase', 'page': 1, 'limit': 8}

        url = 'http://api.destakes.com/search/?%s' % urllib.urlencode(values)
        contents = json.loads(urllib.urlopen(url).read())
        for item in contents:
            news.append({'title': item['title'], 'url': item['url'], 'source': item['source']})
            # got enough?
            if len(news) >= 8:
                break

        '''
        for entry in channels.entries:
            print entry
            try:
                url = unicode(entry.link, channels.encoding)
                source = unicode(entry.source, channels.encoding)
                # summary = unicode(entry.description, channels.encoding)
                # pubdate does not work yet
                # pubdate = unicode(entry.pubdate, channels.encoding)
                title = unicode(entry.title, channels.encoding)
            except:
                url = entry.link
                title = entry.title
                source = entry.source

            news.append({'title': title, 'url': url, 'source': source})
            # got enough?
            if len(news) >= 8:
                break
        '''
    return news



from settings import FEMALE_NAMES_FILE
female_names = open(FEMALE_NAMES_FILE).readlines()

def get_gender_from_name(name):
    if name + '\n' in female_names:
        return 'F'
    else:
        return 'M'

