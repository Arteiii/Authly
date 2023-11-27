from typing import Optional
from pydantic import BaseModel


class BubbleSettings(BaseModel):
    allow_new_user_registration: bool = True
    test_settings: str = "HelloWorld"
    bliblablu: bool = True


class BubbleConfig(BaseModel):
    id: Optional[str]
    name: str
    settings: BubbleSettings

    # NOTE: dict with the collection name and the object id of the document:
    user_document_id: Optional[str]
    key_document_id: Optional[str]
    application_id: Optional[str]


class CreateBubble(BaseModel):
    name: str
    settings: Optional[BubbleSettings]
