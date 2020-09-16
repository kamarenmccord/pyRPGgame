import pygame
from .settings import *

""" 
    players stats screen 
    similar to inventory except shows players information
"""

class Stat_Screen:
    def __init__(self, cursor, game, party):
        self.party = party
        self.game = game
        self.cursor = cursor
        self.index = 0

    def open(self):
        self.is_open = True
        while self.is_open:
            self.events = pygame.event.get()
            self.check_keys()
            self.draw()

    def draw_backdrop(self):
        self.game.screen.fill(LIGHTBLUE)

    def draw(self):
        self.draw_backdrop()

        pygame.display.flip()

    def check_keys(self):
        """ cycle though index of party """

        for event in self.events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.is_open = False

        if len(self.party) == 0:
            return 0
        pass