#!/usr/bin/env python

import sys
import feedparser
from time import mktime
from datetime import datetime
import dateutil.parser


def getFeed(lookback=0):
  d = feedparser.parse('https://offersbot.io/api/program/amex-offers/channel/amex-offers-twitter/offer/rss')
  stuff = d['entries']
  lstuff = [(a['title'], dateutil.parser.parse(a['updated'], ignoretz=True)) for a in stuff]
  lstuff.sort(key=lambda tup: tup[1])
  curr_time = datetime.utcnow()
  loffers = ['#'+a[0] for a in lstuff if (curr_time - a[1]).days <= lookback]
  loffers = list(set(loffers))
  return loffers

def main(argv):
  lookback = 0
  if len(argv) >= 1:
    lookback = int(argv[0])
  hashtags = getFeed(lookback)
  hashtags = [str(ht) for ht in hashtags]
  output = ' '.join(hashtags)
  with open('hashtags.txt', 'w') as out_file:
    out_file.write(output)

if __name__ == "__main__":
  main(sys.argv[1:])
