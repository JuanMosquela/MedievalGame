import pygame, sys, json
from button import Button
from settings import *
from utils.helpers import save_game
from tabulate import tabulate


class Menu:
    def __init__(self) -> None:
        self.header = ""
       
        self.buttons = []
        self.font = pygame.font.SysFont("Arial", 50)


    def draw(self, screen):      

        header = self.font.render(self.header, True, (255, 255, 255))
        header_rect = pygame.Rect(
        ((screen_width / 2) - (200 / 2)) , screen_height / 4, 200, 80)
        screen.blit(header, header_rect)

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

        self.header = "Main Menu"

        self.buttons = [
            Button("play", black, white),
            Button("options", black, white, 80),
            Button("exit", black, white, 160)
        ]

    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.buttons[0].check_clicked(mouse_pos):
            return "form"
        if self.buttons[2].check_clicked(mouse_pos):
            self.exit()


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
        self.buttons = [
            Button("back", white, white),
            
        ]
        self.scores = []


    def load_scores(self):
        try:
            with open("./data/ranking.json", "r") as file:
                    self.scores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
                self.scores = []

    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.buttons[0].check_clicked(mouse_pos):
            return "completed"
        if self.buttons[1].check_clicked(mouse_pos):
            self.exit()

    def draw_scores(self, screen):

        self.load_scores()

        table_data = [[score['username'], score['score']] for score in self.scores]
        table_headers = ['Nombre', 'Puntaje']

        table = tabulate(table_data, headers=table_headers, tablefmt='plain')

        font = pygame.font.Font(None, 36)
        scores_lines = table.split('\n')
        y = (screen_height // 2) - (len(scores_lines) * 20 // 2)

        sorted_scores = sorted(self.scores, key=lambda score: score["score"], reverse=True)  
    

        for line in sorted_scores:
            score_message = font.render(f"{line['username']}: {line['score']} ", True, white)
            score_rect = score_message.get_rect(center=(screen_width // 2, y))
            screen.blit(score_message, score_rect)
            y += 40 

       


class GameOver(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.buttons = [
            Button("restart", white, white),
            Button("exit", white, white, 50)            
        ]


    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.buttons[0].check_clicked(mouse_pos):
            return "restart"
        if self.buttons[1].check_clicked(mouse_pos):
            self.exit()

    
