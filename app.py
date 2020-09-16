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
        self.title_font = path.join(game_folder, 'overpass-regular.otf')
        self.game_folder = path.join('./logics')
        self.all_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.battle_sprites = pygame.sprite.Group()
        self.cursors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.battle_zone_group = pygame.sprite.Group()
        self.draw_debug = True
        pygame.init()
        self.battle_cursor = Cursor(self, -90)
        self.battle_cursor.battleMode = True
        pygame.key.set_repeat(200, 100)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.pause = False
        self.index = 0  # for txt
        self.waiting_for_player = False
        self.text = ''
        self.talking = False
        self.pop_up = False
        self.menu = False
        self.menu_box = pygame.Rect(WIDTH-200, 100, 200, HEIGHT-100)

        self.party = []  # # where we will store the players, limit 3

    def spawn_player(self):
        """ spawn player at map point """
        self.player = Player('Noah', self.map.player_spawnx, self.map.player_spawny, self)
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

        if self.pop_up:
            self.pop_up_window()
            pygame.display.flip()
            if self.pause:
                self.wait_for_key()  # wait for key
        if self.menu:
            self.create_menu()
            pygame.display.flip()
        else:
            pygame.display.flip()

    def pop_up_window(self):
        """ create a window and fill with text if text is too much wrap and break into
            chunks wait until a key is pressed before continuing """
        # self.text = text
        # self.index = number represents splice of text
        # self.pop_up = False when no more text remains
        thisIndex = self.index
        if isinstance(self.text, list):
            text = ' '.join([str(item) for item in self.text])
        else:
            text = self.text
        text = text.split(' ')
        printString = ''
        stringList = []
        posY = 0  # refactor for multi lines
        for words in text[thisIndex:]:
            if len(printString)+len(words) < 65 and len(stringList) < 5:
                printString += words + ' '
                self.index += 1
                if len(printString) >= 55 and len(stringList) < 5:
                    stringList.append(printString)
                    printString = ''

        # draw box
        pygame.draw.rect(self.screen, BLACK, (150, HEIGHT-300, 750, 275))
        pygame.draw.rect(self.screen, WHITE, (150, HEIGHT - 300, 750, 275), 2)

        # draw text
        if stringList:
            for index, text in enumerate(stringList):
                self.draw_text(f'{stringList[index].strip()}', self.title_font, 24, WHITE, 175, HEIGHT-275+posY)
                posY += 65
        else:
            self.draw_text(f'{printString.strip()}', self.title_font, 24, WHITE, 175, HEIGHT-275+posY)

            if len(text[thisIndex:]) <= 0:
                self.pop_up = False
                self.text = ''
                self.index = 0

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
                # debug key prints a snapshot of game data
                if event.key == pygame.K_m:
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
        option_index = self.menu_cursor.check_keys(menu_positions)
        if option_index or option_index == 0:
            # do stuff
            if option_index == 3:
                self.quit()
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
                pass
            if option_index == 0:
                # open the inventory
                self.player.inventory.open()
            print(option_index)

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
