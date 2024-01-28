from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model= List[schemas.PostResponse]) #the response model has to be defined with a list so it doesnt throw an error
def get_all_posts(db: Session = Depends(get_db)):
    get_posts = db.query(models.Post).all()
    # cursor.execute(""" SELECT * from posts""")
    # all_posts = cursor.fetchall()
    return get_posts

# PATH OPERATION FOR CREATING POSTS

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(pyPosts: schemas.PostCreate, db: Session = Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):
    create_posts = models.Post(**pyPosts.model_dump())
    db.add(create_posts)
    db.commit()
    db.refresh(create_posts)
    return create_posts
    # cursor.execute(""" INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *  """, (postSchema.title, postSchema.content, postSchema.published))
    # uploaded_post = cursor.fetchone()
    # conn.commit()
    

  
# PATH OPERATION FOR GETTING POSTS BY ID

@router.get("/{id}", response_model=schemas.PostResponse)
def get_single_post(id: int, db: Session = Depends(get_db)):
    get_one_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s  """, (str(id), ))
    # single_post = cursor.fetchone()
    
    if not get_one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with the id: {id} was not found')
    return get_one_post


# PATH OPERATION FOR DELETING POSTS BY ID

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):
    deleted = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id), ))
    # deleted = cursor.fetchone()
    # conn.commit()
    if deleted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the post with the id: {id} was not found')
    deleted.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# PATH OPERATION FOR UPDATING POSTS BY ID

@router.put("/{id}", response_model=schemas.PostResponse
         )
def update_post(up_posts: schemas.PostUpdate, id: int, db : Session = Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):
    updated = db.query(models.Post).filter(models.Post.id == id)
    post = updated.first()
    
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING * """, (posts.title, posts.content, posts.published, str(id), ) )
    # updated = cursor.fetchone()
    # conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with the id: {id} was not found")
    updated.update(up_posts.model_dump(), synchronize_session=False)
    db.commit()
    return updated.first()