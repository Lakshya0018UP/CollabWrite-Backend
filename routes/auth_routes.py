from fastapi import APIRouter,Depends,HTTPException,status,Response

from datetime import datetime
from utilis.auth_logic import password_hash,check_hash_password
from services.user_service import get_user,get_user_details
from models.user_models import Signup
from config import user
from utilis.jwt_utilis import create_jwt_token,get_current_user
from models.role_models import UserDetails
from bson import ObjectId

router=APIRouter(
    prefix="/api/auth",
    tags=["auth_routes"]
)


@router.post("/signup")
async def signup_user(userdata:Signup):
    exisiting_user=await get_user(userdata.email)

    if exisiting_user:
        raise HTTPException(status_code=400,detail='USER ALREADY EXISTS')
    
    hashed_password=password_hash(userdata.password)

    new_user={"email":userdata.email,"password":hashed_password,"Date_of_ID_creation":datetime.now()}
    result=await user.insert_one(new_user)

    return {
        "id":str(result.inserted_id)
    }

@router.post("/token")
async def login_user(userdata:Signup):
    registered_user=await user.find_one({"email":userdata.email})
    #Find One returnes a dictoionary and . cannot be used for retriving such data
    if not registered_user or not check_hash_password(userdata.password,registered_user["password"]):
        raise HTTPException(status_code=404,detail="Incorrect Details")
    payload={
        "email":registered_user["email"],
        "id":str(registered_user["_id"])
        }
    token=create_jwt_token(payload)

    return {"token":token}

@router.get("/protected")
async def protect(current_user:str=Depends(get_current_user)):
    current_user_email=current_user["email"]
    current_user_id=current_user["id"]
    return {"email":current_user_email,"message":"Hello from protected","id":current_user_id}

@router.post("/add_info")
async def add_info(Userdetails:UserDetails,current_user:str=Depends(get_current_user)):
    current_user_id=current_user["id"]
    
    if not current_user:
        raise HTTPException(status_code=404,detail="User Not found")
    
    User_data_update=Userdetails.dict()
    await user.update_one({"_id":ObjectId(current_user_id)},{
        "$set":{"userdata":User_data_update}
    })
    return {"message":"User data updated successfully"}



