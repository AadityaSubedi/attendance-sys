from flask import Flask, Blueprint, send_from_directory, render_template
from flask.templating import render_template_string
from flask_jwt_extended import jwt_manager, JWTManager
from attendance import attendance_bp
from train import train_bp
from flask_restful import Resource, Api
from flask_cors import CORS
from auth import user_bp
from flask import request
import uuid



UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)




app.register_blueprint(user_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(train_bp)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_SECRET_KEY'] = 'will_edit_this_secret_key'



api ="sl.BBKkaWiIINg06-43YK3JxCV8JTjj9AUf2EEnDEZ57KLkgta_ge2h7PwSqjLnVfBm2nQwOG5BqSLCTccVWU1NPcICpA_siMNwKOuRKEDqT70vIJFT-dc5ZIOmLlhQ98kZJISDSPA"

import dropbox
@app.route("/", methods=['GET', 'POST'])
def hello():
    file = request.files.get('image')
    if file:
        filename = f"{uuid.uuid4()}.jpg"
        dbx = dropbox.Dropbox(api)
        x = dbx.files_upload(file.stream.read(), path=f"/images/{filename}")
        print(x)
    return {"hey": "msg"}



@app.route('/images/<string:imagename>')
def download_image(imagename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               'images/'+imagename)


@app.route('/files/<string:imagename>')
def download_pdf(imagename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               'files/'+imagename)

jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    print("----------------------------------")
    return {
        'data1': 'happy coding ',
        'data2': 'happy coding 2',

    }


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(decrypted_token):
    return decrypted_token['jti'] in {"[blocklist of jti]"}
    #  modify this as per the need later


CORS(app)  # This will enable CORS for all routes


if __name__ == "__main__":
    app.run()

