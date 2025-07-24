from datetime import datetime
from app.models.competeStatus import CompeteStatus
from app.models.player import FantasyPlayer



def calculate_age_from_birthdate(birth_date: str) -> int:
    """
    Calculates age from a birthdate string in the format 'MMM DD, YYYY'.
    """
    birth = datetime.strptime(birth_date, "%b %d, %Y")
    today = datetime.today()
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
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
    

def get_trimmed_min_max(players: list[FantasyPlayer], trim: int, competeStatus: CompeteStatus):
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