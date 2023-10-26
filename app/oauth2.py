from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import  status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl= 'login') #to get the contents in the mentioned tokenurl path


# should provide secret key
# should provide algorithm to be used to to form signature (header+secret+algo)
# expiration time of the token

# secret_key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# algo="HS256"
# access_token_expiry_minutes=30

secret_key= settings.secret_key
algo= settings.algorithm
access_token_expiry_minutes= settings.access_token_expire_minutes


#this function is for creating the token for user
def create_access_token(data:dict):
    to_encode= data.copy()
    expiry= datetime.utcnow() + timedelta(minutes=int(access_token_expiry_minutes))
    to_encode.update({"exp":expiry}) #attaches the expiry to the user credentials

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm= algo) # creates the signature and thus makes it a token
    return encoded_jwt


# this function is for verifying the user token 
def verify_token(token: str, credentials_exception):
    try:
        payload= jwt.decode(token, secret_key, algorithms= [algo])
        id:int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data= schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
# this function is to get the user url information and do the token verification automatically
def get_current_user(token: str = Depends(oauth2_schema),db: Session= Depends(database.get_db)):
    credentials_exception= HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                                         detail= f"Couldnot validate the credentials",
                                         headers= {"WWW-Authenticate": "Bearer"})
    token= verify_token(token, credentials_exception)
    #print("this is token id"+ str(token.id))
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user


