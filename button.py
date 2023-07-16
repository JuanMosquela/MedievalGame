import pygame
from settings import *


class Button:
    def __init__(self, text, color, border_color, offset=0) -> None:

        self.font = pygame.font.SysFont("Arial", 50)
        self.border_color = border_color
        self.text = text
        self.color = color
        self.text_surface = self.font.render(
            self.text, True, (255, 255, 255))
        self.rect = self.text_surface.get_rect()
        self.button_width = self.rect.width
        self.button_height = self.rect.height
        self.rect.x = (screen_width - self.button_width) // 2
        self.rect.y = ((screen_height - self.button_height) // 2) + offset
        self.is_hover = False

    def check_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False
        
    def get_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.is_hover = True
        else:
            self.is_hover = False

    def change_color(self):
        if self.is_hover:
          self.color = hover
        else:
          self.color = black    

      

    def draw(self, screen):

        self.get_hover()
       
        if self.text == "back":
            self.rect.x = 100
            self.rect.y = 100
        
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.rect.x, self.rect.y))
