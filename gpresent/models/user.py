from ..db import db
from motor_odm import Document

class User(Document):
    class Mongo:
        collection = "users"
    
    username: str
    password: str 
    email: str
    avatar: str 
    

Document.use(db)