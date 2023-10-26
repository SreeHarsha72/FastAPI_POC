from fastapi import FastAPI, status,Response, HTTPException, Depends, APIRouter
from .. import models, schemas, utils #imports models,schemas from current directory
from sqlalchemy.orm import Session
from ..database import  get_db #imports engine from ..(prev folder) database file


router=APIRouter() #similar to app=FastAPI()

def dict(payLoad):
    post_dict= payLoad.dict()
    return post_dict

#from browser we get the data and we need to process it and send resposne by validating the sent data
@router.post("/createuser",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(userLoad: schemas.UserCreate, db: Session = Depends(get_db),):
    #hashing the password
    hashed_pwd = utils.hash(userLoad.password)
    userLoad.password = hashed_pwd
    new_user= models.User( **dict(userLoad) )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #it returns back the new user created and store it in the variable new_user
    return new_user

@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the  id: {id} does not exist")
    return user
