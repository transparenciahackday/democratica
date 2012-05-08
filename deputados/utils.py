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

def get_pm_from_date(dt):
    from deputados.models import GovernmentPost
    if GovernmentPost.objects.filter(name="Primeiro-Ministro", date_started__lt=dt, date_ended__gt=dt):
        return GovernmentPost.objects.filter(name="Primeiro-Ministro", date_started__lt=dt, date_ended__gt=dt)[0].mp
    elif GovernmentPost.objects.filter(name="Primeiro-Ministro", date_started__lt=dt):
        # note slicing in order to speed up query, see http://stackoverflow.com/a/8328189
        return GovernmentPost.objects.filter(name="Primeiro-Ministro", date_started__lt=dt).order_by('-government')[:1][0].mp
    return None

def get_minister(dt, mp_id=None, shortname=None, post=None):
    from deputados.models import GovernmentPost
    if shortname:
        if 'Ministr' in shortname or 'Secret' in shortname:
                # no, wrong arguments
            post = shortname
            shortname = None
    if shortname:
        if GovernmentPost.objects.filter(person_name=shortname, date_started__lt=dt, date_ended__gt=dt):
            return GovernmentPost.objects.filter(person_name=shortname, date_started__lt=dt, date_ended__gt=dt)[0]
        elif GovernmentPost.objects.filter(person_name=shortname, date_started__lt=dt):
            # note slicing in order to speed up query, see http://stackoverflow.com/a/8328189
            return GovernmentPost.objects.filter(person_name=shortname, date_started__lt=dt).order_by('-government')[:1][0]
        return None
    elif mp_id:
        if GovernmentPost.objects.filter(mp_id=mp_id, date_started__lt=dt, date_ended__gt=dt):
            return GovernmentPost.objects.filter(mp_id=mp_id, date_started__lt=dt, date_ended__gt=dt)[0]
        elif GovernmentPost.objects.filter(mp_id=mp_id, date_started__lt=dt):
            # note slicing in order to speed up query, see http://stackoverflow.com/a/8328189
            return GovernmentPost.objects.filter(mp_id=mp_id, date_started__lt=dt).order_by('-government')[:1][0]
        return None
    elif post:
        keyword = post
        if GovernmentPost.objects.filter(name=keyword, date_started__lt=dt, date_ended__gt=dt):
            return GovernmentPost.objects.filter(name=keyword, date_started__lt=dt, date_ended__gt=dt)[0]
        elif GovernmentPost.objects.filter(name=keyword, date_started__lt=dt):
            # note slicing in order to speed up query, see http://stackoverflow.com/a/8328189
            return GovernmentPost.objects.filter(name=keyword, date_started__lt=dt).order_by('-government')[:1][0]
        # another run with more permissive search
        if GovernmentPost.objects.filter(name__icontains=keyword, date_started__lt=dt, date_ended__gt=dt):
            return GovernmentPost.objects.filter(name__icontains=keyword, date_started__lt=dt, date_ended__gt=dt)[0]
        elif GovernmentPost.objects.filter(name__icontains=keyword, date_started__lt=dt):
            # note slicing in order to speed up query, see http://stackoverflow.com/a/8328189
            return GovernmentPost.objects.filter(name__icontains=keyword, date_started__lt=dt).order_by('-government')[:1][0]
        # Not found? This is very dumb logic, using the last word to find the post! Just to get by for now
        keyword = post.split(' ')[-1]
        if GovernmentPost.objects.filter(name__icontains=keyword, date_started__lt=dt, date_ended__gt=dt):
            return GovernmentPost.objects.filter(name__icontains=keyword, date_started__lt=dt, date_ended__gt=dt)[0]
        elif GovernmentPost.objects.filter(name__icontains=keyword, date_started__lt=dt):
            # note slicing in order to speed up query, see http://stackoverflow.com/a/8328189
            return GovernmentPost.objects.filter(name__icontains=keyword, date_started__lt=dt).order_by('-government')[:1][0]
        return None


def get_mandate_for_date(mp, dt):
    from deputados.models import Mandate
    if Mandate.objects.filter(mp=mp, date_begin__lt=dt, date_end__gt=dt):
        return Mandate.objects.filter(mp=mp, date_begin__lt=dt, date_end__gt=dt)[0]
    elif Mandate.objects.filter(mp=mp, date_begin__lt=dt):
        # note slicing in order to speed up query, see http://stackoverflow.com/a/8328189
        return Mandate.objects.filter(mp=mp, date_begin__lt=dt).order_by('-date_begin')[:1][0]
    return None

def get_legislature_for_date(dt):
    from deputados.models import Legislature
    if Legislature.objects.filter(date_start__lt=dt, date_end__gt=dt):
        return Legislature.objects.filter(date_start__lt=dt, date_end__gt=dt)[0]
    elif Legislature.objects.filter(date_start__lt=dt):
        # note slicing in order to speed up query, see http://stackoverflow.com/a/8328189
        return Legislature.objects.filter(date_start__lt=dt).order_by('-date_start')[:1][0]
    return None

def get_gender_from_name(name):
    from settings import FEMALE_NAMES_FILE
    female_names = open(FEMALE_NAMES_FILE).readlines()
    if name + '\n' in female_names:
        female_names.close()
        return 'F'
    else:
        female_names.close()
        return 'M'
    

