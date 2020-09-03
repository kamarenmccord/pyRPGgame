import pygame
from os import path
from random import randint, choice

from .settings import *

""" module represent the entire battle phase of in game battles """


class Battle:
    def __init__(self, party, battle_zone, is_boss=False):
        """
        @party: player may join battle with a party of up to 3
        @battle_zone: enemies are randomized within their respective zones(1-20)
        @is_boss: True if trigger for boss
        """
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
        # self.return_xp()
        # self.return_rewards()

    def draw(self):
        # draw all changes after updating
        self.screen.blit()

    def get_enemies(self):
        # check area for bad guys and what level to put them at
        # return list of up to 4 enemies
        enemy_population = []
        for e in range(randint(1, 4)):
            level = randint(self.battle_zone * 5 + randint(0, 5))
            bad_guy = Mob(level)
            enemy_population.append(bad_guy)
        return enemy_population
