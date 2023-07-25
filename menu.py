import pygame
from tabulate import tabulate
import sys
from button import Button
from settings import *


class Menu:
    def __init__(self) -> None:
        self.header = None

        self.buttons = []
        self.background = pygame.image.load(
            "./assets/menu/background/main_menu.png")
        self.background_rect = self.background.get_rect(topleft=(0, 0))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(self.background, self.background_rect)
        screen.blit(self.header, self.header_rect)

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

    def exit(self):
        pygame.quit()
        sys.exit()


class MainMenu(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.header = pygame.image.load("./assets/menu/headers/main_menu.png")
        self.width = self.header.get_width()
        self.header_rect = self.header.get_rect(
            center=((screen_width / 2), screen_height / 4))

        self.buttons = [
            Button(pygame.image.load("./assets/menu/buttons/play.png"),
                   pygame.image.load("./assets/menu/buttons/play_hover.png")),
          
            Button(pygame.image.load("./assets/menu/buttons/options.png"),
                   pygame.image.load("./assets/menu/buttons/options_hover.png"), 80),

            Button(pygame.image.load("./assets/menu/buttons/exit.png"),
                   pygame.image.load("./assets/menu/buttons/exit_hover.png"), 160)
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
        self.header = pygame.image.load("./assets/menu/headers/game_completed.png")
        self.width = self.header.get_width()
        self.header_rect = self.header.get_rect(
            center=((screen_width / 2), screen_height / 4))

        self.buttons = [
            Button(pygame.image.load("./assets/menu/buttons/play_again.png"),
                   pygame.image.load("./assets/menu/buttons/play_again_hover.png")),
            Button(pygame.image.load("./assets/menu/buttons/ranking.png"),
                   pygame.image.load("./assets/menu/buttons/ranking_hover.png"), 80),
            Button(pygame.image.load("./assets/menu/buttons/save.png"),
                   pygame.image.load("./assets/menu/buttons/save_hover.png"), 160),
            Button(pygame.image.load("./assets/menu/buttons/exit.png"),
                   pygame.image.load("./assets/menu/buttons/exit_hover.png"), 240)
        ]

    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.buttons[0].check_clicked(mouse_pos):
            return "restart"
        if self.buttons[1].check_clicked(mouse_pos):
            return "ranking"
        if self.buttons[2].check_clicked(mouse_pos):
            return "save"
        if self.buttons[3].check_clicked(mouse_pos):
            self.exit()


class RankingMenu(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.header = pygame.image.load("./assets/menu/headers/ranking.png")
        self.width = self.header.get_width()
        self.header_rect = self.header.get_rect(
            center=((screen_width / 2), screen_height / 4))
        self.buttons = [
            Button(pygame.image.load("./assets/menu/buttons/back.png"),
                   pygame.image.load("./assets/menu/buttons/back_hover.png"), 80, "back"),

        ]
        self.scores = []

    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.buttons[0].check_clicked(mouse_pos):
            return "completed"
        if self.buttons[1].check_clicked(mouse_pos):
            self.exit()

    def draw_scores(self, screen, data):
        table_headers = ['ID', 'Nombre', 'Puntaje']
        table_data = [[str(score[0]), score[1], str(score[2])]
                      for score in data]

        table = tabulate(table_data, headers=table_headers, tablefmt='plain')

        font = pygame.font.Font(None, 36)
        scores_lines = table.split('\n')
        y = (screen_height // 2) - (len(scores_lines) * 20 // 2)

        for line in scores_lines:
            score_message = font.render(line, True, white)
            score_rect = score_message.get_rect(center=(screen_width // 2, y))
            screen.blit(score_message, score_rect)
            y += 40


class GameOver(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.header = pygame.image.load("./assets/menu/headers/game_over.png")
        self.width = self.header.get_width()
        self.header_rect = self.header.get_rect(
            center=((screen_width / 2), screen_height / 4))
        self.buttons = [
            Button(pygame.image.load("./assets/menu/buttons/restart.png"),
                   pygame.image.load("./assets/menu/buttons/restart_hover.png")),
          
            

            Button(pygame.image.load("./assets/menu/buttons/exit.png"),
                   pygame.image.load("./assets/menu/buttons/exit_hover.png"), 160)
        ]

    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.buttons[0].check_clicked(mouse_pos):
            return "restart"
        if self.buttons[1].check_clicked(mouse_pos):
            self.exit()
