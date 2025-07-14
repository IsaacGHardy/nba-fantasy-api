from pydantic import BaseModel

class Player(BaseModel):
    id: int
    name: str
    team: str
    position: str
    pts: float
    rebs: float
    ast: float
    stl: float
    blk: float
