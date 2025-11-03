from pydantic import BaseModel
from datetime import datetime
from enum import Enum
class Signup(BaseModel):
    email:str
    password:str
    date_time:datetime=datetime.now()

class Role(str,Enum):
    ADMIN="admin"
    EDITOR='editor'
    VIEWER='viewer'