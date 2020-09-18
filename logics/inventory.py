import pygame

from .items import *
from .settings import *
import math


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

        # used for pagination
        self.offset = 0  # used for scroll
        self.scrollIndex = 0
        self.holdOffset = False
        self.current_pos = 0
        self.last_pos = 0
        self.jumpToEnd = False
        self.scroll_y = 0

        """ test lines """
        for x in range(9):
            self.add(Potion())
            self.add(Potion())
            self.add(Elixr())

    def __str__(self):
        a_list = []
        for each, item in self.all_pockets.items():
            a_list.append((each, item))

        return f'{a_list}'

    def scroll_top(self):
        self.cursor.index = 0
        self.current_pos = 0
        self.cursor.moveTo(self.top)

    def scroll_bottom(self, index_list):
        self.current_pos = len(index_list)-1
        self.current_pos = len(index_list)-1
        self.cursor.moveTo(self.bottom)

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
        self.current_pos = 0
        self.cursor.index = 0
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
                    self.current_pos += 1
                    self.scroll_y += 1
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.current_pos -= 1
                    self.scroll_y -= 1

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

        # menu title
        self.game.draw_text(f'{self.screenName}', self.game.title_font, 32, BLACK, WIDTH/2, 100, align='center')
        max_offset = ((math.floor(len(self.all_pockets[self.screenName])/7))*560)*-1
        max_offset += 560
        x = WIDTH - 300

        # draw page indicator
        for page in self.pocket_list:
            if page == self.screenName:
                pygame.draw.circle(self.game.screen, BLACK, (x, 75), 10)
            else:
                pygame.draw.circle(self.game.screen, BLACK, (x, 75), 10, 2)
            x += 25

        if len(self.all_pockets[self.screenName]) > 0:
            if max_offset % 7 == 0:
                max_offset -= 560
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

        # if there is something in inventory do actions
        if self.all_pockets[self.screenName]:
            # item printer
            y = 150 + self.offset
            loop_offset = 0
            keys = []
            scrollBarKeys = []
            thisIndex = 0
            for items in self.all_pockets[self.screenName]:
                if 150 <= y+loop_offset <= 640:
                    pygame.draw.rect(self.game.screen, WHITE, (WIDTH-210, y-10+loop_offset, 100, 50))
                    pygame.draw.rect(self.game.screen, BLACK, (WIDTH-210, y-10+loop_offset, 100, 50), 2)
                    self.game.draw_text(f'{items.name}', self.game.title_font, 24, BLACK, WIDTH-200, y+loop_offset)
                    keys.append((WIDTH-250, y+10+loop_offset))
                scrollBarKeys.append(thisIndex)
                thisIndex += 1
                loop_offset += 80

            pygame.draw.line(self.game.screen, BLACK, (WIDTH-25, 100), (WIDTH-25, HEIGHT-100), 5)
            pygame.draw.rect(self.game.screen, BLACK, (WIDTH-35, 100 + self.scroll_y/len(scrollBarKeys)*570, 20, 20), 4)

            if self.jumpToEnd:
                # has to be done AFTER keys refresh
                self.cursor.moveTo(keys[-1])
                self.current_pos = len(keys) - 1
                self.cursor.index = len(keys)-1
                self.offset += 560
                if self.offset > 150:
                    self.offset = max_offset
                    self.scroll_y = len(scrollBarKeys)
                self.jumpToEnd = False

            # scroller code
            if self.last_pos != self.current_pos:
                if self.last_pos < self.current_pos:
                    # moving down
                    if self.current_pos > len(keys)-1:
                        self.current_pos = 0
                        self.cursor.index = 0
                        self.offset -= 560
                        if self.offset < max_offset:
                            self.offset = 0
                            self.scroll_y = 0
                        # self.cursor.moveTo(self.top)

                if self.last_pos > self.current_pos:
                    # moving up
                    if self.current_pos <= -1:
                        self.jumpToEnd = True

            # get players input
            option_index = None

            self.cursor.draw()
            if self.last_pos == self.current_pos:
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
            self.last_pos = self.current_pos
        pygame.display.flip()
