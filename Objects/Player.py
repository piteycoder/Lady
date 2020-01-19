import pygame
import os
import config

from Objects import Object


class Player(Object.Object):
    def __init__(self, x=0, y=0, x_speed=0, y_speed=0, width=30, height=30):
        self.img = pygame.image.load(os.path.join('Objects/imgs/player.png'))
        Object.Object.__init__(self, x, y, x_speed, y_speed, width, height)
        self.name = config.player_name
        self.score = 0

    def change_name(self, name):
        self.name = name
