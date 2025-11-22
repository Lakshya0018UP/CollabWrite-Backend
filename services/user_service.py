from config import user,documents
#For saving the userInfo in the database after his signup info has been entered
async def save_user_info(uid:str,data=dict):
    await user.update_one({"uid":uid},{
        "$set":{**data}},
        upsert=True
    )

# async def password_hash(password:str)

async def get_user(id:str):
    user_data= await user.find_one({"id":id})
    if user_data:
        return {"message":"User already exists"}
    
    return None

async def get_user_details(id:str):
    user_details=await user.find_one({"id":id})
    return user_details

async def get_doc_details(id:str):
    doc_details=await documents.find_one({"id":id})

    return doc_details

async def get_user_by_email(email:str):
    user_details=await user.find_one({"email":email})
    return user_details


