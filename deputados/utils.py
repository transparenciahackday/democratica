#!/usr/bin/env python

def get_tweets_from_url(url):
    import twitter, urllib2
    username = url.strip('/').split('/')[-1]
    c = twitter.Api()
    try:
        tweets = [s for s in c.GetUserTimeline(username, count=5)]
    except urllib2.URLError:
        tweets = []

from settings import FEMALE_NAMES_FILE
female_names = open(FEMALE_NAMES_FILE).readlines()

def get_gender_from_name(name):
    if name + '\n' in female_names:
        return 'F'
    else:
        return 'M'

