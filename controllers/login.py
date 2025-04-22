from models import model
from fastapi import Cookie, HTTPException, status, Depends, Response
from database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas import login as login_schema
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
EXPIRY_MINUTES = int(os.getenv("TOKEN_EXPIRY_MINUTES"))
EXPIRY_DAYS = int(os.getenv("TOKEN_EXPIRY_DAYS"))

def create_access_token(data: dict, expiry_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expiry_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def login(request: login_schema.Login, db: Session, response: Response):
    user = db.query(model.User).filter(model.User.username == request.username).first() 
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role, "email": user.email}, expiry_delta=timedelta(minutes=EXPIRY_MINUTES))  # 30 minutes expiry for access token
    refresh_token = create_access_token(data={"sub": user.username, "role": user.role, "email": user.email}, expiry_delta= timedelta(days=EXPIRY_DAYS))  # 30 days expiry for refresh token
    
    refresh_token_obj = model.RefreshToken(
        token=refresh_token,
        user_id=user.id,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=EXPIRY_DAYS),
    )
    db.add(refresh_token_obj)
    db.commit()
    db.refresh(refresh_token_obj)

    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=60*60*24*30, expires=60*60*24*30, samesite="strict", secure=False)

    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Unable to verify credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        role: str = payload.get("role")
        username: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = login_schema.TokenData(email=email, username=username, role=role)
        return token_data
    except JWTError:
        raise credentials_exception
    
def refresh_token(token: str = Cookie(None), response: Response = None, db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    refresh_token_obj = db.query(model.RefreshToken).filter(model.RefreshToken.token == token).first()
    if not refresh_token_obj or refresh_token_obj.is_expired():
        try:
            db.delete(refresh_token_obj)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    user = db.query(model.User).filter(model.User.id == refresh_token_obj.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # Generate a new access token
    new_access_token = create_access_token(
        data={"sub": user.username, "role": user.role, "email": user.email},
        expiry_delta=timedelta(minutes=EXPIRY_MINUTES)
    )

    # Commit the changes to revoke the old refresh token
    db.commit()

    response.set_cookie(key="access_token", value=new_access_token, httponly=True, max_age=60*30, expires=60*30, samesite="strict", secure=False)

    return {"access_token": new_access_token, "token_type": "bearer"}

def logout(token: str = Cookie(None), response: Response = None, db: Session = Depends(get_db)):
    if token:
        refresh_token_obj = db.query(model.RefreshToken).filter(model.RefreshToken.token == token).first()
        if refresh_token_obj:
            refresh_token_obj.revoked = True
            db.commit()
            db.delete(refresh_token_obj)
            response.delete_cookie(key="refresh_token")
            return {"message": "Logged out successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")


