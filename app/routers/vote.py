from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router=APIRouter()
@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user)):

    #check if post exists or not
    post= db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} doesnot exists")
    
    #check whether there exists a user vote for the post
    vote_query= db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                     models.Vote.user_id==current_user.id)
    
    vote_exists=vote_query.first()
    if (vote.dir == 1): #to add a vote
        if vote_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else: #to delete a vote
        if not vote_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted the vote"}
