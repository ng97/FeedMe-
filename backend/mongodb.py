import pymongo
import datetime

class MongoCollection:

    def __init__(self, collectionname ,databasename='Feedme',MongoURI="mongodb://localhost:27017/"):
        """
        connect to cloud database default. chage to local,set:  MongoURI="mongodb://localhost:27017/"
        collections: Test;Train;Tweets; default:func_test to test
        create MongoClient instance
        """
        try:
            self.client = pymongo.MongoClient(MongoURI)
            print("connected to client:" + repr(self.client.list_database_names()))
            self.database = self.client[databasename]
            self.collection = self.database[collectionname]
        except pymongo.errors.ConnectionFailure:
            print("failed to connect")
            raise pymongo.errors.ConnectionFailure

    def insert(self, item):
        """
        Insert the given item to the collection

        :param item: item to insert
        """
        try:
            self.collection.insert(item)
        except Exception as e:
            print("Error", e)


    def find(self, query):
        """
        Find a document into this MongoCollection.

        :param query: query for search
        :return: documents returned by query
        """
        print("here", query)
        print(self.collection)
        try:
           return self.collection.find({"query" : str(query)})
        except Exception as e:
            print("Error", e)

    def set_collection(self,collectionname): 
        """
        Change the collection to the given collection name.

        :param collectionname: collection to change to
        """
        if collectionname in ['Test',"Train","Training_token","TweetsData",'queries']:
            self.collection=self.database[collectionname]
            return self
        else:
            # raise collectionException(e)
            print("No such collection")
        

    def find_all(self):
        """
        Find all documents in the collection 

        :return: all documents
        """
        try:
            x = self.collection.find()
        except Exception as e:
            print("Error", e)
        return x

    def print_all(self):
        """
        Print all documents in the collection.
        """
        for e in self.find_all():
            print(e)

    def update_query_time(self,query,time):
        """
        updata category for given Tweets

        :param category: postid, category
        :return: -
        """
        try:
            myquery = { "query": query }
            newvalues = { "$set": { "time_searched": time } }
            self.collection.update_many(myquery,newvalues)
        except Exception as e:
            print("Error", e)

    def return_text_by_query(self,query):
        """
        Return all text about a query in collection.

        :return: list of all data about a query
        """

        l=[]
        all = self.find_all_queries(query)
        for e in all:
            l.append({"data":e["data"], "platform": e["platform"]})
        return l
    
    def find_all_queries(self, query):
        """
        Find all documents in the collection 

        :return: all documents
        """
        try:
            x = self.collection.find({"query" : str(query)})
        except Exception as e:
            print("Error", e)
        return x

    def return_events_tracked(self):
        """
        Return all events/queries being tracked today in collection.

        :return: list of all first query still being updated today
        """

        l=[]
        all = self.find_all_events()
        for e in all:
            l.append({"query":e["query"], "time_searched": e["time_searched"]})
        return l

    def find_all_events(self):
        """
        Find all events from today in the collection 

        :return: all events from today
        """
        try:
            today= datetime.datetime.today()
            x = self.collection.find({"time_searched" : {"$lt": today}})
        except Exception as e:
            print("Error", e)
        return x

    class collectionException(Exception):
        print('your collection is not in our collection list, please read Readme.md to set correct collections')
        pass