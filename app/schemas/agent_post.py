from pydantic import BaseModel


class AgentPost(BaseModel):
    name: str
