import pygame as pg
import settings
from enums import PlayerType


def init_sprites():
    sprites = {}

    scaled_player_sprite = pg.transform.scale(
        pg.image.load("../img/player.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_player_sprite.fill(
        PlayerType.PLAYER.value, special_flags=pg.BLEND_MULT
    )

    scaled_nefor_sprite = pg.transform.scale(
        pg.image.load("../img/player.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_nefor_sprite.fill(
        PlayerType.NEFOR.value, special_flags=pg.BLEND_MULT
    )

    scaled_apple_sprite = pg.transform.scale(
        pg.image.load("../img/food.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_apple_sprite.fill(
        PlayerType.APPLE.value, special_flags=pg.BLEND_MULT)

    scaled_dead_sprite = pg.transform.scale(
        pg.image.load("../img/field.png"),
        (settings.IMG_SCALE, settings.IMG_SCALE)
    )
    scaled_dead_sprite.fill(
        PlayerType.DEAD.value, special_flags=pg.BLEND_MULT)

    illness_note_sprite = pg.transform.scale(
        pg.image.load("../img/illness_note.png"),
        (settings.IMG_SCALE // 4, settings.IMG_SCALE // 4)
    )

    sprites[PlayerType.APPLE] = scaled_apple_sprite
    sprites[PlayerType.DEAD] = scaled_dead_sprite
    sprites[PlayerType.PLAYER] = scaled_player_sprite
    sprites[PlayerType.NEFOR] = scaled_nefor_sprite
    sprites[PlayerType.FRIENDLY] = scaled_nefor_sprite
    sprites["illness"] = illness_note_sprite

    return sprites

SPRITES = init_sprites()