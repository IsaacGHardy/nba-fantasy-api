from app.models.player import Player
from app.services.data_service import calculate_player_values
from app.services.db_service import get_all_players, upsert_player_values
from app.static.scoring import sleeper, espn

from nba_api.stats.endpoints import commonplayerinfo

def main():
    player_data_list = get_all_players()
    player_objs = [Player(**p) for p in player_data_list]
    player_value_list = calculate_player_values(player_objs, sleeper)

    upsert_player_values([pv.model_dump() for pv in player_value_list], "sleeper_value")

    player_value_list = calculate_player_values(player_objs, espn)

    upsert_player_values([pv.model_dump() for pv in player_value_list], "espn_value")

if __name__ == "__main__":
    main()


"""
Separate raw data from fantasy points and value calculations.
Have table for raw data then separate tables for points and value per scoring system.
Or do I? 
get_all_players_raw function that does nothing with value or fantasy points.
Upload into db,  then I can pull all that data directly back out to calculate fantasy points and value.
Then, put all that into new tables...
"""