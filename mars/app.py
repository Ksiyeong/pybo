from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client['e-room']

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/mars", methods=["POST"])
def web_mars_post():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    size_receive = request.form['size_give']
    doc = {
        'name' : name_receive,
        'address' : address_receive,
        'size' : size_receive
    }
    db.mars.insert_one(doc)
    return jsonify({'msg': '주문 완료!'})

@app.route("/mars", methods=["GET"])
def web_mars_get():
    doc = list(db.mars.find({}, {'_id' : False}))
    return jsonify({'msg': '접속 완료!', 'doc' : doc})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)