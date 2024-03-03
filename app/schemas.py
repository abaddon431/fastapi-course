from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    id: int
    created_at : datetime

class PostResponse(PostBase):
    id: int
    user_id: int
    created_at : datetime 
    owner: UserResponse
    class Config:
        from_attributes = True



# Tokens
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

