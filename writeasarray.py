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
        return np.asarray(loadedImage)
    elif loadedImage is None:
        return np.asarray(Image.open(filepath))
    else:  # det er ikke min skyld at denne variable hedder bathmats... pycharm insisted.
        bathmats = (np.asarray(filepath), np.asarray(loadedImage))
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


def print_picture(images=None,filepath=None):
    if images is None and filepath is None:
        raise ValueError('Please either input a valid picture or filepath')
    elif images is None:
        images = Image.open(filepath)
    elif images and filepath:
        if Image.OPEN(filepath) != images:
            raise ValueError('Wat are u duin? Enden den ene eller den anden dummy.')

    screensize = (1600, 900)
    screen = pygame.display.set_mode(screensize)

    print(images.format)
    image = pygame.image.load(images)
    image.transform.scale(image, screensize)
    nigger = (0, 0, 0)
    screen.fill(nigger)
    screen.blit(image(1, 1))
    pygame.display.flip()
    shouldContinue = True
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.typpe == pygame.KEYDOWN:
                waiting = False
