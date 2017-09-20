from PIL import Image, ImageDraw
import numpy as np
import os
from shutil import copyfile
from PIL import Image, ImageDraw
import pygame



# Man kan enden give den en filepath til et billed eller et allerede loaded billed,
# eller begge dele, den vil så endten returnere en matrice eller flere.

def loadImageMatrix(filepath=None, loadedImage=None):
    if filepath is None and loadedImage is None:
        raise ValueError('Please insert either a filepath or a loaded image')
    elif filepath is None:
        return np.asarray(loadedImage)[:,:,:3]
    elif loadedImage is None:
        return np.asarray(Image.open(filepath))
    else:  # det er ikke min skyld at denne variable hedder bathmats... pycharm insisted.
        bathmats = (np.asarray(filepath)[:,:,:3], np.asarray(loadedImage)[:,:,:3])
        return bathmats


def watdo(filepath=None, has_lice=False):
    if filepath is None:
        raise ValueError('The file path was not found.')

    if has_lice:
        if os.path.exists("has_lice/") and os.path.isdir("has_lice/"):
            files = os.walk("has_lice/")
            tot_fil_nr = 0
            # TODO check file names and make sure that the format that we save is the same as the other files.
            for eachfile in files:
                splt = eachfile.split('-', '.')
                cur_fil_nr = int(splt[1])
                if cur_fil_nr > tot_fil_nr:
                    tot_fil_nr = cur_fil_nr

            copyfile(filepath, )


def convert_to_pygame(image):
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pygame.image.fromstring(data,size,mode)


def print_picture(loaded_image=None, filepath=None):
    if loaded_image is None and filepath is None:
        raise ValueError('Please either input a valid picture or filepath')
    elif loaded_image is None:
        pygame_image_file = pygame.image.load(filepath)
    elif filepath is None:
        pygame_image_file = convert_to_pygame(loaded_image)
    elif loaded_image and filepath:
        if Image.open(filepath) != loaded_image:
            raise ValueError('Wat are u duin? Enden den ene eller den anden dummy.')
        else:
            pygame_image_file = convert_to_pygame(loaded_image)


    screensize = (1600, 900)
    screen = pygame.display.set_mode(screensize)
    pygame_image_file = pygame.transform.scale(pygame_image_file, screensize)

    nigger = (0, 0, 0)
    screen.fill(nigger)

    screen.blit(pygame_image_file, (1, 1))
    pygame.display.flip()

    shouldContinue = True
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
