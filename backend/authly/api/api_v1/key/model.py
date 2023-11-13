from pydantic import BaseModel
from typing import List, Optional


class Delete(BaseModel):
    application_ids: Optional[List[str]] = None
    creator_names: Optional[List[str]] = None
    key_list: Optional[List[str]] = None


class KeysResponse(BaseModel):
    keys: List[str]

