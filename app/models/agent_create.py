from pydantic import BaseModel


class AgentCreate(BaseModel):
    agent_post: str
    files: list[str]
