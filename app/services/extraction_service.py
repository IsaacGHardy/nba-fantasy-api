from typing import Any
from app.models.player import Player
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerfantasyprofilebargraph as fantasyprofile

def get_player(id) -> Player | None:
    """
    Fetches a single player from the NBA API and returns it as a Player object.
    Returns None if data is unavailable.
    """
    try:
        raw_data = fantasyprofile.PlayerFantasyProfileBarGraph(player_id=id, season='2024-2025').get_json()['datSets']['SeasonAvg']
        return Player(
            id=raw_data['id'],
            name=raw_data['PLAYER_NAME'],
            team=raw_data['TEAM_ABBREVIATION'],
            position='PG',
            pts=raw_data['PTS'],
            rebs=raw_data['REB'],
            ast=raw_data['AST'],
            stl=raw_data['STL'],
            blk=raw_data['BLK']
        )
    except Exception:
        return None

def get_all_players() -> list[Any]:
    """
    Fetches all players from the NBA API and returns them as a list of Player objects.
    Skips players with missing fantasy data.
    """
    raw_data = players.get_active_players()
    """ player_list = []
    for p in raw_data:
        player = get_player(p['id'])
        if player:
            player_list.append(player) """
    return raw_data
