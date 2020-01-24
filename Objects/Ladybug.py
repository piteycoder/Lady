import pygame
import os
from Objects import Object

img = pygame.image.load(os.path.join('Objects/imgs/ladybug.png'))


class Ladybug(Object.Object):
    def __init__(self, x=0, y=0, x_speed=0, y_speed=0, width=30, height=30):
        self.img = img
        Object.Object.__init__(self, x, y, x_speed, y_speed, width, height)
