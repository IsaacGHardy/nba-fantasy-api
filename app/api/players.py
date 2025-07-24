import enum
from fastapi import APIRouter, Query
from app.services.data_service import get_all_players
from app.models.player import FantasyPlayer

from app.static.scoring import sleeper, espn

router = APIRouter()

@router.get("/players", response_model=list[FantasyPlayer])
def get_players(scoring: str = Query("sleeper", enum=["sleeper", "espn"])):
    scoring_map = {
        "sleeper": sleeper,
        "espn": espn
    }
    return get_all_players(scoring_map[scoring])