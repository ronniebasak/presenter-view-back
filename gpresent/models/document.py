from ..db import db
from motor_odm import Document

class GDocument(Document):
    class Mongo:
        collection = "documents"
    
    created_by: str
    name: str
    content: str

    

Document.use(db)