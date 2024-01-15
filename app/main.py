from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Posts(BaseModel):
    title:str
    content: str
    published: bool = True

while True:   
    try:
        conn = psycopg2.connect(host='localhost', database = 'my fastAPI' , user = 'postgres', password = 'Merciful', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connection to db was successful')
        break
    except Exception as error:
        print('connection failed')
        print("Error: ", error)
        time.sleep(4)
                
                
                

# PATH OPERATION FOR GETTING ALL POSTS
@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"message": posts}


# PATH OPERATION FOR CREATING POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(newpost: Posts):
    cursor.execute(""" INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING * """, 
                   (newpost.title, newpost.content, newpost.published))
    returnedPost = cursor.fetchone()
    conn.commit()
    return{"output": returnedPost}
    
  
# PATH OPERATION FOR GETTING POSTS BY ID
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute (""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    
    if not post:
        print('This was not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f' post with {id} was not found')
    return{"posts detail": post}


# PATH OPERATION FOR DELETING POSTS BY ID
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING * """ , (str(id), ))
    deleted = cursor.fetchone()
    conn.commit()
    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" The post with id: {id} does not exist")
    return Response (status_code=status.HTTP_204_NO_CONTENT)


# PATH OPERATION FOR UPDATING POSTS BY ID
@app.put("/posts/{id}")
def update_posts(id: int, post: Posts):
    cursor.execute (""" UPDATE posts set title = %s, content = %s, is_published = %s WHERE id = %s  RETURNING * """, (post.title, post.content, post.published, str(id), ))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" The post with id: {id} does not exist")
    return {"message": updated_post}



    
    
   
    
