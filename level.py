import pygame
from utils.helpers import *
from settings import tile_size
from tile import *
from player import Player
from enemy import *
from settings import *
from level_data import background_paths


class Level:
    def __init__(self, screen, level_map) -> None:
        self.screen = screen
        self.move_world = -1
        self.move_world_y = 0
        self.distance = 0
        self.completed = False
       

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
        




        # character

        self.player_group = pygame.sprite.GroupSingle()

        # enemys
        self.enemys = pygame.sprite.Group()

        self.characters_layout = import_csv(level_map["characters"])
        self.player_sprites = self.player_setup(
            self.characters_layout)
        self.enemy_sprites = self.enemy_setup(
            self.characters_layout)
       
        
        

    #     self.backgrounds = []

    #     for path in background_paths:
    #         background = pygame.image.load(path).convert_alpha()
    #         background = pygame.transform.scale(
    #             background, (screen_width, screen_height))
    #         background_rect = background.get_rect()
    #         self.backgrounds.append((background, background_rect))

    # def draw_background(self):
    #     for background, background_rect in self.backgrounds:
    #         self.screen.blit(background, background_rect)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):

                if val != "-1":
                    x = col_index * (tile_size * 2)
                    y = row_index * (tile_size * 2)

                    if type == "terrain":
                        terrain_tiles = import_cut_graphics(
                            "./assets/terrain/terrain.png")
                        tile_surface = terrain_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        # Escala y copia la imagen original en la nueva superficie
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    if type == "background":
                        background_tiles = import_cut_graphics(
                            "./assets/terrain/terrain.png")
                        tile_surface = background_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        # Escala y copia la imagen original en la nueva superficie
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    if type == "decorations":
                        decorations_tiles = import_cut_graphics("./assets/terrain/terrain.png")
                        tile_surface = decorations_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    
                    if type == "tramps":
                        tramps_tiles = import_cut_graphics("./assets/terrain/terrain.png")
                        tile_surface = tramps_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = Tramp(x, y, tile_size * 2, new_surface)

                        

                    if type == "obstacles":
                        sprite = Tile(x, y, tile_size)

                    if type == "puzzles":
                        puzzle_tiles = import_cut_graphics("./assets/terrain/terrain_2.png")
                        tile_surface = puzzle_tiles[int(val)]
                        new_surface = pygame.Surface(
                            (tile_size * 2, tile_size * 2), pygame.SRCALPHA)
                        new_surface.blit(pygame.transform.scale(
                            tile_surface, (tile_size * 2, tile_size * 2)), (0, 0))
                        sprite = StaticTile(x, y, tile_size * 2, new_surface)

                    sprite_group.add(sprite)

        return sprite_group

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

                    flyingEye = FlyingEnemy((x, y), "flyingEye", 150, 15, 2,  25, self.screen, self.player)
                    self.enemys.add(flyingEye)


    def check_obstable_collitions(self):

        for enemy in self.enemys.sprites():
            if pygame.sprite.spritecollide(enemy, self.obstacles_sprites, False):
                enemy.change_direction()
    def check_tramps_collisions(self):
        player = self.player_group.sprite
        tramps_colitions = pygame.sprite.spritecollide(
            player, self.tramps_sprites, False, pygame.sprite.collide_rect)  

        for tramp in tramps_colitions:
           
            player.get_hurt(tramp.damage)
            # player.healthbar.max_health -= 20    
            # player.is_alive = False
    def detect_enemy_collitions(self):

        player = self.player_group.sprite

        enemy_collitions = pygame.sprite.spritecollide(
            player, self.enemys, False, pygame.sprite.collide_rect)       

        for enemy in enemy_collitions:  
            
          
            

            enemy.attack()  

    def proyectiles_collision(self):
        player = self.player_group.sprite
        player_group = pygame.sprite.Group(player)  # Create a temporary sprite group with the player sprite
        for enemy in self.enemys.sprites():
            if isinstance(enemy, FlyingEnemy):
                projectiles = enemy.get_projectiles()
                for projectile in projectiles:
                    collisions = pygame.sprite.spritecollide(projectile, player_group, False, pygame.sprite.collide_rect)
                    if collisions:
                        player.get_hurt(projectile.damage)
                        
                        projectile.kill()


   


        
        


   

    def check_arrow_collitions(self):

        arrows = self.player_group.sprite.arrows
        for arrow in arrows:
            collisions = pygame.sprite.spritecollide(
                arrow, self.enemys, False, pygame.sprite.collide_mask)
            for enemy in collisions:

                enemy.take_damage(arrow.damage)
                if enemy.type == "demon" and not enemy.is_alive:
                    print("muere el boss")
                    self.completed = True
                arrow.kill()

    def horizontal_movement_collision(self):
        player = self.player_group.sprite
        player.rect.x += player.direction.x * player.speed
       
        puzzle_collisions = pygame.sprite.spritecollide(
            player, self.puzzle_sprites, False, pygame.sprite.collide_rect)

       
        terrain_collisions = pygame.sprite.spritecollide(
            player, self.terrain_sprites, False, pygame.sprite.collide_rect)

        for sprite in puzzle_collisions + terrain_collisions:
            if sprite.rect.colliderect(player.rect):

                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.x
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.x
        if not player.on_left and not player.on_right:
            self.current_x = player.rect.x

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player_group.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):

                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False


        

    def enemy_horizontal_collision(self):
        for enemy in self.enemys.sprites():
           
            for sprite in self.terrain_sprites:
                if sprite.rect.colliderect(enemy.rect):
                    
                
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
                        
                    elif enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left          

    

                   
                       

    def enemy_vertical_collision(self):
        for enemy in self.enemys.sprites():
            if enemy.type != "flyingEye":
            
                enemy.apply_gravity()      
            

                for sprite in self.terrain_sprites.sprites():
                    if sprite.rect.colliderect(enemy.rect):
                        # Si el enemigo está cayendo y hay una plataforma debajo
                        if enemy.direction.y > 0:
                            enemy.rect.bottom = sprite.rect.top
                            enemy.direction.y = 0
                            enemy.on_ground = True
                            self.collided = True  # Se produjo una colisión

           

    def scroll_x(self):
        player = self.player_group.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x >= (screen_width / 2) and direction_x > 0:
            self.move_world = -8
            self.distance -= self.move_world
            player.speed = 0
        elif player_x <= screen_width / 2 and direction_x < 0:
            self.move_world = 8
            self.distance -= self.move_world
            player.speed = 0

        else:
            self.move_world = 0
            player.speed = 8       
       


    def run(self):
     

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


        # for enemy in self.enemys.sprites():
        #     pygame.draw.rect(self.screen, (255, 0, 0), enemy.rect, 2)

        self.check_obstable_collitions()
 


        self.check_arrow_collitions()
        # self.detect_proyectiles()
        self.proyectiles_collision()
        self.check_tramps_collisions()

        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        self.enemy_horizontal_collision()
        self.enemy_vertical_collision()


        self.player_group.draw(self.screen)
        self.player_group.update()

        self.enemys.draw(self.screen)
        self.enemys.update(self.move_world, self.move_world_y)
