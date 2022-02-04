from flask import Blueprint
from flask_restful import Api

train_bp = Blueprint("train", __name__, url_prefix="/train")
train_api = Api(train_bp)

from . import routes
