from typing import Annotated

from fastapi import Form, UploadFile
from pydantic import BaseModel


class AgentCreate(BaseModel):
    agent_post: Annotated[str, Form()]
    files: list[UploadFile] = Form(default=[])
