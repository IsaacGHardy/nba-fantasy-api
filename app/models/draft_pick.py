from pydantic import BaseModel

class FantasyPick(BaseModel):
    id: int
    year: int
    round: int
    tier: str  # 'early', 'mid', 'late'
    label: str
    value: float
    type: str = "pick"

