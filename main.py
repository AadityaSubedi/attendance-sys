from flask import Flask, Blueprint, send_from_directory, render_template
from flask.templating import render_template_string
from flask_jwt_extended import jwt_manager, JWTManager
from attendance import attendance_bp
from flask_restful import Resource, Api
from flask_cors import CORS
from auth import user_bp





app = Flask(__name__)




app.register_blueprint(attendance_bp)
app.register_blueprint(user_bp)

app.config['JWT_SECRET_KEY'] = 'will_edit_this_secret_key'





@app.route("/")
def hello():
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

