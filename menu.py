import pygame
import sys
from button import Button
from settings import *
from utils.helpers import save_game


class Menu:
    def __init__(self) -> None:

        self.buttons = []

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            button.draw(screen)

    def update(self):
        return self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.handle_button()


class MainMenu(Menu):
    def __init__(self) -> None:
        super().__init__()

        self.buttons = [
            Button("play", white, white),
            Button("options", white, white, 50),
            Button("exit", white, white, 100)
        ]

    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.buttons[0].check_clicked(mouse_pos):
            return "form"
        if self.buttons[2].check_clicked(mouse_pos):
            pygame.quit()
            sys.exit()


class MenuFinal(Menu):
    def __init__(self) -> None:
        super().__init__()

        self.buttons = [
            Button("play again", white, white),
            Button("ranking", white, white, 50),
            Button("save", white, white, 100),
            Button("exit", white, white , 150)
        ]

    
    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.buttons[0].check_clicked(mouse_pos):
            return "playing"
        if self.buttons[1].check_clicked(mouse_pos):
            return "ranking"
        if self.buttons[2].check_clicked(mouse_pos):
            return "save"
        if self.buttons[3].check_clicked(mouse_pos):
            pygame.quit()
            sys.exit()

    