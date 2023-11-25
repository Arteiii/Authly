from typing import Optional, List
from pydantic import BaseModel


class Application(BaseModel):
    id: Optional[str]
    name: str
    version: str
    default_access: Optional[List[str]]
