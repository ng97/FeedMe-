import sys
sys.path.insert(0, '..')
from backend import search_web as searchapi
from backend import data_processing as dp
from flask import request, jsonify, render_template
from app import app
from backend.mongodb import MongoCollection 
import datetime
import json
import urllib.request

# Homepage.
@app.route('/')
@app.route('/home')
def home():
    #connection to db
    connect = MongoCollection(collectionname='queries', MongoURI="mongodb://localhost:27017/")
    res= connect.return_events_tracked()
    return render_template('home.html', title='Home', events= res, search= True)

# Method to retrieve tweets when user submitted query + number of tweets.
@app.route("/search", methods= ['POST'])
def search():
    #connection to db
    connect = MongoCollection(collectionname='queries', MongoURI="mongodb://localhost:27017/")
    # Get form inputs.
    # apis= []
    query= request.form['query']
    # twitter= request.form['twitter']
    # news_check= request.form['news']
    

    #check if query already searched for
    response= connect.find(query)

    #check if query in store
    if response == None:
        query_json= {'query':query, 'time_searched': datetime.datetime.now()}
        connect.insert(query_json)
    else:
        connect.update_query_time(query,datetime.datetime.now())
    
    try:
        # Get data from APIs.
        # if (news_check):
            # news_data = searchapi.search_NewsAPI(query)
        # if (twitter):
            # all_tweets= searchapi.search_TwitterAPI(query)
        # elif (twitter == '' and news_check == ''):
            # news_data = searchapi.search_NewsAPI(query)
            # google_data = searchapi.search_GoogleAPI(query)
            all_tweets= searchapi.search_TwitterAPI(query)
            # all_data= dp.get_query_suggestions(query)
        
        

    except Exception:
        return render_template('search.html', news="No Data Found")
    # Loop over retrieved tweets to get corresponding HTML.
    # for tweet in all_tweets:
    #         try:
    #             # Get embedded HTML from Twitter API to make tweets pretty.
    #             url= 'https://publish.twitter.com/oembed?url=https://twitter.com/anybody/status/'+ tweet['id'] + '?maxwidth=220'
    #             response = urllib.request.urlopen(url)
    #             data = json.load(response)
    #             tweet['html'] = data['html']
    #         except:
    #             # change back to home.html
    #             return render_template('search.html', no_tweets_found_error=False, oembed_error=True)
                # return render_template('search.html', tweets=tweets, query= query)
    
    # # Order tweets.
    # tweets = order_chronological(tweets)
    # Add HTML of tweets to grid with pagination.
    # html = beautify_html(tweets.copy())
    # print(html)
    # return render_template('search.html', news=news_data, data= all_data, tweets=html, query= query)
    # print(all_tweets['html'])
    # return render_template('search.html', news="No Data Found")
    return render_template('search.html', tweets=all_tweets, query= query)
    # return render_template('search.html', news=news_data, query= query)
    # return render_template('search.html', google=google_data, query= query)

# Add HTML of tweets to a grid with pagination.
def beautify_html(tweets):
    data_page = 1
    html = '<div class="pagination-container"><div data-page="1"><div class="row">'

    # Loop over HTML of tweets and add to grid of two columns.
    for i in range(0, len(tweets)):
        if i == len(tweets) - 1:
            html += '<div class="col-sm">' + tweets[i]['html'] + '</div>'
            html += '</div></div>'
            break

        # After 20 tweets, add new page.
        if i % 20 == 0  and i != 0:
            data_page += 1
            html += '</div></div><div data-page="' + str(data_page) + '" style="display:none;"><div class="row">'

        # Create new row when two columns are added.
        if i % 2 == 0 and i != 0 and i % 20 != 0:
            html += '</div><div class="row">'

        # Add tweet HTML to column.
        html += '<div class="col-sm">' + tweets[i]['html'] + '</div>'

    # Add page numbers to bottom of grid.
    html += """<div class="text-center">
                <div class="pagination pagination-centered">
                  <ul class="pagination ">
                    <li data-page="-" ><a href="#" class="page-link">&lt;</a></li>
                    <li data-page="1"><a href="#" class="page-link">1</a></li>"""

    for i in range(2, data_page + 1):
        html += '<li data-page="' + str(i) + '"><a href="#" class="page-link">' + str(i) + '</a></li>'

    html += """     <li data-page="+"><a href="#" class="page-link">&gt;</a></li>
                   </ul>
                  </div>
                 </div>
                </div>"""

    return html

def order_chronological(tweets):
    return sorted(tweets, key=lambda k: k['created_at'], reverse=True)

def order_reverse_chronological(tweets):
    return sorted(tweets, key=lambda k: k['created_at'])

def check_media(media_only, tweet):
    if media_only == 'true':
        if not tweet['Media'] == True:
            return False

    return True
