import pygame
import os
from Objects import Object


class Ladybug(Object.Object):
    def __init__(self, x, y, x_speed, y_speed, width, height):
        self.img = pygame.image.load(os.path.join('ladybug', '.png'))
        self.rend = self.img.get_rect()
        Object.Object.__init__(self, x, y, x_speed, y_speed, width, height)


    def draw(self):

