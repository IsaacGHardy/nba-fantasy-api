from pydantic import BaseModel

class Scoring(BaseModel):
    pts: float = 0.0
    rebs: float = 0.0
    ast: float = 0.0
    blk: float = 0.0
    stl: float = 0.0
    tov: float = 0.0
    fg3m: float = 0.0
    fgm: float = 0.0
    fga: float = 0.0
    ftm: float = 0.0
    fta: float = 0.0
    double_double: float = 0.0
    triple_double: float = 0.0
