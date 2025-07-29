from pydantic import BaseModel

class PlayerValue(BaseModel):
    id: str | int
    fantasy_pts: float = 0.0
    contend_value: float = 0.0
    rebuild_value: float = 0.0
    age: int = 0
