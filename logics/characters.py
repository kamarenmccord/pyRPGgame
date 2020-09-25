import pygame
from os import path
import random

from .settings import *
from .items import *
from .battle import *
from .inventory import Inventory
from .quests import *

vec = pygame.math.Vector2

game_folder = path.dirname(__file__)


def collide_with_boundries(player, dx, dy):
    """boundaries set by map dimensions"""
    if player.pos[0] + dx <= CLIPPING_BUFFER or player.pos[0] + dx >= player.game.map.width - 30:
        return True
    elif player.pos[1] + dy <= CLIPPING_BUFFER or player.pos[1] + dy >= player.game.map.height - 30:
        return True


def collide_with_walls(obj, dx, dy):
    """object hits walls"""
    # this would be more effective via adding a col box around player
    tl = obj.buffer_rect.topleft
    for wall in obj.game.walls:
        wl = wall.rect.topleft
        if (tl[0] + dx < wl[0] + wall.rect.width + CLIPPING_BUFFER and
                tl[0] + obj.buffer_rect.width + dx - CLIPPING_BUFFER > wl[0]):
            if (tl[1] + dy < wl[1] + wall.rect.height + CLIPPING_BUFFER and
                    tl[1] + obj.buffer_rect.height + dy - CLIPPING_BUFFER > wl[1]):
                return True
    return False


def collision_with_bz(plyr, battlezone):
    # returns battle if plyr steps on battle zone
    # battle zones are randomized tiles within "grass"
    # zone is a dict
    if isinstance(plyr.zone, bool):
        for value in battlezone.values():
            for zone in value:
                if plyr.pos[0] >= zone.pos[0] and plyr.pos[0] + TILESIZE <= zone.width:
                    if plyr.pos[1] >= zone.pos[1] and plyr.pos[1] + TILESIZE <= zone.height:
                        plyr.zone = zone.pos[0], zone.pos[1], zone.width, zone.height
                        plyr.area = zone


def collision_with_zone(plyr, zone):
    # zone is a list
    if isinstance(plyr.zone, bool):
        try:
            for coords in zone:
                zone_width = coords[0] + coords[2]
                zone_height = coords[1] + coords[3]
                if plyr.pos[0] >= coords[0] and plyr.pos[0] + TILESIZE <= zone_width:
                    if plyr.pos[1] >= coords[1] and plyr.pos[1] + TILESIZE <= zone_height:

                        if coords[4] == 'save':
                            plyr.zone = coords[0], coords[1], coords[2], coords[3]
                            plyr.area = 'save'
                            for guy in plyr.game.party:
                                guy.stats['hp'] = guy.max_hp
        except TypeError:
            tl = plyr.rect.topleft
            for coords in zone:
                for num, coord in enumerate(coords):
                    if num % 4 != 0 and num != 0:
                        zone_width = coord[0] + coord[2]
                        zone_height = coord[1] + coord[3]
                        if tl[0] < zone_width and tl[0] + plyr.rect.width > coord[0]:
                            if tl[1] < zone_height and tl[1] + plyr.rect.height > coord[1]:
                                if isinstance(coords[-1], (Npc, Book)):
                                    plyr.area = coords[-1]  # npc obj
                                    plyr.zone = coord[:4]  # coords


def player_exit_zone(plyr):
    # check to see if player exited last entered zone
    tl = plyr.buffer_rect.topleft
    br = plyr.buffer_rect
    if not (plyr.zone[0]+plyr.zone[2] > tl[0] and tl[0]+br.width > plyr.zone[0]
            and plyr.zone[1]+plyr.zone[3] > tl[1] and tl[1]+br.height > plyr.zone[1]):
        plyr.zone = False
        plyr.area = False


class Cursor(pygame.sprite.Sprite):
    def __init__(self, game, angle=0):
        self.game = game
        self.groups = []
        self.groups.append(self.game.cursors)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.pos = vec(0, 0)
        self.index = 0
        self.lastIndex = 0
        self.timeout = 0
        self.image = pygame.image.load(path.join(game.game_folder, 'cursor.png'))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()

        self.sfx = pygame.mixer.Sound(path.join(game_folder, 'back_style_2_001.ogg'))
        self.sfx.set_volume(0.4)
        self.sfx_enter = pygame.mixer.Sound(path.join(game_folder, 'confirm_style_3_005.ogg'))
        self.sfx_enter.set_volume(0.4)
        self.sfx_battle_enter = pygame.mixer.Sound(path.join(game_folder, 'confirm_style_3_002.ogg'))
        self.sfx_battle_enter.set_volume(0.3)
        self.battleMode = False

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def moveTo(self, pos, playsnd=False):
        """ move cursor to a location on screen, playsnd=false for no sound fx """
        # get pygame keys and move cursor if movement comes in
        self.pos = pos[0], pos[1]
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.center = pos
        # play sound
        if not self.battleMode:
            if playsnd:
                self.sfx.play()

    def playSound(self, action='none'):
        if action == 'none':
            self.sfx.play()
        if action == 'enter':
            self.sfx_enter.play()
        if action == 'action':
            self.sfx_battle_enter.play()

    def check_keys(self, positions, events, direction=('vertical', 'horizontal')):
        """ direction to check """
        if self.timeout > 0:
            self.timeout -= 1
        if self.timeout <= 0:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if 'vertical' in direction:
                        if event.key == pygame.K_UP:
                            self.index -= 1
                        if event.key == pygame.K_DOWN:
                            self.index += 1
                    if 'horizontal' in direction:
                        if event.key == pygame.K_RIGHT:
                            self.index += 1
                        if event.key == pygame.K_LEFT:
                            self.index -= 1

                if self.index >= len(positions):
                    self.index = 0
                if self.index < 0:
                    self.index = len(positions) - 1
                if not self.index == self.lastIndex:
                    self.moveTo(positions[self.index], playsnd=True)
                    self.lastIndex = self.index
                    self.timeout = 3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        return self.index


class PartyChar(pygame.sprite.Sprite):
    # the char that is in party
    def __init__(self, name, image, game, max_hp=False, stats=False):
        self.name = name
        self.groups = []
        self.game = game
        self.groups.append(self.game.battle_sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.pos = 0, 0
        self.imageFile = image
        self.image = pygame.image.load(path.join(game.game_folder, f'{image}'))
        self.large_image = pygame.transform.scale(self.image, (128, 128))
        self.stats = {'level': 1, 'hp': 175, 'attack': 20, 'defence': 30, 'speed': 5,
                      'sp_att': 3, 'sp_def': 4, 'accuracy': 90, 'mana': 25, 'max_mana': 25,
                      'xp_to_level': 50, 'xp': 0}
        self.max_hp = self.stats['hp']
        self.active = False

        if stats:
            self.stats = stats
        if max_hp:
            self.max_hp = max_hp

    def __str__(self):
        return f'{self.name}'

    def is_alive(self):
        return self.stats['hp'] > 0

    def is_levelup(self, number_of_gained):
        """ check to see if player has reached a level up """
        self.stats['xp'] += number_of_gained
        if self.stats['xp'] > self.stats['xp_to_level'] and self.stats['level'] < MAX_LEVEL:
            print(f'{self.name} has reached lvl {self.stats["level"] + 1}!')
            self.stats['level'] += 1
            self.stats = self.statsIncrease()
            return True
        return False

    def statsIncrease(self):
        """ method used to level up players stats """
        self.stats['xp_to_level'] += math.ceil(math.log(self.stats['xp_to_level'], 2) + self.stats['xp_to_level'] / 2)
        for key in self.stats.keys():
            if key not in ['hp', 'level', 'accuracy', 'xp', 'xp_to_level', 'max_mana', 'mana']:
                self.stats[f'{key}'] += random.randint(2, 7)
        gain = round(self.max_hp * 25 / 100 + self.stats['level'])
        self.stats['mana'] += gain
        self.stats['max_mana'] += gain
        self.max_hp += gain
        self.stats['hp'] += gain

        return self.stats

    def next_level_in(self):
        # how much xp to level up
        return self.stats['xp_to_level'] - self.stats['xp']


class NpcTrainer(pygame.sprite.Sprite):
    """ special npc that helps player though game / gives advice """

    def __init__(self, x, y, game):
        self.pos = x + 16, y + 16
        self.game = game
        self.image = pygame.image.load(path.join(game.game_folder, 'npcTrainer.png'))
        self.image = pygame.transform.scale(self.image, (48, 81))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.groups = [self.game.all_sprites]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # wall around npc to prevent walk through
        Wall(self.pos[0] - 16, self.pos[1] - 16, 32, 32, game)


class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y, game, img, interact=False, speech=False):
        self.pos = x + 16, y + 16
        self.game = game
        self.image = pygame.image.load(path.join(game.game_folder, img))
        self.image = pygame.transform.scale(self.image, (48, 81))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.interact = interact
        if interact:
            self.interact_points = self.make_interact_points(interact=interact)
            self.game.map.interact_points.append(self.interact_points)
        self.groups = [self.game.all_sprites]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.speech = speech
        self.index = 0  # indexes speech
        self.img = pygame.Surface((64, 64))
        self.img_rect = self.img.get_rect()

        Wall(self.pos[0] - 16, self.pos[1] - 16, 32, 32, game)

    def draw(self):
        for pos in self.interact_points[:4]:
            self.img_rect.topleft = pos[0], pos[1]
            self.game.screen.blit(self.img, self.game.camera.apply_box(self.img_rect))

    def make_interact_points(self, interact):
        # make a rect at the n e s w points of npc
        # used to interact with player
        # not all npcs should have interact points
        """ return list of 4 points for player detection """
        if interact:
            rect = self.rect.topleft
            points = ((rect[0] + 64, rect[1], TILESIZE * 2, TILESIZE * 2),
                      (rect[0] - 64, rect[1], TILESIZE * 2, TILESIZE * 2),
                      (rect[0], rect[1] + 64, TILESIZE * 2, TILESIZE * 2),
                      (rect[0], rect[1] - 64, TILESIZE * 2, TILESIZE * 2),
                      self)
            return points
        return False

    def talk(self):
        if self.speech:
            return self.speech[0]
        return False


class RandoNpc(Npc):
    """ returns random speaches """

    def __init__(self, x, y, game, img, interact=False, speech=False):
        super().__init__(x=x, y=y, game=game, img=img, interact=interact, speech=speech)

    def talk(self):
        if self.speech:
            rando_speech = random.randint(0, len(self.speech) - 1)
            return self.speech[rando_speech]
        return False


class QuestNpc(Npc):
    """ gives/ progresses quest """

    def __init__(self, x, y, game, img, quest_object, interact=False, speech=False):
        self.quest = quest_object()  # this is sudo code
        self.index = 0  # tracks quest progression
        super().__init__(x, y, game, img, interact=interact, speech=speech)

    def set_quest(self, player):
        """ adds quest to player """
        player.quests += self.quest


class Player(pygame.sprite.Sprite):
    def __init__(self, name, x, y, game):
        # the char that moves about the screen
        self.name = name
        self.groups = []
        self.game = game
        self.groups.append(self.game.all_sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.prev_pos = x, y
        self.pos = vec(x, y)
        self.images = self.load_images()
        self.image = self.images[0]
        self.interact_img = pygame.image.load(path.join(self.game.game_folder, 'interact_img.png'))
        self.interact_img = pygame.transform.scale(self.interact_img, (32, 64))
        self.interact_rect = self.interact_img.get_rect()
        self.interact_rect.center = self.pos[0], self.pos[1] - 64
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # temp code
        self.buffer_box = pygame.Surface((TILESIZE, TILESIZE))
        self.buffer_box.fill(RED)
        self.buffer_rect = self.buffer_box.get_rect()
        self.buffer_rect.center = self.pos

        self.inventory = Inventory(self.game, Cursor(game))
        self.stats = {'step_count': 0, 'currency': 50}

        # detection
        self.zone = False  # true if player enters a zone, change to False if exit, for triggered events
        self.area = False
        self.grace_period = 0

        # sprite animations
        self.direction = 'down'
        self.next_step = 0
        self.frame = 0

        # add default player to the battle party
        self.partyChar = PartyChar(self.name, 'main_char/player_down2.png', game)

    def load_images(self):
        images = []
        width, height = 64, 64
        for img in MAINCHARIMAGES:
            loaded_img = pygame.image.load(path.join(self.game.game_folder, f'main_char/{img}'))
            loaded_img = pygame.transform.scale(loaded_img, (width, height))
            images.append(loaded_img)
        return images

    def move(self, dx=0, dy=0):
        if self.stats['step_count'] >= self.next_step:
            self.frame = (self.frame + 1) % 3
        self.next_step = self.stats['step_count'] + 1
        if not collide_with_boundries(self, dx, dy):
            if not collide_with_walls(self, dx, dy):
                # get direction, set sprite
                if dx > 0:
                    self.direction = 'right'
                    self.image = self.images[self.frame + 3 * 3]
                elif dx < 0:
                    self.direction = 'left'
                    self.image = self.images[self.frame + 1 * 3]
                elif dy > 0:
                    self.direction = 'down'
                    self.image = self.images[self.frame + 0 * 3]
                elif dy < 0:
                    self.direction = 'up'
                    self.image = self.images[self.frame + 2 * 3]

                self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def check_keys(self):
        keys = pygame.key.get_pressed()

        if not self.game.pause:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.move(dx=-PLAYERSPEED * self.game.dt)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.move(dx=PLAYERSPEED * self.game.dt)
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.move(dy=-PLAYERSPEED * self.game.dt)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.move(dy=PLAYERSPEED * self.game.dt)
            else:
                if self.direction == 'right':
                    self.image = self.images[10]
                if self.direction == 'left':
                    self.image = self.images[4]
                if self.direction == 'up':
                    self.image = self.images[7]
                if self.direction == 'down':
                    self.image = self.images[1]

            if keys[pygame.K_RETURN]:
                if isinstance(self.area, Npc):
                    if self.area.interact:
                        self.game.setup_popup(self.area.talk())

                if isinstance(self.area, Book):
                    self.game.setup_popup(self.area.read())

    def check_steps(self):
        # check for changes
        if not isinstance(self.area, bool):
            player_exit_zone(self)
        if isinstance(self.area, bool):
            # give priority to other areas
            collision_with_zone(self, self.game.map.saves)
            collision_with_zone(self, self.game.map.interact_points)
            collision_with_bz(self, self.game.map.danger_zone)

        # step counter for player
        if (self.pos[0] >= self.prev_pos[0] + STEPSIZE or self.pos[0] <= self.prev_pos[0] - STEPSIZE
                or self.pos[1] >= self.prev_pos[1] + STEPSIZE or self.pos[1] <= self.prev_pos[1] - STEPSIZE):
            self.prev_pos = self.pos
            self.stats['step_count'] += 1
            # battle cooldown
            if self.grace_period > 0:
                self.grace_period -= 1

            # check if battle occurs
            if isinstance(self.area, DangerZone):
                battle_chance = 100 * random.random()
                if battle_chance > 85 and self.grace_period <= 0:
                    b = Battle(self.game.party, self.area.zone, self.game)
                    b.main()

                    # add cooldown
                    self.pos = self.prev_pos
                    self.grace_period = random.randint(0, 3)

    def update(self):
        if not isinstance(self.area, (bool, str, DangerZone)):
            self.interact_rect.center = self.pos[0], self.pos[1] - 64
        self.buffer_rect.center = self.pos[0], self.pos[1] + 16
        self.rect.center = self.pos
        self.check_keys()
        self.check_steps()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        self.pos = vec(x, y)
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        shrink_size = 5
        self.image = pygame.Surface((round(self.width) - shrink_size, round(self.height) - shrink_size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def __str__(self):
        return f'{self.x}, {self.y}, {self.width}, {self.height}'


class DangerZone(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, zoneLevel):
        self.pos = x, y
        self.width = x + width
        self.height = y + height
        self.zone = zoneLevel

    def __str__(self):
        # for debugging
        return f'x:{self.pos[0]} y:{self.pos[1]}, width: {self.width} height:{self.height}, danger: {self.zone}'
