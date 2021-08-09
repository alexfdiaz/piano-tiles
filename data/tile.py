import pygame

class Tile:
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect(x, y, 100, 200)
        self.color = (0, 0, 0)