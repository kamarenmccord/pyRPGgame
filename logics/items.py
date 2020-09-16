import os
import pygame

""" holds item classes for the game """

game_folder = os.getcwd()

class Item:
    def __init__(self, img, pouch, name, description, value):
        self.image = pygame.image.load(os.path.join(game_folder, img))
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
        super().__init__(img=ICONS['potions'][1],
                         pouch='misc',
                         name='Elixr',
                         description='an old parchment with a yellow glow in the centre',
                         value=30)
