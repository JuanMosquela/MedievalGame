import pygame

# ------------------------Game------------------------


screen_width = 900
screen_height = 620
tile_size = 16

# ------------------------Colors------------------------

black = (0, 0, 0)
white = (255, 255, 255)

# ------------------------Sounds------------------------
pygame.mixer.init()

#player
attack = pygame.mixer.Sound("./sounds/player/attack.wav")
jump = pygame.mixer.Sound("./sounds/player/jump.wav")
land = pygame.mixer.Sound("./sounds/player/land.wav")
die = pygame.mixer.Sound("./sounds/player/die.wav")
walk = pygame.mixer.Sound("./sounds/player/walk.wav")
hurt = pygame.mixer.Sound("./sounds/player/hurt.wav")

#enemys
enemy_attack = pygame.mixer.Sound("./sounds/enemys/attack.wav")
enemy_hurt = pygame.mixer.Sound("./sounds/enemys/hurt.wav")
enemy_die = pygame.mixer.Sound("./sounds/enemys/die.wav")


#items
coin_sound = pygame.mixer.Sound("./sounds/coin.wav")
key_sound = pygame.mixer.Sound("./sounds/key.wav")

#background
game = pygame.mixer.Sound("./sounds/game.mp3")
menu = pygame.mixer.Sound("./sounds/menu.mp3")


background_sounds = [ game, menu ]

for sound in background_sounds:
    sound.set_volume(0.15)





