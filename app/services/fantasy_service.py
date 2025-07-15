from app.models.player import FantasyPlayer, Player
from app.models.scoring import Scoring

def calculate_fantasy_points(player: Player, scoring: Scoring) -> float:
    """
    Calculates fantasy points for a player based on their scoring stats.
    """
    fantasy_pts = (
        player.pts * scoring.pts +
        player.rebs * scoring.rebs +
        player.ast * scoring.ast +
        player.blk * scoring.blk +
        player.stl * scoring.stl +
        player.tov * scoring.tov +
        player.fg3m * scoring.fg3m +
        player.fgm * scoring.fgm +
        player.fga * scoring.fga + 
        player.ftm * scoring.ftm +
        player.fta * scoring.fta
    )
    if sum(stat >= 10 for stat in [player.pts, player.rebs, player.ast]) >= 2:
        fantasy_pts += scoring.double_double

    if all(stat >= 10 for stat in [player.pts, player.rebs, player.ast]):
        fantasy_pts += scoring.triple_double

    return fantasy_pts

def get_trimmed_min_max(players: list[FantasyPlayer], trim: int):
    """ 
    Returns the minimum and maximum fantasy points after trimming the top and bottom players.
    This is useful for normalizing player values.
    """
    sorted_players = sorted(players, key=lambda p: p.fantasy_pts)
    if len(players) > 2 * trim:
        trimmed = sorted_players[trim:-trim]
    else:
        trimmed = sorted_players
    min_pts = min(p.fantasy_pts for p in trimmed)
    max_pts = max(p.fantasy_pts for p in trimmed)
    return min_pts, max_pts

def calculate_player_value(player_list: list[FantasyPlayer]): 
    """
    Calculates the value of a player based on their fantasy points 
    and the contention factor of the team.
    """

    min_pts, max_pts = get_trimmed_min_max(player_list, trim=6)
    for player in player_list:
        player.set_normalized_value(min_pts, max_pts)
    
    return player.pts

def create_fantasy_player(player: Player, scoring: Scoring) -> FantasyPlayer:
    """
    Converts a Player object to a FantasyPlayer object and calculates fantasy points.
    """
    fantasy_player = FantasyPlayer(**player.dict())
    fantasy_player.fantasy_pts = calculate_fantasy_points(player, scoring)

    return fantasy_player