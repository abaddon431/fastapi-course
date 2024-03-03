from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Optional
import schemas
import models
import oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user),
limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Posts).filter(
        models.Posts.title.contains(search)
    ).limit(limit).offset(offset).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    new_post = models.Posts(user_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post

@router.get("/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    latest = db.query(models.Posts).order_by(models.Posts.id.desc()).first() 
    if not latest: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"There are no posts")
    return latest

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(
        models.Posts.id == id
    ).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(
        models.Posts.id == id
    ).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Hey man that is not cool :(")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(
        models.Posts.id == id,
    )
    post_data= post_query.first()
    if not post_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post_data.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Hey man that is not cool :(")
    post_query.update(post.model_dump())
    db.commit()
    return post_query.first()