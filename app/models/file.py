from datetime import datetime

from beanie import Document
from pydantic import Field


class File(Document):
    """Uploaded file or website."""

    name: str
    text: str
    tokens: int = 0
    hash: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "files"
        indexes = ["hash"]
