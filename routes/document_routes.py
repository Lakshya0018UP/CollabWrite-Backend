
from fastapi import APIRouter,Depends,HTTPException,status,Response

from datetime import datetime
from utilis.auth_logic import password_hash,check_hash_password
from services.user_service import get_user,get_user_details
from models.user_models import Signup
from config import user,documents
from utilis.jwt_utilis import create_jwt_token,get_current_user
from models.role_models import UserDetails
from bson import ObjectId
from models.document_models import Documents,documentCreate

router=APIRouter(
    prefix="/api/document",
    tags=["doc_routes"]
)

@router.post("/add_doc",response_model=Documents)
async def add_doc(documentModel:documentCreate,current_user:dict=Depends(get_current_user)):
    owner_id=ObjectId(current_user["id"])

    new_doc_data={
        "title":documentModel.title,
        "owner_id":owner_id,
        "content":{},
        "collaborators":[],
        "created_at":datetime.now(),
        "updated_at":datetime.now()
    }

    await documents.insert_one(new_doc_data)
    return new_doc_data

