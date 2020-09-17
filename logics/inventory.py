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
        self.positions = []  # contains indexes
        self.top = (774, 160)
        self.bottom = (774, 640)
        self.screenName = 'healing'  # always opens to first page
        self.clock = self.game.clock
        self.cursor = cursor
        self.cursor.moveTo((WIDTH-250, 160))
        self.index = 0  # used for pagination
        self.offset = 0  # used for scroll
        self.holdOffset = False
        self.direction = False
        self.y = 150  # print point

        """ test lines """
        for x in range(20):
            self.add(Potion())
            self.add(Potion())
            self.add(Elixr())

    def __str__(self):
        a_list = []
        for each, item in self.all_pockets.items():
            a_list.append((each, item))

        return f'{a_list}'

    def scroll_top(self):
        self.index = 0
        self.offset = 0
        self.cursor.moveTo(self.top)

    def scroll_bottom(self):
        self.index = len(self.all_pockets[self.screenName])-1

    def get_positions(self, subPocket):
        # the subPocket is the list under a key
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
                    self.scroll_top()
                    index = self.pocket_list.index(self.screenName)
                    index += 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.scroll_top()
                    index = self.pocket_list.index(self.screenName)
                    index -= 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.direction = 'down'
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.direction = 'up'

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

        if self.holdOffset and self.cursor.index % 7 != 0:
            self.holdOffset = False

        if self.direction == 'down':
            if self.cursor.index > 0 and self.cursor.index % 7 == 0 and not self.holdOffset:
                self.offset -= 560
                self.cursor.moveTo(self.top)
                self.holdOffset = True

            if self.cursor.index == 0 and not self.holdOffset:
                self.scroll_top()

        if self.direction == 'up':
            if self.cursor.index > 0 and self.cursor.index % 7 == 6 and not self.holdOffset:
                self.offset += 560
                self.cursor.moveTo(self.bottom)
                self.holdOffset = True

            if self.cursor.index == len(self.all_pockets[self.screenName])-1 and not self.holdOffset:
                self.scroll_bottom()

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
        self.y += self.offset
        keys = []
        for items in self.all_pockets[self.screenName]:
            if 150 <= self.y <= 640:  # limiter not working
                pygame.draw.rect(self.game.screen, WHITE, (WIDTH-210, self.y-10, 100, 50))
                pygame.draw.rect(self.game.screen, BLACK, (WIDTH-210, self.y-10, 100, 50), 2)
                self.game.draw_text(f'{items.name}', self.game.title_font, 24, BLACK, WIDTH-200, self.y)
                keys.append((WIDTH-250, self.y+10))
            self.y += 80
        print(keys)
        option_index = None
        if self.all_pockets[self.screenName]:
            self.cursor.draw()
            option_index = self.cursor.check_keys(keys, self.event_keys, direction=['vertical'])
        if isinstance(option_index, int):
            if option_index >= 0:
                if self.screenName == 'healing':
                    for player in self.game.party:
                        thing = self.all_pockets[self.screenName][option_index]
                        player.stats[thing.effects] += thing.amt
                        if player.stats['hp'] > player.max_hp:
                            player.stats['hp'] = player.max_hp
                        if player.stats['mana'] > player.stats['max_mana']:
                            player.stats['mana'] = player.stats['max_mana']
                    self.remove(thing)
                    # set index to valid number move cursor there reset option index
                    if len(keys) > 0:
                        pos = option_index-1
                        if 0 > pos < len(keys):
                            pos = 0
                        self.cursor.moveTo(keys[pos])
        pygame.display.flip()
