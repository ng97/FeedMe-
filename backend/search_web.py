import sys
import requests
from backend.mongodb import MongoCollection 
import tweepy
from tweepy import OAuthHandler
import backend.credentials as credentials
import json

connect = MongoCollection(collectionname='test3', MongoURI="mongodb://localhost:27017/")

#method to fetch from News API
def search_NewsAPI(query):
    
    url = 'https://newsapi.org/v2/everything?'
    print(query)
    
    parameters = {
        'q': query, # query phrase
        'pageSize': 20,  # maximum is 100
        'apiKey': credentials.NEWS_API_KEY # your own API key
    }

    response = requests.get(url, params=parameters)

    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    for i in response_json['articles']:
        news= {'data':i, 'query':query, 'platform':'Google News'}
        print(news)
        connect.insert(news)
    print(response_json)

    return response_json

def search_TwitterAPI(query):
    auth= OAuthHandler(credentials.CONSUMER_KEY,credentials.CONSUMER_KEY_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN,credentials.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    tweets=[]

    for tweet in tweepy.Cursor(api.search,q=query,lang="en").items():
        tweets.append(tweet)
        tweet_json= {'data':tweet._json, 'query':query, 'platform':'Twitter'}
        print(tweet_json)
        connect.insert(tweet_json)  #inserting tweets

    return tweets
    