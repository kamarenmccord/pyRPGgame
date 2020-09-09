from logics import *
from logics.settings import *
from logics.characters import *
# from logics.loader import *
from logics.tilemap import *
from logics.initalizer import *
import logics.crud_module as crud_mod

import sys
from os import path, listdir, chdir

import pygame


class Game:
    def __init__(self):
        """ if a vari is not set here check the
            initalizer file for more loads
        """
        self.game_folder = path.join('./logics')
        self.all_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.battle_sprites = pygame.sprite.Group()
        self.cursors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.battle_zone_group = pygame.sprite.Group()
        self.draw_debug = True
        self.grid = False
        pygame.init()
        self.battle_cursor = Cursor(self, -90)
        pygame.key.set_repeat(200, 100)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.pause = False

        self.party = []  # # where we will store the players, limit 3

    def spawn_player(self):
        """ spawn player at map point """
        self.player = Player('test player', self.map.player_spawnx, self.map.player_spawny, self)
        self.party.append(self.player.partyChar)

    def new(self, mapNum):
        load_level(self, mapNum)
        self.spawn_player()

    @staticmethod
    def quit():
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.player.update()  # other function may be calling it on parent objecet
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        # from kids can code
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        if self.draw_debug:
            # function at bottom of initalizer
            draw_debug(self)
        self.screen.blit(self.map_img, self.camera.apply_box(self.map_rect))

        # debug to show (grid locations
        if self.grid:
            self.draw_grid()

        # draw.all_sprites
        if not self.draw_debug:
            for sprite in self.battle_zone_group:
                self.screen.blit(sprite.img, self.camera.apply(sprite))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pygame.display.flip()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.pause:
                self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    self.quit()
                    exit()
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                # debug key prints a snapshot of game data
                if event.key == pygame.K_m:
                    self.grid = not self.grid
                    self.draw_debug = not self.draw_debug
                    draw_snapshot(self)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_0:
                    if not isinstance(self.player.zone, bool):
                        if [(self.player.zone[0], self.player.zone[1]) for y in self.map.saves[:][:2]]:
                            # do crud save
                            chdir('./logics')
                            save_status = crud_mod.save_game(self)
                            chdir('../')
                            print(save_status)

    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS / 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def shows_main_menu(self):
        """ player can select to continue, start new game, or check settings """
        title_font = path.join(game_folder, 'overpass-regular.otf')
        bg_img = pygame.image.load(path.join(game_folder, 'lights_bg.png'))
        font_size_lg = 105
        font_size_sm = 72
        title_cursor = Cursor(self)
        pos = 0
        choices = ['new game']
        positions = [(WIDTH/2-250, HEIGHT/2)]
        display_return = False
        # does user have loadable data?
        if path.exists(f'./logics/{DIRECTORY}'):
            for files in listdir(f'./logics/{DIRECTORY}'):
                if 'save_file+' in files:
                    positions = [(WIDTH/2-250, HEIGHT/2), (WIDTH/2-250, HEIGHT/2+100)]
                    choices.insert(0, 'continue')
                    title_cursor.pos = positions[0]
                    display_return = True
                    break

        title_cursor.moveTo(positions[0], playsnd=False)
        if display_return:
            title_cursor.moveTo((positions[pos][0]+50, positions[pos][1]), playsnd=False)

        menu_loop = True
        count = 0  # cursor blink effect
        self.clock.tick(FPS / 2)  # half fps on main menu
        while menu_loop:
            count += 1
            # draw background screen
            self.screen.blit(bg_img, (0, 20))
            self.draw_text(f'{GAME_TITLE}', title_font, font_size_lg, WHITE, WIDTH/2, HEIGHT/2-200, align='n')
            # draw text on screen
            if display_return:
                # choose new or continue cursor has 2 pos
                if pos == 0:
                    self.draw_text('CONTINUE', title_font, font_size_sm, WHITE, WIDTH / 2+50, HEIGHT / 2,
                                   align='center')
                    self.draw_text('New Game', title_font, font_size_sm, WHITE, WIDTH / 2, HEIGHT / 2 + 100,
                                   align='center')
                if pos == 1:
                    self.draw_text('New Game', title_font, font_size_sm, WHITE, WIDTH / 2+50, HEIGHT / 2 + 100,
                                   align='center')
                    self.draw_text('CONTINUE', title_font, font_size_sm, WHITE, WIDTH / 2, HEIGHT / 2, align='center')

            else:
                # the only option unless we add settings
                self.draw_text('New Game', title_font, font_size_sm, WHITE, WIDTH/2, HEIGHT/2, align='center')

            # draw cursor half of the time
            if count < 60:
                # this is where we draw the cursor
                title_cursor.draw()
            if count > 100:
                count = 0
            pygame.display.flip()
            # check for input and move cursor to left side of text
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        self.quit()
                        exit()
                    if event.key == pygame.K_RETURN:
                        # get pos of cursor and return its state
                        selection = choices[pos]
                        # returned value will be based off of this selection
                        menu_loop = False
                        break  # to prevent arrow key checking
                    if display_return:
                        if event.key == pygame.K_UP:
                            pos -= 1
                            if pos < 0:
                                pos = len(positions)-1
                        if event.key == pygame.K_DOWN:
                            pos += 1
                            if pos >= len(positions):
                                pos = 0
                        if event.key in [pygame.K_UP, pygame.K_DOWN]:
                            title_cursor.moveTo(positions[pos])
                            if display_return:
                                optional_pos = positions[pos][0]+50, positions[pos][1]
                                title_cursor.moveTo(optional_pos, playsnd=True)
                            count = 0

        # move cursor off screen and delete it
        title_cursor.playSound()
        del title_cursor

        # True to load a new game
        if selection == 'continue':
            return True
        # return false to start new game
        return False

    def show_game_over(self):
        # thanks for playing
        # credits and what not
        pass


g = Game()
USE_PREVIOUS_DATA = g.shows_main_menu()

mapNum = 1

if USE_PREVIOUS_DATA:
    # get game data
    chdir('./logics')
    data = crud_mod.load_game()
    chdir('../')
    # call game.new(map) to get map
    g.new(data['gameData']['map'])
    # player is created with map
    # move player to data location (where did they save?)
    g.player.pos = data['playerData']['pos']
    g.player.step_count = data['playerData']['steps']
    g.party = []
    for objData in data['partyData']:
        g.party.append(PartyChar(objData['name'], objData['imageFile'], g, objData['max_hp'], objData['stats']))
        g.party.append(PartyChar('Plyr2', objData['imageFile'], g))

    # start and play game
    while True:
        # if new game
        g.run()
        g.show_game_over()
else:
    while True:
        # if new game
        g.new(mapNum)
        g.run()
        g.show_game_over()
