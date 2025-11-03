from pydantic import BaseModel
from models.user_models import Role


class UserDetails(BaseModel):
    first_name:str
    last_name:str
    role:Role=Role.VIEWER
