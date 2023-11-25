from typing import List, Optional
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    password: str
    email: EmailStr


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


class UserAccount(BaseModel):
    id: Optional[str]
    username: str
    email: str
    password: str
    role: List[str]
    disabled: bool
    geo_location: str
    username_history: List[UsernameHistoryEntry]
    email_history: List[EmailHistoryEntry]
    keys: List[UserKey]
    settings: List
    # add last seen and last login


class UserDB(BaseModel):
    id: Optional[str]
    container_id: str
    container_name: str
    user: List[UserAccount]
