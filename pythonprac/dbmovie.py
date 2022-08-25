from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client['dbsparta']

db.movies.update_one({'title': '가버나움'}, {'$set': {'star': str(0)}})