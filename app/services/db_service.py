
from dotenv import load_dotenv

from app.models.sql_models import PlayerValue
load_dotenv()

from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in the environment or .env file.")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upsert_players(player_data_list: list[dict], table_name: str):
    # Upsert (insert or update) multiple player records into the specified table
    response = supabase.table(table_name).upsert(player_data_list).execute()
    return response.data

def upsert_player(player_data: dict):
    # Upsert a single player record into the specified table
    response = supabase.table("player_data").upsert(player_data).execute()
    return response.data

def get_all_players(table_name: str = "player_data") -> list[dict]:
    # Fetch all players from the specified table
    response = supabase.table(table_name).select("*").execute()
    return response.data

def upsert_player_values(player_value_data: list[dict], table_name: str):
    # Upsert player values into the specified table
    response = supabase.table(table_name).upsert(player_value_data).execute()
    return response.data

def upsert_draft_picks(draft_pick_data: list[dict], table_name: str):
    # Upsert draft picks into the specified table
    response = supabase.table(table_name).upsert(draft_pick_data).execute()
    return response.data

def get_all_draft_picks(table_name: str) -> list[dict]:
    # Fetch all draft picks from the specified table
    response = supabase.table(table_name).select("*").execute()
    return response.data