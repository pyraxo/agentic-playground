from typing import List

from beanie import Document

from app.schemas.file import File
from app.schemas.message import Message
from app.schemas.website import Website


class Agent(Document):
    name: str
    files: List[File] = []
    websites: List[Website] = []
    messages: List[Message] = []

    class Settings:
        name = "agents"
