from email.policy import default
import json
from bson import json_util
from pymongo import MongoClient

connection_string = "mongodb+srv://admin:admin1234@cluster0.460h8.mongodb.net/?retryWrites=true&w=majority"
# mongodb+srv://admin:<password>@cluster0.460h8.mongodb.net/?retryWrites=true&w=majority

client = MongoClient(connection_string)

dbs = client.list_database_names()

Twitter_db = client['Twitter']

Users_collection = Twitter_db['Users']
Tweets_collection = Twitter_db['Tweets']
# print(Users_collection)


def create_user(data):
    createdUser = Users_collection.insert_one(data)
    inserted_user = list(Users_collection.find({"username":data['username']}))
    return json.loads(json.dumps(inserted_user, default=json_util.default))

def all_tweets():
    tweets = list(Tweets_collection.find({}))
    return json.loads(json.dumps(tweets, default=json_util.default))


def insert_tweet(data):
    rec_id1 = Tweets_collection.insert_one(data)
    inserted_data = list(Tweets_collection.find({}))
    return json.loads(json.dumps(inserted_data, default=json_util.default))

def find_user(data):
    User = list(Users_collection.find({"username":data}))
    # print("utils.py   ",User[0])
    return User[0]


def search(data):
    # Tweets_collection.create_index([('tweet', pymongo.TEXT)], name='search_index', default_language='english')

    # Tweets_collection.create_index({"tweet" : "text" , "fullname" : "text"})
    # foundData = list(Tweets_collection.find({ "$text": { "$search": "sundar" } }))
    # print("found data",data)
    searchText = '*' + data["searchText"] + '*'
    print(searchText)
    foundData = list(Tweets_collection.aggregate([
    {
        "$search": {
            "index" : "tweets",
            "wildcard": {
                "query": searchText,
                "path": ["tweet" , "fullname"],
                "allowAnalyzedField": True,
            }
        }
    },
    ]))

    
    print("found data", foundData)
    return json.loads(json.dumps(foundData, default=json_util.default))


# ans = all_tweets()
# print(" data",type(ans))
# print(ans[0])
# print(ans[1])
