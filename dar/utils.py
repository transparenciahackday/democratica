#!/usr/bin/env python
# -*- coding: utf-8 -*-

def remove_strings(st, strings_tuple, once=False):
    for s in strings_tuple:
        if once:
            st = st.replace(s, '', 1)
        else:
            st = st.replace(s, '')
    return st

def get_dates(sess, leg):
    pass

def days_for_year(year):
    year = int(year)
    import datetime
    from democratica.dar.models import Day
    first_day_of_year = datetime.date(year=year, month=1, day=1)
    last_day_of_year = datetime.date(year=year, month=12, day=31)
    all_days = Day.objects.filter(date__gt=first_day_of_year, date__lt=last_day_of_year)
    return all_days

def elections_for_year(year):
    year = int(year)
    import datetime
    from democratica.elections.models import Election
    first_day_of_year = datetime.date(year=year, month=1, day=1)
    last_day_of_year = datetime.date(year=year, month=12, day=31)
    elections = Election.objects.filter(date__gte=first_day_of_year, date__lte=last_day_of_year)
    return elections

def all_years(reverse=False):
    '''Returns all years for which there are saved Days.'''
    from democratica.dar.models import Day
    years = list(set([d['date'].year for d in Day.objects.all().values('date')]))
    years.sort()
    if reverse:
        years.reverse()
    return years


from haystack.utils import Highlighter
from django.utils.html import strip_tags

class MyHighlighter(Highlighter):
    prev_chars = 10

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        start_offset -= self.prev_chars
        end_offset -= self.prev_chars
        return self.render_html(highlight_locations, start_offset, end_offset)



