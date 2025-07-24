from app.models.player import FantasyPlayer, Player
from app.models.scoring import Scoring

from app.services.utility_service import CompeteStatus, get_trimmed_min_max
from app.services.utility_service import get_rebuild_value

def set_contend_value(player: FantasyPlayer, val: float):
    player.contend_value = val

def set_rebuild_value(player: FantasyPlayer, val: float):
    player.rebuild_value = val

def determine_value_to_set(player: FantasyPlayer, val: float, compete_status: CompeteStatus):
    if compete_status == CompeteStatus.CONTEND:
        set_contend_value(player, val)
    elif compete_status == CompeteStatus.REBUILD:
        set_rebuild_value(player, val)

def set_value(player: FantasyPlayer, min_pts: float, max_pts: float, compete_status: CompeteStatus):
    """
    Sets a normalized value (50.00–100.00) for this player based on fantasy_pts.
    """

    min_val, max_val = 50.0, 100.0
    if max_pts == min_pts:
        determine_value_to_set(player, max_val, compete_status)
    else:
        self_value = player.fantasy_pts if compete_status == CompeteStatus.CONTEND else get_rebuild_value(player.fantasy_pts, player.age)
        val = round(((self_value - min_pts) / (max_pts - min_pts)) * (max_val - min_val) + min_val, 2)
        determine_value_to_set(player, val, compete_status)

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

def assign_player_ages(player_ages: dict[str, int], player_list: list[FantasyPlayer]):
    """
    Assigns ages to players in the player_list based on player_ages dictionary.
    """
    for player in player_list:
        if player.id in player_ages:
            player.age = player_ages[player.id]

def calculate_player_value(player_list: list[FantasyPlayer]): 
    """
    Calculates the value of a player based on their fantasy points 
    and the contention factor of the team.
    """

    min_pts, max_pts = get_trimmed_min_max(player_list, trim=6, competeStatus=CompeteStatus.CONTEND)
    for player in player_list:
        set_value(player, min_pts, max_pts, compete_status=CompeteStatus.CONTEND)

    min_pts, max_pts = get_trimmed_min_max(player_list, trim=6, competeStatus=CompeteStatus.REBUILD)
    for player in player_list:
        set_value(player, min_pts, max_pts, compete_status=CompeteStatus.REBUILD)


def create_fantasy_player(player: Player, scoring: Scoring) -> FantasyPlayer:
    """
    Converts a Player object to a FantasyPlayer object and calculates fantasy points.
    """
    fantasy_player = FantasyPlayer(**player.dict())
    fantasy_player.fantasy_pts = calculate_fantasy_points(player, scoring)

    return fantasy_player