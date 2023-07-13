import pygame
from enemy import FlyingEnemy
from settings import *

class Collisions:
    def __init__(self, enemy_group, player_group, terrains_group, puzzle_group, tramps_group, coins_group, keys_group, obstacles_group) -> None:
        self.player_group = player_group
        self.enemys_group = enemy_group
        self.terrains_group = terrains_group
        self.puzzles_group = puzzle_group
        self.tramps_group = tramps_group
        self.coins_group = coins_group
        self.keys_group = keys_group
        self.obstacles_group = obstacles_group

    def horizontal_movement_collision(self):
        player = self.player_group.sprite
        player.rect.x += player.direction.x * player.speed
       
        puzzle_collisions = pygame.sprite.spritecollide(
            player, self.puzzles_group, False, pygame.sprite.collide_rect)

       
        terrain_collisions = pygame.sprite.spritecollide(
            player, self.terrains_group, False, pygame.sprite.collide_rect)

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

        for sprite in self.terrains_group.sprites():
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
        for enemy in self.enemys_group.sprites():
           
            for sprite in self.terrains_group:
                if sprite.rect.colliderect(enemy.rect):
                    
                
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
                        
                    elif enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left                   
                       

    def enemy_vertical_collision(self):
        for enemy in self.enemys_group.sprites():           
            
            enemy.apply_gravity()             

            for sprite in self.terrains_group.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    # Si el enemigo está cayendo y hay una plataforma debajo
                    if enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                        enemy.on_ground = True
                        self.collided = True  # Se produjo una colisión   


    def detect_enemy_collitions(self):

        player = self.player_group.sprite

        enemy_collitions = pygame.sprite.spritecollide(
            player, self.enemys_group, False, pygame.sprite.collide_rect)       

        for enemy in enemy_collitions:        

            enemy.attack()  

    def check_tramps_collisions(self):
     
        player = self.player_group.sprite
        tramps_colitions = pygame.sprite.spritecollide(
            player, self.tramps_group, False, pygame.sprite.collide_rect)  

        for tramp in tramps_colitions:
            hurt.play()
           
            player.get_hurt(tramp.damage)

    def check_arrow_collitions(self):
       

        arrows = self.player_group.sprite.arrows
        for arrow in arrows:
            collisions = pygame.sprite.spritecollide(
                arrow, self.enemys_group, False, pygame.sprite.collide_mask)
            for enemy in collisions:
                enemy_hurt.play()

                enemy.take_damage(arrow.damage)
                if enemy.type == "demon" and not enemy.is_alive:
                    print("muere el boss")
                    self.completed = True
                arrow.kill()

    def proyectiles_collision(self):

       

        player = self.player_group.sprite
        player_group = pygame.sprite.Group(player) 
        for enemy in self.enemys_group.sprites():
            if isinstance(enemy, FlyingEnemy):
                projectiles = enemy.get_projectiles()
                for projectile in projectiles:
                    collisions = pygame.sprite.spritecollide(projectile, player_group, False, pygame.sprite.collide_rect)
                    if collisions:
                        hurt.play()
                        player.get_hurt(projectile.damage)
                        
                        projectile.kill()

    def puzzle_collision(self):
        player = self.player_group.sprite

        for puzzle in self.puzzles_group:
            if pygame.sprite.collide_rect(puzzle, player) and player.has_key:          
              
                self.puzzles_group.empty()
                player.has_key = False

    def coins_collision(self):
       
        
        player = self.player_group.sprite

        for coin in self.coins_group:
            if pygame.sprite.collide_rect(player, coin):   
                coin_sound.play()                
                player.increse_points(5)
                coin.kill()   

    def check_obstable_collitions(self):

        for enemy in self.enemys_group.sprites():
            if pygame.sprite.spritecollide(enemy, self.obstacles_group, False):
                enemy.change_direction()


  

    def check_take_key(self):
       
        player = self.player_group.sprite
        for key in self.keys_group:
            if pygame.sprite.collide_rect(player, key): 
                key_sound.play()             
                player.has_key = True
                key.kill()
          



    def check(self):
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.enemy_horizontal_collision()
        self.enemy_vertical_collision()
        self.detect_enemy_collitions()
        self.proyectiles_collision()
        self.check_arrow_collitions()
        self.coins_collision()
        self.puzzle_collision()
        self.check_take_key()
        self.check_obstable_collitions()
        self.check_tramps_collisions()