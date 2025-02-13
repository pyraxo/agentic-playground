from typing import List

from beanie import Document

from app.models.file import File
from app.models.website import Website
from app.schemas.message import Message


class Agent(Document):
    name: str
    files: List[File] = []
    websites: List[Website] = []
    messages: List[Message] = []

    class Settings:
        name = "agents"
