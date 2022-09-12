from fastapi import Depends, FastAPI, Request
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
import os 
import uvicorn


from app.models import models
from app.database import db
from app.routes.api import router as api_router

from rich.traceback import install
install(show_locals=True)

app = FastAPI()

# Cors middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Create tables
db.Base.metadata.create_all(db.engine)
