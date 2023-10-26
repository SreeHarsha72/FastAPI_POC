from pydantic import BaseModel,EmailStr
#Pydantic/Schema Models: used for handling the requests and responses from/to browser
from datetime import datetime
from typing import Optional
from pydantic.types import conint

#REQUEST MODELS,  specifies what the incoming requests from the browser should include, and how they should be.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #direction: this specifies whether to like/unlike the post, 'le' means lessthan or equal to.



#RESPONSE MODELS, these tell how should be the final response in browser

class UserOut(BaseModel):
    id: int
    email: EmailStr
    createdAt: datetime
    class Config:
        orm_mode = True #from_attributes = True

class Post(PostBase): 
    id: int
    createdAt: datetime
    user_id: int
    owner: UserOut #gets the pydantic model of the user
    class Config:
        orm_mode = True # or from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

# below Token response model is used in the process of verification of tokens from clients
class Token(BaseModel):
    access_token: str
    token_type: str












