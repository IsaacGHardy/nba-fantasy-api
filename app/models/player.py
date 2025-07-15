from pydantic import BaseModel

class Player(BaseModel):
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
    value: float = 0.0

    def set_normalized_value(self, min_pts: float, max_pts: float):
        """
        Sets a normalized value (50.00–100.00) for this player based on fantasy_pts.
        """
        min_val, max_val = 00.0, 100.0
        if max_pts == min_pts:
            self.value = max_val
        else:
            self.value = round(((self.fantasy_pts - min_pts) / (max_pts - min_pts)) * (max_val - min_val) + min_val, 2)
    """
    In order to calculate age, we need the birth date of the player, and then, we will perform 
    some nifty calculations to get the age. The tricky part is that there is no good API endpoint
    that will provide birthdates of all players. What's looking like the best option is to use
    the commonteamroster endpoint and make requests for all teams and then conglomerate the data.
    Unfortunately, 30 API calls takes a while, so I'd like to only implement this once we have 
    our own database set up and will make all these calls once a day. 
    
    """
