"""
NBA Fantasy API
A FastAPI backend for NBA fantasy basketball analysis and draft pick valuations.

Copyright (c) 2025 Isaac Hardy
All rights reserved.

This software contains proprietary algorithms for fantasy basketball 
player valuation and draft pick analysis.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.players import router as players_router
from app.jobs.scheduler import start_scheduler, stop_scheduler
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os
import logging

# Load environment variables from .env
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.info("Starting NBA Fantasy API...")
    start_scheduler()
    yield
    # Shutdown
    logging.info("Shutting down NBA Fantasy API...")
    stop_scheduler()

app = FastAPI(title="NBA Fantasy API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

app.include_router(players_router)

@app.get("/")
def read_root():
    return {"message": "NBA Fantasy API", "version": "1.0.0", "status": "running"}

