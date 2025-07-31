from app.models.fantasy_player import FantasyPlayer
from app.models.sql_models import PlayerValue, Player, DraftPick
from app.models.scoring import Scoring

from app.services.utility_service import CompeteStatus, generate_round_with_suffix, get_trimmed_min_max
from app.services.utility_service import get_rebuild_value


def determine_value_to_set(player: PlayerValue, val: float, compete_status: CompeteStatus):
    if compete_status == CompeteStatus.CONTEND:
        player.contend_value = val
    elif compete_status == CompeteStatus.REBUILD:
        player.rebuild_value = val

def set_value(player: PlayerValue, min_pts: float, max_pts: float, compete_status: CompeteStatus):
    """
    Sets a normalized value (25.00–100.00) for this player based on fantasy_pts.
    """

    min_val, max_val = 25.0, 100.0
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

def calculate_player_value(player_list: list[PlayerValue]): 
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

def generate_draft_picks(players: list[FantasyPlayer], years=(2025, 2026, 2027, 2028), rounds=(1, 2, 3), tiers=("early", "mid", "late")) -> list[DraftPick]:
    """
    Given a list of FantasyPlayer, segment the top 1/3 into 12 sections and assign each pick the value at the bottom of its section.
    Returns a list of DraftPick objects.
    """
    # Sort players by value (rebuild_value)
    sorted_players = sorted(players, key=lambda p: p.rebuild_value, reverse=True)
    top_third = sorted_players[:len(sorted_players)//3]
    num_unique_picks = len(rounds) * len(tiers)
    section_size = max(1, len(top_third) // num_unique_picks)
    # Compute value for each unique (round, tier) combo
    pick_value_map = {}
    pick_idx = 0
    for rnd in rounds:
        for tier in tiers:
            idx = min((pick_idx + 1) * section_size - 1, len(top_third) - 1)
            value = top_third[idx].rebuild_value if idx >= 0 else 0.0
            pick_value_map[(rnd, tier)] = value
            pick_idx += 1
    # Now assign value to all years for each (round, tier)
    picks = []
    tier_digit = {"early": "1", "mid": "2", "late": "3"}
    for year in years:
        for rnd in rounds:
            for tier in tiers:
                label = f"{year} {tier.title()} {generate_round_with_suffix(rnd)}"
                value = pick_value_map[(rnd, tier)]
                id_str = f"{year}{rnd}{tier_digit[tier]}"
                id = int(id_str)
                picks.append(DraftPick(id=id, year=year, round=rnd, tier=tier, label=label, value=value))
    return picks