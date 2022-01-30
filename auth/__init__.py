from flask import Blueprint
from flask_restful import Api

user_bp = Blueprint("user", __name__, url_prefix ="/user")
user_api = Api(user_bp)

from . import routes
