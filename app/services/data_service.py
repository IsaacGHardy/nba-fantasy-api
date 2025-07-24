from app.models.player import FantasyPlayer, Player
from app.models.scoring import Scoring

from nba_api.stats.endpoints import fantasywidget
from nba_api.stats.endpoints import leaguestandings
from nba_api.stats.endpoints import commonteamroster

from app.services.fantasy_service import assign_player_ages, create_fantasy_player
from app.services.fantasy_service import calculate_player_value
from app.services.utility_service import calculate_age_from_birthdate

import time

def convert_player_data_to_model(player_data: dict) -> Player:  
    """
    Converts raw player data dictionary to Player model.
    """
    return Player(
        id=str(player_data[0]),
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



def get_all_players_ages(teams: list[str]) -> dict[str, int]:
    """
    Fetches all players' ages from the NBA API by making requests for each team.
    Returns a dictionary mapping player IDs to their ages.
    """
    player_ages = {}
    for team in teams:
        time.sleep(1)
        raw_data = commonteamroster.CommonTeamRoster(team_id=team).get_dict()
        players = raw_data['resultSets'][0]['rowSet']
        for player in players:
            player_id = str(player[14])
            birth_date = player[10]
            if birth_date:
                age = calculate_age_from_birthdate(birth_date)
                player_ages[player_id] = age
    return player_ages

def get_all_teams_id() -> list[str]:
    """
    Fetches all NBA teams from the NBA API.
    """
    raw_data = leaguestandings.LeagueStandings().get_dict()
    teams = raw_data['resultSets'][0]['rowSet']

    return [team[2] for team in teams]  # Extract the ID for each team

def get_all_players(scoring: Scoring) -> list[FantasyPlayer]:
    """
    Fetches all players from the NBA API and returns them as a list of FantasyPlayer objects.
    Skips players with missing fantasy data.
    """
    # Fetch raw player data from the NBA API
    raw_data = fantasywidget.FantasyWidget(active_players='Y', last_n_games='41', season_type_all_star='Regular Season').get_dict()
    players_stats = raw_data['resultSets'][0]['rowSet']

    player_list = []

    # Convert raw player data to FantasyPlayer models
    for p in players_stats:
        player = convert_player_data_to_model(p)
        if player:
            #Calculate fantasy specific attributes
            player_list.append(create_fantasy_player(player, scoring))

    # Get all teams and their players' ages
    teams = get_all_teams_id()
    player_ages = get_all_players_ages(teams)

    # Assign ages to players
    assign_player_ages(player_ages, player_list)
    
    # Sort players by fantasy points in descending order
    calculate_player_value(player_list)
    player_list = sorted(player_list, key=lambda x: x.rebuild_value, reverse=True)


    return player_list
   