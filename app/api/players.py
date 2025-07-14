from fastapi import APIRouter
from app.services.nba_api_service import get_player_data
from app.models.player import Player

router = APIRouter()

@router.get("/players", response_model=list[Player])
def get_players():
    return get_player_data()
