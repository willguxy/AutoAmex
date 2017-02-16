#!/usr/bin/env python

import json
import tweepy
from tweepy import OAuthHandler
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

def getAuth(file_name):
  with open(file_name) as data_file:    
    myauth = json.load(data_file)
  return myauth

def setupAPI(myauth):
  auth = OAuthHandler(myauth['consumer_key'], myauth['consumer_secret'])
  auth.set_access_token(myauth['access_token'], myauth['access_secret'])
  api = tweepy.API(auth)
  return api

def dumpHashtags(api, max_num=10, max_day=1):
  hashtags = set()
  for tweet in tweepy.Cursor(api.user_timeline).items(max_num):
    tweet_dict = tweet._json
    timestamp = mktime_tz(parsedate_tz(tweet_dict['created_at']))
    dt = datetime.fromtimestamp(timestamp)
    dt_diff = datetime.now() - dt
    if dt_diff.days < max_day:
      text = tweet_dict['text']
      ht = (w for w in text.split() if w.startswith("#"))
      hashtags = hashtags.union(ht)
  try:
    hashtags.remove('#available')
  except:
    pass
  return hashtags

def main():
  myauth = getAuth('../conf/cred.json')
  api = setupAPI(myauth)
  hashtags = dumpHashtags(api, 10, 1)
  hashtags = [str(ht) for ht in hashtags]
  output = ' '.join(hashtags)
  with open('hashtags.txt', 'w') as out_file:
    out_file.write(output)

if __name__ == "__main__":
  main()
