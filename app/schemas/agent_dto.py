from fastapi import UploadFile
from pydantic import BaseModel


class AgentPost(BaseModel):
    name: str | None
    websites: list[str] | None = None
    files: list[UploadFile] | None = None
