from pydantic import BaseModel

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str
    role: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: int
    country: str
    country_code: str
    phone: int

class DisplayUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    role: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: int
    country: str
    country_code: str
    phone: int

    class Config:
        from_attributes = True

class UpdatePassword(BaseModel):
    password: str
    confirm_password: str

class UpdateUserData(BaseModel):
    first_name: str
    last_name: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: int
    country: str
    country_code: str
    phone: int

class DeleteUser(BaseModel):
    confirm_delete: bool = False
    password: str