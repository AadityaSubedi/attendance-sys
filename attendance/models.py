from typing import Union
from database import DB
from bson.objectid import ObjectId
import nepali_datetime
  

class Classes:
    """
    {
        class_name: str
        attendance: {
            subject_name: {
                date: set_of_attendees
            }
        }
        
    }
    """

    collection = "classes"

    def __init__(
        self,
        class_name: str,
        subject_name: str,
        attendees: list
    ):
        self.class_name = class_name
        self.subject_name = subject_name
        self.attendees = attendees  
        self.date = nepali_datetime.date.today().strftime('%K-%n-%D')
        #self.date = nepali_datetime.date(1977, 10, 25).strftime('%K-%n-%D')

    def json(self):
        attendance = {
            self.subject_name: {
                self.date: self.attendees
            }
        }
        return {
        'class_name': self.class_name, 
        'attendance': attendance
        }

    def save(self):
        print("save")
        return DB.insert_one(self.collection, data=self.json())

    def check_class(self):
        print("check_class")
        classes = DB.find_one(self.collection, query={'class_name': self.class_name})
        if classes==None:
            return False
        else:
            return True

    def check_subject(self):
        print("check_subject")
        subject = DB.find_one(self.collection, query={'class_name': self.class_name, f'attendance.{self.subject_name}':{"$exists": True}})
        if subject==None:
            return False
        else:
            return True

    def add_subject(self):  
        print("add_subject")
        new_subject = {
                    self.date: self.attendees
                }  
        return DB.find_one_and_update(self.collection, query={'class_name': self.class_name}, data= {f'attendance.{self.subject_name}': new_subject}, action="$set")

    def add_date(self):
        print("add_date")
        new_date = self.attendees
        return DB.find_one_and_update(self.collection, query={'class_name': self.class_name}, data= {f'attendance.{self.subject_name}.{self.date}': new_date}, action="$set")




