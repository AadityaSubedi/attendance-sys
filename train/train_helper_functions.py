
from database import DB
from .models import Cache
from datetime import datetime

from utils.add_new_datasets import updated_train

def start_training():
    try:
        DB.update_one(Cache.collection, {'type': 'cache'}, {'ModelTraining.isModelTraining': True, 'ModelTraining.lastStartedTime': datetime.now(),'ModelTraining.lastEndedTime': None})
        updated_train()
        DB.update_one(Cache.collection, {'type': 'cache'},  {'ModelTraining.isModelTraining': False,'ModelTraining.lastEndedTime': datetime.now()})
    except Exception as e:
        DB.update_one(Cache.collection, {'type': 'cache'},  {'ModelTraining.isModelTraining': False,'ModelTraining.lastEndedTime': datetime.now()})
        # later eslai logging garne 
        print(e)

