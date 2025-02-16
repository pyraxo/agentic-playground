from fastapi import HTTPException, UploadFile
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.chatbot import graph
from app.models import Agent, File
from app.schemas.agent_post import AgentPost
from app.schemas.message import Message
from app.services import file_service


def get_total_tokens(agent: Agent) -> int:
    """Get the total tokens of an agent's knowledge base.

    Args:
        agent (Agent): The agent to get the total tokens of.

    Returns:
        int: The total tokens of the agent's knowledge base.
    """
    return sum(file.tokens for file in agent.files)


async def create_agent(
    agent_post: AgentPost,
    files: list[UploadFile] | None = None,
) -> Agent:
    """Create a new agent with the given name and files.

    Args:
        agent_post (str): The name of the agent to create.
        files (list[UploadFile]): Files to add.
        websites (list[str]): Websites to add.

    Raises:
        HTTPException: If the agent already exists.
        HTTPException: If there is an error creating the agent.

    Returns:
        Agent: The created agent.
    """
    if await Agent.find_one(Agent.name == agent_post.name):
        raise HTTPException(status_code=400, detail="Agent already exists")

    agent = Agent(name=agent_post.name)
    await agent.insert()

    if files and len(files) > 0:
        agent.files.extend(await process_batch_files(agent, files))

    await agent.save()
    return agent


async def get_all_agents() -> list[Agent]:
    """Get all agents.

    Returns:
        list[Agent]: A list of all agents.
    """
    return await Agent.find_all(fetch_links=True).to_list()


async def get_agent(agent_id: str) -> Agent:
    """Get an agent by name.

    Args:
        agent_id (str): The name of the agent to get.

    Raises:
        HTTPException: If the agent is not found.

    Returns:
        Agent: The agent.
    """
    if not (agent := await Agent.find_one(Agent.name == agent_id, fetch_links=True)):
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


async def delete_agent(agent_id: str) -> None:
    """Delete an agent by name.

    Args:
        agent_id (str): The name of the agent to delete.

    Returns:
        None.
    """
    agent = await get_agent(agent_id)
    await agent.delete()


async def update_agent_websites(agent_id: str, websites: list[str]) -> None:
    """Update the websites of an agent.

    Args:
        agent_id (str): The name of the agent to update.
        websites (list[str]): The websites to update.

    Returns:
        None.
    """
    agent = await get_agent(agent_id)
    agent.files.extend(await process_batch_websites(agent, websites))
    await agent.save()


async def process_batch_websites(agent: Agent, websites: list[str]) -> list[File]:
    """Process a batch of websites and add them to an agent.

    Args:
        agent (Agent): The agent to add the websites to.
        websites (list[str]): The websites to add.

    Returns:
        list[File]: The processed websites.
    """
    processed_websites = []
    for website in websites:
        website_doc = await file_service.process_website(website)
        if get_total_tokens(agent) + website_doc.tokens > 120000:
            raise HTTPException(status_code=400, detail="Total tokens limit reached")
        processed_websites.append(website_doc)
    return processed_websites


async def update_agent_files(agent_id: str, files: list[UploadFile]) -> dict:
    """Update the files of an agent.

    Args:
        agent_id (str): The id of the agent to update.
        files (list[bytes]): The files to update.

    Returns:
        dict: Status message
    """
    agent = await get_agent(agent_id)

    processed_files = await process_batch_files(agent, files)
    agent.files.extend(processed_files)
    await agent.save()
    return


async def process_batch_files(agent: Agent, files: list[UploadFile]) -> list[File]:
    """Process a batch of files and add them to an agent.

    Args:
        agent (Agent): The agent to add the files to.
        files (list[UploadFile]): The files to add.

    Raises:
        HTTPException: If the total tokens limit is reached.

    Returns:
        list[File]: The processed files.
    """
    processed_files = []
    for file in files:
        file_doc = await file_service.process_file(file)
        if file_doc in processed_files:
            continue
        if file_doc in agent.files:
            continue
        if get_total_tokens(agent) + file_doc.tokens > 120000:
            raise HTTPException(status_code=400, detail="Total tokens limit reached")
        processed_files.append(file_doc)
    return processed_files


async def send_message(agent_id: str, message: Message) -> list[dict]:
    """Send a message to an agent.

    Args:
        agent_id (str): The id of the agent to send the message to.
        message (Message): The message to send.

    Returns:
        list[dict]: The response from the agent.
    """
    agent = await get_agent(agent_id)
    knowledge_base = ""
    if len(agent.files) + len(agent.websites) > 0:
        files = (
            "\n\nFiles:\n" + "\n".join([file.text for file in agent.files])
            if agent.files
            else ""
        )
        websites = (
            "\n\nWebsites:\n"
            + "\n".join([website.content for website in agent.websites])
            if agent.websites
            else ""
        )
        knowledge_base = f"Your knowledge base is the following:{files}{websites}"
    messages = [
        SystemMessage(content=f"You are a research assistant. {knowledge_base}"),
        HumanMessage(content=message.message),
    ]
    result = await graph.ainvoke({"messages": messages})
    return result
