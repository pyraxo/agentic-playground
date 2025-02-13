import os

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.schemas.agent_create import AgentCreate
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
        client.get_default_database(),
        document_models=[
            "app.models.agent",
            "app.models.file",
            "app.models.website",
        ],
    )


@app.post("/agents")
async def create_agent(agent: AgentCreate):
    return await agent_service.create_agent(agent)


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    return await agent_service.get_agent(agent_id)


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    return await agent_service.delete_agent(agent_id)


@app.put("/agents/{agent_id}/websites")
async def update_agent_websites(agent_id: str, website_paths: list[str]):
    return {"message": "Hello World"}


@app.put("/agents/{agent_id}/files")
async def update_agent_files(agent_id: str, file_paths: list[str]):
    return {"message": "Hello World"}


@app.post("/agents/{agent_id}/queries")
async def send_message(agent_id: str, message: str):
    return {"message": "Hello World"}
