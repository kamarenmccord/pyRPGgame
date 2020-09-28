from logics import *
from logics.settings import *
from logics.characters import *
# from logics.loader import *
from logics.tilemap import *
from logics.initalizer import *
import logics.crud_module as crud_mod
from logics.stats_screen import *

import sys
from os import path, listdir, chdir

import pygame


class Game:
    def __init__(self):
        """ if a vari is not set here check the
            initalizer file for more loads
        """
        self.title_font = path.join(game_folder, 'overpass-regular.otf')
        self.game_folder = path.join('./logics')

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.battle_sprites = pygame.sprite.Group()
        self.cursors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.battle_zone_group = pygame.sprite.Group()
        # debug varis
        self.draw_debug = True
        self.draw_walls = False

        # pygame block
        pygame.init()
        self.battle_cursor = Cursor(self, -90)
        self.battle_cursor.battleMode = True
        pygame.key.set_repeat(200, 100)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # global block
        self.scale = 1  # 0.5 to 2 where 2 == 128 and 0.5 = 16 pixel squares

        # drawing variables, global for async
        self.pause = False
        self.word_count = 0
        self.index = 0
        self.first_pass = True
        self.waiting_for_player = False
        self.text = ''
        self.talking = False
        self.pop_up = False
        self.menu = False
        self.menu_box = pygame.Rect(WIDTH-200, 100, 200, HEIGHT-100)

        self.party = []  # # where we will store the players, limit 3

    def spawn_player(self):
        """ spawn player at map point """
        print(self.map.player_spawnx, self.map.player_spawny)

        self.player = Player('Noah', self.map.player_spawnx, self.map.player_spawny, self)
        self.party.append(self.player.partyChar)

    def new(self, mapNum):
        load_level(self, mapNum)
        self.spawn_player()

    def verify_quit(self):
        x = WIDTH/2-200
        y = HEIGHT/2
        menu_pos = ((x+50, y+20), (x+250, y+20))
        self.menu_cursor.index = 0
        self.menu_cursor.moveTo(menu_pos[0])

        waiting = True
        while waiting:
            self.event_keys = pygame.event.get()
            self.clock.tick(30)
            pygame.draw.rect(self.screen, BLACK, (200, 200, 600, 400))
            pygame.draw.rect(self.screen, WHITE, (200, 200, 600, 400), 2)

            self.draw_text('are you sure you want to quit?', self.title_font,
                           36, WHITE, WIDTH/2, HEIGHT/2-100, align='center')
            self.draw_text('NO', self.title_font, 36, WHITE, x+100, y)
            self.draw_text('YES', self.title_font, 36, WHITE, x+300, y)

            self.menu_cursor.draw()
            option = self.menu_cursor.check_keys(menu_pos, self.event_keys, direction=['horizontal'])
            if option == 0:
                waiting = False
            if option == 1:
                self.quit()
            pygame.display.flip()

    @staticmethod
    def quit():
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        exit()

    def update(self):
        self.all_sprites.update()
        self.player.update()  # other function may be calling it on parent object
        self.camera.update(self.player)

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        # from kidsCanCode on youtube
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
            # displays fps at top of window
            draw_debug(self)
        self.screen.blit(self.map_img, self.camera.apply_box(self.map_rect))

        # draw.all_sprites
        if not self.draw_debug:
            for sprite in self.battle_zone_group:
                self.screen.blit(sprite.img, self.camera.apply(sprite))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # debug lines
        if self.draw_walls:
            for sprite in self.walls:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            self.screen.blit(self.player.buffer_box, self.camera.apply_box(self.player.buffer_rect))
        if not isinstance(self.player.area, (bool, str)):
            self.screen.blit(self.player.interact_img, self.camera.apply_box(self.player.interact_rect))

        if self.pop_up:
            if self.pause:
                self.pop_up_window()
                pygame.display.flip()
                if self.pause:
                    self.wait_for_key()  # wait for key
                    self.index += 1
        if self.menu:
            self.create_menu()
            pygame.display.flip()
        else:
            pygame.display.flip()

    def pop_up_window(self):
        """ create a window and fill with text if text is too much wrap and break into
            chunks wait until a key is pressed before continuing """
        # self.text = has the lines
        # self.index = what page of self.text
        # self.pop_up = False when no more text remains

        if isinstance(self.text, str):
            self.text = [self.text]
        try:
            text_on_this_page = self.text[self.index]
        except IndexError:
            self.pop_up = False
            self.index = 0
            self.pause = False
            self.text = ''
            self.word_count = 0
            return

        # break this index into sub_index for wrap effect
        wrapped_text = [[]]

        # word wrap
        count = 0
        for word in text_on_this_page.split(' '):
            if len(' '.join(wrapped_text[count])) + len(word) < 50:
                wrapped_text[count].append(word)
            else:
                wrapped_text.append([])
                count += 1
                wrapped_text[count].append(word)

        # print each sub_index out
        x = WIDTH * 25/100
        y = HEIGHT * 65/100
        pygame.draw.rect(self.screen, BLACK, (x-50, y-50, 600, 250))
        pygame.draw.rect(self.screen, WHITE, (x-50, y-50, 600, 250), 2)
        for list_slice in wrapped_text:
            self.draw_text(f'{" ".join(list_slice)}', self.title_font, 24, WHITE, x, y)
            y += 50

    def run(self):
        self.playing = True
        while self.playing:
            self.event_keys = pygame.event.get()
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
                # debug key prints a snapshot of game data
                if event.key == pygame.K_m:
                    self.draw_walls = not self.draw_walls
                    self.draw_debug = not self.draw_debug
                    draw_snapshot(self)
                if event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                    self.open_menu()

    def open_menu(self):
        self.pause = not self.pause
        self.menu = not self.menu
        self.menu_cursor = Cursor(self)
        self.menu_cursor.moveTo((WIDTH-250, 160))

    def create_menu(self):
        menu_text = ['inventory', 'stats', 'save', 'quit']
        menu_positions = []
        x = WIDTH-200
        y = 50
        pygame.draw.rect(self.screen, LIGHTGREY, (x-100, 100, 400, HEIGHT-300))
        pygame.draw.rect(self.screen, BLUE, (x-100, 100, 400, HEIGHT-300), 5)

        self.menu_cursor.draw()

        for option in menu_text:
            menu_positions.append((x-50, y+110))
            y += 100
            if not option == 'save':
                self.draw_text(f'{option}', self.title_font, 24, WHITE, x, y)
            if option == 'save':
                if self.player.area == 'save':
                    self.draw_text(f'{option}', self.title_font, 24, WHITE, x, y)
                else:
                    self.draw_text(f'{option}', self.title_font, 24, BLACK, x, y)
        option_index = self.menu_cursor.check_keys(menu_positions, self.event_keys, direction=['vertical'])
        if option_index or option_index == 0:
            # do stuff
            if option_index == 3:
                self.verify_quit()
                self.menu_cursor.moveTo(menu_positions[3])
            if option_index == 2:
                if self.player.area == 'save':
                    # do crud save
                    chdir('./logics')
                    save_status = crud_mod.save_game(self)
                    chdir('../')
                    self.setup_popup('saved')
                    if self.draw_debug:
                        print('save status: ', save_status)
                else:
                    self.setup_popup('you must be in a safe area to save')
            if option_index == 1:
                # show party and stats screen
                SS = Stat_Screen(Cursor(self), self, self.party)
                SS.open()
            if option_index == 0:
                # open the inventory
                self.player.inventory.open()

    def setup_popup(self, text):
        self.text = text
        self.pause = True
        self.pop_up = True

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
            self.draw_text(f'{GAME_TITLE}', self.title_font, font_size_lg, WHITE, WIDTH/2, HEIGHT/2-200, align='n')
            # draw text on screen
            if display_return:
                # choose new or continue cursor has 2 pos
                if pos == 0:
                    self.draw_text('CONTINUE', self.title_font, font_size_sm, WHITE, WIDTH / 2+50, HEIGHT / 2,
                                   align='center')
                    self.draw_text('New Game', self.title_font, font_size_sm, WHITE, WIDTH / 2, HEIGHT / 2 + 100,
                                   align='center')
                if pos == 1:
                    self.draw_text('New Game', self.title_font, font_size_sm, WHITE, WIDTH / 2+50, HEIGHT / 2 + 100,
                                   align='center')
                    self.draw_text('CONTINUE', self.title_font, font_size_sm, WHITE, WIDTH / 2, HEIGHT / 2, align='center')

            else:
                # the only option unless we add settings
                self.draw_text('New Game', self.title_font, font_size_sm, WHITE, WIDTH/2, HEIGHT/2, align='center')

            # draw cursor half of the time
            if count < 60:
                # this is where we draw the cursor
                title_cursor.draw()
            if count > 100:
                count = 0
            pygame.display.flip()
            # check for input and move cursor to left side of text
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    self.quit()
                    exit()
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
                        title_cursor.playSound(action='enter')
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


if USE_PREVIOUS_DATA:
    # get game data
    chdir('./logics')
    data = crud_mod.load_game()
    chdir('../')

    # call game.new(map) to get map
    # player is created with map
    g.new(data['gameData']['map'])

    # set up new player with old player data
    g.player.pos = data['playerData']['pos']
    g.player.stats = data['playerData']['stats']

    # create a party and populate with players that were in the party
    g.party = []
    for objData in data['partyData']:
        g.party.append(PartyChar(objData['name'], objData['imageFile'], g, id_num=objData['id'],
                                 max_hp=objData['max_hp'], stats=objData['stats']))

    # start and play game
    while True:
        # if new game
        g.run()
        g.show_game_over()
else:
    while True:
        # if new game
        mapNum = 2  # test line for start level
        g.new(mapNum)
        g.run()
        g.show_game_over()
