from typing import Optional
from pydantic import BaseModel


class ContainerSettings(BaseModel):
    allow_new_user_registration: bool
    test_settings: str
    bliblablu: bool


class ContainerConfig(BaseModel):
    id: Optional[str]
    name: str
    settings: ContainerSettings

    # NOTE: dict with the collection name and the object id of the document:
    user_document_id: Optional[str]
    key_document_id: Optional[str]
    application_id: Optional[str]
