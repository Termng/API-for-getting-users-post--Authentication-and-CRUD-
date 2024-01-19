from pydantic import BaseModel


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
    
    class Config:
        orm_mode = True
    
  