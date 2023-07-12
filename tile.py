import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()

        self.image = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, move, move_y):
        self.rect.x += move
        self.rect.y += move_y


class StaticTile(Tile):
    def __init__(self, x, y, size, surface):
        super().__init__(x, y, size)
        self.image = surface
        self.mask = pygame.mask.from_surface(self.image)

class Tramp(StaticTile):
    def __init__(self, x, y, size, surface):
        super().__init__(x, y, size, surface)
        self.damage = 15
