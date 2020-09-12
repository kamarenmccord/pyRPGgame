
import pygame
from os import path
import os
import random
import math

from .settings import *

game_folder = path.join('./logics')
mob_dir = MOB_DIR
pipo_mobs = path.join(mob_dir, 'monster_pack')


class Mob(pygame.sprite.Sprite):
    def __init__(self, level, image, game, width=128, height=128, xp=10):
        self.level = level
        self.level_check()
        self.hardness = 10
        self.stats = self.get_stats(self.level)
        self.stats['max_hp'] = self.stats['hp']
        self.xp_value = xp * self.level
        self.groups = []
        self.groups.append(game.enemy_sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.battle_rewards = []  # fill with dict to hold items
        self.pos = 0, 0
        self.img = pygame.image.load(path.join(game_folder, f'{image}'))
        self.img = pygame.transform.scale(self.img, (width, height))
        self.rect = self.img.get_rect()
        self.health_rect = pygame.Rect((0, 0), (width, height))

    def is_alive(self):
        return self.stats['hp'] > 0

    def level_check(self):
        if self.level <= 0:
            self.level = 1
        if self.level > 100:
            self.level = 100

    def get_stats(self, level):
        # returns a dict of stats
        stats = {'hp': 5*level, 'attack': 1, 'defence': 1, 'speed': 1,
                 'sp_att': 1, 'sp_def': 1, 'accuracy': 90, 'mana': 1}
        for key, value in stats.items():
            if not key == 'hp' and not key == 'accuracy':
                ri = random.random()  # random integer
                stats[key] = round(random.randint(1, 5) * level + math.ceil(ri*self.hardness))
        stats['hp'] += round(stats['hp'] * 25/100 + level)
        return stats

    def set_health_bar_location(self):
        self.health_rect.x = self.pos[0]-10
        self.health_rect.y = self.pos[1]+64+10

    def draw_health(self, screen):
        self.set_health_bar_location()
        width = int(self.rect.width * self.stats['hp']/self.stats['max_hp'])
        depth = 4
        back_bar = pygame.Rect(self.pos[0], self.pos[1]+self.rect.height+13, width, depth)
        health_bar = pygame.Rect(self.pos[0]-5, self.pos[1]+self.rect.height+10, width, depth)
        pygame.draw.rect(screen, BLACK, back_bar)
        pygame.draw.rect(screen, RED, health_bar)

    def draw(self, screen):
        self.draw_health(screen)
        screen.blit(self.img, self.pos)


class pipo_BAT(Mob):
    def __init__(self, level, game):
        img = path.join(pipo_mobs, 'pipo-enemy001.png')
        super().__init__(level, img, game, xp=5)
        self.name = 'Cave Bat'


class pipo_SNAKE(Mob):
    def __init__(self, level, game):
        img = path.join(pipo_mobs, 'pipo-enemy003.png')
        super().__init__(level, img, game, xp=7)
        self.name = 'Grass Snake'


class pipo_CREEPER(Mob):
    def __init__(self, level, game):
        img = path.join(pipo_mobs, 'pipo-enemy011.png')
        super().__init__(level, img, game, xp=10)
        self.name = 'crEEper kId'


class pipo_SKELETON(Mob):
    def __init__(self, level, game):
        img = path.join(pipo_mobs, 'pipo-enemy039.png')
        super().__init__(level, img, game, xp=10)
        self.name = 'White Skeleton'
