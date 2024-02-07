from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

from .routers import login, posts, users, votes


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# while True:   
#     try:
#         conn = psycopg2.connect(host='localhost', database = 'Torah' , user = 'postgres', password = 'Merciful', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Connection to Postgres was successful')
#         break
#     except Exception as error:
#         print('connection failed')
#         print("Error: ", error)
#         time.sleep(4)
                


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(votes.router)