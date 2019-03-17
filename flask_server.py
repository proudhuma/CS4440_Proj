import os
import time
import hashlib
from flask import Flask, flash, request, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config.update(
    MONGO_URI='mongodb+srv://heng:HH970218hh@hh-0-jo59l.mongodb.net/4440?retryWrites=true',
)
mongo = PyMongo(app)

@app.route('/')
def index():
    f = open("./index.html")
    content = f.read()
    return bytes(content, 'UTF-8')

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

        f = open("success.html")
        response = f.read()
        return bytes(response, 'UTF-8')

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
        m.update(name_str)
        hashed_str = m.hexdigest()

        one_document = {"name" : hashed_str, "time" : cur_time, "tag" : all_tags}
        
        result = mongo.db.pic.insert_one(one_document)
        print(str(result.inserted_count) + " document is inserted succesfully")
        
        '''
        upload the tmpfile to azure with name=hash
        '''

        ff = open("success.html")
        response = ff.read()
        return bytes(response, 'UTF-8')

@app.route('/download', methods=['GET', 'POST'])
def down():
    if request.method == 'GET':
        f = open("./download.html")
        content = f.read()
        return bytes(content, 'UTF-8')
    else:
        f = open("success.html")
        response = f.read()
        return bytes(response, 'UTF-8')