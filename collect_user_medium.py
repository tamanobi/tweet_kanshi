import tweepy
import json
import sys
import os

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user_ids = []
with open('user_ids.txt', 'r') as f:
    user_ids = [line.strip() for line in f]

urls_in_tl = [];
for user_id in user_ids:
    tl = api.user_timeline(user_id)
    for tweet in tl:
       if tweet.text.startswith('RT @'):
           continue
       if tweet.entities is not None or hasattr(tweet, 'extended_entities'):
           if hasattr(tweet, 'extended_entities'):
               entities = tweet.extended_entities
           else:
               entities = tweet.entities

           if 'media' in entities:
               medium = tweet.entities.get('media')
               for media in medium:
                   # print(media)
                   if media.get('type') != 'photo':
                       continue

                   if 'media_url_https' in media:
                       orig_url = "{}:orig".format(media.get('media_url_https'))
                       urls_in_tl.append((user_id, tweet.id_str, orig_url, tweet.retweet_count, tweet.favorite_count, tweet.created_at))

print(urls_in_tl)
