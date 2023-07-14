import pygame
from settings import *


class Button:
    def __init__(self, text, color, border_color) -> None:

        self.font = pygame.font.SysFont("Arial", 50)
        self.border_color = border_color
        self.text = text
        self.text_surface = self.font.render(
            self.text, True, (255, 255, 255))
        self.rect = self.text_surface.get_rect()
        self.button_width = self.rect.width
        self.button_height = self.rect.height
        self.button_x = (screen_width - self.button_width) // 2
        self.button_y = (screen_height - self.button_height) // 2

    def draw(self, screen):

        screen.blit(self.text_surface, (self.button_x, self.button_y))
