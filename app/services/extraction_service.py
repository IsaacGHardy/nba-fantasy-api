from app.models.player import Player
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerfantasyprofilebargraph as fantasyprofile

def get_player(id) -> Player | None:
    """
    Fetches a single player from the NBA API and returns it as a Player object.
    Returns None if data is unavailable.
    """
    try:
        raw_data = fantasyprofile.PlayerFantasyProfileBarGraph(player_id=id, season='2024-25').get_data_frames()[1]
        stats = raw_data.iloc[0]  # First row (player's stats)
        return Player(
            name=stats['PLAYER_NAME'],
            team=stats['TEAM_ABBREVIATION'],
            position='PG',
            pts=stats['PTS'],
            rebs=stats['REB'],
            ast=stats['AST'],
            stl=stats['STL'],
            blk=stats['BLK']
        )
    except Exception:
        return None

def get_all_players() -> list[Player]:
    """
    Fetches all players from the NBA API and returns them as a list of Player objects.
    Skips players with missing fantasy data.
    """

    
    raw_data = players.get_active_players()[:30]
    player_list = []
    for p in raw_data:
        player = get_player(p['id'])
        if player:
            player_list.append(player)
    return player_list
