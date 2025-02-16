from typing import Annotated

from fastapi import APIRouter, Body, File, Form, UploadFile, status

from app.models import Agent
from app.schemas.agent_dto import AgentPost
from app.schemas.message import Message
from app.services import agent_service

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_agent(
    name: Annotated[str | None, Form()] = "ResearchAgent",
    prompt: Annotated[str | None, Form()] = None,
    websites: Annotated[list[str] | None, Form()] = None,
    files: Annotated[list[UploadFile] | None, File()] = None,
) -> dict:
    """Create a new research agent."""
    agent_post = AgentPost(name=name, prompt=prompt, websites=websites, files=files)
    return await agent_service.create_agent(agent_post)


@router.get("/")
async def get_all_agents() -> list[Agent]:
    """Get all research agents."""
    return await agent_service.get_all_agents()


@router.get("/{agent_id}", status_code=status.HTTP_200_OK)
async def get_agent(agent_id: str) -> Agent:
    """Get a research agent."""
    return await agent_service.get_agent(agent_id)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: str):
    """Delete a research agent."""
    return await agent_service.delete_agent(agent_id)


@router.put("/{agent_id}/websites", status_code=status.HTTP_204_NO_CONTENT)
async def update_agent_websites(agent_id: str, websites: list[str] = Body(...)):
    """Update the websites of a research agent."""
    return await agent_service.update_agent_websites(agent_id, websites)


@router.put("/{agent_id}/files", status_code=status.HTTP_204_NO_CONTENT)
async def update_agent_files(
    agent_id: str,
    files: list[UploadFile],
):
    return await agent_service.update_agent_files(agent_id, files)


@router.post("/{agent_id}/queries", status_code=status.HTTP_201_CREATED)
async def send_message(agent_id: str, message: Message) -> dict:
    """Send a message to a research agent."""
    return await agent_service.send_message(agent_id, message)
