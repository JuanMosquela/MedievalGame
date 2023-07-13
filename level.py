import pygame
from utils.helpers import *
from settings import tile_size
from tile import *
from player import Player
from enemy import *
from settings import *
from level_data import background_paths
from collisions import Collisions


class Level:
    def __init__(self, screen, level_map, current_level) -> None:
        self.screen = screen
        self.move_world = -1
        self.move_world_y = 0
        self.distance = 0
        self.completed = False
        self.current_level = current_level
        self.completed = False
        self.level_limit = 2200
        self.points = 0

        
       

        # terrain
        self.terrain_layout = import_csv(level_map["terrain"])
        self.terrain_sprites = self.create_tile_group(
            self.terrain_layout, "terrain")

        # background
        self.background_layout = import_csv(level_map["background"])
        self.background_sprites = self.create_tile_group(
            self.background_layout, "background")

        #decorations
        self.decorations_layout = import_csv(level_map["decorations"])
        self.decorations_sprites = self.create_tile_group(self.decorations_layout, "decorations")

        #tramps
        self.tramps_layout = import_csv(level_map["tramps"])
        self.tramps_sprites = self.create_tile_group(self.tramps_layout, "tramps")

        #obstacles
        self.obstacles_layout = import_csv(level_map["obstacles"])
        self.obstacles_sprites = self.create_tile_group(self.obstacles_layout, "obstacles")

        #obstacles
        self.puzzle_layout = import_csv(level_map["puzzles"])
        self.puzzle_sprites = self.create_tile_group(self.puzzle_layout, "puzzles")

        #keys
        self.keys_layout = import_csv(level_map["keys"])
        self.keys_sprites = self.create_tile_group(self.keys_layout, "keys")
        
        #coins
        self.coins_layout = import_csv(level_map["coins"])
        self.coins_sprites = self.create_tile_group(self.coins_layout, "coins")
        




        # character

        self.player_group = pygame.sprite.GroupSingle()

        # enemys
        self.enemys = pygame.sprite.Group()

        self.characters_layout = import_csv(level_map["characters"])
        self.player_sprites = self.player_setup(
            self.characters_layout)
        self.enemy_sprites = self.enemy_setup(
            self.characters_layout)
       
        
        

        self.backgrounds = []

        for path in background_paths:
            background = pygame.image.load(path).convert_alpha()
            background = pygame.transform.scale(
                background, (screen_width, screen_height))
            background_rect = background.get_rect()
            self.backgrounds.append((background, background_rect))

        self.collisions = Collisions(self.enemys, self.player_group, self.terrain_sprites, self.puzzle_sprites, self.tramps_sprites, self.coins_sprites, self.keys_sprites, self.obstacles_sprites)

   

    def draw_background(self):
        for background, background_rect in self.backgrounds:
            self.screen.blit(background, background_rect)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):

                if val != "-1":
                    x = col_index * (tile_size * 2)
                    y = row_index * (tile_size * 2)

                    if type == "terrain":
                        terrain_tiles = import_cut_graphics(
                            f"./assets/terrain/{self.current_level}/terrain.png")
                        tile_surface = terrain_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        # Escala y copia la imagen original en la nueva superficie
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    if type == "background":
                        background_tiles = import_cut_graphics(
                            f"./assets/terrain/{self.current_level}/terrain.png")
                        tile_surface = background_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        # Escala y copia la imagen original en la nueva superficie
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    if type == "decorations":
                        decorations_tiles = import_cut_graphics(f"./assets/terrain/{self.current_level}/terrain.png")
                        tile_surface = decorations_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    
                    if type == "tramps":
                        tramps_tiles = import_cut_graphics(f"./assets/terrain/{self.current_level}/terrain.png")
                        tile_surface = tramps_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = Tramp(x, y, tile_size * 2, new_surface)

                        

                    if type == "obstacles":
                        sprite = Tile(x, y, tile_size)

                    if type == "puzzles":
                        puzzle_tiles = import_cut_graphics(f"./assets/terrain/{self.current_level}/terrain_2.png")
                        tile_surface = puzzle_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    if type == "keys":
                        keys_tiles = import_cut_graphics(f"./assets/terrain/{self.current_level}/terrain_2.png")
                        tile_surface = keys_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    if type == "coins":
                        coin_tiles = import_cut_graphics(f"./assets/terrain/{self.current_level}/terrain_2.png")
                        tile_surface = coin_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    sprite_group.add(sprite)

        return sprite_group
    
    def update_points(self):
        self.points = self.player_group.sprite.points

    def player_setup(self, layout):

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):

                x = col_index * (tile_size * 2)
                y = row_index * (tile_size * 2)
                if val == "0":

                    self.player = Player((x, y), self.screen)
                    self.player_group.add(self.player)
               

    def enemy_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * (tile_size * 2)
                y = row_index * (tile_size * 2)

                if val == "1":

                    goblin = NormalEnemy((x, y), "goblin", 100, 10, 3,  15, self.screen, self.player)
                    self.enemys.add(goblin)
                if val == "2":

                    mushroom = NormalEnemy((x, y), "mushroom", 120, 15, 2,  25, self.screen, self.player)
                    self.enemys.add(mushroom)
                if val == "3":

                    skeleton = NormalEnemy((x, y), "skeleton", 150, 15, 2,  25, self.screen, self.player)
                    self.enemys.add(skeleton)
                if val == "4":

                    flyingEye = FlyingEnemy((x, y), "flyingEye", 50, 15, 2,  25, self.screen, self.player)
                    self.enemys.add(flyingEye)  

   

           

    def scroll_x(self):
        player = self.player_group.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x >= (screen_width / 2) and direction_x > 0 and self.distance < self.level_limit:
            self.move_world = -8
            self.distance -= self.move_world
            player.speed = 0
        elif player_x <= screen_width / 2 and direction_x < 0 and self.distance > 0:
            self.move_world = 8
            self.distance -= self.move_world
            player.speed = 0

        else:
            self.move_world = 0
            player.speed = 8   
            if player.rect.x >= screen_width:
                self.completed = True 
                
       


    def run(self):       
     
        self.draw_background()
        self.scroll_x()
      

        self.background_sprites.draw(self.screen)
        self.background_sprites.update(self.move_world,  self.move_world_y )

        self.decorations_sprites.draw(self.screen)
        self.decorations_sprites.update(self.move_world, self.move_world_y)

        self.terrain_sprites.draw(self.screen)
        self.terrain_sprites.update(self.move_world, self.move_world_y ) 

        self.tramps_sprites.draw(self.screen)
        self.tramps_sprites.update(self.move_world, self.move_world_y)

        self.obstacles_sprites.draw(self.screen)
        self.obstacles_sprites.update(self.move_world, self.move_world_y)

        self.puzzle_sprites.draw(self.screen)
        self.puzzle_sprites.update(self.move_world, self.move_world_y)

        self.keys_sprites.draw(self.screen)
        self.keys_sprites.update(self.move_world, self.move_world_y)

        self.coins_sprites.draw(self.screen)
        self.coins_sprites.update(self.move_world, self.move_world_y)


        # for enemy in self.enemys.sprites():
        #     pygame.draw.rect(self.screen, (255, 0, 0), enemy.rect, 2)     


        self.collisions.check()
        self.update_points()
        
        self.player_group.draw(self.screen)
        self.player_group.update()

        self.enemys.draw(self.screen)
        self.enemys.update(self.move_world, self.move_world_y)
