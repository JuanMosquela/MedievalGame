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
        # self.current_level = level_map[self.current_level_index]

        # self.level = Level(self.screen, self.current_level, self.current_level_index)
        self.level = None

        self.running = True
        self.playing = True
        self.pause_game = False

        self.pause_game = False
        self.level_points = 0
        self.total_points = 0

        self.font = pygame.font.SysFont("arialblack", 50)

        self.levels = []

        for level_index, level_data in enumerate(level_map): 
            print(level_data, level_index) 
    
            level = Level(self.screen, level_data, level_index)
            self.levels.append(level)

        self.current_level = self.levels[self.current_level_index]

        


    def game_loop(self):

        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    self.running = False
                    self.playing = False
                    pygame.quit()   


          
           
            self.current_level.run()

            if self.current_level.completed:
               
                self.current_level_index += 1
                if self.current_level_index >= len(self.levels):
                    print("ganaste el juego")
                    self.current_level_index = 0
                self.current_level = self.levels[self.current_level_index]

            pygame.display.update()
            self.clock.tick(60)
