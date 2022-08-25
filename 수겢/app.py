from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client['e-room']

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']
    doc = {
        "nickname" : nickname_receive,
        "comment" : comment_receive
    }
    db.homework.insert_one(doc)
    return jsonify({'msg':'응원 남기기 완료!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    doc = list(db.homework.find({}, {"_id" : False}))
    return jsonify({'msg':'새로고침 완료!', 'doc' : doc})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)