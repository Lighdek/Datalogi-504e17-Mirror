from os import listdir
from os.path import join

import pygame
import simplejson as json

loaded_imgs = {}


def read_from_file(file_path):
    global loaded_imgs
    with open(file_path) as f:
        file_text = f.read()
        if len(file_text) > 0:
            loaded_imgs = json.loads(file_text)
    return loaded_imgs


def write_to_file(file_path):
    global loaded_imgs
    with open(file_path, 'w') as f:
        json.dump(loaded_imgs, f)


def main_imgs(file_path, root_folder):
    global loaded_imgs
    read_from_file(file_path)
    # Check if there is any pictures.

    files = listdir(root_folder)

    for filename in files:
        print(filename)
        if not filename in loaded_imgs:
            coordinates = print_pictures(pygame.image.load(join(root_folder, filename)))
            if coordinates is False:
                break
            loaded_imgs[filename] = coordinates

    write_to_file(file_path)


def print_pictures(picture):
    coordinates = []
    print("now to print")
    screen = pygame.display.set_mode(picture.get_rect().size)
    default_color=(0,0,0)
    main_loop = True
    screen.fill(default_color)
    screen.blit(picture,(1,1))
    exitted = False
    while main_loop:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == 27\
                        or event.type == pygame.QUIT:
                main_loop = False
                exitted = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coordinates = pygame.mouse.get_pos()
                pygame.draw.circle(screen,0xff0000,mouse_coordinates,5,5)
                coordinates.append(mouse_coordinates)
                if len(coordinates) == 4:
                    main_loop = False

        pygame.display.update()

    return coordinates if not exitted else False


