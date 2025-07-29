import os
from databases import Database
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the connection string
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

if not USER or not PASSWORD or not HOST or not PORT or not DBNAME:
    raise RuntimeError("Database environment variables are not set correctly in the .env file")

database = Database(DATABASE_URL)