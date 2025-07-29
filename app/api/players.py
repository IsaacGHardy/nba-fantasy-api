import enum
from fastapi import APIRouter, Query
from app.models.sql_models import PlayerValue
from app.models.player import FantasyPlayer, Player
from app.services.data_service import calculate_player_values
from app.static.scoring import sleeper, espn
from app.services.db_service import get_all_players, upsert_player_values

router = APIRouter()

@router.get("/players", response_model=list[FantasyPlayer])
def get_players(scoring: str = Query("sleeper", enum=["sleeper", "espn"])):
    table_name: str
    if scoring == "sleeper":
        table_name = "sleeper_data"
    else:
        table_name = "espn_data"
    return get_all_players(table_name)
