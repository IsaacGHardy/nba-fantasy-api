from typing import Union
from fastapi import APIRouter, Query
from app.models.fantasy_player import FantasyPlayer
from app.models.fantasy_pick import FantasyPick  
from app.services.db_service import get_all_players, get_all_draft_picks

router = APIRouter()

@router.get("/players", response_model=list[Union[FantasyPlayer, FantasyPick]])
def get_players(scoring: str = Query("sleeper", enum=["sleeper", "espn"])):
    # Get players and picks
    if scoring == "sleeper":
        table_name = "sleeper_data"
        pick_table = "sleeper_picks"
    else:
        table_name = "espn_data"
        pick_table = "espn_picks"

    players = [FantasyPlayer(**p) for p in get_all_players(table_name)]
    picks = [FantasyPick(**p) for p in get_all_draft_picks(pick_table)]
    return players + picks
