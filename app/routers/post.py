from fastapi import FastAPI, status,Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db #imports engine from ..(prev folder) database file
from .. import models, schemas, oauth2 #imports models,schemas from current directory


router=APIRouter() #similar to app=FastAPI(), router which later includes in the main.py to app() object

@router.get("/posts",response_model=List[schemas.PostOut]) #for retrieving we use 'Get'
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int =10, skip:int = 0, search : Optional[str]=""):
    #posts=db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    # posts= db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #perform left outer join
    posts= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                                                                         models.Post.id == models.Vote.post_id, 
                                                                         isouter=True).group_by(models.Post.id).filter(
                                                                            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

#For sending user data from browser and process it in server and provide response we use 'Post'
@router.post("/createpost",status_code=status.HTTP_201_CREATED, response_model=schemas.Post) 
def  create_post(payLoad: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    #print(**dict(payLoad)) #the ** operation unpacks the dictionary {title="",content="" and so on} individually with all the elements in it
    #new_post= models.Post( title = payLoad.title, content = payLoad.content, published = payLoad.published )
    #print(current_user.id) #this gives the authenticated user id
    new_post= models.Post( user_id = current_user.id, **dict(payLoad) ) #adds the logged in user id to the user_id and adds the elements in the dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #to return back the new post created and store it in the variable new_post
    return new_post

def dict(payLoad):
    post_dict= payLoad.dict()
    return post_dict

@router.get("/posts/{id}", response_model=schemas.PostOut)#  this has path with path parameter<'str'>
def get_post(id: int,  db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),): # mentioning the datatypes performs the validtion on the variable and converts to desired type
    #post= db.query(models.Post).filter(models.Post.id == id).first()
    post= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                                                                         models.Post.id == models.Vote.post_id, 
                                                                         isouter=True).group_by(models.Post.id).filter(
                                                                             models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
    # if post.user_id != current_user.id: #this checks whether authorized user deleting the post or not
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail = "Not authorized, You are not the owner of that post")
    
    print(post)
    return post


@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), ):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first()==None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    if post.first().user_id != current_user.id: #this checks whether authorized user deleting the post or not
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail = "Not authorized, You are not the owner of that post")
    
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, payLoad: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):
    print(type(payLoad))
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
    if post.first().user_id != current_user.id: #this checks whether authorized user deleting the post or not
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail = "Not authorized, You are not the owner of that post")
    
    post.update(dict(payLoad), synchronize_session=False)
    db.commit()
    return post.first()