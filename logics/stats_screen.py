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
        self.screen = game.screen
        self.cursor = cursor
        self.index = 0  # used for pagination

    def open(self):
        self.is_open = True
        while self.is_open:
            self.events = pygame.event.get()
            self.check_keys()
            self.draw()

    def draw_backdrop(self):
        self.game.screen.fill(LIGHTBLUE)
        pygame.draw.rect(self.game.screen, GREY, (100, 100, WIDTH-200, HEIGHT-200))

    def draw(self):
        self.draw_backdrop()

        box = 300
        rect = 500
        player = self.party[self.index]
        # sprite box
        pygame.draw.rect(self.game.screen, BLACK, (100, 100, box, box), 2)
        self.game.draw_text(f'{player.name}', self.game.title_font, 24, BLACK, 200, 120)
        self.screen.blit(player.large_image, (box/2+25, box/2+50, box, box))

        # page indicator
        x = 325
        y = 380
        if len(self.party) > 1:
            for num, member in enumerate(self.party):
                if self.index == num:
                    pygame.draw.circle(self.screen, DARKRED, (x, y), 10)
                else:
                    pygame.draw.circle(self.screen, DARKBROWN, (x, y), 10, 2)
                x += 25

        # bars
        pygame.draw.rect(self.game.screen, BLACK, (100, 400, rect, 250), 2)
        # hp
        self.game.draw_text(f'Hp: {player.stats["hp"]} / {player.max_hp}', self.game.title_font, 24, BLACK, 120, 445)
        pygame.draw.rect(self.screen, DARKRED, (120, 474, 400, 4))
        pygame.draw.rect(self.screen, RED, (120, 470, 400*player.stats['hp']/player.max_hp, 8))
        # mana
        self.game.draw_text(f'Mana: {player.stats["mana"]} / {player.stats["max_mana"]}', self.game.title_font,
                            24, BLACK, 120, 545)
        pygame.draw.rect(self.screen, DARKGREEN, (120, 574, 400, 4))
        pygame.draw.rect(self.screen, GREEN, (120, 570, 400*player.stats['mana']/player.stats['max_mana'], 8))

        # text information
        pygame.draw.rect(self.game.screen, BLACK, (600, 100, box, HEIGHT-200), 2)
        x = 650
        y = 180
        stats_to_show = ['attack', 'sp_att', 'defence', 'sp_def', 'xp_to_level']
        clean_labels = ['Attack', 'Sp attack', 'Defence', 'Sp Defence', 'next Level in']
        self.game.draw_text(f'Level : {player.stats["level"]}', self.game.title_font, 24, BLACK, x, 110)
        for num, stat in enumerate(stats_to_show):
            self.game.draw_text(f'{clean_labels[num]} : {player.stats[stat]}', self.game.title_font, 24, BLACK, x, y)
            y += 50
        self.game.draw_text(f'Steps: {self.game.player.stats["step_count"]}',
                            self.game.title_font, 24, BLACK, x, HEIGHT*80/100)

        pygame.display.flip()

    def check_keys(self):
        """ cycle though index of party """
        for event in self.events:
            if event.type == pygame.QUIT:
                self.game.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    self.is_open = False

                if len(self.party) > 1:
                    if event.key == pygame.K_RIGHT:
                        self.index += 1
                    if event.key == pygame.K_LEFT:
                        self.index -= 1
        if self.index > len(self.party)-1:
            self.index = 0
        if self.index < 0:
            self.index = len(self.party)-1
