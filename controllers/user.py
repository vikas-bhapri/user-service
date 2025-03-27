from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import user as user_schema
from models import model as user_model
from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_user_data(request: user_schema.User, db: Session, is_update: bool):
    errors = {}
    if not is_update:
        # user name format validation. Username should not have any spaces, should have only lowercase characters, should be alphanumeric and special characters like _, ., - are allowed.
        if not re.match(r'^[a-z0-9_.-]+$', request.username):
            errors["username"] = "Username should not have any spaces and should be alphanumeric and special characters like _, ., - are allowed."

        if db.query(user_model.User).filter(user_model.User.email == request.email).first():
            errors["email"] = "Email already registered."
        
        if db.query(user_model.User).filter(user_model.User.username == request.username).first():
            errors["username"] = "Username already taken."
        
        if request.role not in ["admin", "user", "seller"]:
            errors["role"] = "Invalid role. Role must be either 'admin', 'user', or 'seller'."
        
        if len(request.password) < 8:
            errors["password"] = "Password must be at least 8 characters."
        
        if request.password != request.confirm_password:
            errors["confirm_password"] = "Passwords do not match."
        
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex, request.email):
            errors["email"] = "Invalid email address."
        
    if not type(request.phone) == int or len(str(request.phone)) < 10:
        errors["phone"] = "Invalid phone number."
    
    if request.zip_code < 100000 or request.zip_code > 999999:
        errors["zip_code"] = "Invalid zip code."
    
    # Loop through all fields and check if any are empty
    for field in request.model_dump():
        if not request.model_dump()[field]:
            errors[field] = f"{field} cannot be empty."

    if errors:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors)
    else:
        return True

def create_new_user(request: user_schema.User, db: Session):
    validate_user_data(request, db, False)
    
    hashed_password = pwd_context.hash(request.password)
    
    new_user = user_model.User(
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=hashed_password,
        role = request.role,
        address_line_1=request.address_line_1,
        address_line_2=request.address_line_2,
        city=request.city,
        state=request.state,
        zip_code=request.zip_code,
        country=request.country,
        country_code=request.country_code,
        phone=request.phone
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

def update_user(email: str, request: user_schema.UpdateUserData, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    validate_user_data(request, db, True)
        
    user.first_name = request.first_name
    user.last_name = request.last_name
    user.address_line_1 = request.address_line_1
    user.address_line_2 = request.address_line_2
    user.city = request.city
    user.state = request.state
    user.zip_code = request.zip_code
    user.country = request.country
    user.country_code = request.country_code
    user.phone = request.phone
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
