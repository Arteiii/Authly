from typing import List, Optional
from pydantic import BaseModel


class UsernameHistoryEntry(BaseModel):
    from_date: str
    to_date: Optional[str]


class EmailHistoryEntry(BaseModel):
    from_date: str
    to_date: Optional[str]


class UserKey(BaseModel):
    from_date: str
    to_date: str
    banned: bool


class UserModel(BaseModel):
    _id: dict
    username: str
    email: str
    password: str
    role: List[str]
    disabled: bool
    geo_location: str
    username_history: List[UsernameHistoryEntry]
    email_history: List[EmailHistoryEntry]
    keys: List[UserKey]
    # add last seen and last login
