from turtle import update
from flask_jwt_extended.utils import get_jwt_identity
from auth.models import User
from flask_restful import Resource
from . import train_api
from flask import Flask, request
from flask_bcrypt import Bcrypt
from database import DB

from . import train_helper_functions as thf

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

from .models import Cache
from .train_helper_functions import start_training
from threading import Thread


@train_api.resource("/start")
class StartTrain(Resource):
    # @ jwt_required()
    def post(self):
        try:
            cacheInstance = DB.find_one(Cache.collection, {'type': 'cache'})
            isModelTraining = False
            if cacheInstance is None:
                cacheInstance = Cache()
                cacheInstance.save()
            else:
                isModelTraining = cacheInstance['ModelTraining']['isModelTraining']
            assert not isModelTraining, "Model is already training."

            Thread(target=start_training, args=()).start()

            return (hf.success(
                    "data training",
                    "data training started",

                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "model training",
                    str(e),
                    ),
                    500
                    )

   



@train_api.resource("/upload")
class UploadData(Resource):
    # @ jwt_required()
    def post(self):
        try:
            # uploads the confirmed data to the local location
            images = request.files.getlist("images")
            label = request.form.get("label")
            for image in images:
                fhf.save_image(image,dir = "datasets",subdir=label)
            # (fhf.save_image(image,dir=label) for image in images)

        

            return (hf.success(
                    "data uploads",
                    "data uploaded successfully",

                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "data uploads",
                    str(e),
                    ),
                    500
                    )

   