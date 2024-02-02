from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/votes',
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_sch: schemas.Votes, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    pass