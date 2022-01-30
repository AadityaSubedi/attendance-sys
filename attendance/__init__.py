from flask import Blueprint
from flask_restful import Api

attendance_bp = Blueprint("attendance", __name__, url_prefix="/api")
attendance_api = Api(attendance_bp)

from . import routes
