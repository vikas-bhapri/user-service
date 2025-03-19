from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import login as login_schema
from controllers import login as login_controller

router = APIRouter(
    tags=["Login"],
    prefix="/login"
)

@router.post("/", response_model=login_schema.AccessToken)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    access_token = login_controller.login(request, db)
    return access_token