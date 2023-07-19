import pygame
from settings import *


class Button:
    def __init__(self, image, image_hover,  offset=0) -> None:

        self.image = image
        self.image_hover = image_hover
        self.current_image = self.image
        self.width = self.image.get_width()

        self.rect = self.image.get_rect(center=(self.width / 2, offset))
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
            self.current_image = self.image_hover
        else:
            self.current_image = self.image

    def draw(self, screen):

        self.get_hover()
        self.change_color()

        # if self.text == "back":
        #     self.rect.x = 100
        #     self.rect.y = 100

        screen.blit(self.current_image, self.rect)
