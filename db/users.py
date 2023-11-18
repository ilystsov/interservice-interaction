from typing import Optional

from sqlalchemy.orm import Session
from . import models


class UsersRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: str) -> Optional[models.User]:
        return (
            self.db.query(models.User)
            .filter(models.User.id == user_id)
            .first()
        )

    def get_user_by_username(self, name: str) -> Optional[models.User]:
        return (
            self.db.query(models.User).filter(models.User.name == name).first()
        )

    def create_user(self, user: models.User) -> models.User:
        self.db.add(user)
        return user
