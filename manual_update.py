from app.models.fantasy_player import FantasyPlayer
from app.services.db_service import get_all_players, upsert_draft_picks
from app.services.fantasy_service import generate_draft_picks


def main():
    player_data_list = get_all_players("sleeper_data")
    player_objs = [FantasyPlayer(**p) for p in player_data_list]

    draft_picks = generate_draft_picks(player_objs)

    upsert_draft_picks([dp.model_dump() for dp in draft_picks], "sleeper_picks")

    player_data_list = get_all_players("espn_data")
    player_objs = [FantasyPlayer(**p) for p in player_data_list]

    draft_picks = generate_draft_picks(player_objs)

    upsert_draft_picks([dp.model_dump() for dp in draft_picks], "espn_picks")

if __name__ == "__main__":
    main()  
