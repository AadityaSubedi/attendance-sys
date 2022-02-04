from flask import Flask
from attendance.models import Classes
from auth.models import User
from flask_restful import Resource
from . import attendance_api
from flask import Flask, request
from flask_bcrypt import Bcrypt
from auth.models import Teacher
from database import DB
from threading import Thread
import time

from . import attendance_helper_functions as ahf

from json import loads
from bson.json_util import dumps

from utils import helper_functions as hf
from utils import file_helper_functions as fhf
from utils import webcam

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jti
)

app = Flask("after_response")


@ attendance_api.resource("/takeattendance")
class TakeAttendance(Resource):
    # @ jwt_required()
    def get(self):
        try:
            class_name = request.form.get('classname')
            subject_name = request.form.get('subjectname')
            attandence_time = request.form.get('time')
            names=set()

            def long_recognization(time):
              global names
              names = webcam.predict(time)
              names = list(names)
              class_attendance = Classes(class_name=class_name, subject_name=subject_name, attendees=names)
              if class_attendance.check_subject():
                class_attendance.add_date()
              elif class_attendance.check_class():
                class_attendance.add_subject()
              else:
                class_attendance.save()
              print(names)

            thread = Thread(target=long_recognization, kwargs={'time': attandence_time})
            thread.start()

            # return the command line output as the response
            return (hf.success(
                    "take attendance",
                    "attendance started",
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "take attendance",
                    str(e),
                    ),
                    401
                    )


