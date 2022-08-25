from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client['e-room']

star = db.movies.find_one({"rank" : "30"})["star"]

stars = list(db.movies.find({"star" : star}))

print(len(stars))