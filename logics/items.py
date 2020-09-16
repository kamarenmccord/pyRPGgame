
import pygame

""" holds item classes for the game """


class Item:
    def __init__(self, pouch, name, description, value):
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
        name = 'potion'
        value = 5
        description = """ a questionable drink that builds constitution """
        super().__init__(pouch=pouch, name=name, description=description, value=value)


class FireBallScroll(Item):
    def __init__(self):
        pouch = 'misc'
        name = "Scroll of FireBall"
        value = 30
        desc = """ an old parchment with a glowing red symbol in the centre """
        super().__init__(pouch=pouch, name=name, description=desc, value=value)


class Elixr(Item):
    def __init__(self):
        super().__init__(pouch='misc',
                         name='Elixr',
                         description='an old parchment with a yellow glow in the centre',
                         value=30)