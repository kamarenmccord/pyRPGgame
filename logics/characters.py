import pygame
from os import path
import random

vec = pygame.math.Vector2

from .settings import *
from .battle import *
from .inventory import Inventory

game_folder = path.dirname(__file__)


def collide_with_boundries(player, dx, dy):
    """boundaries set by map dimensions"""
    if player.pos[0] + dx <= CLIPPING_BUFFER or player.pos[0] + dx >= player.game.map.width-CLIPPING_BUFFER:
        return True
    elif player.pos[1] + dy <= CLIPPING_BUFFER or player.pos[1] + dy >= player.game.map.height-CLIPPING_BUFFER:
        return True


def collide_with_walls(obj, dx, dy):
    """object hits walls"""
    # this would be more effective via adding a col box around player
    for wall in obj.game.walls:
        if wall.x-CLIPPING_BUFFER <= obj.pos[0]+dx and obj.pos[0]+dx <= wall.width+CLIPPING_BUFFER:
            if wall.y-CLIPPING_BUFFER <= obj.pos[1]+dy and obj.pos[1]+dy <= wall.height+CLIPPING_BUFFER:
                return True
    return False


def collision_with_bz(plyr, battlezone):
    # returns battle if plyr steps on battle zone
    # battle zones are randomized tiles within "grass"
    if isinstance(plyr.zone, bool):
        for value in battlezone.values():
            for zone in value:
                if plyr.pos[0] >= zone.pos[0] and plyr.pos[0] + TILESIZE <= zone.width:
                    if plyr.pos[1] >= zone.pos[1] and plyr.pos[1] + TILESIZE <= zone.height:
                        plyr.zone = zone.pos[0], zone.pos[1], zone.width, zone.height
                        plyr.area = zone


def collision_with_zone(plyr, zone):
    if isinstance(plyr.zone, bool):
        for coords in zone:
            zone_width = coords[0] + coords[2]
            zone_height = coords[1] + coords[3]
            if plyr.pos[0] >= coords[0] and plyr.pos[0] + TILESIZE <= zone_width:
                if plyr.pos[1] >= coords[1] and plyr.pos[1] + TILESIZE <= zone_height:
                    plyr.zone = coords[0], coords[1], zone_width, zone_height

                    if coords[4] == 'save':
                        for guy in plyr.game.party:
                            print(f'{guy.name} healed')
                            guy.stats['hp'] = guy.max_hp

def player_exit_zone(plyr):
    # check to see if player exited last entered zone
    if not isinstance(plyr.zone, bool):
        if (plyr.pos[0] < plyr.zone[0] or plyr.pos[0] + TILESIZE > plyr.zone[2]
                or plyr.pos[1] < plyr.zone[1] or plyr.pos[1] + TILESIZE > plyr.zone[3]):
            plyr.zone = False
            if isinstance(plyr.area, DangerZone):
                plyr.area = False


class Character(pygame.sprite.Sprite):
    # blueprint for sprites
    def __init__(self, name, x, y, hp, game):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.game = game
        self.pos = vec(x, y)

    def is_alive(self):
        return self.hp > 0

    def init_groups(self, add_default=False):
        """add add_default=True to add to all sprites"""
        if add_default:
            self.groups.append(self.game.all_sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)


class Cursor(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = []
        self.groups.append(self.game.all_sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.pos = vec(0, 0)
        self.image = pygame.image.load(path.join(game.game_folder, 'cursor.png'))
        self.rect = self.image.get_rect()

        self.sfx = pygame.mixer.Sound(path.join(game_folder, 'Coins13.wav'))
        self.sfx.set_volume(0.4)
        self.battleMode = False

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def moveTo(self, pos, playsnd=True):
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

    def moveOff(self):
        self.moveTo((-500, -500), playsnd=False)

    def playSound(self):
        self.sfx.play()


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
        self.stats = {'level': 1, 'hp': 100, 'attack': 20, 'defence': 30, 'speed': 5,
                       'sp_att': 3, 'sp_def': 4, 'accuracy': 90, 'mana': 25,
                       'xp_to_level': 50, 'xp': 0, 'step_count': 0}
        self.max_hp = self.stats['hp']

        if stats:
            self.stats = stats
        if max_hp:
            self.max_hp = max_hp

    def __str__(self):
        return f'{self.name}'

    def is_alive(self):
        return self.stats['hp'] > 0

    def is_levelup(self):
        """ check to see if player has reached a level up """
        while self.stats['xp'] > self.stats['xp_to_level'] and self.stats['level'] < MAX_LEVEL:
            print(f'{self.name} has leveld up to: lvl {self.stats["level"]+1}!')
            self.stats['level'] += 1
            self.stats = self.statsIncrease()
            self.max_hp = self.stats['hp']

    def statsIncrease(self):
        """ method used via stats.setter to level up stats """
        """ return stats for the setter to update """
        self.stats['xp_to_level'] += 100
        return self.stats

    def next_level_in(self):
        # how much xp to level up
        return self.stats['xp_to_level'] - self.stats['xp']


class Player(Character):
    def __init__(self, name, x, y, game, hp=100):
        # the main char that moves about the screen
        super().__init__(name=name, x=x, y=y, hp=hp, game=game)
        self.groups = []
        self.init_groups(add_default=True)
        self.prev_pos = x, y
        self.pos = vec(x, y)
        self.image = pygame.image.load(path.join(game.game_folder, MAINCHARIMAGE))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.inventory = Inventory()
        self.max_level = 100
        self.step_count = 0

        self.zone = False  # true if player enters a zone, change to False if exit, for triggered events
        self.area = False
        self.grace_period = 0

        self.partyChar = PartyChar(self.name, MAINCHARIMAGE, game)

    def move(self, dx=0, dy=0):
        if not collide_with_boundries(self, dx, dy):
            if not collide_with_walls(self, dx, dy):
                self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move(dx=-PLAYERSPEED * self.game.dt)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move(dx=PLAYERSPEED * self.game.dt)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move(dy=-PLAYERSPEED * self.game.dt)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move(dy=PLAYERSPEED * self.game.dt)

    def check_steps(self):
        if (self.pos[0] >= self.prev_pos[0]+STEPSIZE or self.pos[0] <= self.prev_pos[0]-STEPSIZE
                or self.pos[1] >= self.prev_pos[1]+STEPSIZE or self.pos[1] <= self.prev_pos[1]-STEPSIZE):
            self.prev_pos = self.pos
            self.step_count += 1
            if self.grace_period > 0:
                self.grace_period -= 1

            if isinstance(self.area, DangerZone):
                battle_chance = 100 * random.random()
                if battle_chance > 85 and self.grace_period <= 0:
                    b = Battle(self.game.party, self.area.zone, self.game)
                    b.main()

                    # post battle effects
                    self.pos = self.prev_pos
                    self.grace_period = 3  # battle cooldown

    def update(self):
        collision_with_bz(self, self.game.map.danger_zone)
        collision_with_zone(self, self.game.map.saves)
        player_exit_zone(self)

        self.check_steps()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.rect.center = self.pos
        self.check_keys()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        self.pos = vec(x, y)
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = x+width
        self.height = y+height

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

