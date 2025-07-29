from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.players import router as players_router
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="NBA Fantasy API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(players_router)

@app.get("/")
async def root():
    return {"message": "hello"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
