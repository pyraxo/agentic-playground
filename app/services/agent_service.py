from fastapi import HTTPException, UploadFile
from langchain_core.messages import HumanMessage

from app.agents.chatbot import graph
from app.models.agent import Agent
from app.schemas.message import Message


# TODO: File logic
async def create_agent(agent_post: str, files: list[UploadFile]) -> Agent:
    """Create a new agent with the given name and files.

    Args:
        agent_post (str): The name of the agent to create.
        files (list[UploadFile]): The files to upload.

    Raises:
        HTTPException: If the agent already exists.
        HTTPException: If there is an error creating the agent.

    Returns:
        Agent: The created agent.
    """
    if await Agent.find_one(Agent.name == agent_post):
        raise HTTPException(status_code=400, detail="Agent already exists")
    try:
        agent = Agent(name=agent_post)
        await agent.insert()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"message": "Agent created successfully"}


async def get_all_agents():
    """Get all agents.

    Returns:
        list[Agent]: A list of all agents.
    """
    return await Agent.find_all().to_list()


async def get_agent(agent_name: str) -> Agent:
    """Get an agent by name.

    Args:
        agent_name (str): The name of the agent to get.

    Returns:
        Agent: The agent.
    """
    return await Agent.find_one(Agent.name == agent_name)


async def delete_agent(agent_name: str) -> None:
    """Delete an agent by name.

    Args:
        agent_name (str): The name of the agent to delete.

    Returns:
        None.
    """
    agent = await Agent.find_one(Agent.name == agent_name)
    await agent.delete()
    return agent


async def update_agent_websites(agent_name: str, websites: list[str]) -> None:
    """Update the websites of an agent.

    Args:
        agent_name (str): The name of the agent to update.
        websites (list[str]): The websites to update.

    Returns:
        None.
    """
    agent = await Agent.find_one(Agent.name == agent_name)
    agent.websites.extend(websites)
    await agent.save()


async def update_agent_files(agent_name: str, files: list[str]) -> None:
    """Update the files of an agent.

    Args:
        agent_name (str): The name of the agent to update.
        files (list[str]): The files to update.

    Returns:
        None.
    """
    agent = await Agent.find_one(Agent.name == agent_name)
    agent.files.extend(files)


async def send_message(agent_name: str, message: Message) -> None:
    """Send a message to an agent.

    Args:
        agent_id (str): The id of the agent to send the message to.
        message (Message): The message to send.

    Returns:
        None.
    """
    result = await graph.ainvoke({"messages": HumanMessage(content=message.message)})
    return result
