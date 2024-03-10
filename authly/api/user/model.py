from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    MODERATOR = "MODERATOR"


class CreateUserResponse(BaseModel):
    id: Optional[str]
    username: str
    email: str


class UsernameHistoryEntry(BaseModel):
    from_date: str
    to_date: Optional[str] = None


class EmailHistoryEntry(BaseModel):
    from_date: str
    to_date: Optional[str] = None


class UserKey(BaseModel):
    from_date: str
    to_date: str
    banned: bool


class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    password: str
    role: List[UserRole]
    disabled: bool
    geo_location: Optional[str] = None
    username_history: Optional[List[UsernameHistoryEntry]] = []
    email_history: Optional[List[EmailHistoryEntry]] = []
    # keys: Optional[List[UserKey]] = []
    # settings: Optional[List] = []
    # add last seen and last login
