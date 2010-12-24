#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from heapq import nlargest
from operator import itemgetter
import re
from cStringIO import StringIO
import subprocess

from django.conf import settings

import sys
STOPWORD_FILE = '/home/rlafuente/code/transparencia/repo/dptd/core/stopwords.txt'

r_punctuation = re.compile(r"[^\s\w0-9'-]", re.UNICODE)
r_whitespace = re.compile(r'\s+')

def text_token_iterator(text, statement_separator=None):
    text = r_punctuation.sub('', text.lower())
    for word in r_whitespace.split(text):
        yield word
    if statement_separator:
        yield statement_separator

def qs_token_iterator(queryset, statement_separator=None):
    for statement in queryset.iterator():
        # changed the following line from statement.text_plain() to statement.text
        # for this to work with demo.cratica. -- ricardo
        for x in text_token_iterator(statement.text, statement_separator):
            yield x

STOPWORDS = frozenset([word.strip() for word in open(STOPWORD_FILE, 'r').readlines()])
            
class WordCounter(dict):
    
    def __init__(self, stopwords=STOPWORDS):
        self.stopwords = []
        for word in stopwords:
            self.stopwords.append(unicode(word, 'utf-8'))
        super(WordCounter, self).__init__(self)
    
    def __missing__(self, key):
        return 0
        
    def __setitem__(self, key, value):
        if key not in self.stopwords:
            super(WordCounter, self).__setitem__(key, value)

    def most_common(self, n=None):    
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))
        
class WordAndAttributeCounter(object):
    
    def __init__(self, stopwords=STOPWORDS):
        self.counter = defaultdict(WordAttributeCount)
        self.stopwords = stopwords
        
    def add(self, word, attribute):
        if word not in self.stopwords and len(word) > 2:
            self.counter[word].add(attribute)
        
    def most_common(self, n=None):    
        if n is None:
            return sorted(self.counter.iteritems(), key=lambda x: x[1].count, reverse=True)
        return nlargest(n, self.counter.iteritems(), key=lambda x: x[1].count)
        
class WordAttributeCount(object):
    
    __slots__ = ('count', 'attributes')
    
    def __init__(self):
        self.attributes = defaultdict(int)
        self.count = 0
        
    def add(self, attribute):
        self.attributes[attribute] += 1
        self.count += 1
        
    def winning_attribute(self):
        return nlargest(1, self.attributes.iteritems(), key=itemgetter(1))[0][0]
        
def most_frequent_word(qs):
    counter = WordCounter()
    for word in qs_token_iterator(qs):
        counter[word] += 1
    try:
        return counter.most_common(1)[0][0]
    except IndexError:
        return None

PARTY_COLOURS = {
    'liberal': 'f51c18',
    'bloc': '18d7f5',
    'cpc': '1883f5',
    'alliance': '1883f5',
    'canadian-alliance': '1883f5',
    'conservative': '1883f5',
    'progressive-conservative': '1883f5',
    'pc': '1883f5',
    'reform': '3ae617',
    'ndp': 'f58a18',
}
def statements_to_cloud(qs):
    counter = WordAndAttributeCounter()
    for statement in qs.iterator():
        if statement.member and not statement.speaker:
            party = statement.member.party.slug.lower()
        else:
            party = None
        for word in text_token_iterator(statement.text_plain()):
            counter.add(word, party)
    result = [(x[0], unicode(x[1].count), PARTY_COLOURS.get(x[1].winning_attribute(), '777777'))
        for x in counter.most_common(100)]
    cmd_input = "\n".join(["word\tweight\tcolor"] + [u"\t".join(x) for x in result]).encode('utf8')
    p = subprocess.Popen(settings.PARLIAMENT_WORDCLOUD_COMMAND, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate(cmd_input)[0]
    
