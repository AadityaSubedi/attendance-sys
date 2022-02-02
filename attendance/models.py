from typing import Union
from database import DB
from bson.objectid import ObjectId
import nepali_datetime

#new teacher class
class Teacher:
    
    """
    {
        user_id: ObjectId/str Username of user
        name: str fullname
        subject: dictionary with subject as keys and array of class as values
        
    }
    """

    collection = "teacher"

    def __init__(
        self,
        user_id: str,
        name: str,
        subjects: dict,
    ):
        self.user_id = user_id
        self.name = name
        self.subjects = subjects

    def json(self):
        return {
        'user_id': self.user_id, 
        'name': self.name, 
        'subjects':self.subjects, 
        }

    def save(self):
        return DB.insert_one(self.collection, data=self.json())
        

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
        attendees: set
    ):
        self.class_name = class_name
        self.subject_name = subject_name
        self.attendees = attendees  
        self.date = nepali_datetime.date.today().strftime('%K-%n-%D')

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
        return DB.insert_one(self.collection, data=self.json())

    def add_subject(self):  
        new_subject = {
                    self.date: self.attendes
                }  
        return DB.find_one_and_update(self.collection, query={'class_name': self.class_name}, data= {f'attendance.{self.subject_name}': new_subject}, action="$set")

    def add_date(self):
        new_date = self.attendees
        return DB.find_one_and_update(self.collection, query={'class_name': self.class_name}, data= {f'attendance.{self.subject_name}.{self.date}': new_date}, action="$set")




