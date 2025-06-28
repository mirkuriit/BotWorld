import settings
import pygame as pg
import sys
import time

from random import randint, choice
from abc import abstractmethod
from enum import Enum
from loguru import logger
from functools import wraps
from itertools import chain


pg.init()
screen = pg.display.set_mode(settings.RES)
clock = pg.time.Clock()


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


def init_sprites():
    sprites = {}

    scaled_player_sprite = pg.transform.scale(
        pg.image.load("player.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_player_sprite.fill(
        PlayerType.PLAYER.value, special_flags=pg.BLEND_MULT
    )

    scaled_nefor_sprite = pg.transform.scale(
        pg.image.load("player.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_nefor_sprite.fill(
        PlayerType.NEFOR.value, special_flags=pg.BLEND_MULT
    )

    scaled_apple_sprite = pg.transform.scale(
        pg.image.load("food.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_apple_sprite.fill(
        PlayerType.APPLE.value, special_flags=pg.BLEND_MULT)

    scaled_dead_sprite = pg.transform.scale(
        pg.image.load("field.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_dead_sprite.fill(
        PlayerType.DEAD.value, special_flags=pg.BLEND_MULT)

    sprites[PlayerType.APPLE] = scaled_apple_sprite
    sprites[PlayerType.DEAD] = scaled_dead_sprite
    sprites[PlayerType.PLAYER] = scaled_player_sprite
    sprites[PlayerType.NEFOR] = scaled_nefor_sprite
    sprites[PlayerType.FRIENDLY] = scaled_nefor_sprite

    return sprites


### TODO move decorator something out like a log.py
def move_log(func):
    @wraps(func)
    def inner(o: GameObject):
        if o.is_alive():
            s = f"{o.id}`s {o.type} move"
            if o.type == PlayerType.PLAYER:
                s += f" current refs: {sys.getrefcount(o)}"
            logger.info(s)
        func(o)

    return inner


class GameObject:
    def __init__(self, scaler, x: int, y: int, t: PlayerType, hp: int):
        self.scaler = scaler
        self.x = x
        self.y = y
        self.type: PlayerType = t
        self.sprite = SPRITES[self.type]
        self.has_move = True
        self.id = x + y * settings.WORLD_WIDTH
        self.hp = -100 if t == PlayerType.DEAD else hp

    def is_dead(self):
        return self.type == PlayerType.DEAD

    def is_alive(self):
        return not (self.type == PlayerType.DEAD)

    def increase_hp(self, n=1):
        self.hp += n

    def decrease_hp(self, n=1):
        self.hp -= n

    def draw(self):
        screen.blit(self.sprite, (self.x * self.scaler, self.y * self.scaler))
        font = pg.font.SysFont(None, 24)
        # text_id = font.render(str(self.id), 1, (255, 255, 255))
        # screen.blit(text_id, (self.x * self.scaler, self.y * self.scaler))
        if self.is_alive():
            text_hp = font.render(str(self.hp), 1, (255, 255, 255))
            screen.blit(text_hp, (self.x * self.scaler + self.scaler // 2.5, self.y * self.scaler + self.scaler // 2))

    def dead(self):
        self.type = PlayerType.DEAD
        self.sprite = SPRITES[self.type]

    @abstractmethod
    def live(self):
        pass


class Food(GameObject):
    def __init__(self, scaler, x: int, y: int, t: PlayerType):
        super().__init__(scaler, x, y, t)

    @move_log
    def live(self):
        pass


class Player(GameObject):
    def __init__(self, scaler, x: int, y: int, t: PlayerType, hp: int):
        super().__init__(scaler, x, y, t, hp)
        self.speed = 1

    @move_log
    def live(self):
        match self.type:
            case PlayerType.AGRESSIVE:
                self._argessive_move()
            case PlayerType.FRIENDLY:
                self._friendly_move()
            case PlayerType.NEFOR:
                self._nefor_move()
            case PlayerType.PLAYER:
                self._player_move()
        self.has_move = False

    def _nefor_move(self):
        pass

    def _argessive_move(self):
        pass

    def _neutral_move(self):
        pass

    def _friendly_move(self):
        pass

    def _player_move(self):
        while True:  ### TODO Ну это мем ебаный вообще
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        if self.x == 0:
                            logger.warning(f"{self.type} {self.id} сделаал недопустимсый ход")
                        else:
                            OLD_WORLD.swap_game_object(self.x, self.y, self.x - 1, self.y)
                        return True
                    elif event.key == pg.K_RIGHT:
                        if self.x == settings.WORLD_WIDTH - 1:
                            logger.warning(f"{self.type} {self.id} сделаал недопустимсый ход")
                        else:
                            OLD_WORLD.swap_game_object(self.x, self.y, self.x + 1, self.y)
                        return True
                    elif event.key == pg.K_UP:
                        if self.y == 0:
                            logger.warning(f"{self.type} {self.id} сделаал недопустимсый ход")
                        else:
                            OLD_WORLD.swap_game_object(self.x, self.y, self.x, self.y - 1)
                        return True
                    elif event.key == pg.K_DOWN:
                        if self.y == settings.WORLD_HEIGHT - 1:
                            logger.warning(f"{self.type} {self.id} сделаал недопустимсый ход")
                        else:
                            OLD_WORLD.swap_game_object(self.x, self.y, self.x, self.y + 1)

                        return True
            pg.time.delay(100)

    def __repr__(self):
        return f"x:{self.x} y:{self.y} {self.type.name}"

    def __str__(self):
        return self.type.name


class World:
    def __init__(self, width, height, dead_coef, fill_strategy="random"):
        self.width = width
        self.height = height
        self.fill_strategy = fill_strategy
        self.dead_coef = dead_coef
        self.world: list[list[Player]] = self.generate_world(
            self.width,
            self.height,
            self.fill_strategy,
            self.dead_coef
        )

    def generate_world(
            self,
            width: int,
            height: int,
            fill_strategy: str,
            dead_coef: int
    ) -> list[list[Player]]:
        num_players = width * height
        ### TODO some algo for GameObjects allocation on game field
        player_types = [PlayerType.DEAD] * int(dead_coef * num_players) + [PlayerType.NEFOR] * 10 + [
            PlayerType.APPLE] * 4 + [PlayerType.PLAYER]
        if len(player_types) > num_players:
            player_types = player_types[::-1][:num_players]
        elif len(player_types) < num_players:
            player_types += [PlayerType.DEAD] * (
                    num_players - len(player_types))
        world = [
            [
                Player(
                    scaler=settings.IMG_SCALE,
                    x=i,
                    y=j,
                    t=player_types.pop(randint(0, len(player_types) - 1)),
                    hp=randint(1, 100)
                ) for i in range(width)
            ]
            for j in range(height)]
        return world

    @classmethod
    def from_world(cls, source_world):
        new_world = cls.__new__(cls)

        new_world.width = source_world.width
        new_world.height = source_world.height
        new_world.dead_coef = source_world.dead_coef
        new_world.fill_strategy = source_world.fill_strategy

        new_world.world = [
            [
                Player(
                    scaler=player.scaler,
                    x=player.x,
                    y=player.y,
                    t=player.type
                )
                for player in row
            ]
            for row in source_world.world
        ]

        return new_world

    def _draw_lines(self):
        for i in range(settings.WORLD_WIDTH):
            pg.draw.line(
                screen, (116, 116, 116, 100), (i * settings.IMG_SCALE, 0),
                (i * settings.IMG_SCALE, settings.WORLD_HEIGHT * settings.IMG_SCALE), 10)
        for j in range(settings.WORLD_WIDTH):
            pg.draw.line(
                screen, (116, 116, 116, 10), (0, j * settings.IMG_SCALE),
                (settings.WORLD_WIDTH * settings.IMG_SCALE, j * settings.IMG_SCALE), 10)

    def draw(self):
        self._draw_lines()
        for player in chain.from_iterable(self.world):
            player.draw()

    def _aging_step(self):
        for player in chain.from_iterable(self.world):
            player.decrease_hp()
            if player.hp == 0:
                logger.warning(f"{player.id} was killed")
                player.dead()

    def _fight(self, obj1: Player, obj2: Player):
        if obj1.hp == obj2.hp:
            obj1.dead()
            obj2.dead()
        elif obj1.hp >= obj2.hp:
            obj1.increase_hp(obj2.hp)
            obj2.dead()
        else:
            obj2.increase_hp(obj1.hp)
            obj1.dead()

    def _eat(self, obj1: Player, obj2: Food):
        obj1.increase_hp(obj2.hp)
        obj2.dead()

    def _check_collisions(self, obj1: GameObject | Player, obj2: GameObject | Player | Food):
        if {obj1.type, obj2.type} == PlayerCollision.PLAYER_APPLE.value:
            self._eat(obj1, obj2)
        elif {obj1.type, obj2.type} == PlayerCollision.PLAYER_NEFOR.value:
            self._fight(obj1, obj2)

    def _players_step(self):
        for row in OLD_WORLD.world:
            for player in row:
                player.has_move = True
        for player in chain.from_iterable(self.world):
            if player.has_move:
                player.live()

    def live(self):
        self._aging_step()
        self._players_step()

    def swap_game_object(self, x1, y1, x2, y2):

        obj1: GameObject = self.world[y1][x1]
        obj2: GameObject = self.world[y2][x2]

        self._check_collisions(obj1, obj2)
        self.world[y1][x1], self.world[y2][x2] = obj2, obj1

        obj1.x, obj2.x = x2, x1
        obj1.y, obj2.y = y2, y1
        tmp_id = obj1.id
        obj1.id = obj2.id
        obj2.id = tmp_id

    def __repr__(self):
        s = ""
        for row in self.world:
            s += ("\t".join(map(str, row)) + "\n")
        return s


SPRITES = init_sprites()
OLD_WORLD: World = World(
    settings.WORLD_WIDTH, settings.WORLD_HEIGHT, dead_coef=settings.DEAD_COEF)

move = 0
while True:
    logger.info(f"MOVE {move}")
    move += 1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()


    OLD_WORLD.draw()
    pg.display.flip()
    OLD_WORLD.live()

    clock.tick(settings.FPS)
    pg.display.set_caption(f'FPS: {clock.get_fps()}')
    screen.fill((0, 0, 0))

