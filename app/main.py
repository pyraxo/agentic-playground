import os

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import Agent, File, Website
from app.routers import agent_router

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router.router)


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
