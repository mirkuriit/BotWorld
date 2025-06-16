import pygame as pg
import settings
from random import randint, choice
from enum import Enum
from pprint import pprint
import copy
import numpy as np

from abc import abstractmethod


class PlayerType(Enum):
    AGRESSIVE = (255, 0, 0)
    FRIENDLY = (0, 255, 0)
    NEFOR = (0, 0, 255)
    DEAD = (0, 0, 0)

def init_sprites():
    sprites = {}
    scaled_player_sprite = pg.transform.scale(
        pg.image.load("img.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )

    for player_type in PlayerType:
        colored_sprite = scaled_player_sprite.copy()
        colored_sprite.fill(
            player_type.value, special_flags=pg.BLEND_MULT)
        sprites[player_type] = colored_sprite

    return sprites

SPRITES = init_sprites()

print(SPRITES)

class Player:
    def __init__(self, scaler, x: int, y: int, t: PlayerType):
        self.scaler = scaler
        self.x = x
        self.y = y
        self.type: PlayerType = t
        self.sprite = SPRITES[self.type] if self.type != PlayerType.DEAD else None

    def is_dead(self):
        return self.type == PlayerType.DEAD

    def is_alive(self):
        return not (self.type == PlayerType.DEAD)

    def dead(self):
        self.type = PlayerType.DEAD
        self.sprite = SPRITES[self.type]

    def born(self):
        self.type = PlayerType.NEFOR
        self.sprite = SPRITES[self.type]

    def draw(self):
        if self.is_alive():
            screen.blit(self.sprite, (self.x * self.scaler, self.y * self.scaler))

    def live(self):
        match self.type:
            case PlayerType.AGRESSIVE:
                self._argessive_move()
            case PlayerType.FRIENDLY:
                self._friendly_move()
            case PlayerType.NEFOR:
                self._nefor_move()

    def _nefor_move(self):
        pass

    def _argessive_move(self):
        pass

    def _neutral_move(self):
        pass

    def _friendly_move(self):
        pass

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
        player_types = [PlayerType.DEAD] * int(dead_coef * num_players) + [PlayerType.NEFOR] * int(
            (1 - dead_coef) * num_players)
        if len(player_types) > num_players:
            player_types = player_types[::-1][:num_players]
        elif len(player_types) < num_players:
            player_types += [PlayerType.DEAD] * (
                    num_players - len(player_types))
        world = [
            [
            Player(scaler=settings.IMG_SCALE,
                   x=i,
                   y=j,
                   t=player_types.pop(randint(0, len(player_types) - 1))) for i in
            range(width)
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

    def draw(self):
        for row in self.world:
            for player in row:
                if player.is_alive():
                    player.draw()

    def __repr__(self):
        s = ""
        for row in self.world:
            s += ("\t".join(map(str, row)) + "\n")
        return s


def get_neighbours(player: Player, world: World) -> list[Player]:
    px, py = player.x, player.y
    neighbours_tmp = [
        (px + 1, py + 1),
        (px, py + 1),
        (px - 1, py + 1),
        (px + 1, py),
        (px - 1, py),
        (px - 1, py - 1),
        (px, py - 1),
        (px + 1, py - 1),
    ]
    neighbours_coords = [(x, y) for x, y in neighbours_tmp if
                         (x >= 0) and (y >= 0) and \
                         (x <= world.width - 1) and (y <= world.height - 1)]
    neighbors = [world.world[y][x] for x, y in neighbours_coords]
    return neighbors


def step(OLD_WORLD, NEW_WORLD):
    for i in range(OLD_WORLD.height):
        for j in range(OLD_WORLD.width):
            player = NEW_WORLD.world[i][j]
            neighbours = get_neighbours(player, OLD_WORLD)

            ### TODO in other function
            num_alive = sum(n.is_alive() for n in neighbours)
            if (num_alive < 2 or num_alive > 3) and player.is_alive():
                player.dead()
            elif num_alive == 3 and player.is_dead():
                player.born()
    return NEW_WORLD


OLD_WORLD: World = World(
    settings.WORLD_WIDTH, settings.WORLD_HEIGHT, dead_coef=settings.DEAD_COEF)

pg.init()
screen = pg.display.set_mode(settings.RES)
clock = pg.time.Clock()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    NEW_WORLD = World.from_world(OLD_WORLD)
    OLD_WORLD = step(OLD_WORLD, NEW_WORLD)

    clock.tick(settings.FPS)
    pg.display.set_caption(f'FPS: {clock.get_fps()}')
    screen.fill((0, 0, 0))
    OLD_WORLD.draw()
    pg.display.flip()
