import sys
import requests
from backend.mongodb import MongoCollection 
import tweepy
from tweepy import OAuthHandler
import backend.credentials as credentials
import json
import asyncio  
import aiohttp 
import signal
import time
import pprint
from googleapiclient.discovery import build

# from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream

connect = MongoCollection(collectionname='google_test', MongoURI="mongodb://localhost:27017/")

#method to fetch from News API
def search_NewsAPI(query):
    
    url = 'https://newsapi.org/v2/everything?'
    print(query)
    
    parameters = {
        'q': query, # query phrase
        'pageSize': 20,  # maximum is 100
        'apiKey': credentials.NEWS_API_KEY # your own API key
    }

    all_news= []

    try:
        response = requests.get(url, params=parameters)

        # Convert the response to JSON format and pretty print it
        response_json = response.json()
        for i in response_json['articles']:
            news= {'data':i, 'query':query, 'platform':'Google News'}
            all_news.append(i)
            print(news)
            connect.insert(news)
        print(response_json)

    except Exception as e:
        print('Error',e)
    return all_news

#method to fetch from Google Search API
def search_GoogleAPI(query):
    url = 'https://www.googleapis.com/customsearch/v1'
    print(query)
    
    parameters = {
        'q': query, # query phrase
        'cx': credentials.SEARCH_ID,  # search engine ID
        'key': credentials.GOOGLE_API_KEY # your own API key
    }

    res= []

    try:
        response = requests.get(url, params=parameters)
        # Convert the response to JSON format and pretty print it
        response_json = response.json()
        for i in response_json['items']:
            google_data= {'data':i, 'query':query, 'platform':'Google Search'}
            res.append(i)
        #     print(news)
            connect.insert(google_data)
        print(response_json['items'])

    except Exception as e:
        print('Error',e)
    return res

def search_TwitterAPI(query):
    auth= OAuthHandler(credentials.CONSUMER_KEY,credentials.CONSUMER_KEY_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN,credentials.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    tweets=[]
    time_started = time.time()

    try: 
        for tweet in tweepy.Cursor(api.search,q=query,lang="en", timeout=60).items():
            # ,  wait_on_rate_limit=True
            if(time.time() > time_started+30):
                tweets.append(tweet)
                tweet_json= {'data':tweet._json, 'query':query, 'platform':'Twitter'}
                print(tweet_json)
                connect.insert(tweet_json)  #inserting tweets
                return tweets

    except Exception as e:
        print('Error',e)
    # return tweets
    # listener= StreamingTweets()
    # auth= OAuthHandler(credentials.CONSUMER_KEY,credentials.CONSUMER_KEY_SECRET)
    # auth.set_access_token(credentials.ACCESS_TOKEN,credentials.ACCESS_TOKEN_SECRET)

    # stream= Stream(auth, listener)

    # stream.filter(track=[query])
    

# def searchAllApis(query):
#     print('here',query)
    
#     async def get_tweets(query): #asynchronious function for twitter API
#         auth= OAuthHandler(credentials.CONSUMER_KEY,credentials.CONSUMER_KEY_SECRET)
#         auth.set_access_token(credentials.ACCESS_TOKEN,credentials.ACCESS_TOKEN_SECRET)
       
#         print('now',query)
#         api = tweepy.API(auth)
#         tweets=[]
#         print('Getting all tweets...')
#         for tweet in tweepy.Cursor(api.search,q=query,lang="en", timeout=60).items():
#             tweets.append(tweet)
#             tweet_json= {'data':tweet._json, 'query':query, 'platform':'Twitter'}
#             print(tweet_json)
#             # connect.insert(tweet_json)  #inserting tweets
#         return tweets
    
#     async def get_news(query): #asynchronious function for News API
#         print('finally')
#         # await get_tweets(query)

#         parameters = {
#             'q': query, # query phrase
#             'pageSize': 20,  # maximum is 100
#             'apiKey': credentials.NEWS_API_KEY # your own API key
#         }
#         print('now',query)
#         url = 'https://newsapi.org/v2/everything?'
#         print('Getting all news...')
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, params=parameters) as resp: #get request using aiohttp client
#                 print(resp)
#                 data = await resp.json()
#                 # return data
#                 for i in data['articles']:
#                     news= {'data':i, 'query':query, 'platform':'Google News'}
#                     print(news)
#                     # connect.insert(news)
#                 return data
                

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     currentTasks=[get_tweets(query),get_news(query)]
#     loop.run_until_complete(asyncio.gather(*currentTasks))

# class StreamingTweets(StreamListener):  #class the listens for streaming data
#     def on_data(self, data):  #function that gets data from streaming API
#         try:
#             #for tweet in data:  # looping through data for individual tweets
#             print(data)
#             tweets= json.loads(data)
#             connect.insert(tweets)  #inserting tweets
#             return True
#         except BaseException as e:
#             print('An error occurred with streaming API', e)
#             pass

#     def on_error(self, status):
#         print(status)
#         pass