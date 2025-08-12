from enum import Enum


class PlayerType(Enum):
    AGRESSIVE = None
    APPLE = (219, 214, 93)
    FRIENDLY = None
    NEFOR = (225, 101, 47)
    DEAD = (39, 39, 39)
    PLAYER = (20, 167, 108)


class PlayerCollision(Enum):
    NEFOR_APPLE = {PlayerType.NEFOR, PlayerType.APPLE}
    NEFOR_DEAD = {PlayerType.NEFOR, PlayerType.DEAD}
    NEFOR_NEFOR = {PlayerType.NEFOR, PlayerType.NEFOR}