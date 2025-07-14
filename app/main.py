from fastapi import FastAPI
from app.api.players import router as players_router

app = FastAPI(title="NBA Fantasy API", version="1.0.0")

app.include_router(players_router)

@app.get("/")
async def root():
    return {"message": "Welcome to NBA Fantasy API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
