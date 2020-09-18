import os
import pygame

from .settings import *

""" holds item classes for the game """

text_folder = os.path.join('logics/text')


class Book(pygame.sprite.Sprite):
    """ in game book """
    def __init__(self, x, y, img, text_file, game):
        self.pos = x, y
        self.interact_point = self.pos[0], self.pos[1]-TILESIZE
        self.image = pygame.image.load(os.path.join('logics', img))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game = game
        self.groups = [game.all_sprites]
        pygame.sprite.Sprite.__init__(self, self.groups)
        with open(os.path.join('logics', text_file), 'r') as tx:
            self.text = tx.readlines()  # list
        self.text = '\n'.join(self.text)
        self.text = self.text.strip


class Item:
    def __init__(self, img, pouch, name, description, value):
        self.image = pygame.image.load(os.path.join(ICONS_FOLDER, img))
        self.pouch = pouch  # key_items, weapons, healing, misc
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Potion(Item):
    def __init__(self):
        self.effects = 'hp'
        self.amt = 20
        pouch = 'healing'
        img = ICONS['potions'][0]
        name = 'potion'
        value = 5
        description = """ a questionable drink that builds constitution """
        super().__init__(img=img, pouch=pouch, name=name, description=description, value=value)


class FireBallScroll(Item):
    def __init__(self):
        pouch = 'misc'
        name = "Scroll of FireBall"
        value = 30
        desc = """ an old parchment with a glowing red symbol in the centre """
        super().__init__(pouch=pouch, name=name, description=desc, value=value)


class Elixr(Item):
    def __init__(self):
        self.effects = 'mana'
        self.amt = 50
        super().__init__(img=ICONS['potions'][1],
                         pouch='healing',
                         name='Elixr',
                         description='an old parchment with a yellow glow in the centre',
                         value=30)
