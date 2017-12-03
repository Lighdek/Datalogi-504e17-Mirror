from PIL import Image
from os import listdir
from os.path import isdir, join
import random
from image_file import *
import math
from ImageGeneration.licence_plate_inserter import combine_pictures
from ImageGeneration.pyImgMarker.image_handler import read_from_file
# The dict with all the pictures in. The key is the foldername,
# and the value is an array with all pictures in said folder


# In here, we get the name for all the folders, this was originally
# intended so that it was possible to search the keynames for the folder
# that resempled the name of the needed folder the most
images_root = join("ImageGeneration", "Images")
cars_root = join(images_root, "car")
cars_l_root = join(images_root, "car_l")
licence_plate_root = join(images_root, "licence_plates")
background_root = join(images_root, "backgrounds")
signs_root = join(images_root, "signs")


def find_file_paths():
    return {"cars": listdir(cars_root), "licenceplates": listdir(licence_plate_root),
            "backgrounds": listdir(background_root), "signs": listdir(signs_root),
            "cars_l": listdir(cars_l_root).extend(listdir(cars_root))}

def new_generator(tbgenerated=1, wlicence=50, nolicar=75, nothing=50):
    feededInfo = {}
    filepath = find_file_paths()

    if any(v <= 0 or v >= 100 for v in [tbgenerated, wlicence, nolicar, nothing]):
        raise ValueError("lpnl must be larger than 0.0 and less than 1.0")

    for x in range(0, tbgenerated):
        chosen_bg = filepath["backgrounds"][random.randint(0, len(filepath["backgrounds"]))]
        background = Image.open(join(background_root, chosen_bg))

        has_licence_plate = True if random.randint(1, 100) < wlicence else False
        has_car = True if random.randint(1, 100) < nolicar else False
        has_nothing = True if random.randint(1, 100) < nothing else False

        foreground = {
            True: filepath["cars_l"][random.randint(0, len(filepath["cars_l"]))],
            False: {
                True: filepath["car"][random.randint(0, len(filepath["cars"]))],
                False: {
                    True: None,
                    False: filepath["signs"][random.randint(0, len(filepath["signs"]))]
                }.get(has_nothing)
            }.get(has_car)
        }.get(has_licence_plate)

        if(has_licence_plate):
            coordinates = get_coordinates(foreground)

def get_coordinates(car):

    pass

def generator(filepaths, tbgenerated=1, licenseplatePercentage=50):
    # Generator. As this function is the most complicated in this py file. We will descripe everything as goes


    #Firstly we find the filepaths
    find_file_paths(filepaths)

    # Check if we get parameters as "how many to generate" and "licenceplate per non-licenceplate" ratio

    if licenseplatePercentage >= 1.0 or licenseplatePercentage <= 0.0:
        raise ValueError("lpnl must be larger than 0 and smaller than 100")

    # Check if the folders required is there.
    checker()

    # Start dir that we are going to return containing the picture + information about the picture.
    feededInfo = {}

    count = 0
    # Weighted list, where we calculate how the ratio between cars with licenceplates vs cars without
    #randlst = ['licence'] * licenseplatePercentage + ['no_licence'] * (100 - licenseplatePercentage)

    # The big while loop that keeps generating pictures untill it is not needed anymore
    # One might think it would be more optimal to ONLY load 1 image pr function call.
    # Yet there is SO many pictures to be loaded, so if we should load and deload everything EVERY time
    # this function is called.. Well.. Shit..
    while tbgenerated > 0:

        # Rawbackground is the to get the object 'DizImage'.
        # This is to pass information about the "chosen" background later on.
        rawbackground = dict_with_pictures.get(aliasForBackground[0])[random.randint(0, (aliasForBackground[1] - 1))]
        background = rawbackground.get_image()

        # Find a foreground based on if there is going to be a licence plate or knot.
        if random.random() < licenseplatePercentage:
            rawForeground = dict_with_pictures.get(aliasForWithLicence[0])[random.randint(0, (aliasForWithLicence[1] - 1))]
        else:
            rawForeground = dict_with_pictures.get(aliasForWithoutLicence[0])[random.randint(0, (aliasForWithoutLicence[1] - 1))]

        # Start the creation of the new image. This image is going to support alpha (or transparrent
        # And is going to have the same dimentions as the background image.
        newImg = Image.new('RGBA', (background.size[0], background.size[1]), (0, 0, 0, 0))

        foreground = rawForeground.get_image()

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

        foreground = foreground.resize((carWidth, carHeight), Image.ANTIALIAS)

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
        newImg = newImg.resize(512,512)
        # For each itteration append a new item in the dictionary with the itteration number as the key and an array as the value
        # The 1 item in said array contains the image that is the resoult of this fuckshow, the secon is the
        # forground information that we get from the 'DizImage' object
        # And the third item is the background information from the 'DizImage' object
        feededInfo[count] = [newImg,rawForeground,rawbackground]

        # Incriment and decriment
        count += 1
        tbgenerated -= 1

    return feededInfo
