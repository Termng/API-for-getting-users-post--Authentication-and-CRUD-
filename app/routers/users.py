from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import Optional,List
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db



router = APIRouter(
    prefix = "/users",
    tags=['Users'] 
)



@router.get("/")
def get_users(db: Session = Depends(get_db)):
    get_all_users = db.query(models.User).all()
    return get_all_users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_User(new_user: schemas.CreateUser, db:Session = Depends(get_db)):
    hashed_password = utils.hash(new_user.password) #this hashes the password
    new_user.password= hashed_password #this assigns the users password to a hashing function
    newUser = models.User(**new_user.model_dump()) #stores the pydantic model to a variable and maps it to the users table
    db.add(newUser) 
    db.commit()
    db.refresh(newUser)
    return newUser

@router.get("/{id}", response_model=schemas.GetUser)
def get_one_user(id:int, db:Session = Depends(get_db)):
    get_single = db.query(models.User).filter(models.User.id == id).first()
    
    if not get_single:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return get_single







    
    
   
    
