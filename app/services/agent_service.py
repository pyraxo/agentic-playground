from fastapi import HTTPException, UploadFile

from app.models.agent import Agent


async def create_agent(agent_post: str, files: list[UploadFile]) -> Agent:
    if await Agent.find_one(Agent.name == agent_post):
        raise HTTPException(status_code=400, detail="Agent already exists")
    try:
        agent = Agent(name=agent_post)
        await agent.insert()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"message": "Agent created successfully"}


async def get_all_agents():
    return await Agent.find_all().to_list()


async def get_agent(agent_name: str) -> Agent:
    return await Agent.find_one(Agent.name == agent_name)


async def delete_agent(agent_name: str) -> None:
    agent = await Agent.find_one(Agent.name == agent_name)
    await agent.delete()
    return agent


async def update_agent_websites(agent_name: str, websites: list[str]) -> None:
    agent = await Agent.find_one(Agent.name == agent_name)
    agent.websites.extend(websites)
    await agent.save()


async def update_agent_files(agent_name: str, files: list[str]) -> None:
    agent = await Agent.find_one(Agent.name == agent_name)
    agent.files.extend(files)
    await agent.save()


async def send_message(agent_id: str, message: str) -> None:
    pass
