import pygame
import config


class Caption:
    def __init__(self, text="", size=1, color=config.colors.get("White")):
        self.font = pygame.font.SysFont("Arial", size, 1)
        self.text = self.font.render(text, 1, color)
        self.size = size

    def size(self):
        return self.size
