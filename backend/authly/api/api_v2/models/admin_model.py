from pydantic import BaseModel


class CreateAdminReponse(BaseModel):
    status: bool
    id: str
