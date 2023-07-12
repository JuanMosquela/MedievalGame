import pygame
from settings import *


class HealthBar():
    def __init__(self, width, height, max_health) -> None:               

        self.health = max_health
        self.max_health = max_health      
        self.width = width
        self.height = height
        

    def draw(self, screen, pos, type):
        self.ratio = self.max_health / self.health

        if self.max_health >= 0:
            if type == "enemy":
                pygame.draw.rect(screen, "red", (pos[0] - self.width // 2 , pos[1] - 50, self.width, self.height))
                pygame.draw.rect(screen, "green", (pos[0] - self.width // 2, pos[1] - 50, self.width * self.ratio, self.height))
            else: 
                pygame.draw.rect(screen, "red", (pos[0] , pos[1] - 50, self.width, self.height))
                pygame.draw.rect(screen, "green", (pos[0] , pos[1] - 50, self.width * self.ratio, self.height))
