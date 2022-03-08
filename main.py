from flask import Flask, Blueprint, after_this_request, send_file, send_from_directory, render_template
from flask.templating import render_template_string
from flask_jwt_extended import jwt_manager, JWTManager
from attendance import attendance_bp
from train import train_bp
from flask_restful import Resource, Api
from config import JWT_SECRET_KEY
from flask_cors import CORS
from auth import user_bp
from flask import request
import uuid
from flask import Response
import os


UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)


app.register_blueprint(user_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(train_bp)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY


# import dropbox
# @app.route("/", methods=['GET', 'POST'])
# def hello():
#     return {1:2}


@app.route('/')
def index():
    @after_this_request
    def add_header(response):
        print("after request")
        return response
    return 'Hello World!'


@app.route('/face/<string:imagename>', methods=['GET', 'POST'])
def download_and_remove_detected_face(imagename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               'temp/'+imagename)


jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    return {
        'data1': 'happy coding ',
        'data2': 'happy coding 2',

    }


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(_,decrypted_token):
    return decrypted_token['jti'] in {"[blocklist of jti]"}
    #  modify this as per the need later


CORS(app)  # This will enable CORS for all routes


if __name__ == "__main__":
    app.run()
