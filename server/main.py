import logging.config

from faker import Faker
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError

import clients
import db.models
from clients.black_list.models.check_request import CheckRequest
from clients.black_list.api_client import ApiClient
from clients.black_list.api.default_api import DefaultApi
from clients.black_list.configuration import Configuration
from config.settings import app_settings
from config.logging import logging_config
from db.users import UsersRepo
from .contracts import Message, User, Result


fake = Faker()

app = FastAPI()

logging.config.dictConfig(logging_config)

engine = create_engine(app_settings.db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

configuration = Configuration(host=app_settings.black_list_host)
client = ApiClient(configuration)
api = DefaultApi(client)


@app.get("/")
async def root() -> Message:
    return Message(message="Hello that")


@app.get("/hello/{name}")
async def say_hello(name: str) -> Message:
    return Message(message=f"Hello {name}")


@app.post('/users')
async def create_user(new_user: User) -> Result | JSONResponse:
    check_request = CheckRequest(name=new_user.name)
    try:
        result = api.is_in_list_check_post(check_request=check_request)
    except clients.black_list.exceptions.BadRequestException:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Black list error occurred: Bad request"},
        )
    except ValidationError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Black list error occurred: Validation error"},
        )
    if result.in_list:
        return Result(created=False)
    with SessionLocal() as session:
        user = db.models.User(name=new_user.name, email=fake.email())
        UsersRepo(session).create_user(user)
        session.commit()
    return Result(created=True)
