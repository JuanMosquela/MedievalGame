import pygame
from button import Button
from settings import *


class TextInput:
    def __init__(self, x, y, width, height, max_length):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.SysFont("white", 50)
        self.max_length = max_length
        self.min_characters = 4
        self.done = False
        self.accept_button = Button("Accept", (255, 255, 255), (255, 255, 255))
        self.background = pygame.image.load("./assets/menu/background/main_menu.png")
        self.background_rect = self.background.get_rect(topleft=(0,0))
        

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < self.max_length:
                    self.text += event.unicode

    def check_button_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.accept_button.rect.collidepoint(mouse_pos) and len(self.text) >= self.min_characters:
                self.done = True

    def draw(self, screen, width, height):
        header = self.font.render("Ingresa tu nombre", True, (255, 255, 255))
        header_rect = pygame.Rect(
            width, height, ((screen_width / 2) - (width / 2)), screen_height / 4)        


        screen.blit(self.background, self.background_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        rendered_text = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(header, header_rect)
        screen.blit(rendered_text, (self.rect.x + 5, self.rect.y + 5))
        self.accept_button.draw(screen)
