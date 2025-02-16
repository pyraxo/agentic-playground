import os
from typing import Annotated

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import Body, FastAPI, Form, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import Agent, File, Website
from app.schemas.message import Message
from app.services import agent_service

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def init_db():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    await init_beanie(
        client["agent_workflow"],
        document_models=[Agent, File, Website],
    )
    print("Database initialized")


@app.on_event("startup")
async def startup_db_client():
    await init_db()


@app.post("/agents", status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_post: Annotated[str, Form()],
    files: list[UploadFile] = None,
) -> Agent:
    return await agent_service.create_agent(agent_post, files)


@app.get("/agents")
async def get_all_agents() -> list[Agent]:
    return await agent_service.get_all_agents()


@app.get("/agents/{agent_id}", status_code=status.HTTP_200_OK)
async def get_agent(agent_id: str) -> Agent:
    return await agent_service.get_agent(agent_id)


@app.delete("/agents/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: str):
    return await agent_service.delete_agent(agent_id)


@app.put("/agents/{agent_id}/websites", status_code=status.HTTP_204_NO_CONTENT)
async def update_agent_websites(agent_id: str, websites: list[str] = Body(...)):
    return await agent_service.update_agent_websites(agent_id, websites)


@app.put("/agents/{agent_id}/files", status_code=status.HTTP_204_NO_CONTENT)
async def update_agent_files(
    agent_id: str,
    files: list[UploadFile],
):
    return await agent_service.update_agent_files(agent_id, files)


@app.post("/agents/{agent_id}/queries", status_code=status.HTTP_201_CREATED)
async def send_message(agent_id: str, message: Message):
    return await agent_service.send_message(agent_id, message)
