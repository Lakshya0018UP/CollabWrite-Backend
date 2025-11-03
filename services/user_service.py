from config import user
#For saving the userInfo in the database after his signup info has been entered
async def save_user_info(uid:str,data=dict):
    await user.update_one({"uid":uid},{
        "$set":{**data}},
        upsert=True
    )

# async def password_hash(password:str)

async def get_user(email:str):
    user_data= await user.find_one({"email":email})
    if user_data:
        return {"message":"User already exists"}
    
    return None

async def get_user_details(qr_id:str):
    user_details=await user.find_one({"_id":qr_id})
    return await user_details


