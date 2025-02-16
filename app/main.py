from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.api import agents
from app.config import get_settings
from app.models import Agent, File

settings = get_settings()


async def init_db():
    client = AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(
        client[settings.mongo_db_name],
        document_models=[Agent, File],
    )
    print("Database initialized")
    return client


def close_db(client: AsyncIOMotorClient):
    client.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    client = await init_db()
    yield
    close_db(client)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

app.include_router(agents.router)
