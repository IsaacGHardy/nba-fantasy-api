from typing import Any
from fastapi import APIRouter
from app.services.extraction_service import get_all_players
from app.models.player import Player

router = APIRouter()

@router.get("/players", response_model=list[Any])
def get_players():
    return get_all_players()
