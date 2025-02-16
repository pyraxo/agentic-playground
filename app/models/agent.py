from datetime import datetime
from typing import List, Optional

from beanie import Document, Link
from pydantic import Field

from app.models.file import File


class Agent(Document):
    """Research agent."""

    name: str
    files: List[Link[File]] = []
    messages: List[str] = []
    prompt: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "agents"
        indexes = ["name"]
