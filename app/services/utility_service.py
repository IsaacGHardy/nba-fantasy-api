from datetime import date
from app.models.competeStatus import CompeteStatus
from app.models.sql_models import PlayerValue



def calculate_age_from_birthdate(birth_date: date | None) -> int:
    """
    Calculates age from a birthdate string in the format 'MMM DD, YYYY'.
    """

    if birth_date is None:
        return 0
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def get_rebuild_value(pts: float, age: int) -> float:
    """
    Calculates the rebuild value for a player based on their age.
    Young players have their value increased at a greater rate than older players.
    """
    if(age <= 19):
        return pts * 2
    elif(age <= 22):
        return pts * 1.9
    elif(age <= 24):
        return pts * 1.8
    elif(age <= 26):
        return pts * 1.6
    elif(age <= 28):
        return pts * 1.2
    elif(age <= 30):
        return pts * 1.0
    elif(age <= 32):
        return pts * 0.8
    else:
        return pts * 0.6
    

def get_trimmed_min_max(players: list[PlayerValue], trim: int, competeStatus: CompeteStatus):
    """ 
    Returns the minimum and maximum fantasy points after trimming the top and bottom players.
    This is useful for normalizing player values.
    """
    sorted_players = sorted(players, key=lambda p: p.fantasy_pts if competeStatus == CompeteStatus.CONTEND else get_rebuild_value(p.fantasy_pts, p.age))
    if len(players) > 2 * trim:
        trimmed = sorted_players[trim:-trim]
    else:
        trimmed = sorted_players
    min_pts = min(p.fantasy_pts if competeStatus == CompeteStatus.CONTEND else get_rebuild_value(p.fantasy_pts, p.age) for p in trimmed)
    max_pts = max(p.fantasy_pts if competeStatus == CompeteStatus.CONTEND else get_rebuild_value(p.fantasy_pts, p.age) for p in trimmed)
    return min_pts, max_pts

def generate_round_with_suffix(round: int) -> str:
    """
    Generates a round string with the appropriate suffix.
    """
    if round == 1: return "1st"
    if round == 2: return "2nd"
    if round == 3: return "3rd"
    else: return f"{round}th"