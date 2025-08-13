from datetime import date
from app.models.competeStatus import CompeteStatus
from app.models.fantasy_player import FantasyPlayer
from app.models.sql_models import PlayerValue
from app.services.player_value_service import (
    get_player_compete_value,
    get_player_neutral_value,
    get_player_reload_value,
    get_player_rebuild_value
)


def calculate_age_from_birthdate(birth_date: date | None) -> int:
    """
    Calculates age from a birthdate string in the format 'MMM DD, YYYY'.
    """

    if birth_date is None:
        return 0
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age



def get_trimmed_min_max(players: list[PlayerValue], trim: int, competeStatus: CompeteStatus):
    """ 
    Returns the minimum and maximum fantasy points after trimming the top and bottom players.
    This is useful for normalizing player values.
    """
    # Define the value function based on compete status
    if competeStatus == CompeteStatus.REBUILD:
        value_func = lambda p: get_player_rebuild_value(p.fantasy_pts, p.age)
    elif competeStatus == CompeteStatus.RELOAD:
        value_func = lambda p: get_player_reload_value(p.fantasy_pts, p.age)
    elif competeStatus == CompeteStatus.NEUTRAL:
        value_func = lambda p: get_player_neutral_value(p.fantasy_pts, p.age)
    elif competeStatus == CompeteStatus.COMPETE:
        value_func = lambda p: get_player_compete_value(p.fantasy_pts, p.age)
    else:  # CompeteStatus.CONTEND
        value_func = lambda p: p.fantasy_pts
    
    # Sort players using the appropriate value function
    sorted_players = sorted(players, key=value_func)
    
    # Trim players if we have enough
    if len(players) > 2 * trim:
        trimmed = sorted_players[trim:-trim]
    else:
        trimmed = sorted_players
    
    # Calculate min and max using the same value function
    min_pts = value_func(trimmed[0])
    max_pts = value_func(trimmed[-1])
    
    return min_pts, max_pts

def generate_round_with_suffix(round: int) -> str:
    """
    Generates a round string with the appropriate suffix.
    """
    if round == 1: return "1st"
    if round == 2: return "2nd"
    if round == 3: return "3rd"
    else: return f"{round}th"

def get_player_value_by_compete_status(player: FantasyPlayer, compete_status: CompeteStatus) -> float:
    """
    Returns the player value based on the compete status. Assumes player has all value attributes.
    """
    if compete_status == CompeteStatus.REBUILD:
        return player.rebuild_value
    elif compete_status == CompeteStatus.RELOAD:
        return player.reload_value
    elif compete_status == CompeteStatus.NEUTRAL:
        return player.neutral_value
    elif compete_status == CompeteStatus.COMPETE:
        return player.compete_value
    else:  # CompeteStatus.CONTEND
        return player.contend_value