import os
from natsort import natsorted
import pygame, json
import csv
from settings import tile_size


def import_csv(path):

    with open(path) as file:
        map = []
        level_list = csv.reader(file, delimiter=",")

        for row in level_list:
            map.append(row)
        return map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    surface_width, surface_height = surface.get_size()
    tile_num_x = int(surface_width / tile_size)
    tile_num_y = int(surface_height / tile_size)

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface(
                (tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(
                x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)

    return cut_tiles


def import_spritesheet(path):

    spritesheet = pygame.image.load(f"{path}.png").convert_alpha()
    image_width = spritesheet.get_width()
    image_height = spritesheet.get_height()

    image_qty = int(image_width / image_height)

    images = []
    for i in range(image_qty):
        rect = pygame.Rect(i * image_height, 0, image_height, image_height)
        image = spritesheet.subsurface(rect)
        image = image.subsurface(pygame.Rect(55, 50, 60, 53))
        image = pygame.transform.scale(
            image, (image.get_width() * 2, image.get_height() * 2))
        images.append(image)

    return images


def import_assets(path):

    files_list = []

    for __, __, images in os.walk(path):

        sorted_images = natsorted(images)
        for image in sorted_images:
            image = pygame.image.load(f"{path}/{image}")
            # image = image.subsurface((100, 60), (82, 68))
            scaled_image = pygame.transform.scale(
                image, (image.get_width() * 2.5, image.get_height() * 2.5))
            files_list.append(scaled_image)

    return files_list


def save_game(path, data):
    if os.path.exists(path):       
        try:
            with open(path, 'r') as file:
                json_file = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):          
            json_file = []
    else:       
        json_file = []
   
    json_file.append(data)
   
    with open(path, 'w') as file:
        json.dump(json_file, file, indent=4)

