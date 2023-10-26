from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter()

@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(database.get_db),):

    # username and password are returned by OAuth2passwordequestForm from a login form
    user= db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")
    
    #create a token and return
    access_token = oauth2.create_access_token(data= {"user_id":user.id}) #encodes the user id of the data
    return {"access_token": access_token, "token_type": "bearer"}
