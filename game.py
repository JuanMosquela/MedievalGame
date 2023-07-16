import pygame
import sys
import json
from settings import *
from level import Level
from level_data import level_map
from button import Button
from utils.helpers import save_game
from form import TextInput
from menu import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.current_level_index = 1
       
        self.level = None

        self.running = True
        self.playing = False
        self.pause_game = False
        self.restart = False

        self.level_points = 0
        self.total_points = 0

        self.state = "playing"
        self.username = ""

        self.font = pygame.font.SysFont("Arial", 50)

        self.levels = []

        for level_index, level_data in enumerate(level_map):

            level = Level(self.screen, level_data, level_index)
            self.levels.append(level)

        self.current_level = self.levels[self.current_level_index]


    def game_state(self):       

        if self.state == "playing":
            menu.stop()
            self.game_loop()

        if self.state == "menu":
            self.display_menu()

        if self.state == "completed":
            self.display_game_completed_screen()

        if self.state == "ranking":
            self.ranking_menu()

        if self.state == "form":
            self.display_form()

        if self.state == "gameover":
            self.game_over()
        if self.state == "restart":
            self.restart_game()
        if self.state == "save":
            save_game("./data/ranking.json", { "username": self.username, "score": self.total_points })
            self.state = "ranking"

       

    def restart_game(self):
        self.current_level_index = 0
        self.level_points = 0
        self.total_points = 0
        self.state = "playing"
        self.username = ""
        self.levels = []
        self.current_level = None

        for level_index, level_data in enumerate(level_map):
            level = Level(self.screen, level_data, level_index)
            self.levels.append(level)

        self.current_level = self.levels[self.current_level_index]


    def display_menu(self):
        menu.play(-1)
        main_menu = MainMenu()

        while self.state == "menu":
            self.screen.fill((0, 0, 0))
            main_menu.draw(self.screen)
            state = main_menu.update()
            if state != None:
                self.state = state          

            pygame.display.update()
            self.clock.tick(60)

    def display_form(self):       

        self.screen.fill((0, 0, 0))
        width = 300
        height = 50
       
        form = TextInput(((screen_width / 2) - (width / 2)),
                         screen_height / 4, width, height, 25)

        while self.state == "form":
            form.draw(self.screen, width, height)
            for event in pygame.event.get():

                form.handle_event(event)
                form.check_button_click(event)                

            if form.done:
                self.username = form.text
                self.state = "playing"

            pygame.display.update()
            self.clock.tick(60)

    
    def game_loop(self):
        game.play(-1)

        while self.state == "playing":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        self.state = "menu"
                    if event.key == pygame.K_p:
                        self.pause_game = not self.pause_game

          

            if not self.pause_game:

                self.current_level.run()

                if self.current_level.game_over:
                    self.state = "gameover"

                if self.current_level.completed:

                    self.current_level_index += 1
                    self.total_points += self.current_level.points

                    if self.current_level_index >= len(self.levels):                      
                        self.state = "completed"

                    else:
                        self.current_level = self.levels[self.current_level_index]
            else:
                self.draw_pause_screen()

            pygame.display.update()
            self.clock.tick(60)

    def draw_pause_screen(self):

        message = self.font.render("PAUSED GAME", True, white)
        sub_message = self.font.render("Press R to play", True, white)
        message_rect = message.get_rect(
            center=(screen_width // 2, screen_height // 2))
        sub_message_rect = sub_message.get_rect(
            center=(screen_width // 2, screen_height // 2))
        sub_message_rect.y += 50
        self.screen.blit(message, message_rect)
        self.screen.blit(sub_message, sub_message_rect)
        pygame.display.update()

    def display_game_completed_screen(self):

        final_menu = MenuFinal()

        while self.state == "completed":
            self.current_level_index = 0

            self.screen.fill((0, 0, 0))

            message = self.font.render(
                "You won the game.", True, white)
            message_rect = message.get_rect(
                center=(screen_width // 2, screen_height // 2 - 200))

            self.screen.blit(message, message_rect)

            final_menu.draw(self.screen)            

            state = final_menu.update()
            if state != None:
                self.state = state               

            pygame.display.update()
            self.clock.tick(60)

    def ranking_menu(self):
        ranking = RankingMenu()
        while self.state == "ranking":

            self.screen.fill((0, 0, 0))

            # font = pygame.font.Font(None, 36)
            # score_message = font.render(
            #     f"Your score: {self.total_points}", True, white)
            # score_rect = score_message.get_rect(
            #     center=(screen_width // 2, screen_height // 2))
            # self.screen.blit(score_message, score_rect)

            ranking.draw(self.screen)           
           
            ranking.draw_scores(self.screen)
          
            state = ranking.update()
            if state != None:
                self.state = state            

            pygame.display.update()
            self.clock.tick(60)

    def game_over(self):
        game_over_menu = GameOver()


        while self.state == "gameover":
            self.screen.fill((0, 0, 0))
            game_over_menu.draw(self.screen)

            state = game_over_menu.update()

            if state == "restart":
                self.restart_game()


            pygame.display.update()
            self.clock.tick(60)

      