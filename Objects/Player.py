import pygame
import os
from Objects import Object


class Player(Object.Object):
    def __init__(self, x, y, x_speed, y_speed, width, height):
        self.img = pygame.image.load(os.path.join('Objects/imgs/player.png'))
        Object.Object.__init__(self, x, y, x_speed, y_speed, width, height)