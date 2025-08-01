from app.models.sql_models import Player
from app.services.data_service import convert_player_to_player_values
from app.services.db_service import get_all_players, upsert_player_values
from app.static import scoring


def main():
    player_list_raw = get_all_players()

    player_list = [Player(**p) for p in player_list_raw]

    player_values = convert_player_to_player_values(player_list, scoring.sleeper)
    # Convert to dictionaries before upserting
    upsert_player_values([pv.model_dump() for pv in player_values], "sleeper_value")

    player_values = convert_player_to_player_values(player_list, scoring.espn)
    # Convert to dictionaries before upserting  
    upsert_player_values([pv.model_dump() for pv in player_values], "espn_value")

if __name__ == "__main__":
    main()