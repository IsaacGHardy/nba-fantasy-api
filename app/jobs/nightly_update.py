import asyncio
import logging
from app.models.fantasy_player import FantasyPlayer
from app.models.sql_models import Player, PlayerBirthdate, PlayerValue
from app.services.data_service import convert_player_to_player_values, get_all_players_raw
from app.services.db_service import get_all_players, upsert_draft_picks, upsert_player, upsert_player_values, upsert_players
from app.services.fantasy_service import generate_draft_picks
from app.services.utility_service import get_player_birthdate
from app.static import scoring

async def update_draft_picks(scoring: str):
    """Update draft picks for given scoring"""
    try:
        logging.info(f"Starting {scoring} draft picks update...")

        # Update Sleeper picks
        players_raw = get_all_players(f"{scoring}_data")
        players = [FantasyPlayer(**p) for p in players_raw]
        picks = generate_draft_picks(players)
        upsert_draft_picks([pick.model_dump() for pick in picks], f"{scoring}_picks")
        logging.info(f"Updated {len(picks)} {scoring} picks")
        
    except Exception as e:
        logging.error(f"{scoring} picks update failed: {e}")
        raise

async def check_birthdates(players_new: list[Player]):
    players_old = get_all_players("player_birthdates")
    
    # Create a set of existing player IDs for fast lookup
    old_player_ids = {player['id'] for player in players_old}
    
    # Find new players not in the old birthdates list
    for player in players_new:
        if player.id not in old_player_ids:
            # Get player's birthdate
            birthdate = get_player_birthdate(player.id)

            upsert_player({"id": player.id, "birth_date": birthdate}, "player_birthdates")

            logging.info(f"Found new player: ID {player.id}, Name: {player.name}")
            await asyncio.sleep(5)
    


async def update_player_data(): 
    try:
        logging.info("Starting player data update...")
        players = get_all_players_raw()

        # Check for new players before updating
        await check_birthdates(players)

        upsert_players([player.model_dump() for player in players])

        logging.info(f"Updated {len(players)} player records")
    except Exception as e:
        logging.error(f"Player data update failed: {e}")
        raise

async def update_player_values():
    try:
        logging.info(f"Starting player values update...")
        
        player_list_raw = get_all_players()

        player_list = [PlayerBirthdate(**p) for p in player_list_raw]
    
        player_values = convert_player_to_player_values(player_list, scoring.sleeper)
        # Convert to dictionaries before upserting
        upsert_player_values([pv.model_dump() for pv in player_values], "sleeper_value")

        player_values = convert_player_to_player_values(player_list, scoring.espn)
        # Convert to dictionaries before upserting  
        upsert_player_values([pv.model_dump() for pv in player_values], "espn_value")
    except Exception as e:
        logging.error(f"Player values update failed: {e}")
        raise

async def update_data(): 
    try:
        logging.info("Starting nightly data update...")
        
        await update_player_data()
        await update_player_values()
        await update_draft_picks("sleeper")
        await update_draft_picks("espn")

    except Exception as e:
        logging.error(f"Nightly data update failed: {e}")
        raise