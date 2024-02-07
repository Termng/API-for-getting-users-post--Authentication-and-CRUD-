from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model= List[schemas.PostResponse]) #the response model has to be defined with a list so it doesnt throw an error
def get_all_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = " " ):
    get_posts = db.query(models.Post).filter(models.Post.post.contains(search)).limit(limit).offset(skip).all() #limit & skip here are query parameter
    
    return get_posts


    

# PATH OPERATION FOR CREATING POSTS

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(pyPosts: schemas.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    create_posts = models.Post(user_id = current_user.id ,**pyPosts.model_dump())
    print(current_user)
    db.add(create_posts)
    db.commit() 
    db.refresh(create_posts)
    return create_posts

    

  
# PATH OPERATION FOR GETTING POSTS BY ID

@router.get("/{id}", response_model=schemas.PostResponse)
def get_single_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    get_one_post = db.query(models.Post).filter(models.Post.id == current_user.id).all()
    
    
    
    if not get_one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with the id: {id} was not found')
    return get_one_post


# PATH OPERATION FOR DELETING POSTS BY ID

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = delete_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the post with the id: {id} was not found')
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# PATH OPERATION FOR UPDATING POSTS BY ID

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(up_posts: schemas.PostUpdate, id: int, db : Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    updated = db.query(models.Post).filter(models.Post.id == id)
    post = updated.first()
    
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with the id: {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    updated.update(up_posts.model_dump(), synchronize_session=False)
    
    db.commit()
    return updated.first()