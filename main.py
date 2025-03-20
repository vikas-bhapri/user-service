from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import model
from routes import user, login
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="User Microservice",
    description="This is a simple user microservice using FastAPI",
    version="1.0.3",
    contact={
        "name": "Vikas Bhapri",
        "email": "vikasbhapri@gmail.com"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(login.router)

# create tables from models
model.Base.metadata.create_all(bind=engine)
