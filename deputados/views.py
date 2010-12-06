# -*- coding: utf-8 -*-

from dptd.deputados.models import MP, LinkSet, Session, Party, Constituency
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

def index(request):
    return direct_to_template('index.html')

def mp_list(request):
    session_number = request.GET.get('session', Session.objects.order_by('-number')[0].number)
    party = request.GET.get('party', 'all')
    constituency_id = request.GET.get('constituency', 'all')

    if not session_number == 'all':
        queryset = MP.objects.filter(caucus__session__number=int(session_number)).distinct()
    else:
        queryset = MP.objects.all()

    if not party == 'all':
        queryset = queryset.filter(caucus__party__abbrev=party)
    if not constituency_id == 'all':
        queryset = queryset.filter(caucus__constituency__id=int(constituency_id))

    queryset = queryset.distinct()

    # queryset = queryset[1:60]

    # q1 = queryset.filter(has_mps=True)
    # q2 = queryset.filter(has_mps=False)
    # queryset = q1 | q2

    # divide list into 3, so that we can lay them out properly
    # inside the template
    cols = 3
    row_number, remainder = divmod(queryset.count(), cols)
    extra_row_1 = 0
    extra_row_2 = 0
    if remainder >= 1:
        extra_row_1 = 1
    if remainder == 2:
        extra_row_2 = 1
    rowcount1 = row_number + extra_row_1
    rowcount2 = row_number + extra_row_2
    queryset_1 = queryset[:rowcount1]
    queryset_2 = queryset[rowcount1:rowcount1+rowcount2]
    queryset_3 = queryset[rowcount1+rowcount2:]
    extra = {}
    extra['querysets'] = [queryset_1, queryset_2, queryset_3]

    extra['sessions'] = Session.objects.order_by('-number')
    extra['session'] = int(session_number) if session_number != 'all' else 'all'

    extra['parties'] = Party.objects.filter(has_mps=True)
    extra['party'] = party

    extra['constituency'] = int(constituency_id) if constituency_id != 'all' else 'all'
    extra['constituencies'] = Constituency.objects.all()

    return object_list(request, queryset,
                       extra_context=extra,
                       ) 

def mp_detail(request, object_id):
    queryset = MP.objects.all()
    mp = MP.objects.get(id=object_id)

    # get Google News feed
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

    # get Twitter posts
    import urllib2
    try:
        if mp.linkset.twitter_url:
            username = mp.linkset.twitter_url.strip('/').split('/')[-1]
            import twitter
            c = twitter.Api()
            tweets = [s for s in c.GetUserTimeline(username, count=5)]
        else:
            tweets = []
    except (LinkSet.DoesNotExist, urllib2.HTTPError):
            tweets = []



    return object_detail(request, queryset, object_id,
            extra_context={'news': news, 'tweets': tweets,
                })


