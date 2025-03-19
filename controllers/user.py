from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import user as user_schema
from models import model as user_model
from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_new_user(request: user_schema.User, db: Session):
    if db.query(user_model.User).filter(user_model.User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    if request.role not in ["admin", "user", "seller"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    
    if len(request.password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters")
    
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(regex, request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")
    
    hashed_password = pwd_context.hash(request.password)
    
    new_user = user_model.User(
        username=request.username,
        email=request.email,
        password=hashed_password,
        role = request.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(user_id: str, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

def update_password(email: str, request: user_schema.UpdatePassword, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    if len(request.password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters")
    
    hashed_password = pwd_context.hash(request.password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)
    return user

def delete_user(email: str, request: user_schema.DeleteUser, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not request.confirm_delete:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please confirm deletion")
    
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

