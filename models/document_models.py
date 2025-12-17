from pydantic import BaseModel,Field
from typing import Optional,List,Any
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from models.role_models import Role

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        """
        This is the new Pydantic v2 validator.
        It tells Pydantic how to handle this type.
        """
        # This is the logic from your old 'validate' function
        def validate(v):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid objectid")
            return ObjectId(v)

        return core_schema.union_schema(
            [
                # Check if it's already an ObjectId
                core_schema.is_instance_schema(ObjectId),
                # If not, try to validate it (e.g., from a string)
                core_schema.no_info_plain_validator_function(validate),
            ],
            # This makes Pydantic prefer the 'str' type for serialization
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> JsonSchemaValue:
        """
        This is the new v2 replacement for '__modify_schema__'.
        It tells FastAPI's /docs to show this as a string.
        """
        return {"type": "string"}
class documentCreate(BaseModel):
    title:str

class Documents(BaseModel):
    id: str
    title:str
    collaborators:List[str]=[]
    content:Optional[dict]={}
    owner_id:str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Collaborators(BaseModel):
    user_id:str
    role:Role=Role.VIEWER
    user_email:str
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class InviteRequest(BaseModel):
    doc_id:str
    invitee_mail:str
    role:Role=Role.EDITOR