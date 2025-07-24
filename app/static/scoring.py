from app.models.scoring import Scoring


sleeper = Scoring(
    pts=0.5,
    rebs=1,
    ast=1,
    blk=2.0,
    stl=2.0,
    tov=-1.0,
    fg3m=0.5,
    double_double=1,
    triple_double=2
)

espn = Scoring(
    pts=1.0,         
    fg3m=1.0,        
    fga=-1.0,        
    fgm=2.0,        
    fta=-1.0,        
    ftm=1.0,        
    rebs=1.0,
    ast=2.0,         
    stl=4.0,         
    blk=4.0,         
    tov=-2.0        
)