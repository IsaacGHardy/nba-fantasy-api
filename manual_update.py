from app.models.fantasy_player import FantasyPlayer
from app.services.db_service import get_all_players, upsert_draft_picks
from app.services.fantasy_service import generate_draft_picks


def main():
    player_list_raw = get_all_players("sleeper_data")

    player_list = [FantasyPlayer(**p) for p in player_list_raw]

    picks = generate_draft_picks(player_list)

    upsert_draft_picks([pick.model_dump() for pick in picks], "sleeper_picks")

if __name__ == "__main__":
    main()