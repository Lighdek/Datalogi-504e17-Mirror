from PIL import Image, ImageDraw
import numpy as np
import os
from shutil import copyfile
from PIL import Image
import pygame
import math


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


# Man kan enden give den en filepath til et billed eller et allerede loaded billed,
# eller begge dele, den vil så endten returnere en matrice eller flere.
def loadImageMatrix(filepath=None, loadedImage=None, Alpha=False):
    if filepath is None and loadedImage is None:
        raise ValueError('Please insert either a filepath or a loaded image')
    elif filepath is None:
        in_the_end = np.asarray(loadedImage)
    elif loadedImage is None:
        in_the_end = np.asarray(Image.open(filepath))
    else:  # det er ikke min skyld at denne variable hedder bathmats... pycharm insisted.
        bathmats = (np.asarray(filepath)[:,:,:3], np.asarray(loadedImage)[:,:,:3])
        return bathmats

    if not Alpha:
        in_the_end = in_the_end[:,:,:3]

    return np.array(in_the_end)

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

            copyfile(filepath)


def convert_to_pygame(image):
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pygame.image.fromstring(data,size,mode)


def print_picture(loaded_image=None, filepath=None):
    if loaded_image is None and filepath is None:
        raise ValueError('Please either input a valid picture or filepath')
    elif loaded_image is None:
        pygame_image_file = pygame.image.load_basic(filepath)
    elif filepath is None:
        pygame_image_file = convert_to_pygame(loaded_image)
    else:
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


def combinePics(loaded_imagessss=None, filepathes = None):
    if loaded_imagessss is None and filepathes is None:
        raise ValueError('Please either put pictures or filepathess into this function.')

    elif loaded_imagessss is not None and len(loaded_imagessss) is 1 or filepathes is not None and len(filepathes) is 1:
        raise ValueError('Please insert more than one picture....')

    elif loaded_imagessss is None:
        pictures = []
        for filepath in filepathes:
            pictures.append(Image.open(filepath))
        __loadPictures(pictures)

    elif filepathes is None:
        __loadPictures(loaded_imagessss)


    else:
        raise ValueError('Please only send one or the other. I can\'t handle both senpi </3')


def __loadPictures(imgs):
    length = len(imgs)
    print (length)
    collum = row = 0
    size_w, size_h = 500, 300
    if length <= 5 :
        divfive = 1
        bg_s_w = length * size_w
    else:
        divfive = math.ceil(length / 5)
        bg_s_w = 5 * size_w

    background = Image.new('RGBA',(bg_s_w, divfive * size_h),(255, 255, 255, 255))
    print(background.size)
    while row < divfive:
        while collum < 5:
            index = collum + row * 5
            if index is length :
                break

            img = imgs[index]
            img = img.resize((size_w, size_h), Image.LANCZOS)
            offset = collum * size_w, row * size_h
            background.paste(img, offset)
            collum += 1

        collum = 0
        row += 1
    print_picture(loaded_image=background)

