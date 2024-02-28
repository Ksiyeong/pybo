from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('주소', tlsCAFile=ca)
db = client.projects

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/best', methods=['GET'])
def show_record():
   record_list = list(db.best.find({}, {'_id' : False}))
   return jsonify({'record_list' : record_list, 'msg' : '이 요청은 GET!'})

@app.route('/best', methods=['POST'])
def save_record():
   title_receive = request.form['title_give']
   address_receive = request.form['address_give']
   google_receive = request.form['google_give']
   diary_receive = request.form['diary_give']
   doc = {
      'title': title_receive,
      'address': address_receive,
      'google': google_receive,
      'diary': diary_receive
   }
   db.best.insert_one(doc)
   return jsonify({'msg': '기록 완료!'})

@app.route("/apply_photo")
def save_doc():
    doc = {
       'title': request.args.get('input_title'),
       'address': request.args.get('input_address'),
       'google': request.args.get('input_address_url'),
       'diary': request.args.get('input_diary')
    }
    db.best.insert_one(doc)
    return render_template('apply_photo.html')

@app.route("/", methods=['POST'])
def upload_done():
   uploaded_files = request.files["file"]
   uploaded_files.save("static/img/{}.jpg".format(now_index()))
   return redirect(url_for("home"))

def now_index():
   record_list = list(db.best.find({}, {'_id' : False}))
   return len(record_list) - 1

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
