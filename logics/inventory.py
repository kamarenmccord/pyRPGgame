
from .items import *
from .settings import *


class Inventory:
    # default class for the players inventory
    def __init__(self, game, cursor):
        self.game = game
        self.all_pockets = {
                            'misc': [],
                            'key_items': [],
                            'healing': [],
                            'weapons': []
                            }

        self.cursor = cursor
        self.index = 0

    def __str__(self):
        a_list = []
        for each, item in self.all_pockets.items():
            a_list.append((each, item))

        return f'{a_list}'

    def get_positions(self, subPocket):
        # subPocket is a keys value in the all_pockets
        positions = []
        for num, _ in enumerate(subPocket):
            positions.append(num)

        return positions

    def add(self, something):
        # add something to a given pocket
        for key in self.all_pockets.keys():
            if key == something.pouch:
                self.all_pockets[f'{key}'].append(something)

    def remove(self, something):
        # remove an item obj from a pouch
        for key, value in self.all_pockets.items():
            index = 0
            for listItem in value:
                if something.name == listItem.name:
                    del self.all_pockets[f'{key}'][index]
                    break  # prevents multiple of like items from being removed
                index += 1


    """ Functionality to backpack pages """
    def open(self):
        self.open = True
        while self.open:
            self.draw()
            self.events()

    def events(self):
        # check keys, move cursor or switch page
        # if esc back out of inventory
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.open = False

    def draw_backdrop(self):
        self.game.screen.fill(TAN)

    def draw(self):
        # main draw section
        self.draw_backdrop()

        # code here

        pygame.display.flip()
