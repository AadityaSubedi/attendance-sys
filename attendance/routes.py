from attendance.models import Teacher
from auth.models import User
from flask_restful import Resource
from . import attendance_api
from flask import Flask, request
from flask_bcrypt import Bcrypt
from .models import Teacher
from database import DB

from . import attendance_helper_functions as ahf

from json import loads
from bson.json_util import dumps

from utils import helper_functions as hf
from utils import file_helper_functions as fhf
