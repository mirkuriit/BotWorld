import pygame as pg
import settings
from random import randint, choice
from enum import Enum
from pprint import pprint
import copy
import time

from abc import abstractmethod


class PlayerType(Enum):
    AGRESSIVE = (255, 0, 0)
    APPLE = (170, 50, 20)
    FRIENDLY = (0, 255, 0)
    NEFOR = (0, 0, 255)
    DEAD = (0, 0, 0)


def init_sprites():
    sprites = {}

    scaled_nefor_sprite = pg.transform.scale(
        pg.image.load("player.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_nefor_sprite.fill(
        PlayerType.NEFOR.value, special_flags=pg.BLEND_MULT
    )

    scaled_friendly_sprite = pg.transform.scale(
        pg.image.load("player.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_friendly_sprite.fill(
        PlayerType.FRIENDLY.value, special_flags=pg.BLEND_MULT
    )

    apple = pg.transform.scale(
        pg.image.load("food.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
        )
    apple.fill(
        PlayerType.APPLE.value, special_flags=pg.BLEND_MULT)

    sprites[PlayerType.APPLE] = apple
    sprites[PlayerType.NEFOR] = scaled_nefor_sprite
    sprites[PlayerType.FRIENDLY] = scaled_friendly_sprite

    return sprites


SPRITES = init_sprites()

print(SPRITES)


class GameObject:
    def __init__(self, scaler, x: int, y: int, t: PlayerType):
        self.scaler = scaler
        self.x = x
        self.y = y
        self.type: PlayerType = t
        self.sprite = SPRITES[self.type] if self.type != PlayerType.DEAD else None
        self.has_move = True

    def is_dead(self):
        return self.type == PlayerType.DEAD

    def is_alive(self):
        return not (self.type == PlayerType.DEAD)

    def draw(self):
        if self.is_alive():
            screen.blit(self.sprite, (self.x * self.scaler, self.y * self.scaler))

    def dead(self):
        self.type = PlayerType.DEAD
        self.sprite = SPRITES[self.type]

    @abstractmethod
    def live(self):
        pass


class Food(GameObject):
    def __init__(self, scaler, x: int, y: int, t: PlayerType):
        super().__init__(scaler, x, y, t)

    def live(self):
        print("apple move")


class Player(GameObject):
    def __init__(self, scaler, x: int, y: int, t: PlayerType):
        super().__init__(scaler, x, y, t)
        self.hp = 100
        self.speed = 1

    def increase_level(self):
        self.hp += 1

    def decrease_level(self):
        self.hp -= 1

    def move_right(self):
        self.x += self.speed

    def move_left(self):
        self.x -= self.speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def live(self):
        match self.type:
            case PlayerType.AGRESSIVE:
                self._argessive_move()
            case PlayerType.FRIENDLY:
                self._friendly_move()
            case PlayerType.NEFOR:
                self._nefor_move()
        self.has_move = False

    def _nefor_move(self):
        print("nefor_move")

    def _argessive_move(self):
        pass

    def _neutral_move(self):
        pass

    def _friendly_move(self):
        while True:  # Ждём любое событие
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return False

                if event.type == pg.KEYDOWN:  # Только событие нажатия
                    if event.key == pg.K_LEFT:
                        print('Левая стрелка', f"{self.x}, {self.y}")
                        OLD_WORLD.swap_game_object(self.x, self.y, self.x - 1, self.y)
                        print('Левая стрелка', f"{self.x}, {self.y}")
                        return True
                    elif event.key == pg.K_RIGHT:
                        print('Правая стрелка', f"{self.x}, {self.y}")

                        OLD_WORLD.swap_game_object(self.x, self.y, self.x + 1, self.y)
                        print('Правая стрелка', f"{self.x}, {self.y}")

                        return True
                    elif event.key == pg.K_UP:
                        print('Стрелка вверх', f"{self.x}, {self.y}")
                        OLD_WORLD.swap_game_object(self.x, self.y, self.x, self.y - 1)
                        print('Стрелка вверх', f"{self.x}, {self.y}")
                        return True
                    elif event.key == pg.K_DOWN:
                        print('Стрелка вниз', f"{self.x}, {self.y}")
                        OLD_WORLD.swap_game_object(self.x, self.y, self.x, self.y + 1)
                        print('Стрелка вниз', f"{self.x}, {self.y}")
                        return True

            # Не нагружаем процессор в ожидании
            pg.time.delay(100)
        # self.move_right()
        print("friendly move")

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
        player_types = [PlayerType.DEAD] * int(dead_coef * num_players) + [PlayerType.NEFOR] * 4 + [
            PlayerType.APPLE] * 4 + [PlayerType.FRIENDLY]
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

    def swap_game_object(self, x1, y1, x2, y2):

        obj1 = self.world[y1][x1]
        obj2 = self.world[y2][x2]

        self.world[y1][x1], self.world[y2][x2] = obj2, obj1

        obj1.x, obj2.x = x2, x1
        obj1.y, obj2.y = y2, y1

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
    return NEW_WORLD


OLD_WORLD: World = World(
    settings.WORLD_WIDTH, settings.WORLD_HEIGHT, dead_coef=settings.DEAD_COEF)

pg.init()
screen = pg.display.set_mode(settings.RES)
clock = pg.time.Clock()

print(OLD_WORLD)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
    clock.tick(settings.FPS)
    pg.display.set_caption(f'FPS: {clock.get_fps()}')
    screen.fill((0, 0, 0))

    # NEW_WORLD = World.from_world(OLD_WORLD)
    # OLD_WORLD = step(OLD_WORLD, OLD_WORLD)

    OLD_WORLD.draw()
    pg.display.flip()
    for row in OLD_WORLD.world:
        for player in row:
            player.has_move = True
    for row in OLD_WORLD.world:
        for player in row:
            if player.has_move:
                player.live()
    print(OLD_WORLD)
