from fastapi import FastAPI, status, HTTPException, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .routers import posts, users,auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:   
    try:
        conn = psycopg2.connect(host='localhost', database = 'Torah' , user = 'postgres', password = 'Merciful', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connection to Postgres was successful')
        break
    except Exception as error:
        print('connection failed')
        print("Error: ", error)
        time.sleep(4)
                


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)