import os
import time
import hashlib
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
DOWNLOAD_FOLDER = '/down'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config.update(
    MONGO_URI='mongodb+srv://heng:HH970218hh@hh-0-jo59l.mongodb.net/4440?retryWrites=true',
)
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def up():
    if request.method == 'GET':
        f = open("./upload.html")
        content = f.read()
        return bytes(content, 'UTF-8')
    else:
        print(request)

        f = request.files['file']
        f.save(secure_filename(f.filename))

        return render_template("success.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save("tmpfile")
        # tmpfile is the uploaded file

        # curtime, tag1, tag2, ... tagn are returned by ML model

        # compute a hash of time||tag1||tag2||...||tagn

        '''
        store the hash in MangoDB with json{
            name = hash
            uptime = timestamp
            tag = []
        }
        '''
        cur_time = time.time()
        all_tags = []
        name_str = "" + str(cur_time)
        for tag in all_tags:
            name_str += str(tag)
        m = hashlib.sha256()
        m.update(name_str.encode('utf-8'))
        hashed_str = m.hexdigest()

        one_document = {"name" : hashed_str, "time" : cur_time, "tag" : all_tags}
        
        result = mongo.db.pic.insert_one(one_document)
        print(result)
        
        '''
        upload the tmpfile to azure with name=hash
        '''

        return render_template("success.html")

@app.route('/download', methods=['GET', 'POST'])
def down():
    if request.method == 'GET':
        return render_template("download.html")
    else:
        return render_template("success.html")

@app.route('/downloader', methods=['GET','POST'])
def find_file():
    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        all_tags = request.form['tags']
        print(start_time, end_time, all_tags)
        # parse all tags

        # search on mongodb

        # download the pics from azure

        # show the pictures

        return render_template("select.html")