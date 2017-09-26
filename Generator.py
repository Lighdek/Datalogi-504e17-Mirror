from PIL import Image
# import pygame
import os
import random
from help_functions import print_picture
from image_file import *
import math


dict_with_pictures = {}

aliasForWithLicence = []
aliasForWithoutLicence = []
aliasForBackground = []
aliasForLicenceAndBackground = []
aliasForNoLicenceAndBackground = []


def find_filepaths(filepathes):
    for filepath in filepathes:
        if not os.path.isdir(filepath):
            raise ValueError(f"Sorry" + filepath + " filepath does not exsists..")

        dict_with_pictures[os.path.basename(os.path.normpath(filepath))] = load_pictures(filepath)


def load_pictures(filepath):
    picz = []
    for pictures in os.listdir(filepath):
        #print(pictures)
        if pictures.endswith(".png") or pictures.endswith(".jpg"):
            picz.append(DizImage(pictures[:-4], Image.open(filepath+"/"+pictures)))
        elif pictures.endswith(".jpeg"):
            picz.append(DizImage(pictures[:-5], Image.open(filepath+"/"+pictures)))
    return picz
def checker():
    dirWithLicencePlates = False
    dirWithBackgrounds = False
    dirWithoutLicenceplates = False
    dirWithBackgroundAndNoLicencePlates = False
    dirWithBackgroundAndLicencePlates = False

    for key in dict_with_pictures.keys():
        if "WithLicence" in key:
            # print ("bob")
            dirWithLicencePlates = True
            aliasForWithLicence.append(key)
            aliasForWithLicence.append(len(dict_with_pictures.get(key)))
        elif "Backgrounds" in key:
            # print("kurt")
            dirWithBackgrounds = True
            aliasForBackground.append(key)
            aliasForBackground.append(len(dict_with_pictures.get(key)))
        elif "WithoutLicence" in key:
            # print("søren")
            dirWithoutLicenceplates = True
            aliasForWithoutLicence.append(key)
            aliasForWithoutLicence.append(len(dict_with_pictures.get(key)))
        elif "BackgroundAndCarWithLicence" in key:
            dirWithBackgroundAndLicencePlates = True
            aliasForLicenceAndBackground.append(key)
            aliasForLicenceAndBackground.append(len(dict_with_pictures.get(key)))
        elif "BackgroundAndCarWithoutLicence" in key:
            dirWithBackgroundAndNoLicencePlates = True
            aliasForNoLicenceAndBackground.append(key)
            aliasForNoLicenceAndBackground.append(len(dict_with_pictures.get(key)))

    if not dirWithoutLicenceplates or not dirWithBackgrounds or not dirWithLicencePlates:
        raise ValueError(f"Sorry you did not provide a dir in one of the following catagories\n"
                         f"dirWithLicencePlates = " + str(dirWithLicencePlates) + "\n"
                         f"dirWithBackgrounds = " + str(dirWithBackgrounds) + "\n"
                         f"dirWithoutLicenceplates = " + str(dirWithoutLicenceplates))

def generator(filepaths, tbgenerated=None, lpnl=None):
    find_filepaths(filepaths)

    if tbgenerated is None:
        tbgenerated = 1
    if lpnl is None or lpnl > 100 or lpnl < 1:
        lpnl = 50

    try:
        checker()
    except Exception:
        print(Exception)

    feededInfo = {}

    randlst = ['licence'] * lpnl + ['no_licence'] * (100 - lpnl)
    count = 0
    while tbgenerated > 0:
        # print(aliasForBackground[0])
        testRandInt = random.randint(0, (aliasForBackground[1] - 1))
        # print (testRandInt)

        rawbackground = dict_with_pictures.get(aliasForBackground[0])[testRandInt]
        background = rawbackground.getImage()

        isThereALicence = random.choice(randlst)

        if "licence" == isThereALicence:
            rawforground = dict_with_pictures.get(aliasForWithLicence[0])[random.randint(0, (aliasForWithLicence[1] - 1))]
        else:
            rawforground = dict_with_pictures.get(aliasForWithoutLicence[0])[random.randint(0, (aliasForWithoutLicence[1] - 1))]


        newImg = Image.new('RGBA',(background.size[0],background.size[1]),(0,0,0,0))

        forground = rawforground.getImage()

        carWidth = math.ceil(background.size[0] / random.uniform(1.5, 5.5))

        wpercent = carWidth / float(forground.size[0])
        carHeight = math.ceil(int((float(forground.size[1]) * float(wpercent))))

        forground = forground.resize((carWidth, carHeight), Image.ANTIALIAS)

        if random.randint(0, 3) != 3:
            forground = forground.rotate(random.randint(-40, 40), expand=True)

        offset = (random.randint(0, background.size[0] - forground.size[0]),
                  random.randint(0, background.size[1] - forground.size[1]))
        newImg.paste(background,(0,0))
        newImg.paste(forground,offset,mask=forground)

        feededInfo[count] = [newImg,rawforground,rawbackground]
        count += 1
        tbgenerated -= 1

    return feededInfo
