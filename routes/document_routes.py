
from fastapi import APIRouter,Depends,HTTPException,status,Response,Body
from services.user_service import get_doc_details
from datetime import datetime,timedelta
from utilis.auth_logic import password_hash,check_hash_password
from services.user_service import get_user_details,get_user_by_email
from models.user_models import Signup
from config import user,documents,invitations
from utilis.jwt_utilis import create_jwt_token,get_current_user
from models.role_models import UserDetails
from bson import ObjectId
from typing import List
from models.document_models import Documents,documentCreate,Collaborators,InviteRequest
import secrets
import uuid

router=APIRouter(
    prefix="/api/document",
    tags=["doc_routes"]
)

@router.post("/add_doc",response_model=Documents)
async def add_doc(documentModel:documentCreate,current_user:dict=Depends(get_current_user)):
    owner_id=current_user["id"]
    new_doc_id=str(uuid.uuid4())

    new_doc_data={
        "id":new_doc_id,
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
    current_user_id=current_user["id"]
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
    current_user_id=current_user["id"]
    docs=await get_doc_details(document_id)
    if not docs:
        raise HTTPException(status_code=404,detail="Document is not found")
    

    is_owner=docs["owner_id"]==current_user_id
    is_colab=any(
        col["user_id"]==current_user_id for col in docs.get("collaborators",[])
    )

    if not is_owner and not is_colab:
        raise HTTPException(status_code=403,detail="You are not authorized to see this")
    
    return docs


@router.post("/invite")
async def add_collaborator(inviteRequest:InviteRequest,current_user:dict=Depends(get_current_user)):

    doc_id=inviteRequest.doc_id
    invitee_mail=inviteRequest.invitee_mail
    user_id=current_user["id"]
    user_in=await get_user_details(user_id)
    document=await get_doc_details(doc_id)
    if not document:
        raise HTTPException(status_code=404,details="Document has not been found")
    user_data=user_in.get("userdata",{})
    head_name=user_data.get("first_name")
    invitee_user=await get_user_by_email(invitee_mail)
    if not invitee_user:
        raise HTTPException(status_code=404,detail="User DOC has not been found")

    token=secrets.token_urlsafe(32)

    invitation={
        "head_uid":user_id,
        "head_name":head_name,
        "token":token,
        "invitee_mail":invitee_mail.lower(),
        "expiry":datetime.now()+timedelta(days=3)

    }
    await invitations.insert_one(invitation)
    

    return {"message":f'A email has been sent to {invitee_mail}'}

#Will do Check Later on 





