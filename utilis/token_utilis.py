from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from utilis.jwt_utilis import verify_jwt_token

import logging

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def get_custom_user(token:str=Depends(oauth2_scheme)):
    return verify_jwt_token(token)