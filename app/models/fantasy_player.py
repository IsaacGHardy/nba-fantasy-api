from app.models.sql_models import Player


class FantasyPlayer(Player):
    fantasy_pts: float = 0.0
    contend_value: float = 0.0
    rebuild_value: float = 0.0
    age: int = 0  
    type: str = "player"

    
