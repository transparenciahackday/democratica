# -*- coding: utf-8 -*-

from democratica.deputados.models import MP, LinkSet, Session, Party, Constituency
from democratica.deputados import utils

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
    news = utils.get_news_for_mp(mp)

    # get Twitter posts
    import urllib2
    try:
        if mp.linkset.twitter_url:
            from utils import get_tweets_from_url
            tweets = get_tweets_from_url(mp.linkset.twitter_url)
            
        else:
            tweets = []
    except (LinkSet.DoesNotExist, urllib2.HTTPError):
            tweets = []



    return object_detail(request, queryset, object_id,
            extra_context={'news': news, 'tweets': tweets,
                })

def mp_search(request, query=''):
    if not query:
        query = request.GET.get('query', '')
    queryparts = query.split(' ')
    results = MP.objects.all()
    for q in queryparts:
        # "id:2479" or simply "2479" should return an MP with that id, if exists
        if q.startswith('id:') or (MP.objects.filter(id=q) and len(queryparts) == 1):
            id = q.split(':')[-1]
            return mp_detail(object_id=id)
        results = results.filter(name__icontains=q)

    #relevant_results
    #partial_results

    return direct_to_template(request, 'mp_search.html',
                              extra_context={
                                  'results': results,
                                  })
