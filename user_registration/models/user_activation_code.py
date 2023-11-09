from typing import Any
from datetime import datetime
from user_registration.models.base import Base


class UserActivationCode(Base):
    code: int
    user_id: int
    creation_date: datetime

    def __init__(self, code: int, user_id: int, id: Any = 0, creation_date: datetime = None):
        super().__init__(id)
        self.code = code
        self.user_id = user_id
        self.creation_date = creation_date
