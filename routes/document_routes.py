
from fastapi import APIRouter,Depends,HTTPException,status,Response

from datetime import datetime
from utilis.auth_logic import password_hash,check_hash_password
from services.user_service import get_user,get_user_details
from models.user_models import Signup
from config import user,documents
from utilis.jwt_utilis import create_jwt_token,get_current_user
from models.role_models import UserDetails
from bson import ObjectId
from typing import List
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

@router.get("/get_all_docs",response_model=List[Documents])
async def get_doc(current_user:dict=Depends(get_current_user)):
    current_user_id=ObjectId(current_user["id"])
    # user_doc=await documents.find_one({"owner_id":current_user_id})

    #A list is used here as the Documents is Dict and it cannot be converted into a List, so the response model shall be list

    #There is a OR Query in mongoDB, which can look accross Multiple Domains which can be used single handedly

    query={
        "$or":[{
            "owner_id":current_user_id,
        },{"collaborators.user_id":current_user_id}]
    }
    #Find_one returns a single object Dict but find returns a Cursor[List] also the query find runs without await 
    user_doc= documents.find(query)

    if not user_doc:
        raise HTTPException(status_code=404, details="No document related to you")
    
    #Return the List of Documents
    docs=await user_doc.to_list(length=None)

    return docs

@router.get("/{document_id}",response_model=Documents)
async def open_your_doc(document_id:str,current_user:dict=Depends(get_current_user)):
    doc_id=ObjectId(document_id)
    current_user_oid=ObjectId(current_user["id"])
    #Here we have just found out the doc, we havent retured it 
    curr_doc=await documents.find_one({"_id":doc_id})
    if not curr_doc:
        raise HTTPException(status_code=404,detail="Document Not Found")

    is_owner=curr_doc["owner"]==current_user_oid
    is_colab=any(
        col["user_id"]==current_user_oid for col in curr_doc.get("collaborators",[])
    )

    if not is_owner and not is_colab:
        raise HTTPException(status_code=403,detail="You are not authorized to see this")
    
    return curr_doc





