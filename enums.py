from enum import Enum


class PlayerType(Enum):
    AGRESSIVE = None
    APPLE = (219, 214, 93)
    FRIENDLY = None
    NEFOR = (225, 101, 47)
    DEAD = (39, 39, 39)
    PLAYER = (20, 167, 108)


class PlayerCollision(Enum):
    PLAYER_APPLE = {PlayerType.PLAYER, PlayerType.APPLE}
    PLAYER_DEAD = {PlayerType.PLAYER, PlayerType.DEAD}
    PLAYER_NEFOR = {PlayerType.PLAYER, PlayerType.NEFOR}
