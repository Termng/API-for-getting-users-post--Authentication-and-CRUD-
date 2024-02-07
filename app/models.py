from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False )
    post = Column(String, nullable= False)
    content = Column(String, nullable=False)
    is_published =Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user= relationship("User")
    
    
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    

class Votes(Base):
    __tablename__= 'votes'
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), primary_key=True)
    
    
    

# class Stats(Base):
#     __tablename__ = 'Stats'
#     id: Column(Integer, primary_key=True, unique=True, nullable=False)
#     email: Column(String, unique=True, nullable=False)
#     details: Column(String, nullable=False, unique=True)
#     stat_created : Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))
    
    