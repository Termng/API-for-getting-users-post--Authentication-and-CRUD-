from fastapi import Response, HTTPException, APIRouter, Depends, status
from ..import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login_user(user_cred: schemas.Authenticate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    
    if not utils.validate_user(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    return {"message": "token received"}