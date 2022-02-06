from typing import Union
from database import DB


class Cache:
    
    """
    {
        isTraining: bool,
        
    }
    """

    collection = "cache"

    def __init__(
        self,


    ):
        pass


    def save(self):
        return DB.insert_one(self.collection, data=self.json())
        

    def json(self):
        return {
            'type': 'cache',
            'ModelTraining': {'isModelTraining':False,
                              'lastStartedTime':None,
                              'lastEndedTime':None,},

        }




