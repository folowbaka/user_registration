from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserActivationCodeBase(BaseModel):
    code: int


# Properties to receive via API on creation
class UserActivationCodeCreate(UserActivationCodeBase):
    user_id: int


# Properties to receive via API on update
class UserActivationCodeUpdate(UserActivationCodeBase):
    pass


class UserActivationCodeInDBBase(UserActivationCodeBase):
    id: Optional[int]
    creation_date: Optional[datetime] = None


# Additional properties to return via API
class UserActivationCode(UserActivationCodeInDBBase):
    pass


# Additional properties stored in DB
class UserActivationCodeInDB(UserActivationCodeInDBBase):
    pass