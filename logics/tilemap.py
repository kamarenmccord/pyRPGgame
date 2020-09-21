
import pygame
from pytmx import *
from os import path

from .settings import *
from .characters import *


class TiledMap():
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)
        self.tm = load_pygame(filename, pixelalpha=True)
        self.width = self.tm.width * self.tm.tilewidth
        # self.width = self.tm.width * 64
        # self.height = self.tm.height * 64
        self.height = self.tm.height * self.tm.tileheight
        self.tmxdata = self.tm

    def render(self, surface):
        ti = self.tm.get_tile_image_by_gid
        for layer in self.tm.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (round(64*SCALE), round(64*SCALE)))
                        surface.blit(tile, (x*64*SCALE, y*64*SCALE))
                        # surface.blit(tile, (x*self.tm.tilewidth, y*self.tm.tileheight))


    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # move sprites to offest of camera(player usually)
        return entity.rect.move(self.camera.topleft)

    def apply_box(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        # update the position of the camera
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)

        # limit scrolling to borders of map
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        # set cameras new location
        self.camera = pygame.Rect(x, y, self.width, self.height)
