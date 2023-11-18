"""
hello_server.py
---------------

This module provides a basic HTTP server that responds to incoming requests
with a "Hello, World!" message.

"""
import logging.config

from faker import Faker
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import app_settings
from .contracts import Message

fake = Faker()

app = FastAPI()

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": app_settings.log_level,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": app_settings.log_level,
    },
}

logging.config.dictConfig(logging_config)

engine = create_engine(app_settings.db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


@app.get("/", response_model=Message)
async def root() -> Message:
    return Message(message="Hello that")


@app.get("/hello/{name}", response_model=Message)
async def say_hello(name: str) -> Message:
    return Message(message=f"Hello {name}", code=1)
