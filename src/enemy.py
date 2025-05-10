import pygame
from character import Character

#aa

class Enemy(Character):
    def __init__(self):
        super().__init__()
        self.x = 400
        self.y = 400