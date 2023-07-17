import pygame, sys, json
from button import Button
from settings import *
from utils.helpers import save_game
from tabulate import tabulate


class Menu:
    def __init__(self) -> None:
        self.header = None
        
        self.buttons = []
        
        self.font = pygame.font.SysFont("Arial", 50)
        self.background = pygame.image.load("./assets/menu/background/main_menu.png")
        self.background_rect = self.background.get_rect(topleft=(0,0))


    def draw(self, screen):  

        if self.header == "¡Game Completed!":
            width = 350
        else:
            width = 200

        # header = self.font.render(self.header, True, (255, 255, 255))
        # header_rect = pygame.Rect(
        # ((screen_width / 2) - (width / 2)) , screen_height / 4, width, 80)
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
        self.header_rect = self.header.get_rect(center=((screen_width / 2) , screen_height / 4 ))
        

        self.buttons = [
            Button( pygame.image.load("./assets/menu/buttons/play.png"), pygame.image.load("./assets/menu/buttons/play_hover.png")),
            Button( pygame.image.load("./assets/menu/buttons/options.png"), pygame.image.load("./assets/menu/buttons/options_hover.png"), 80),
            Button( pygame.image.load("./assets/menu/buttons/exit.png"), pygame.image.load("./assets/menu/buttons/exit_hover.png") ,  160)
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
        self.header = "¡Game Completed!"

        self.buttons = [
            Button("play again", white, white),
            Button("ranking", white, white, 80),
            Button("save", white, white, 160),
            Button("exit", white, white , 240)
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
        self.header = "Ranking"
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
        self.header = "Game Over"
        self.buttons = [
            Button("restart", white, white),
            Button("exit", white, white, 80)            
        ]


    def handle_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.buttons[0].check_clicked(mouse_pos):
            return "restart"
        if self.buttons[1].check_clicked(mouse_pos):
            self.exit()

    
