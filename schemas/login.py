from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    username: str
    role: str