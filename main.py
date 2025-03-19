from fastapi import FastAPI
from database import engine
from models import model
from routes import user, login
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="User Microservice",
    description="This is a simple user microservice using FastAPI",
    version="0.1.0",
    contact={
        "name": "Vikas Bhapri",
        "email": "vikasbhapri@gmail.com"
    }
)

app.include_router(user.router)
app.include_router(login.router)

# create tables from models
model.Base.metadata.create_all(bind=engine)
