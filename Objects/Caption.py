import pygame
import config


class Caption:
    def __init__(self, text="", size=1, color=config.colors.get("White"), x_pos=0, y_pos=0):
        self.font = pygame.font.SysFont("comicsansms", size, 1)
        self.text = self.font.render(str(text), 1, color)
        self.size = size
        self.caption = str(text)
        self.color = color
        self.x = x_pos
        self.y = y_pos

    def change_color(self, color=config.colors.get("Grey")):
        self.font = pygame.font.SysFont("comicsansms", self.size, color)
        self.text = self.font.render(self.caption, 1, color)

    def resize(self, size=1):
        self.font = pygame.font.SysFont("comicsansms", size, 1)
        self.text = self.font.render(self.caption, 1, self.color)

    def get_width(self):
        return self.text.get_width()

    def get_height(self):
        return self.text.get_height()

    def __eq__(self, other):
        return self.caption == other.caption
