import os
from typing import Annotated

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import Body, FastAPI, Form
from fastapi import File as FastAPIFile
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


@app.post("/agents")
async def create_agent(
    agent_post: Annotated[str, Form()],
    files: Annotated[list[bytes], FastAPIFile()],
):
    return await agent_service.create_agent(agent_post, files)


@app.get("/agents")
async def get_all_agents():
    return await agent_service.get_all_agents()


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    return await agent_service.get_agent(agent_id)


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    return await agent_service.delete_agent(agent_id)


@app.put("/agents/{agent_id}/websites")
async def update_agent_websites(agent_id: str, websites: list[str] = Body(...)):
    return await agent_service.update_agent_websites(agent_id, websites)


@app.put("/agents/{agent_id}/files")
async def update_agent_files(
    agent_id: str,
    files: Annotated[list[bytes], FastAPIFile()],
):
    return await agent_service.update_agent_files(agent_id, files)


@app.post("/agents/{agent_id}/queries")
async def send_message(agent_id: str, message: Message):
    return await agent_service.send_message(agent_id, message)
