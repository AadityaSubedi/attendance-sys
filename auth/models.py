from typing import Union
from database import DB


class User:
    
    """
    {
        code: str, level code 
        name: str, level name 
        programs: List[ObjectId], list of programs 
        
    }
    """

    collection = "users"

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        image:Union[str,None]

    ):
        self.username = username
        self.email = email

        self.password = password
        self.image = image


    def save(self):
        return DB.insert_one(self.collection, data=self.json())

    def json(self):
        return {
        'username' :self.username,
        'email' :self.email,
        'password' :self.password,
        'image': self.image
        }


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




