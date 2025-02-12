from beanie import Document

from app.schemas.file import File
from app.schemas.message import Message
from app.schemas.website import Website


class Agent(Document):
    name: str
    files: list[File]
    websites: list[Website]
    messages: list[Message]
