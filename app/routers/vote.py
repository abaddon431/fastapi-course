from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import Response, status, HTTPException, APIRouter, Depends
from database import get_db
from typing import List, Optional
import models
import schemas
import oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(
        models.Posts.id == vote.post_id
    ).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post does not exist") 

    found_vote = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id,
        models.Votes.user_id == current_user.id
    ).first()

    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already liked this post") 
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "post liked"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This vote cannot be found")
        db.delete(found_vote)
        db.commit()
        return {"message":"like removed"}