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

    def attack(self):
        # player party gets to attack for each player (up to 3)
        # get keys, use cursor to pick options
        # when entered on option do actions

        # temp code to do damage to other party
        for player in self.party:
            random_enemy = -1
            # keep consistant for max survival
            if not self.enemies[random_enemy].is_alive():
                while not self.enemies[random_enemy].is_alive():
                    random_enemy -= 1
            self.enemies[random_enemy].stats['hp'] -= player.stats['attack']

            print(f'{player.name} does {player.stats["attack"]} damage to moblin.')
            if not self.enemies[random_enemy].is_alive():
                print('enemy died')

    def defend(self):
        # enemies auto attack player takes damages
        # player takes hits from enemies
        for enemy in self.enemies:
            random_player = random.randint(1, len(self.party))-1
            if not self.party[random_player].is_alive():
                while not self.party[random_player].is_alive():
                    random_player = random.randint(1, len(self.party))
            self.party[random_player].stats['hp'] -= enemy.stats['attack']

            print(f'moblin does {enemy.stats["attack"]} damage to {self.party[random_player]}.')
            if not self.party[random_player].is_alive():
                print(f'{self.party[random_player].name} died')
            else:
                print(f'{self.party[random_player].name} has {self.party[random_player].stats["hp"]} hp remaining.')

    def is_victorious(self, party):
        # check each player for death status
        escape = True  # only stays True if all players have died
        for player in party:
            if player.is_alive():
                escape = False
        return escape

    def main(self):
        # main loop of battle
        round_count = 0
        print(f'there are {len(self.enemies)}')
        while True:
            print('attack')
            # attack iterations
            self.attack()
            if self.is_victorious(self.enemies):
                print('victory')
                break

            print('defend')
            # defend iterations
            self.defend()
            if self.is_victorious(self.party):
                print('GAME OVER')
                pygame.display.quit()
                pygame.quit()
            round_count += 1
            print(f'round count: {round_count}')
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
