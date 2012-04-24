# -*- coding: utf-8 -*-

from democratica.deputados.models import MP, Legislature, Party, Constituency

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template


def index(request):
    return direct_to_template('index.html')

def mp_list(request):
    legislature_number = request.GET.get('legislature', Legislature.objects.order_by('-number')[0].number)
    party = request.GET.get('party', 'all')
    constituency_id = request.GET.get('constituency', 'all')

    if not legislature_number == 'all':
        queryset = MP.objects.select_related().filter(mandate__legislature__number=int(legislature_number))
    else:
        queryset = MP.objects.select_related().all()

    if not party == 'all':
        queryset = queryset.filter(mandate__party__abbrev=party)
    if not constituency_id == 'all':
        queryset = queryset.filter(mandate__constituency__id=int(constituency_id))

    # queryset = queryset.distinct().values('id', 'shortname', 'current_party')
    queryset = queryset.distinct()

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

    # extra['legislatures'] = Legislature.objects.order_by('-number').values('id', 'number')
    extra['legislatures'] = Legislature.objects.order_by('-number')
    extra['legislature'] = int(legislature_number) if legislature_number != 'all' else 'all'

    # extra['parties'] = Party.objects.filter(has_mps=True).values('id', 'abbrev')
    extra['parties'] = Party.objects.filter(has_mps=True)
    extra['party'] = party

    extra['constituency'] = int(constituency_id) if constituency_id != 'all' else 'all'
    extra['constituencies'] = Constituency.objects.all()

    return object_list(request, queryset,
                       extra_context=extra,
                       ) 

def mp_detail(request, object_id):
    queryset = MP.objects.select_related().all()

    return object_detail(request, queryset, object_id)

def mp_statistics(request, object_id):
    queryset = MP.objects.all()
    mp = MP.objects.get(id=object_id)

    return object_detail(request, queryset, object_id,
            template_name="deputados/mp_detail_statistics.html", )

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
