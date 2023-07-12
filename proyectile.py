import pygame
from utils.helpers import import_spritesheet

class Proyectile(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()

        self.image = pygame.image.load("./assets/enemys/flyingEye/proyectile.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.Vector2(0,0)

        self.gravity = 0.4
        self.damage = 8

    # def import_proyectile(self):
    #     image = import_spritesheet("./assets/enemys/flyingEye/proyectile")
    #     print(image)
    #     return image
    
    
    def apply_gravity(self):

        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    
   

    def update(self, move_world, move_world_y):
        
        self.rect.x += move_world
        self.rect.y += move_world_y


        self.apply_gravity()