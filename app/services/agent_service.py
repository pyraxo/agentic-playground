from app.models.agent import Agent
from app.models.agent_create import AgentCreate


async def create_agent(agent_create: AgentCreate) -> Agent:
    agent = Agent(agent_name=agent_create.agent_name)
    await agent.insert()
    return agent
