from datetime import datetime

from beanie import Document
from pydantic import Field


class Website(Document):
    path: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "websites"
        indexes = ["path"]
