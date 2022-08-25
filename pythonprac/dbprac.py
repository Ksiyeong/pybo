from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['test']
##################################

db.users.delete_one({'name':'bobby'})