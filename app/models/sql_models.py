from pydantic import BaseModel
from datetime import date


class PlayerValue(BaseModel):
    id: int
    fantasy_pts: float = 0.0
    contend_value: float = 0.0
    rebuild_value: float = 0.0
    age: int = 0


class Player(BaseModel):
    id: int
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
    birth_date: date | None = None

class DraftPick(BaseModel):
    id: int
    year: int
    round: int
    tier: str  # 'early', 'mid', 'late'
    label: str
    value: float