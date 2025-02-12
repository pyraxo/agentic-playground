from pydantic import BaseModel


class Website(BaseModel):
    path: str
    content: str
