from pydantic import BaseModel, EmailStr, PastDatetime
from typing import Optional


class PostBase(BaseModel):
    post:str
    content: str 
    is_published: bool = True 
    
class PostCreate(PostBase):
    pass
    
class PostUpdate(PostBase):
    pass

class PostResponse(BaseModel):
    post: str
    content: str
    is_published: bool
    user_id: int
    created_at : PastDatetime
    
    class Config:
        orm_mode = True
        
# USER SCHEMAS DEFINED BELOW
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
class GetUser(BaseModel):
    email: str
    created_at: PastDatetime
    
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    
    class Config:
        orm_mode = True


class Authenticate(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
      
  