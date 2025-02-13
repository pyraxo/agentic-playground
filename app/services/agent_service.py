from fastapi import HTTPException

from app.models.agent import Agent
from app.schemas.agent_create import AgentCreate


async def create_agent(agent_create: AgentCreate) -> Agent:
    if await Agent.find_one(Agent.name == agent_create.agent_post):
        raise HTTPException(status_code=400, detail="Agent already exists")
    agent = Agent(name=agent_create.agent_post)
    await agent.insert()
    return agent


async def get_agent(agent_id: str) -> Agent:
    return await Agent.find_one(Agent.id == agent_id)


async def delete_agent(agent_id: str) -> None:
    await Agent.find_one(Agent.id == agent_id).delete()
