from app.models.player import Player

# Dummy function to simulate NBA API data

def get_player_data() -> list[Player]:
    return [
        Player(id=1, name="LeBron James", team="Lakers", position="SF"),
        Player(id=2, name="Stephen Curry", team="Warriors", position="PG"),
    ]
