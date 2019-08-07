from backend.mongodb import MongoCollection
import spacy
import pandas as pd
import itertools
import collections

"""
Majority of the code is gotten from the Text as Data Lab Solutions by Dr. Jeff Dalton

"""

#connection to db
connect = MongoCollection(collectionname='new_data_collect', MongoURI="mongodb://localhost:27017/")

def get_query_suggestions(query):
# query= "world cup" 
    # print(query)
    data= connect.return_text_by_query(query)

    # print(" waiting " ,data)

    data_list = list()

    for i in data:
        # print(i['data']['content'])
        if i['platform'] == "Twitter":
            data_list.append( i['data']['text'])
        if i['platform'] == "Google News":
            data_list.append( i['data']['description'])
                    

    collabels = ['content']
    new_all_data = pd.DataFrame(data_list, columns=collabels)
    # print(new_all_data)

    
    all_posts_tokenized = new_all_data.content[:10].apply(spacy_tokenize)
    # print(all_posts_tokenized)

    # A single variable with the (flattened) tokens from all posts.
    flat_tokens = list(itertools.chain.from_iterable(all_posts_tokenized))
    # print(flat_tokens)

    #most frequent tokens
    raw_words = [t.text for t in flat_tokens]
    raw_count = collections.Counter(raw_words)
    print(raw_count.most_common(20))

    # for title in new_all_data.content:
    #     doc = nlp(title)
        
    #     for token in doc:
    #         print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(
    #         token.text,
    #         token.idx,
    #         token.lemma_,
    #         token.is_punct,
    #         token.is_space,
    #         token.shape_,
    #     ))
    return new_all_data.head()

def spacy_tokenize(string):
  nlp = spacy.load("en_core_web_sm")
  tokens = list()
  doc = nlp(string)
  for token in doc:
    #   print(token)
      tokens.append(token)
  return tokens
    