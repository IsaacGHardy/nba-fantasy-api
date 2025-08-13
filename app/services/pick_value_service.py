from app.models.competeStatus import CompeteStatus
from app.models.fantasy_pick import Tier
from app.models.fantasy_player import FantasyPlayer
from app.models.sql_models import DraftPick

from app.services.utility_service import get_player_value_by_compete_status

def trim_player_list(players: list[FantasyPlayer], competeStatus: CompeteStatus) -> list[FantasyPlayer]:
    if competeStatus == CompeteStatus.REBUILD:
        return players[:len(players)//6]
    elif competeStatus == CompeteStatus.RELOAD:
        return players[:len(players)//4]
    elif competeStatus == CompeteStatus.NEUTRAL:
        return players[:len(players)//3]
    elif competeStatus == CompeteStatus.COMPETE:
        return players[:len(players)//2]
    else:
        return players

def get_pick_values(players: list[FantasyPlayer],
                           compete_status: CompeteStatus,
                           rounds: list[int], 
                           tiers: list[Tier]) -> dict[tuple[int, Tier], float]:

    sorted_players = sorted(players, key=lambda p: get_player_value_by_compete_status(p, compete_status), reverse=True)
    pick_value_map = {}

    # Determine range of values based on compete status
    players = trim_player_list(sorted_players, compete_status)

    # Determine gap between picks based on number of unique picks
    num_unique_picks = len(rounds) * len(tiers)
    section_size = max(1, len(players) // num_unique_picks)

    pick_idx = 0
    for rnd in rounds:
        for tier in tiers:
            idx = min((pick_idx + 1) * section_size - 1, len(players) - 1)
            value = get_player_value_by_compete_status(players[idx], compete_status) if idx >= 0 else 0.0
            pick_value_map[(rnd, tier)] = value
            pick_idx += 1

    return pick_value_map

def get_pick_value_by_year(value: float, earliestYear: int, currYear: int) -> float:
    """
    Adjusts the value based on the year of the pick.
    """
    weight = 0.95 ** (currYear - earliestYear)
    return round(value * weight, 2)
