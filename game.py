import pygame
from settings import *
from level import Level
from level_data import level_map


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.current_level_index = 0
        self.playing = True
        self.current_level = level_map[self.current_level_index]

        self.level = Level(self.screen, self.current_level,
                           self.current_level_index)

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

            if self.level.completed:
                self.current_level_index += 1
                if self.current_level_index >= len(level_map):
                    # Has completado todos los niveles, puedes reiniciar el juego o realizar otra acción
                    self.current_level_index = 0
                    # Otra acción...
            print(self.current_level_index)

            self.current_level = level_map[self.current_level_index]
            self.level = Level(self.screen, self.current_level,
                               self.current_level_index)

            pygame.display.update()
            self.clock.tick(60)
