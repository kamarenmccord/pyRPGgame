from .characters import *
from .tilemap import *
from .items import *

import pygame

""" initalizes all of the other game data, if not under game.init check here """


def check_map_num(num):
    """ allows maps of different pixel sizes to be loaded """
    # pixel_scale = 32 base pixels times num
    # 128 = 32 * 4
    # 64 =  32 * 2
    if num in [1]:
        scale_map_to = 2
    if num in [2]:
        scale_map_to = 3
    return scale_map_to


def load_level(game, level):
    """@game: an instance of the pygame
        @level: numerical value of current map area"""
    # top level map data
    game.map_data = []
    game.scale = check_map_num(level)

    # map
    game.map = TiledMap(path.join(game.game_folder, f'level{level}.xml'), game)
    game.mapLevel = level

    map_zones = range(20)
    game.map.danger_zone = {}
    game.map.saves = []
    game.map.interact_points = []
    for zone in map_zones:
        game.map.danger_zone[f'zone_{zone+1}'] = []

    if game.map:
        game.map_img = game.map.make_map()
        game.map_rect = game.map_img.get_rect()
        for tile_objs in game.map.tmxdata.objects:
            if tile_objs.name == 'player':
                game.map.player_spawnx = tile_objs.x*game.scale
                game.map.player_spawny = tile_objs.y*game.scale
            for lvl in map_zones:
                if tile_objs.name == f'zone_{lvl+1}':
                    game.map.danger_zone[f'zone_{lvl+1}'].append(DangerZone(tile_objs.x * game.scale, tile_objs.y * game.scale, tile_objs.width * game.scale,
                                                                            tile_objs.height * game.scale, lvl+1))
            if tile_objs.name == 'save_spot':
                game.map.saves.append((tile_objs.x * game.scale, tile_objs.y * game.scale, tile_objs.width * game.scale, tile_objs.height * game.scale, 'save'))
            if tile_objs.name == 'wall':
                Wall(tile_objs.x * game.scale, tile_objs.y * game.scale, tile_objs.width * game.scale, tile_objs.height * game.scale, game)
            if tile_objs.name == 'trainer':
                NpcTrainer(tile_objs.x * game.scale, tile_objs.y * game.scale, game)
            if tile_objs.name == 'npc':
                if tile_objs.type == 'rando':
                    RandoNpc(tile_objs.x * game.scale, tile_objs.y * game.scale, game, tile_objs.img, interact=True, speech=[tile_objs.speech])
            if tile_objs.name == 'book':
                Book(tile_objs.x * game.scale, tile_objs.y * game.scale, tile_objs.img, tile_objs.contents, game)
        game.camera = Camera(game.map.width, game.map.height)


def draw_snapshot(game):
    if game.draw_debug:
        print('/'*50)
        print('// game shapshot: //')
        print('// im hiding in the initalizer //')
        if game.player:
            x = str(game.player.pos[0])[:5]
            y = str(game.player.pos[1])[:5]
            print(f'// player pos: {x, y} //')
            print(f'// player area: {game.player.area}')
        print('** current party: **')
        for persons in game.party:
            print(f'** plyr name: {persons.name} **')
        print('** end party ** ')
        if game.map:
            print(f'// map size(w,h): {game.map.width, game.map.height} //')
        print(f'// paused: {game.pause} //')
        print('/'*50)


def draw_debug(game):
    # remove on final release
    pygame.display.set_caption('{:.2f}'.format(game.clock.get_fps()))
    # game.draw_grid()
