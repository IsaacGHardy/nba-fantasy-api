from typing import Any
from pydantic import BaseModel

class Player(BaseModel):
    name: str
    team: Any
    position: str
    pts: float
    rebs: float
    ast: float
    stl: float
    blk: float
