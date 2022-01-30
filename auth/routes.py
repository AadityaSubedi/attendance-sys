from flask_jwt_extended.utils import get_jwt_identity
from auth.models import User
from flask_restful import Resource
from . import user_api
from flask import Flask, request
from .models import User
from database import DB

from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jti
    
)


from json import loads
from bson.json_util import dumps

from utils import helper_functions as hf
from utils import file_helper_functions as fhf


@ user_api.resource("/register")
class RegisterUsers(Resource):
    @ jwt_required()
    def post(self):
        try:
            inputData = {
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'password': request.form.get('password'),

            }
            file = request.files['image']
            # handle file upload
            filename = None
            if file:
                filename = fhf.save_image(file)

            user = User(
                username=inputData['username'], email=inputData['email'], password=inputData['password'], image=filename)
            registered_user = user.save()

            token = {}
            token['access_token'] = create_access_token(
                identity=inputData['username'], fresh=True)
            token['refresh_token'] = create_refresh_token(
                identity=inputData['username'])

            return (hf.success(
                    "user registration",
                    "user registered succesfully",
                    token
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "user registration",
                    str(e),
                    ),
                    500
                    )




    # @ jwt_required()
    def get(self):
        try:


            users = DB.find_many(User.collection, {}, ["username","email"])



            return (hf.success(
                    "registered users",
                    "registered users fetched succesfully",
                    loads(dumps(users))
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "Fetching registered users",
                    str(e),
                    ),
                    500
                    )


@ user_api.resource("/login")
class LoginUser(Resource):
    def post(self):
        try:
            inputData = request.get_json()
            user = DB.find_one(User.collection, {
                'username': inputData['username']})

            assert user and safe_str_cmp(
                user['password'], inputData['password']), "Invalid credentials"

            token = {
                'access_token': create_access_token(
                    identity=user['username'], fresh=True),
                'refresh_token': create_refresh_token(
                    identity=user['username'])

            }

            # return the command line output as the response
            return (hf.success(
                    "user login",
                    "user logged in succesfully",
                    token
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "user login",
                    str(e),
                    ),
                    401
                    )


@user_api.resource("/refresh")
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, fresh=False)

            token = {
                'access_token': new_token,
            }

            # return the command line output as the response
            return (hf.success(
                    "token refresh",
                    "token refreshed succesfully",
                    token
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "user login",
                    str(e),
                    ),
                    401
                    )




@user_api.resource("/logout")
class Logout(Resource):
    @jwt_required()
    def post(self):
        try:
            jti =get_jti()
            # TODO: add this jti to  blacklist 
            #  using redis or db

            # return the command line output as the response
            return (hf.success(
                    "User logout",
                    "user logged out succesfully",
                    
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "user logout",
                    str(e),
                    ),
                    401
                    )
