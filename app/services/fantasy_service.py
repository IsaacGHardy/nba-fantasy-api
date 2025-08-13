from app.models.fantasy_pick import Tier
from app.models.fantasy_player import FantasyPlayer
from app.models.sql_models import PlayerValue, Player, DraftPick
from app.models.scoring import Scoring
from app.models.competeStatus import CompeteStatus

from app.static.pick_info import YEARS, ROUNDS, TIERS

from app.services.pick_value_service import get_pick_value_by_year, get_pick_values
from app.services.utility_service import generate_round_with_suffix, get_player_compete_value, get_player_neutral_value, get_player_reload_value, get_trimmed_min_max
from app.services.utility_service import get_player_rebuild_value


def determine_value_to_set(player: PlayerValue, val: float, compete_status: CompeteStatus):
    if compete_status == CompeteStatus.CONTEND:
        player.contend_value = val
    elif compete_status == CompeteStatus.COMPETE:
        player.compete_value = val
    elif compete_status == CompeteStatus.NEUTRAL:
        player.neutral_value = val
    elif compete_status == CompeteStatus.RELOAD:
        player.reload_value = val
    elif compete_status == CompeteStatus.REBUILD:
        player.rebuild_value = val

def get_value_by_compete_status(pts: float, age: int, compete_status: CompeteStatus) -> float:
    if compete_status == CompeteStatus.CONTEND:
        return pts
    elif compete_status == CompeteStatus.COMPETE:
        return get_player_compete_value(pts, age)
    elif compete_status == CompeteStatus.NEUTRAL:
        return get_player_neutral_value(pts, age)
    elif compete_status == CompeteStatus.RELOAD:
        return get_player_reload_value(pts, age)
    elif compete_status == CompeteStatus.REBUILD:
        return get_player_rebuild_value(pts, age)
    else:
        return 0.0

def set_value(player: PlayerValue, min_pts: float, max_pts: float, compete_status: CompeteStatus):
    """
    Sets a normalized value (25.00–100.00) for this player based on fantasy_pts.
    """

    min_val, max_val = 25.0, 100.0
    if max_pts == min_pts:
        determine_value_to_set(player, max_val, compete_status)
    else:
        self_value = get_value_by_compete_status(player.fantasy_pts, player.age, compete_status)
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

def calculate_player_values(player_list: list[PlayerValue]): 
    """
    Calculates the value of a player based on their fantasy points 
    and the contention factor of the team.
    """

    min_pts, max_pts = get_trimmed_min_max(player_list, trim=6, competeStatus=CompeteStatus.CONTEND)
    for player in player_list:
        set_value(player, min_pts, max_pts, compete_status=CompeteStatus.CONTEND)

    min_pts, max_pts = get_trimmed_min_max(player_list, trim=6, competeStatus=CompeteStatus.COMPETE)
    for player in player_list:
        set_value(player, min_pts, max_pts, compete_status=CompeteStatus.COMPETE)   

    min_pts, max_pts = get_trimmed_min_max(player_list, trim=6, competeStatus=CompeteStatus.NEUTRAL)
    for player in player_list:
        set_value(player, min_pts, max_pts, compete_status=CompeteStatus.NEUTRAL)

    min_pts, max_pts = get_trimmed_min_max(player_list, trim=6, competeStatus=CompeteStatus.RELOAD)
    for player in player_list:
        set_value(player, min_pts, max_pts, compete_status=CompeteStatus.RELOAD)

    min_pts, max_pts = get_trimmed_min_max(player_list, trim=6, competeStatus=CompeteStatus.REBUILD)
    for player in player_list:
        set_value(player, min_pts, max_pts, compete_status=CompeteStatus.REBUILD)

def generate_draft_picks(players: list[FantasyPlayer], years=YEARS, rounds=ROUNDS, tiers=TIERS) -> list[DraftPick]:
    """
    Given a list of FantasyPlayer, segment the top 1/3 into 12 sections and assign each pick the value at the bottom of its section.
    Returns a list of DraftPick objects.
    """
    pick_contend_value_map = get_pick_values(players, CompeteStatus.CONTEND, rounds, tiers)
    pick_compete_value_map = get_pick_values(players, CompeteStatus.COMPETE, rounds, tiers)
    pick_neutral_value_map = get_pick_values(players, CompeteStatus.NEUTRAL, rounds, tiers)
    pick_reload_value_map = get_pick_values(players, CompeteStatus.RELOAD, rounds, tiers)
    pick_rebuild_value_map = get_pick_values(players, CompeteStatus.REBUILD, rounds, tiers)

    picks = []
    tier_digit = {Tier.EARLY: "1", Tier.MID: "2", Tier.LATE: "3"}
    for year in years:
        for rnd in rounds:
            for tier in tiers:
                label = f"{year} {tier.value} {generate_round_with_suffix(rnd)}"
                contend_value = get_pick_value_by_year(pick_contend_value_map[(rnd, tier)], years[0], year)
                compete_value = get_pick_value_by_year(pick_compete_value_map[(rnd, tier)], years[0], year)
                neutral_value = get_pick_value_by_year(pick_neutral_value_map[(rnd, tier)], years[0], year)
                reload_value = get_pick_value_by_year(pick_reload_value_map[(rnd, tier)], years[0], year)
                rebuild_value = get_pick_value_by_year(pick_rebuild_value_map[(rnd, tier)], years[0], year)
                id_str = f"{year}{rnd}{tier_digit[tier]}"
                id = int(id_str)
                picks.append(DraftPick(id=id, year=year, round=rnd, tier=tier.value, label=label, 
                                       contend_value=contend_value, compete_value=compete_value, 
                                       neutral_value=neutral_value, reload_value=reload_value, 
                                       rebuild_value=rebuild_value))
    return picks
