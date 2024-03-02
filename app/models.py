from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, String, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now())



class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now())