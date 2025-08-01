from app.models.sql_models import Player
from app.models.scoring import Scoring

from nba_api.stats.endpoints import fantasywidget

from app.models.sql_models import PlayerValue
from app.services.fantasy_service import calculate_fantasy_points
from app.services.fantasy_service import calculate_player_values
from app.services.utility_service import calculate_age_from_birthdate

def convert_player_data_to_model(player_data: dict) -> Player:  
    """
    Converts raw player data dictionary to Player model.
    """
    return Player(
        id=player_data[0],
        name=player_data[1],
        team=player_data[4],
        position=player_data[2],
        pts=player_data[9],
        rebs=player_data[10],
        ast=player_data[11],
        blk=player_data[12],
        stl=player_data[13],
        tov=player_data[14],
        fg3m=player_data[15],
        fga=player_data[16],
        fgm=player_data[16]* player_data[17], #Calculate field goals made using attempts and percentage
        fta=player_data[18],
        ftm=player_data[18] * player_data[19], #Calculate free throws made using attempts and percentage
    )

def get_all_players_raw() -> list[Player]:
    """
    Fetches all players from the NBA API and returns them as a list of Player objects.
    This function does not calculate fantasy points or values.
    """
    # Fetch raw player data from the NBA API
    raw_data = fantasywidget.FantasyWidget(active_players='Y', last_n_games='41', season_type_all_star='Regular Season').get_dict()
    players_stats = raw_data['resultSets'][0]['rowSet']

    player_list = []

    # Convert raw player data to Player models
    for p in players_stats:
        player = convert_player_data_to_model(p)
        if player:
            player_list.append(player)

    return player_list

def convert_player_to_player_values(player_list: list[Player], scoring: Scoring) ->list[PlayerValue]: 
    player_value_list = []
    for player in player_list: 
        player_value = PlayerValue(
            id=player.id,
            fantasy_pts=calculate_fantasy_points(player, scoring),
            age=calculate_age_from_birthdate(player.birth_date)
        )
        player_value_list.append(player_value)


    calculate_player_values(player_value_list)

    return player_value_list
