from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def password_hash(password:str):
    return pwd_context.hash(password)


#This route is checking the password so entered, if it is entered, then it is compared with hased passwrod retrived from database
def check_hash_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)
    