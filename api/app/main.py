from fastapi import Depends, FastAPI, Request
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import models
from app.database import db as database
from app.routes.api import router as api_router

from rich.traceback import install
install(show_locals=True)

app = FastAPI()


# Connect to database on startup 
# @app.on_event("startup")
# async def db_setup():
#     try:
#         async with database.async_engine.begin() as conn:
#             # await conn.run_sync(models.Base.metadata.drop_all)
#             await conn.run_sync(models.Base.metadata.create_all)
#     except Exception as e:
#         print(e)
#         print(
#             "No connection to database could be made. Endpoint using database are not accessible in this deployment."
#         )


app.include_router(api_router)
