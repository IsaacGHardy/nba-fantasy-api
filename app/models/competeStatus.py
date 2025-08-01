import enum

class CompeteStatus(enum.Enum):
    CONTEND = "contend"
    COMPETE = "compete"
    NEUTRAL = "neutral"
    RELOAD = "reload"
    REBUILD = "rebuild"