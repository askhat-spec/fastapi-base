from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import src.database as db
from src.api import main_router


app = FastAPI(title='Shop API')

app.include_router(main_router)

register_tortoise(app, config=db.DATABASE_CONFIG)
