import pygame
from settings import *

class UI:
    def __init__(self):
        self.displaysurf=pygame.display.get_surface()
        self.hitpoints=[
            pygame.image.load('health/0.png'),
            pygame.image.load('health/1.png'),
            pygame.image.load('health/2.png'),
            pygame.image.load('health/3.png'),
            pygame.image.load('health/4.png'),
        ]
    
    def display(self,player):
        pass
