from pydantic import BaseModel

class Player(BaseModel):
    id: str
    name: str
    team: str
    position: str
    pts: float
    rebs: float
    ast: float
    blk: float
    stl: float
    tov: float
    fg3m: float
    fgm: float
    fga: float
    ftm: float
    fta: float

class FantasyPlayer(Player):
    fantasy_pts: float = 0.0
    contend_value: float = 0.0
    rebuild_value: float = 0.0
    age: int = 0  

    
