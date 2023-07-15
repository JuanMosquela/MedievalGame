import pygame
import sys
import json
from settings import *
from level import Level
from level_data import level_map
from button import Button
from utils.helpers import save_game
from form import TextInput
from menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.current_level_index = 0
        self.playing = True
        self.username = ""
        # self.current_level = level_map[self.current_level_index]

        # self.level = Level(self.screen, self.current_level, self.current_level_index)
        self.level = None

        self.running = True
        self.playing = False
        self.pause_game = False

        self.pause_game = False
        self.level_points = 0
        self.total_points = 0
        self.state = "menu"

        self.font = pygame.font.SysFont("arialblack", 50)

        self.levels = []

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

            # play_button = Button("Play", white, white)
            # options_button = Button("Options", white, white)
            # exit_button = Button("Exit", white, white)

            # button_spacing = 100
            # play_button.button_x = (
            #     screen_width - play_button.button_width) // 2
            # play_button.button_y = (
            #     screen_height - play_button.button_height) // 2 - button_spacing
            # options_button.button_x = (
            #     screen_width - options_button.button_width) // 2
            # options_button.button_y = (
            #     screen_height - options_button.button_height) // 2
            # exit_button.button_x = (
            #     screen_width - exit_button.button_width) // 2
            # exit_button.button_y = (
            #     screen_height - exit_button.button_height) // 2 + button_spacing

            # Dibujar los botones en la pantalla
            # play_button.draw(self.screen)
            # options_button.draw(self.screen)
            # exit_button.draw(self.screen)

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         self.running = False

            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         if play_button.rect.collidepoint(event.pos[0] - play_button.button_x, event.pos[1] - play_button.button_y):

            #             self.state = "form"

            pygame.display.update()
            self.clock.tick(60)

    def display_form(self):
        game.play(-1)

        self.screen.fill((0, 0, 0))
        width = 300
        height = 50
        header = self.font.render("Ingresa tu nombre", True, (255, 255, 255))
        header_rect = pygame.Rect(
            width, height, ((screen_width / 2) - (width / 2)), screen_height / 4)
        self.screen.blit(header, header_rect)
        form = TextInput(((screen_width / 2) - (width / 2)),
                         screen_height / 4, width, height, 25)

        while self.state == "form":
            form.draw(self.screen)
            for event in pygame.event.get():

                form.handle_event(event)
                form.check_button_click(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

            if form.done:
                self.username = form.text
                self.state = "playing"

            pygame.display.update()
            self.clock.tick(60)

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

    def game_loop(self):

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

                if self.current_level.completed:

                    self.current_level_index += 1
                    self.total_points += self.current_level.points
                    if self.current_level_index >= len(self.levels):

                        playing = False
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

        while self.state == "completed":
            self.current_level_index = 0

            self.screen.fill((0, 0, 0))

            message = self.font.render(
                "¡Congratulations! You won the game.", True, white)
            message_rect = message.get_rect(
                center=(screen_width // 2, screen_height // 2 - 200))

            self.screen.blit(message, message_rect)

            restart_button = Button("Play again", white, white)
            ranking_button = Button("Ranking", white, white)
            save_button = Button("Save Game", white, white)
            exit_button = Button("Exit", white, white)

            button_spacing = 100
            restart_button.button_x = (
                screen_width - restart_button.button_width) // 2
            restart_button.button_y = (
                screen_height - restart_button.button_height) // 2 - button_spacing
            ranking_button.button_x = (
                screen_width - ranking_button.button_width) // 2
            ranking_button.button_y = (
                screen_height - ranking_button.button_height) // 2
            save_button.button_x = (
                screen_width - save_button.button_width) // 2
            save_button.button_y = (
                screen_height - save_button.button_height) // 2 + button_spacing
            exit_button.button_x = (
                screen_width - exit_button.button_width) // 2
            exit_button.button_y = (
                screen_height - exit_button.button_height) // 2 + button_spacing + button_spacing

            # self.screen.blit(message, message_rect)
            restart_button.draw(self.screen)
            ranking_button.draw(self.screen)
            save_button.draw(self.screen)
            exit_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.rect.collidepoint(event.pos[0] - restart_button.button_x, event.pos[1] - restart_button.button_y):

                        self.state = "playing"
                    if ranking_button.rect.collidepoint(event.pos[0] - ranking_button.button_x, event.pos[1] - ranking_button.button_y):

                        self.state = "ranking"
                    if save_button.rect.collidepoint(event.pos[0] - save_button.button_x, event.pos[1] - save_button.button_y):

                        game_stats = {
                            "username": self.username,
                            "points": self.total_points
                        }
                        save_game("./data/ranking.json", game_stats)
                    if exit_button.rect.collidepoint(event.pos[0] - exit_button.button_x, event.pos[1] - exit_button.button_y):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)

    def ranking_menu(self):
        while self.state == "ranking":

            self.screen.fill((0, 0, 0))

            font = pygame.font.Font(None, 36)
            score_message = font.render(
                f"Your score: {self.total_points}", True, white)
            score_rect = score_message.get_rect(
                center=(screen_width // 2, screen_height // 2))
            self.screen.blit(score_message, score_rect)

            # Cargar los puntajes guardados desde el archivo JSON
            try:
                with open("./data/ranking.json", "r") as file:
                    puntajes = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                puntajes = []

            y = 250  # Posición vertical para mostrar los puntajes
            for puntaje in puntajes:
                puntaje_texto = f"{puntaje['username']}: {puntaje['points']}"
                puntaje_renderizado = font.render(puntaje_texto, True, white)
                puntaje_rect = puntaje_renderizado.get_rect(
                    center=(screen_width // 2, y))
                self.screen.blit(puntaje_renderizado, puntaje_rect)
                y += 30  # Incrementar la posición vertical para el siguiente

            back_button = Button("Back", white, white)
            exit_button = Button("Exit", white, white)

            button_spacing = 100
            exit_button.button_x = (
                screen_width - exit_button.button_width) // 2
            exit_button.button_y = (
                screen_height - exit_button.button_height) // 2 + button_spacing

            back_button.button_x = 150
            back_button.button_y = 150

            back_button.draw(self.screen)
            exit_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.rect.collidepoint(event.pos[0] - back_button.button_x, event.pos[1] - back_button.button_y):

                        self.state = "completed"

                    if exit_button.rect.collidepoint(event.pos[0] - exit_button.button_x, event.pos[1] - exit_button.button_y):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)

    def game_over(self):

        button = Button("Press R to restart",
                        (250, 250, 250), (250, 250, 250))
        button.draw(self.screen)
