from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

class Posts(BaseModel):
    post:str
    content: str
    is_published: bool = True

while True:   
    try:
        conn = psycopg2.connect(host='localhost', database = 'Torah' , user = 'postgres', password = 'Merciful', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connection to db was successful')
        break
    except Exception as error:
        print('connection failed')
        print("Error: ", error)
        time.sleep(4)
                
                
                

# PATH OPERATION FOR GETTING ALL POSTS



@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    get_posts = db.query(models.Post).all()
    # cursor.execute(""" SELECT * from posts""")
    # all_posts = cursor.fetchall()
    return{"my_output": get_posts}

# PATH OPERATION FOR CREATING POSTS

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(pyPosts: Posts, db: Session = Depends(get_db)):
    create_posts = models.Post(**pyPosts.dict())
    db.add(create_posts)
    db.commit()
    db.refresh(create_posts)
    return{"my_output": create_posts}
    # cursor.execute(""" INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *  """, (postSchema.title, postSchema.content, postSchema.published))
    # uploaded_post = cursor.fetchone()
    # conn.commit()
    
    
    
    
    
  
# PATH OPERATION FOR GETTING POSTS BY ID

@app.get("/posts/{id}")
def get_single_post(id: int, db: Session = Depends(get_db)):
    get_one_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s  """, (str(id), ))
    # single_post = cursor.fetchone()
    
    if not get_one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with the id: {id} was not found')
    return{"single": get_one_post}


# PATH OPERATION FOR DELETING POSTS BY ID

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id), ))
    deleted = cursor.fetchone()
    conn.commit()
    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the post with the id: {id} was not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# PATH OPERATION FOR UPDATING POSTS BY ID

@app.put("/posts/{id}")
def update_post(posts: Posts, id: int):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING * """, (posts.title, posts.content, posts.published, str(id), ) )
    updated = cursor.fetchone()
    conn.commit()
    if updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with the id: {id} was not found")
    return{"updated_Post": updated}






    
    
   
    
