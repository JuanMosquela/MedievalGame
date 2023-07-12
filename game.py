import pygame
from settings import *
from level import Level
from level_data import level_map


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.current_level_index = 1
        self.playing = True
        self.current_level = level_map[self.current_level_index]

        self.level = Level(self.screen, self.current_level)

        self.running = True
        self.playing = True
        self.pause_game = False

        self.pause_game = False
        self.level_points = 0
        self.total_points = 0

        self.font = pygame.font.SysFont("arialblack", 50)

    def game_loop(self):

        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    self.running = False
                    self.playing = False
                    pygame.quit()

            self.level.run()
            # horizontal_line = screen_height -80  # Altura de la línea en la mitad de la pantalla
            # pygame.draw.line(self.screen, (255, 255, 255), (0, horizontal_line), (screen_width, horizontal_line))
            # pygame.draw.line(self.screen, (255, 255, 255), (0,  (screen_height + 80) - screen_height), (screen_width,  (screen_height + 80) - screen_height))


            pygame.display.update()
            self.clock.tick(60)
