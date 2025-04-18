from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import login as login_schema
from controllers import login as login_controller

router = APIRouter(
    tags=["Login"],
)

@router.post("/login", response_model=login_schema.AccessToken)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), response: Response = None):
    access_token = login_controller.login(request, db, response)
    return access_token

@router.post("/refresh", response_model=login_schema.AccessToken)
def refresh_token(refresh_token: str = Cookie(...), db: Session = Depends(get_db)):
    access_token = login_controller.refresh_token(refresh_token, db)
    return access_token

@router.post("/logout")
def logout(refresh_token: str = Cookie(...), response: Response = None, db: Session = Depends(get_db)):
    message = login_controller.logout(refresh_token, response, db)
    return message