from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Header,HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TOKEN = 30


def create_access_token (data : dict):  # data collect user sending data 

    to_encode = data.copy()  # assign to_encode from data 

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_TOKEN)
    to_encode.update({"exp":expire})

    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM) # assign data , time , sec_key and algorithim 

    return token


#take token from header
def get_current_user (credentials: HTTPAuthorizationCredentials = Depends(security)) :
    
    token = credentials.credentials   # only token
    return verify_token(token)


# verify token
def verify_token(token :str):

    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        
        if username is None or role is None:  
            raise HTTPException(status_code=401, detail="invalid token")
        
        return {
            "username":username,
            "role":role
        }
    
    except JWTError:  
        raise HTTPException(status_code=401, detail="invalid or expired token")
