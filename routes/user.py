from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import user as user_schema, login as login_schema
from controllers import user as user_controller
from controllers.login import get_current_user

router = APIRouter(
    tags=["User"],
    prefix="/user"
)

@router.post("/", response_model=user_schema.DisplayUser, status_code=status.HTTP_201_CREATED)
def create_user(request: user_schema.User, db: Session = Depends(get_db)):
    new_user = user_controller.create_new_user(request, db)
    return new_user

@router.get("/", response_model=user_schema.DisplayUser)
def get_user(email: str, db: Session = Depends(get_db)):
    user = user_controller.get_user(email, db)
    return user

@router.get("/validate", response_model=login_schema.TokenData)
def validate_user(current_user = Depends(get_current_user)):
    return current_user

@router.put("/")
def update_password(email: str, request: user_schema.UpdatePassword, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.email != email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_controller.update_password(email, request, db)
    return {"message": "Password updated successfully"}

@router.delete("/")
def delete_user(email: str, request: user_schema.DeleteUser, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.email != email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_controller.delete_user(email, request, db)
    return {"message": "User deleted successfully"}

