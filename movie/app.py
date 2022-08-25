from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client['e-room']

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    img = soup.select_one('meta[property="og:image"]')['content']
    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    doc = {
        'img' : img,
        'title' : title,
        'desc' : desc,
        'star' : star_receive,
        'comment' : comment_receive
    }
    db.movies.insert_one(doc)
    return jsonify({'msg':'기록 완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    doc = list(db.movies.find({}, {"_id" : False}))
    return jsonify({'msg':'접속 완료!', 'doc' : doc})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)