import pygame
from os import path
import random
import math

from .settings import *
game_folder = path.join('./logics')

""" module represent the entire battle phase of in game battles """


class Mob(pygame.sprite.Sprite):
    def __init__(self, level, image, game):
        self.level = level
        self.level_check()
        self.hardness = 10
        self.stats = self.get_stats(level)
        self.groups = []
        self.groups.append(game.enemy_sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.pos = 0, 0
        self.img = pygame.image.load(path.join(game_folder, f'{image}'))
        self.rect = self.img.get_rect()

    def is_alive(self):
        return self.stats['hp'] > 0

    def level_check(self):
        if self.level <= 0:
            self.level = 1
        if self.level > 100:
            self.level = 100

    def get_stats(self, level):
        # returns a dict of stats
        stats = {'hp': 4 * level, 'attack': 1, 'defence': 1, 'speed': 1,
                 'sp_att': 1, 'sp_def': 1, 'accuracy': 90, 'mana': 1}
        for key, value in stats.items():
            if not stats[key] == 'hp' or stats[key] == 'accuracy':
                ri = random.random()  # random integer
                stats[key] = round(random.randint(1, 5) * level + ri*self.hardness)
        return stats


class Battle:
    def __init__(self, party, battle_zone, game, is_boss=False):
        """
        @party: player may join battle with a party of up to 3
        @battle_zone: enemies are randomized within their respective zones(1-20)
        @is_boss: True if trigger for boss
        """
        self.game = game
        self.party = party  # make sure to return this to game.party
        self.battle_zone = battle_zone
        self.is_boss = is_boss
        self.enemies = self.get_enemies(battle_zone, len(party))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.main()

    def attack(self):
        # player party gets to attack for each player (up to 3)
        pass

    def defend(self):
        # player takes hits from enemies
        pass

    def is_victorious(self):
        # check each enemy for death status
        escape = True  # only stays True if all enemies have died
        for bad_guy in self.enemies:
            if bad_guy.is_alive():
                escape = False
        return escape

    def main(self):
        # main loop of battle
        win = False
        while not win:
            self.attack()
            self.defend()
            win = self.is_victorious()
            if not [x.is_alive() for x in self.party]:
                pass  # gameover
            if [x.is_alive() for x in self.enemies]:
                win = False
            print('battled')
            break
        # self.return_xp()
        # self.return_rewards()

    def draw(self):
        # draw all changes after updating
        self.screen.blit()

    def get_enemies(self, areaLevel, partySize):
        # amount of enemies depends on partySize
        # strength of enemies depends on areaLevel
        # return list of up to 4 enemies
        enemy_population = []
        while len(enemy_population) == 0:
            pop_size = random.randint(2, math.ceil(partySize*1.5))
            for e in range(random.randint(1, pop_size)):
                level = areaLevel * 5 + random.randint(-5, 5) + random.randint(-ENEMYVARIANCE, ENEMYVARIANCE)
                enemy_population.append(Mob(level, 'shadow_d-kin.png', self.game))
        return enemy_population
