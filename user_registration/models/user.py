from typing import Any

from user_registration.models.base import Base


class User(Base):
    email: str
    hashed_password: str
    is_activated: bool = False

    def __init__(self, id: Any, email: str, hashed_password: str, is_activated: bool):
        super().__init__(id)
        self.email = email
        self.hashed_password = hashed_password
        self.is_activated = is_activated
