from flask import Flask, jsonify, Response
import json
from bson import json_util
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
from utils import videoStream
from json import loads
from bson.json_util import dumps

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jti
)

@ attendance_api.resource("/userinfo")
class UserInfo(Resource):
    @ jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            user = DB.find_one(Teacher.collection,{"user_id":username})
            assert user, f"user doesn't exist"

            # return the command line output as the response
            return (hf.success(
                    "user info",
                    "user info fetched succesfully",
                    loads(dumps(user)),
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "user Info",
                    str(e),
                    ),
                    500
                    )


@ attendance_api.resource("/takeattendance")
class TakeAttendance(Resource):
    # @ jwt_required()
    def post(self):
        try:
            inputData = request.get_json()
            subject_name, class_name, attandence_time = inputData['subjectname'], inputData['classname'] , inputData['time']
            names=set()
            def long_recognization(time):
              global names
              names = webcam.predict(time)
              names = list(names)
              class_attendance = Classes(class_name, subject_name, names)
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
                    f"attendance started for {attandence_time} minutes",
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "take attendance",
                    str(e),
                    ),
                    500
                    )


@ attendance_api.resource("/getattendancelist")
class GetAttendanceList(Resource):
  def get(self):
    try:
      inputData = request.args
      class_name = inputData.get('classname')
      subject_name = inputData.get('subjectname')
      class_attendance = Classes(class_name)
      class_attendance = class_attendance.find_attendance()   
      attendance_list = class_attendance['attendance'][subject_name]
      return (hf.success(
                    "get attendance list",
                    f"attendance list for {class_name}, ({subject_name}).",
                    attendance_list
                    ),
                    200
                    )

    except Exception as e:
        return (hf.failure(
                "get attendance list",
                str(e),
                ),
                500
                )

@ attendance_api.resource("/getattendance")
class GetAttendance(Resource):
    # @ jwt_required()
    def get(self):
        try:
            inputData = request.get_json()
            subject_name, class_name, date = inputData['subjectname'], inputData['classname'], inputData['date']

            class_attendance = Classes(class_name)
            classattendance = class_attendance.find_attendance()
            print(classattendance)
            attendance = classattendance['attendance'][subject_name][date]
            # return the command line output as the response
            return (hf.success(
                    "get attendance",
                    f"attendance for {inputData['date']}.",
                    attendance
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "get attendance",
                    str(e),
                    ),
                    401
                    )


@ attendance_api.resource("/getinfo")
class GetStudentInfo(Resource):
    # @ jwt_required()
    
    
    def get(self):
        try:
            dataIn = request.args
            class_name = dataIn.get('classname')
            subject_name = dataIn.get('subjectname')
            class_attendance = Classes(class_name)
            classattendance = class_attendance.find_attendance()
            print(classattendance)
            attendance = classattendance['attendance'][subject_name]
            total_days = len(attendance)
            working_days = ahf.countDays(attendance)
            return_item = {
                          'total_days': total_days,
                          'working_days': working_days
                          }

            # return the command line output as the response
            return (hf.success(
                    "get student info",
                    f"sucessfully loaded.",
                    return_item
                    ),
                    200
                    )

        except Exception as e:
            return (hf.failure(

                    "get student info",
                    str(e),
                    ),
                    401
                    )



@ attendance_api.resource("/getstream/<float:time>")
class Stream(Resource):
    # @ jwt_required()
    def get(self, time):
        try:
          src = 0
          vid = videoStream.WebcamVideoStream(src,time) 
            # return the command line output as the response
          return Response(vid.update(), mimetype='multipart/x-mixed-replace; boundary=frame')
        except Exception as e:
            return (hf.failure(

                    "get stream",
                    str(e),
                    ),
                    500
                    )




