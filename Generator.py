from PIL import Image
import os
import random
from image_file import *
import math

# The dict with all the pictures in. The key is the foldername,
# and the value is an array with all pictures in said folder
dict_with_pictures = {}

# In here, we get the name for all the folders, this was originally
# intended so that it was possible to search the keynames for the folder
# that resempled the name of the needed folder the most
aliasForWithLicence = []
aliasForWithoutLicence = []
aliasForBackground = []
aliasForLicenceAndBackground = []
aliasForNoLicenceAndBackground = []


def find_filepaths(filepathes):
    # The name says it all, here we get the paths to the folders,
    # and whilest itterrating over the pictures contained in said folder,
    # we load the pictures into the dictionary.
    for filepath in filepathes:
        if not os.path.isdir(filepath):
            raise ValueError(f"Sorry" + filepath + " filepath does not exsists..")

        dict_with_pictures[os.path.basename(os.path.normpath(filepath))] = load_pictures(filepath)


def load_pictures(filepath):
    # Here is where the magic happens. We get a filepath, and then loads the images.
    # Currently the only supported formats is png, jpg and jpeg.
    # It also saves the filename (without the format) and stores it as an object of the type "DizImage"
    # TODO: Change the name of the type "DizImage" to something a bit more appealing

    picz = []
    for pictures in os.listdir(filepath):

        if pictures.endswith(".png") or pictures.endswith(".jpg"):
            picz.append(DizImage(pictures[:-4], Image.open(filepath+"/"+pictures)))
        elif pictures.endswith(".jpeg"):
            picz.append(DizImage(pictures[:-5], Image.open(filepath+"/"+pictures)))
    return picz


def checker():
    # Checker, checks if there is dictionaries with everything we need.
    # To generate data that can be used, we need both pictures with:
    # cars (with and without licenceplate) and backgrounds
    # Possibly support for background ALREADY with a car that either has licence plate or not
    dirWithLicencePlates = False
    dirWithBackgrounds = False
    dirWithoutLicenceplates = False
    dirWithBackgroundAndNoLicencePlates = False
    dirWithBackgroundAndLicencePlates = False

    for key in dict_with_pictures.keys():
        if "WithLicence" in key:

            dirWithLicencePlates = True
            aliasForWithLicence.append(key)
            aliasForWithLicence.append(len(dict_with_pictures.get(key)))
        elif "Backgrounds" in key:

            dirWithBackgrounds = True
            aliasForBackground.append(key)
            aliasForBackground.append(len(dict_with_pictures.get(key)))
        elif "WithoutLicence" in key:

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
    # Generator. As this function is the most complicated in this py file. We will descripe everything as goes


    #Firstly we find the filepaths
    find_filepaths(filepaths)

    # Check if we get parameters as "how many to generate" and "licenceplate per non-licenceplate" ratio
    if tbgenerated is None:
        tbgenerated = 1
    if lpnl is None or lpnl > 100 or lpnl < 1:
        lpnl = 50

    # Check if the folders required is there.
    try:
        checker()
    except Exception:
        print(Exception)

    # Start dir that we are going to return containing the picture + information about the picture.
    feededInfo = {}

    count = 0
    # Weighted list, where we calculate how the ratio between cars with licenceplates vs cars without
    randlst = ['licence'] * lpnl + ['no_licence'] * (100 - lpnl)

    # The big while loop that keeps generating pictures untill it is not needed anymore
    # One might think it would be more optimal to ONLY load 1 image pr function call.
    # Yet there is SO many pictures to be loaded, so if we should load and deload everything EVERY time
    # this function is called.. Well.. Shit..
    while tbgenerated > 0:

        # Rawbackground is the to get the object 'DizImage'.
        # This is to pass information about the "chocen" background later on.
        rawbackground = dict_with_pictures.get(aliasForBackground[0])[random.randint(0, (aliasForBackground[1] - 1))]
        background = rawbackground.getImage()


        # Check if in this picture there is going to be a licenceplate
        isThereALicence = random.choice(randlst)

        # Find a forground based on if there is going to be a licenceplate or knot.
        if "licence" == isThereALicence:
            rawforground = dict_with_pictures.get(aliasForWithLicence[0])[random.randint(0, (aliasForWithLicence[1] - 1))]
        else:
            rawforground = dict_with_pictures.get(aliasForWithoutLicence[0])[random.randint(0, (aliasForWithoutLicence[1] - 1))]


        # Start the creation of the new image. This image is going to support alpha (or transparrent
        # And is going to have the same dimentions as the background image.
        newImg = Image.new('RGBA',(background.size[0],background.size[1]),(0,0,0,0))

        foreground = rawforground.getImage()


        # if random.randint(0, 3) != 3 and False:
        # Rotate the picture to anything from -40 degrees to 40 degrees. Expand = true is to ensure that
        # the dimentions of the picture supports the possible change in dimentions from the rotation
        rotation_int = random.randint(-40, 40)
        foreground = foreground.rotate(rotation_int, expand=True)

        print("Image: {}\nSize: {}".format(foreground, foreground.size))
        # Som magic about the width of the car.

        min_division = 1.5 - (abs(rotation_int) / 45 * .3)
        carWidth = math.ceil(background.size[0] / random.uniform(1.5, 5.5))
        # Get the precentage change from the width of the car to where it was
        #print(carWidth)
        wpercent = carWidth / float(foreground.size[0])
        #print(wpercent)
        # Use this magic to determine the cars height.
        carHeight = math.ceil(int((float(foreground.size[1]) * float(wpercent))))

        foreground = foreground.resize((carWidth,carHeight), Image.ANTIALIAS)

        # There will be 1/4 chance that there is not going to happen shit to the picture.


        # Calculate what the offset for the forground image is going to be.
        # Based on that we don't want the picture to start in the lower right corner and be cut off
        # print("Size differentiation between background image and forground image (in that order):\n"
        #       "X: {} vs {} \n"
        #       "Y: {} vs {}".format(background.size[0],forground.size[0],background.size[1],forground.size[1]))


        offset = (random.randint(0, background.size[0] - foreground.size[0]),
                  random.randint(0, background.size[1] - foreground.size[1]))

        # Paste the background at the coordinates (0,0)
        newImg.paste(background,(0,0))
        # Paste the forground image at the coordinates (0,0) and make sure that we have alpha
        newImg.paste(foreground,offset,mask=foreground)

        # For each itteration append a new item in the dictionary with the itteration number as the key and an array as the value
        # The 1 item in said array contains the image that is the resoult of this fuckshow, the secon is the
        # forground information that we get from the 'DizImage' object
        # And the third item is the background information from the 'DizImage' object
        feededInfo[count] = [newImg,rawforground,rawbackground]

        # Incriment and decriment
        count += 1
        tbgenerated -= 1

    return feededInfo
