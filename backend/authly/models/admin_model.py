from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr


class CreateAdmin(BaseModel):
    password: str
    email: EmailStr


class AdminAccount(BaseModel):
    id: Optional[str]
    username: str
    password: str
    email: EmailStr
    role: List[str]
    geo_location: str
    container: List[str]
    settings: Dict[str, str]


class AllAdminAccounts(BaseModel):
    data: List[AdminAccount]
