import pygame
from os import path
import random
import math
import time

from .settings import *
game_folder = path.join('./logics')

""" module represent the entire battle phase of in game battles """


class Mob(pygame.sprite.Sprite):
    def __init__(self, level, image, game, xp=10):
        self.level = level
        self.level_check()
        self.hardness = 10
        self.stats = self.get_stats(self.level)
        self.stats['max_hp'] = self.stats['hp']
        self.xp_value = xp * self.level
        self.groups = []
        self.groups.append(game.enemy_sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.battle_rewards = []  # fill with dict to hold items
        self.pos = 0, 0
        self.img = pygame.image.load(path.join(game_folder, f'{image}'))
        self.img = pygame.transform.scale(self.img, (64, 64))
        self.rect = self.img.get_rect()
        self.health_rect = pygame.Rect((0, 0), (64, 64))

        self.dt = game.clock.tick(FPS) / 1000

    def is_alive(self):
        return self.stats['hp'] > 0

    def level_check(self):
        if self.level <= 0:
            self.level = 1
        if self.level > 100:
            self.level = 100

    def get_stats(self, level):
        # returns a dict of stats
        stats = {'hp': 5*level, 'attack': 1, 'defence': 1, 'speed': 1,
                 'sp_att': 1, 'sp_def': 1, 'accuracy': 90, 'mana': 1}
        for key, value in stats.items():
            if not key == 'hp' and not key == 'accuracy':
                ri = random.random()  # random integer
                stats[key] = round(random.randint(1, 5) * level + math.ceil(ri*self.hardness))
        stats['hp'] += round(stats['hp'] * 25/100 + level)
        return stats

    def set_health_bar_location(self):
        self.health_rect.x = self.pos[0]-10
        self.health_rect.y = self.pos[1]+64+10

    def draw_health(self, screen):
        self.set_health_bar_location()
        width = int(self.rect.width * self.stats['hp']/self.stats['max_hp'])
        depth = 4
        back_bar = pygame.Rect(self.pos[0], self.pos[1]+self.rect.height+13, self.rect.width, depth)
        health_bar = pygame.Rect(self.pos[0]-5, self.pos[1]+self.rect.height+10, width, depth)
        pygame.draw.rect(screen, BLACK, back_bar)
        pygame.draw.rect(screen, RED, health_bar)

    def draw(self, screen):
        self.draw_health(screen)
        screen.blit(self.img, self.pos)


class Battle:
    def __init__(self, party, battle_zone, game, is_boss=False):
        """
        @party: player may join battle with a party of up to 3
        @battle_zone: enemies are randomized within their respective zones(1-20)
        @is_boss: True if trigger for boss
        """
        self.game = game
        self.party = party  # make sure to return this to game.party
        self.battle_zone = battle_zone
        self.is_boss = is_boss
        self.enemies = self.get_enemies(battle_zone, len(party))
        self.set_positions()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = self.game.screen
        self.backdrop = pygame.image.load(BACKDROP_BLUE)

        self.battle_rewards = []
        self.battle_xp = 0
        self.battle_font = path.join(game_folder, FONTSBATTLE)
        self.battle_font_size = 32
        self.attack_positions = [(WIDTH * 15 / 100, HEIGHT - 50), (WIDTH * 35 / 100, HEIGHT - 50),
                                 (WIDTH * 60 / 100, HEIGHT - 50), (WIDTH * 85 / 100, HEIGHT - 50)]
        if self.is_boss:
            self.attack_positions.pop()

    def attack(self, attack_num):
        # player party gets to attack for each player (up to 3)
        # get keys, use cursor to pick options
        # when entered on option do actions

        # do damage to other party
        for player in self.party:
            if player.is_alive():
                hit_miss = random.random() * 100
                if hit_miss < player.stats['accuracy']:
                    last_enemy = -1
                    if not self.enemies[last_enemy].is_alive():
                        while not self.enemies[last_enemy].is_alive():
                            last_enemy -= 1

                    if attack_num < 2:
                        if attack_num == 0:
                            damage_delt = player.stats['attack']
                            self.enemies[last_enemy].stats['hp'] -= damage_delt

                        if attack_num == 1:
                            if player.stats['mana'] > 5:
                                damage_delt = player.stats['sp_att']
                                self.enemies[last_enemy].stats['hp'] -= damage_delt
                                player.stats['mana'] -= 5

                        print(f'{player.name} does {damage_delt} damage to moblin.')
                        if not self.enemies[last_enemy].is_alive():
                            print('enemy died')

                    if attack_num == 2:
                        pass  # items

                    if attack_num == 3:
                        escape_chance = random.random() * 100 - self.enemies[last_enemy].stats['speed']
                        if escape_chance > 35:
                            return 'escape'
                        else:
                            print('failed to escape')
                else:
                    print(f'{player.name} missed')

    def get_player_choice(self, mem_pos):
        """ return the players selection """
        # [attack, magic, items, run]
        pos = mem_pos
        # temp to give player one option
        battle_loop = True
        battle_cursor = self.game.battle_cursor

        battle_cursor.moveTo((self.attack_positions[pos][0], self.attack_positions[pos][1]-75), playsnd=False)

        # get keys
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # get pos of cursor and return its state
                    battle_loop = False
                    return [pos, pos]

                if event.key == pygame.K_LEFT:
                    pos -= 1
                    if pos < 0:
                        pos = len(self.attack_positions) - 1
                if event.key == pygame.K_RIGHT:
                    pos += 1
                    if pos >= len(self.attack_positions):
                        pos = 0
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    battle_cursor.moveTo((self.attack_positions[pos][0], self.attack_positions[pos][1]-75), playsnd=False)

        # return selected option
        return [-1, pos]

    def defend(self):
        # enemies auto attack random player
        for enemy in self.enemies:
            if enemy.is_alive():
                hit_miss = random.random() * 100
                if hit_miss < enemy.stats['accuracy']:
                    random_player = random.randint(1, len(self.party))-1
                    if not self.party[random_player].is_alive() and len(self.party) > 1:
                        while not self.party[random_player].is_alive():
                            random_player = random.randint(1, len(self.party))
                    self.party[random_player].stats['hp'] -= enemy.stats['attack']

                    """ print statements for debugging"""
                    print(f'moblin does {enemy.stats["attack"]} damage to {self.party[random_player]}.')
                    if not self.party[random_player].is_alive():
                        print(f'{self.party[random_player].name} died')
                    else:
                        print(f'{self.party[random_player].name} has '
                              f'{self.party[random_player].stats["hp"]} hp remaining.')
                else:
                    print('moblin missed')

    def has_fainted(self, party):
        """ does @party have anyone alive? """
        escape = True  # only stays True if all players have died
        for player in party:
            if player.is_alive():
                escape = False
        return escape

    def get_battle_start(self):
        self.draw()
        for num, enemy in enumerate(self.enemies, 1):
            print(f'enemy {num} has {enemy.stats["hp"]} hit points, level {enemy.level}')

    def main(self):
        # main loop of battle
        round_count = 0
        self.get_battle_start()
        attack_trigger = [-1, 0]
        player_attacked = False
        while True:
            if player_attacked:
                # defend iterations
                self.defend()
                if self.has_fainted(self.party):
                    print('GAME OVER')
                    self.game.quit()
                attack_trigger[0] = -1
                player_attacked = False
                round_count += 1
                print(f'round count: {round_count}')
                time.sleep(1)

            # attack iterations
            attack_trigger = self.get_player_choice(attack_trigger[1])
            if attack_trigger[0] > -1:
                escape = self.attack(attack_trigger[0])
                if escape:
                    print('ran away')
                    break
                player_attacked = True
                if self.has_fainted(self.enemies):
                    print('victory')
                    self.check_rewards()
                    break

            self.draw(attack_trigger[0])
        self.return_xp()
        # self.return_rewards()

    def check_rewards(self):
        for mob in self.enemies:
            self.battle_xp += mob.xp_value

    def return_xp(self):
        for player in self.party:
            player.stats['xp'] += self.battle_xp
            player.is_levelup()

    def draw(self, plyr_turn=0):
        # draw all changes after updating
        self.screen.blit(self.backdrop, (0, 0))
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.draw(self.screen)

        if plyr_turn == -1:
            choices = ['attack', 'magic', 'items', 'run']
            for num in range(len(choices)):
                self.game.draw_text(f'{choices[num]}', self.battle_font, self.battle_font_size,
                                    BLACK, self.attack_positions[num][0], self.attack_positions[num][1], align='center')
            self.game.battle_cursor.draw()
        pygame.display.flip()

    def get_enemies(self, areaLevel, partySize):
        # amount of enemies depends on partySize
        # strength of enemies depends on areaLevel
        enemy_population = []
        while len(enemy_population) == 0:
            pop_size = random.randint(2, math.ceil(partySize*1.5))
            for e in range(random.randint(1, pop_size)):
                level = (areaLevel * 5 + math.ceil(random.randint(-5, 5)) +
                         math.ceil(random.randint(-ENEMYVARIANCE, ENEMYVARIANCE)))
                enemy_population.append(Mob(int(level), 'shadow_d-kin.png', self.game))
        return enemy_population

    def set_positions(self):
        position_count = len(self.enemies)
        CENTER = WIDTH/2, HEIGHT/2
        CENTER_LEFT = WIDTH/2-150, HEIGHT/2-50
        CENTER_RIGHT = WIDTH/2+150, HEIGHT/2-50
        HIGH_LEFT = CENTER_LEFT[0]-150, CENTER_LEFT[1]-50
        HIGH_RIGHT = CENTER_RIGHT[0]+150, CENTER_RIGHT[1]-50
        HIGH_CENTER = CENTER[0]-200, HEIGHT

        positions = CENTER, CENTER_LEFT, CENTER_RIGHT, HIGH_LEFT, HIGH_RIGHT, HIGH_CENTER

        try:
            for num in range(position_count):
                self.enemies[num].pos = positions[num]
        except IndexError:
            print('index out of range cannot position enemy or position does not exist')
