import pygame
from random import randint
from utils.helpers import import_spritesheet, import_assets
from healthbar import HealthBar
from settings import *
from proyectile import Proyectile


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, type, health, damage, speed, reward, screen, player) -> None:
        super().__init__()
        self.type = type
        self.animations = self.import_enemy_assets()
        self.pos = pos
        self.screen = screen
        self.player = player

        self.current_frame = 0
        self.frame_velocity = 0.15
        self.gravity = 0.8
        self.state = None
        self.image = None  # No asignar ninguna imagen aún
        self.rect = None  # No asignar ningún rectángulo aún
        self.mask = None  # No asignar ninguna máscara aún

        self.flipped = True

        self.health = health
        self.damage = damage
        self.speed = speed
        self.reward = reward
        self.hit = False

        self.direction = pygame.Vector2(0, 0)
        self.healthbar = HealthBar(150, 10, self.health)
        self.gravity = 0.8

        self.current_frame = 0
        self.player_detected = False

        self.on_ground = False

        self.is_alive = True
        self.is_attacking = False
        self.is_hurt = False
        self.horizontal_collision = False

        # death cooldown
        self.cooldown = 2000
        self.death_timer = 0

        # attack cooldown
        self.attack_cooldown = 2000
        self.last_attack = 0

    def set_initial_state(self):
        raise NotImplementedError(
            "Subclass must implement set_initial_state()")

    def apply_gravity(self):
        if self.type != "flyingEye" or not self.is_alive:

            self.direction.y += self.gravity
            self.rect.y += self.direction.y

    def import_enemy_assets(self):
        enemy_path = f"./assets/enemys/{self.type}/"

        animations = {"idle": [], "attack": [],
                      "hit": [], "death": [], "run": []}

        for animation in animations.keys():
            full_path = enemy_path + animation

            animations[animation] = import_spritesheet(full_path)

        return animations

    def take_damage(self, arrow_damage):

        self.healthbar.max_health -= arrow_damage
        if self.healthbar.max_health <= 0:
            enemy_die.play()

            self.is_alive = False
            self.death_timer = pygame.time.get_ticks()
            self.player.increse_points(self.reward)

        else:
            enemy_hurt.play()
            self.is_hurt = True

    def attack(self):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= self.attack_cooldown and self.player.is_alive and self.is_alive:

            self.current_frame = 0
            self.last_attack = current_time
            self.is_attacking = True

    def update_state(self):
        if not self.is_alive:
            self.state = "death"

        else:
            if self.is_hurt:
                self.state = "hit"
            elif self.direction.x != 0:
                self.state = "run"
            elif self.is_attacking:
                self.state = "attack"

    def animation(self):

        animation = self.animations[self.state]

        self.current_frame += self.frame_velocity

        is_last_frame = self.current_frame >= len(animation)

        if is_last_frame:
            self.current_frame = 0

        if self.is_hurt and is_last_frame:
            self.is_hurt = False
            self.state = "run"

        if self.is_attacking:
            if self.type != "boss":
                if int(self.current_frame) == 7:
                   

                    if pygame.sprite.collide_rect(self.player, self):

                        self.player.get_hurt(self.damage)
            else:
                if int(self.current_frame) == 11:
                

                    if pygame.sprite.collide_rect(self.player, self):

                        self.player.get_hurt(self.damage)

            if is_last_frame:

                self.is_attacking = False
                self.hit = False
                self.state = "run"

        if not self.is_alive and is_last_frame:

            self.current_frame = len(animation) - 1
            current_time = pygame.time.get_ticks()

            if current_time - self.death_timer >= self.cooldown:
                self.kill()

        self.image = animation[int(self.current_frame)]

        if self.flipped:
            flipped_image = pygame.transform.flip(self.image, True, False)
            self.image = flipped_image

    def update(self,  move_world, move_world_y):

        self.rect.x += move_world
        self.rect.y += move_world_y

        self.update_state()
        self.healthbar.draw(
            self.screen, (self.rect.centerx, self.rect.top), "enemy")
        self.animation()


class NormalEnemy(Enemy):
    def __init__(self, pos, type, health, damage, speed, reward, screen, player) -> None:
        super().__init__(pos, type, health, damage, speed, reward, screen, player)

        self.state = "idle"

        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def check_collision(self, rect):
        if pygame.sprite.collide_rect(rect, self.player):
            self.player_detected = True

    def update_enemy_vision(self):
        rect_width = 200
        vision_rect = pygame.Rect(self.rect.centerx - rect_width - (self.rect.width / 2),
                                  self.rect.centery - (self.rect.height / 2),
                                  rect_width, 50)
        collision_sprite = pygame.sprite.Sprite()
        collision_sprite.rect = vision_rect

        self.check_collision(collision_sprite)

    def move(self):

        if self.is_alive:

            if self.player_detected or self.healthbar.max_health < self.health:
                if self.type != "boss":
                    distance = 40
                else:
                    distance = 180

                if self.rect.centerx > self.player.rect.centerx + distance:
                    self.rect.x -= self.speed
                    self.direction.x = -1
                    if not self.flipped:
                        self.flipped = True
                elif self.rect.centerx < self.player.rect.centerx - distance:
                    self.rect.x += self.speed
                    self.direction.x = 1
                    if self.flipped:
                        self.flipped = False
                else:
                    self.direction.x = 0

    def update(self,  move_world, move_world_y):

        self.rect.x += move_world
        self.rect.y += move_world_y

        self.move()

        self.update_state()

        self.healthbar.draw(
            self.screen, (self.rect.centerx, self.rect.top), "enemy")

        self.update_enemy_vision()

        self.animation()


class FlyingEnemy(Enemy):
    def __init__(self, pos, type, health, damage, speed, reward, screen, player) -> None:
        super().__init__(pos, type, health, damage, speed, reward, screen, player)
        self.state = "run"
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.distance = 0
        self.flipped = False

        self.proyectiles = pygame.sprite.Group()

    def import_enemy_assets(self):
        enemy_path = f"./assets/enemys/{self.type}/"

        animations = {"attack": [], "run": [], "hit": [], "death": []}

        for animation in animations.keys():
            full_path = enemy_path + animation

            animations[animation] = import_spritesheet(full_path)

        return animations

    def change_direction(self):

        self.speed = -self.speed
        self.flipped = not self.flipped

    def fly(self):
        if self.is_alive:
            self.rect.x += self.speed

    def shoot(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_attack >= self.attack_cooldown and self.is_alive:

            self.last_attack = current_time
            self.is_attacking = True

            proyectile = Proyectile((self.rect.centerx, self.rect.centery))
            self.proyectiles.add(proyectile)

    def update_state(self):
        if not self.is_alive:
            self.state = "death"
            self.frame_velocity = 0.05
        else:
            if self.is_hurt:
                self.state = "hit"
            elif self.direction.x != 0:
                self.state = "run"
            elif self.is_attacking:
                self.state = "attack"

    def get_projectiles(self):
        return self.proyectiles

    def update(self,  move_world, move_world_y):

        self.rect.x += move_world
        self.rect.y += move_world_y

        self.fly()
        self.update_state()
        self.shoot()

        self.proyectiles.draw(self.screen)
        self.proyectiles.update(move_world, move_world_y)

        self.healthbar.draw(
            self.screen, (self.rect.centerx, self.rect.top), "enemy")

        self.animation()


class Boss(NormalEnemy):
    def __init__(self, pos, type, health, damage, speed, reward, screen, player, level) -> None:
        super().__init__(pos, type, health, damage, speed, reward, screen, player)
        self.player_detected = True

        self.level = level
        self.SPAWN_ENEMIES = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_ENEMIES, 5000)

    def flip_images(self, image_list):
        flipped_images = []
        for image in image_list:
            flipped_image = pygame.transform.flip(image, True, False)
            # image = flipped_image.subsurface(pygame.Rect(85, 40, 126, 119))
            flipped_images.append(flipped_image)
        return flipped_images

    def spawn_random_enemy(self):
        random_int = randint(1, 4)
        random_origin = randint(1, 2)

        if random_origin == 1:
            origin = 0
        else:
            origin = screen_width

        match(random_int):
            case 1:
                type = "goblin"
            case 2:
                type = "mushroom"
            case 3:
                type = "skeleton"
            case 4:
                type = "flyingEye"

        if type != "flyingEye":

            enemy = NormalEnemy((origin, 500), type, 150, 15,
                                2, 25, self.screen, self.player)
            enemy.player_detected = True

        else:
            enemy = FlyingEnemy((0, 100), type, 50, 15, 4,
                                25, self.screen, self.player)

        self.level.add_enemies(enemy)

    def import_enemy_assets(self):
        animations = {"idle": [], "run": [],
                      "attack": [], "hit": [], "death": []}
        path = "./assets/enemys/boss/"

        for action in animations.keys():
            full_path = path + action

            image_list = import_assets(full_path)
            animations[action] = self.flip_images(image_list)

        return animations

    def handle_event(self, event):
        if event.type == self.SPAWN_ENEMIES and self.is_alive:
            self.spawn_random_enemy()
