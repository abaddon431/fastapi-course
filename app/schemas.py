from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    created_at : datetime 

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    id: int
    created_at : datetime