import pygame
import config


class Caption:
    def __init__(self, text="", size=1, color=config.colors.get("White")):
        self.font = pygame.font.SysFont("comicsansms", size, 1)
        self.text = self.font.render(text, 1, color)
        self.size = size
        self.caption = text
        self.color = color
        self.x = 0
        self.y = 0

    def change_color(self, color=config.colors.get("Grey")):
        self.font = pygame.font.SysFont("comicsansms", self.size, color)
        self.text = self.font.render(self.caption, 1, color)

    def resize(self, size=1):
        self.font = pygame.font.SysFont("comicsansms", size, 1)
        self.text = self.font.render(self.caption, 1, self.color)
