import pygame

from .items import *
from .settings import *


class Inventory:
    # default class for the players inventory
    def __init__(self, game, cursor):
        self.game = game
        self.pocket_list = ['healing', 'key_items', 'weapons', 'misc']
        self.all_pockets = {
            'misc': [],
            'key_items': [],
            'healing': [],
            'weapons': []
        }
        self.positions = []  # contains indexes of x items
        self.screenName = 'healing'
        self.clock = self.game.clock
        self.cursor = cursor
        self.cursor.moveTo((WIDTH-250, 160))
        self.index = 0

        """ test lines """
        self.add(Potion())
        self.add(Potion())
        self.add(Elixr())

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

    """ Functionality to back pack pages """
    def open(self):
        self.is_open = True
        while self.is_open:
            self.event_keys = pygame.event.get()
            self.clock.tick(FPS)
            self.draw()
            self.events()

    def events(self):
        # check keys, move cursor or switch page
        # if esc back out of inventory
        for event in self.event_keys:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    self.is_open = False
                    print(self.is_open)
            if event.type == pygame.KEYUP:
                index = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    index = self.pocket_list.index(self.screenName)
                    index += 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    index = self.pocket_list.index(self.screenName)
                    index -= 1

                if index >= len(self.pocket_list):
                    index = 0
                if index < 0:
                    index = len(self.pocket_list)-1
                self.screenName = self.pocket_list[index]
                self.positions = range(len(self.pocket_list[index]))

    def draw_backdrop(self):
        self.game.screen.fill(TAN)
        pygame.draw.rect(self.game.screen, WHITE, (50, 50, WIDTH-100, HEIGHT-100))
        pygame.draw.rect(self.game.screen, TAN, (200, 200, WIDTH-400, HEIGHT-400), 100)

    def draw(self):
        # main draw section
        self.draw_backdrop()

        # code here
        # title
        self.game.draw_text(f'{self.screenName}', self.game.title_font, 32, BLACK, WIDTH/2, 100, align='center')
        if self.screenName == 'healing':
            y = 220
            for guy in self.game.party:
                self.game.draw_text(f'{guy.name} hp: {guy.stats["hp"]} / {guy.max_hp}',
                                    self.game.title_font, 24, BLACK, 200, 200)
                pygame.draw.rect(self.game.screen, DARKRED, (200, y, 300, 6))
                pygame.draw.rect(self.game.screen, RED, (200, y, 300*guy.stats['hp']/guy.max_hp, 6))
                self.game.draw_text(f'mana: {guy.stats["mana"]} / {guy.stats["max_mana"]}',
                                    self.game.title_font, 24, BLACK, 200, y+10)
                y += 30
                pygame.draw.rect(self.game.screen, DARKGREEN, (200, y, 300, 6))
                pygame.draw.rect(self.game.screen, GREEN, (200, y, 300*guy.stats['mana']/guy.stats['max_mana'], 6))
                y += 75
        # items
        index = 0
        y = 150
        keys = []
        for items in self.all_pockets[self.screenName]:
            pygame.draw.rect(self.game.screen, WHITE, (WIDTH-210, y-10, 100, 50))
            pygame.draw.rect(self.game.screen, BLACK, (WIDTH-210, y-10, 100, 50), 2)
            self.game.draw_text(f'{items.name}', self.game.title_font, 24, BLACK, WIDTH-200, y)
            keys.append((WIDTH-250, y+10))
            index += 1
            y += 60

        if self.all_pockets[self.screenName]:
            self.cursor.draw()
            option_index = self.cursor.check_keys(keys, self.event_keys, direction=['vertical'])
        if isinstance(option_index, int):
            if option_index >= 0:
                if self.screenName == 'healing':
                    for player in self.game.party:
                        player.stats['hp'] += self.all_pockets[self.screenName][option_index].amt
                        if player.stats['hp'] > player.max_hp:
                            player.stats['hp'] = player.max_hp
                    self.remove(self.all_pockets[self.screenName][option_index])
                    # set index to valid number move cursor there reset option index
        pygame.display.flip()
