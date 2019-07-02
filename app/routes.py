import sys
sys.path.insert(0, '..')
from backend import search_web as searchapi
from flask import request, jsonify, render_template
from app import app
from backend.mongodb import MongoCollection 
import datetime

# Homepage.
@app.route('/')
@app.route('/home')
def home():
        return render_template('search.html', title='Home', search= True)

# Method to retrieve tweets when user submitted query + number of tweets.
@app.route("/search", methods= ['POST'])
def search():
    #connection to db
    connect = MongoCollection(collectionname='queries', MongoURI="mongodb://localhost:27017/")
    # Get form inputs.
    query= request.form['query']
    response= connect.find(query)
    # response= response.json()

    if response == None:
        query_json= {'query':query, 'time_searched': datetime.datetime.now()}
        connect.insert(query_json)
    else:
        connect.update_query_time(query,datetime.datetime.now())
    
    try:
        # Get news from APIs.
        news_data = searchapi.search_NewsAPI(query)
        tweets= searchapi.search_TwitterAPI(query)
    except Exception:
        return render_template('search.html', news="No Data Found")
    # Loop over retrieved tweets to get corresponding HTML.
    # for tweet in tweets:
    #         try:
    #             # Get embedded HTML from Twitter API to make tweets pretty.
    #             url= 'https://publish.twitter.com/oembed?url=https://twitter.com/anybody/status/'+ tweet['Postid'] + '?maxwidth=220'
    #             response = urllib.request.urlopen(url)
    #             data = json.load(response)
    #             tweet['html'] = data['html']
    #         except:
    #             return render_template('home.html', no_tweets_found_error=False, oembed_error=True)
    
    return render_template('search.html', news=news_data, tweets=tweets, query= query)
    # return render_template('search.html', tweets=tweets, query= query) 
