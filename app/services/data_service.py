from app.models.player import FantasyPlayer, Player
from nba_api.stats.endpoints import fantasywidget
from app.services.fantasy_service import create_fantasy_player
from app.services.fantasy_service import calculate_player_value
from app.models.scoring import Scoring

default_scoring = Scoring(
    pts=0.5,
    rebs=1,
    ast=1,
    blk=2.0,
    stl=2.0,
    tov=-1.0,
    fg3m=0.5,
    double_double=1,
    triple_double=2
)

def convert_player_data_to_model(player_data: dict) -> Player:  
    """
    Converts raw player data dictionary to Player model.
    """
    return Player(
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

def get_all_players() -> list[FantasyPlayer]:
    """
    Fetches all players from the NBA API and returns them as a list of FantasyPlayer objects.
    Skips players with missing fantasy data.
    """
    raw_data = fantasywidget.FantasyWidget(active_players='Y', last_n_games='41', season_type_all_star='Regular Season').get_dict()
    players_stats = raw_data['resultSets'][0]['rowSet']

    player_list = []

    for p in players_stats:
        player = convert_player_data_to_model(p)
        if player:
            #Calculate fantasy specific attributes
            player_list.append(create_fantasy_player(player, default_scoring))
    # Sort players by fantasy points in descending order
    player_list = sorted(player_list, key=lambda x: x.fantasy_pts, reverse=True)
    calculate_player_value(player_list)
    return player_list
   
