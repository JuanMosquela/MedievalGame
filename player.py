import pygame
from utils.helpers import import_assets
from arrow import Arrow
from healthbar import HealthBar
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen) -> None:
        super().__init__()
        self.screen = screen
        self.current_frame = 0

        self.state = "idle"
        self.animation_speed = 0.15

        self.animations = self.import_character_assets()

        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image =  self.mask.to_surface()


        self.direction = pygame.Vector2(0, 0)
        self.arrows = pygame.sprite.Group()


        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -16
        self.points = 0

        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.is_alive = True
        self.attacking = False
        self.is_hurt = False
        self.invulnerable = False
        self.has_key = False
        

        self.healthbar = HealthBar(400, 40, 100)

        self.cooldown_time = 1000
        self.last_action_time = 0

        self.last_hurt_time = 0

    def import_character_assets(self):
        animations = {"idle": [], "run": [], "jump": [],
                      "attack": [], "hit": [], "death": []}
        path = "./assets/player/"

        for action in animations.keys():
            full_path = path + action

            animations[action] = import_assets(full_path)

        return animations

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def increse_points(self, points):
        self.points += points

    def draw_points(self):
        font = pygame.font.SysFont("arialblack", 30)
        text_surface = font.render(
            f"Points {self.points} ", True, (250, 250, 250))
        text_rect = text_surface.get_rect(
            center=(screen_width - 100, 40))
        self.screen.blit(text_surface, text_rect)

    

    

    def move(self):

        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if self.is_alive:
            if keys[pygame.K_d]:
               

                self.direction.x = 1
                self.facing_right = True

            elif keys[pygame.K_a] and self.rect.x >= 150:
              

                self.direction.x = -1
                self.facing_right = False

            else:
                self.direction.x = 0

            if keys[pygame.K_w] and self.on_ground:
                self.jump()

            if keys[pygame.K_e]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_action_time >= self.cooldown_time:
                    self.shoot_arrow()
                    self.is_attacking = True
                    self.last_action_time = current_time

    def jump(self):
        jump.play()

        self.direction.y = self.jump_speed

    def shoot_arrow(self):
        attack.play()
        self.attacking = True
        arrow = Arrow((self.rect.centerx, self.rect.centery),
                      self.facing_right)
        self.arrows.add(arrow)

    def get_hurt(self, damage):


        if not self.invulnerable :
            enemy_attack.play()       
   
            self.invulnerable = True
            self.is_hurt = True
            self.healthbar.max_health -= damage
            self.last_hurt_time = pygame.time.get_ticks()

            if self.healthbar.max_health <= 0:
                die.play()
                self.is_alive = False
                

    def update_state(self):
        if self.is_alive:
            if self.direction.y != 0:

                self.state = 'jump'

            else:
                if self.direction.x != 0:

                    self.state = 'run'
                elif self.attacking:
                    self.state = "attack"

                elif self.is_hurt:
                    self.state = "hit"

                else:
                    self.state = 'idle'
                    
        else:

            self.state = "death"

    def animate(self):
        animation = self.animations[self.state]

        self.current_frame += self.animation_speed
        is_last_frame = self.current_frame >= len(animation)


        if is_last_frame:
            self.current_frame = 0

        if self.attacking and is_last_frame:
            self.state = "idle"
            self.attacking = False

        if self.is_hurt :
            if is_last_frame:
                self.state = "idle"
                self.is_hurt = False
           
        if not self.is_alive and is_last_frame:
            self.current_frame = len(animation) - 1
            
            

        image = animation[int(self.current_frame)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_health(self):
        return self.healthbar.max_health

    def update(self):
        self.move()
        self.draw_points()
        self.arrows.draw(self.screen)
        self.healthbar.draw(self.screen, (25, 75), "player")

        current_time = pygame.time.get_ticks()

        if current_time - self.last_hurt_time >= self.cooldown_time:
            self.invulnerable = False   

      
        
        self.arrows.update()
        self.update_state()
        self.animate()

     

       
       