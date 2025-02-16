from typing import Annotated

from fastapi import APIRouter, Body, Form, UploadFile, status

from app.models import Agent
from app.schemas.message import Message
from app.services import agent_service

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_post: Annotated[str, Form()],
    files: list[UploadFile] = None,
) -> Agent:
    return await agent_service.create_agent(agent_post, files)


@router.get("/")
async def get_all_agents() -> list[Agent]:
    return await agent_service.get_all_agents()


@router.get("/{agent_id}", status_code=status.HTTP_200_OK)
async def get_agent(agent_id: str) -> Agent:
    return await agent_service.get_agent(agent_id)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: str):
    return await agent_service.delete_agent(agent_id)


@router.put("/{agent_id}/websites", status_code=status.HTTP_204_NO_CONTENT)
async def update_agent_websites(agent_id: str, websites: list[str] = Body(...)):
    return await agent_service.update_agent_websites(agent_id, websites)


@router.put("/{agent_id}/files", status_code=status.HTTP_204_NO_CONTENT)
async def update_agent_files(
    agent_id: str,
    files: list[UploadFile],
):
    return await agent_service.update_agent_files(agent_id, files)


@router.post("/{agent_id}/queries", status_code=status.HTTP_201_CREATED)
async def send_message(agent_id: str, message: Message):
    return await agent_service.send_message(agent_id, message)
