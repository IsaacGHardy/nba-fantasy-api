from datetime import date
from app.models.competeStatus import CompeteStatus
from app.models.sql_models import PlayerValue
from app.services.value_service import (
    get_compete_value,
    get_neutral_value,
    get_reload_value,
    get_rebuild_value
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
        value_func = lambda p: get_rebuild_value(p.fantasy_pts, p.age)
    elif competeStatus == CompeteStatus.RELOAD:
        value_func = lambda p: get_reload_value(p.fantasy_pts, p.age)
    elif competeStatus == CompeteStatus.NEUTRAL:
        value_func = lambda p: get_neutral_value(p.fantasy_pts, p.age)
    elif competeStatus == CompeteStatus.COMPETE:
        value_func = lambda p: get_compete_value(p.fantasy_pts, p.age)
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