def get_player_rebuild_value(pts: float, age: int) -> float:
    """
    Calculates the rebuild value for a player based on their age.
    Young players have their value greatly increased, 
    and older players have their value greatly decreased.
    """
    if(age <= 20):
        return pts * 4
    elif(age <= 21):
        return pts * 3.5
    elif(age <= 22):
        return pts * 3
    elif(age <= 23):
        return pts * 2.5
    elif(age <= 24):
        return pts * 2
    elif(age <= 26):
        return pts * 1.5
    elif(age <= 30):
        return pts * 1
    elif(age <= 34):
        return pts * 0.5
    else:
        return pts * 0.25

def get_player_reload_value(pts: float, age: int) -> float:
    """
    Calculates the reload value for a player based on their age.
        Young players have their value increased, 
        and older players have their value decreased.

    """
    if(age <= 20):
        return pts * 2.5
    elif(age <= 21):
        return pts * 2.25
    elif(age <= 22):
        return pts * 2
    elif(age <= 23):
        return pts * 1.85
    elif(age <= 24):
        return pts * 1.75
    elif(age <= 26):
        return pts * 1.5
    elif(age <= 28):
        return pts * 1.25
    elif(age <= 30):
        return pts * 1
    elif(age <= 32):
        return pts * 0.75
    elif(age <= 34):
        return pts * 0.6
    elif(age <= 36):
        return pts * 0.5
    else:
        return pts * 0.25
    
def get_player_neutral_value(pts: float, age: int) -> float:
    """
    Calculates the neutral value for a player based on their age.
        Young players have their value slightly increased,
        and older players have their value slightly decreased.

    """
    if(age <= 20):
        return pts * 1.5
    elif(age <= 21):
        return pts * 1.45
    elif(age <= 22):
        return pts * 1.4
    elif(age <= 23):
        return pts * 1.35
    elif(age <= 24):
        return pts * 1.3
    elif(age <= 25):
        return pts * 1.25
    elif(age <= 26):
        return pts * 1.2
    elif(age <= 28):
        return pts * 1.1
    elif(age <= 30):
        return pts * 1
    elif(age <= 32):
        return pts * 0.9
    elif(age <= 34):
        return pts * 0.8
    elif(age <= 36):
        return pts * 0.7
    else:
        return pts * 0.5
    
def get_player_compete_value(pts: float, age: int) -> float:
    """
    Calculates the compete value for a player based on their age.
        Young players have their value barely increased,
        and older players have their value barely decreased.

    """
    if(age <= 24):
        return pts * 1.2
    elif(age <= 28):
        return pts * 1.1
    elif(age <= 32):
        return pts * 1
    elif(age <= 36):
        return pts * 0.9
    else:
        return pts * 0.8