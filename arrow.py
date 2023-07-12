import pygame


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos, flip) -> None:
        super().__init__()
        self.image = pygame.image.load(
            "./assets/player/proyectiles/arrow/arrow.png")
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 16
        self.damage = 35
        self.flip = flip

    def move(self):

        if self.flip:

            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):

        self.move()