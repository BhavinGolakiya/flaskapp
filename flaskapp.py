import os
import requests
from flask_cors import CORS
import subprocess
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO
from flask_autoindex import AutoIndex
import uuid
import shutil

UPLOAD_FOLDER = '/app/htmlfile'
ppath = "/app/htmlfile"

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
AutoIndex(app, browse_root=ppath)    

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
    # check if file selected or not
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
    # check if file is there thne perform uploading and convert in to html
        filename = secure_filename(file.filename)
        random_name  = uuid.uuid4().hex.lower()[0:6]
        pdf_name = '.pdf'
        o_name = "".join([random_name,pdf_name])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], o_name))
        # path = "/app/htmlfile/"+o_name+""
        path = os.path.join(app.config['UPLOAD_FOLDER'], o_name)

        try:
            print(path)
            print("-----------------------------------------")
            subprocess.call(["pdf2htmlEX" ,path], shell=True)
            print("=========================================")
            # htmlfile = "".join([random_name,'.html'])
            # shutil.move("/app/"+htmlfile+"", "/app/htmlfile/"+htmlfile+"")
        except Exception as e:
            print(e)
        data = jsonify({'message' : 'File successfully converted',"file": "".join([random_name,'.html'])})
        data.status_code = 201
        # os.remove("/app/htmlfile/"+o_name+"")
        return data
    else:
        resp = jsonify({'message' : 'Allowed file types pdf'})
        resp.status_code = 400
        return resp

if __name__ == "__main__":
    app.run()