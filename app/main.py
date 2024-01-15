from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
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
def get_all_posts():
    cursor.execute(""" SELECT * from posts""")
    all_posts = cursor.fetchall()
    return{"my_output": all_posts}

# PATH OPERATION FOR CREATING POSTS

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(postSchema: Posts):
    cursor.execute(""" INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *  """, (postSchema.title, postSchema.content, postSchema.published))
    uploaded_post = cursor.fetchone()
    conn.commit()
    return {"uploaded": uploaded_post}
    
  
# PATH OPERATION FOR GETTING POSTS BY ID

@app.get("/posts/{id}")
def get_single_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s  """, (str(id), ))
    single_post = cursor.fetchone()
    
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with the id: {id} was not found')
    return{"single": single_post}


# PATH OPERATION FOR DELETING POSTS BY ID

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
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






    
    
   
    
