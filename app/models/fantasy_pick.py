from pydantic import BaseModel
from enum import Enum

class Tier(Enum):
    EARLY = "Early"
    MID = "Mid"
    LATE = "Late"

class FantasyPick(BaseModel):
    id: int
    year: int
    round: int
    tier: Tier
    label: str
    contend_value: float
    compete_value: float
    neutral_value: float
    reload_value: float
    rebuild_value: float
    type: str = "pick"

