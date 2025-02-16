from fastapi import UploadFile
from pydantic import BaseModel


class AgentPost(BaseModel):
    """Agent post schema."""

    name: str | None
    prompt: str | None
    websites: list[str] | None
    files: list[UploadFile] | None
