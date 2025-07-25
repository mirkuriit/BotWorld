from typing import override

import settings
from sprites import SPRITES
from enums import PlayerType, PlayerCollision
from utils import move_log
from utils import need_ill
from utils import get_player_startup_hp

import pygame as pg
import sys
import time

from random import randint, choice, gauss, sample
from abc import abstractmethod
from loguru import logger
from functools import wraps
from itertools import chain


pg.init()
screen = pg.display.set_mode(settings.RES)
clock = pg.time.Clock()


class GameObject:
    def __init__(self, scaler, x: int, y: int, t: PlayerType, hp: int):
        self.scaler = scaler
        self.x = x
        self.y = y
        self.type: PlayerType = t
        self.sprite = SPRITES[self.type]
        self.has_move = True
        self.id = x + y * scaler
        self.hp = -1000 if t == PlayerType.DEAD else hp

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
        text_id = font.render(str(self.id), 1, settings.ID_COLOR)
        screen.blit(text_id, (self.x * self.scaler, self.y * self.scaler))
        if self.is_alive():
            text_hp = font.render(str(self.hp), 1, settings.HP_COLOR)
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

    def live(self):
        pass


class Player(GameObject):
    def __init__(self, scaler, x: int, y: int, t: PlayerType, hp: int):
        super().__init__(scaler, x, y, t, hp)
        self.speed = 1
        self.is_ill = False
        self.steps_from_ill = 0

    @override
    def draw(self):
        screen.blit(self.sprite, (self.x * self.scaler, self.y * self.scaler))
        font = pg.font.SysFont(None, 24)
        ### text_id is debug info
        text_id = font.render(str(self.id), 1, settings.ID_COLOR)
        screen.blit(text_id, (self.x * self.scaler, self.y * self.scaler))
        if self.is_alive():
            text_hp = font.render(str(self.hp), 1, settings.HP_COLOR)
            screen.blit(text_hp, (self.x * self.scaler + self.scaler // 2.5, self.y * self.scaler + self.scaler // 2))
            if self.is_ill:
                screen.blit(SPRITES["illness"], (self.x * self.scaler + self.scaler // 2, self.y * self.scaler))

    @move_log(is_log=True)
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
    def __init__(self, width, height, live_coef):
        self.width = width
        self.height = height
        self.live_cof = live_coef
        self.world: list[list[Player]] = self.generate_world(
            self.width,
            self.height,
            self.live_cof
        )
        self.GLOBAL_PLAYER_COUNT = 0

    def _get_players_coord(self, num_players, x_limit, y_limit) -> set[(int, int)]:
        coords = set()
        while len(coords) < num_players:
            coords.add((randint(0, x_limit-1), randint(0, y_limit-1)))
        return coords

    def generate_world(
            self,
            width: int,
            height: int,
            live_coef: float
    ) -> list[list[Player]]:
        num_players = width * height
        live_players_count = int(num_players * live_coef)

        assert live_players_count < (num_players // 2)
        live_players_coords = self._get_players_coord(num_players=live_players_count,
                                                     x_limit=width,
                                                     y_limit=height)
        # ### TODO rewrite rules - control random food spawn
        # ### TODO some algo for GameObjects allocation on game field
        # player_types = [PlayerType.DEAD] * int(dead_coef * num_players) + [PlayerType.NEFOR] * 10 + [
        #     PlayerType.APPLE] * 4 + [PlayerType.PLAYER]
        # if len(player_types) > num_players:
        #     player_types = player_types[::-1][:num_players]
        # elif len(player_types) < num_players:
        #     player_types += [PlayerType.DEAD] * (
        #             num_players - len(player_types))

        world = [
            [
                Player(
                    scaler=settings.IMG_SCALE,
                    x=i,
                    y=j,
                    t=PlayerType.DEAD,
                    hp=-1000
                ) for i in range(width)
            ]
            for j in range(height)]

        for y, x in live_players_coords:
            player: Player = world[x][y]
            player.type = PlayerType.NEFOR
            player.sprite = SPRITES[PlayerType.NEFOR]
            player.hp = get_player_startup_hp()
        player_y, player_x = choice(list(live_players_coords))
        world[player_x][player_y].type = PlayerType.PLAYER
        world[player_x][player_y].sprite = SPRITES[PlayerType.PLAYER]
        print(live_players_coords)
        print(world)
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
                screen, settings.LINE_COLOR, (i * settings.IMG_SCALE, 0),
                (i * settings.IMG_SCALE, settings.WORLD_HEIGHT * settings.IMG_SCALE), 10)
        for j in range(settings.WORLD_WIDTH):
            pg.draw.line(
                screen, settings.LINE_COLOR, (0, j * settings.IMG_SCALE),
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
                continue
            if player.is_ill:
                player.steps_from_ill += 1
            if player.steps_from_ill == 10:
                player.is_ill = False

    def _fight(self, obj1: Player, obj2: Player):
        if obj1.is_ill and obj2.is_ill:
            obj1.dead()
            obj2.dead()
            return
        if obj1.is_ill:
            obj2.increase_hp(obj1.hp)
            obj1.dead()
            return
        if obj2.is_ill:
            obj1.increase_hp(obj2.hp)
            obj2.dead()
            return
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
        ### TODO move self_eat and self_fight
        if {obj1.type, obj2.type} == PlayerCollision.PLAYER_APPLE.value:
            self._eat(obj1, obj2)
        elif {obj1.type, obj2.type} == PlayerCollision.PLAYER_NEFOR.value:
            self._fight(obj1, obj2)

    def _random_event_step(self):
        ill_flag = need_ill()
        if ill_flag:
            players = []
            for row in OLD_WORLD.world:
                for player in row:
                    if player.is_alive():
                        players.append(player)
            sorry = choice(players)
            sorry.is_ill = True

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
        self._random_event_step()

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


OLD_WORLD: World = World(
    settings.WORLD_WIDTH, settings.WORLD_HEIGHT, settings.LIVE_COEF)

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
