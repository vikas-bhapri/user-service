from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str
    role: str

class DisplayUser(BaseModel):
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

class UpdatePassword(BaseModel):
    password: str
    confirm_password: str

class DeleteUser(BaseModel):
    confirm_delete: bool = False
    password: str