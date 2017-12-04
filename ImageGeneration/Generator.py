from PIL import Image, ImageFilter
from os import listdir
from os.path import join
import random
from image_file import *
import math
from ImageGeneration.licence_plate_inserter import combine_pictures
from ImageGeneration.image_effects import randomNoise
from ImageGeneration.pyImgMarker.image_handler import read_from_file
# The dict with all the pictures in. The key is the foldername,
# and the value is an array with all pictures in said folder


# In here, we get the name for all the folders, this was originally
# intended so that it was possible to search the keynames for the folder
# that resempled the name of the needed folder the most
images_root = join("ImageGeneration", "Images")
cars_root = join(images_root, "car")
licence_plate_root = join(images_root, "licence_plates")
background_root = join(images_root, "backgrounds")
signs_root = join(images_root, "signs")


def find_file_paths():
    return {"cars": listdir(cars_root), "licenceplates": listdir(licence_plate_root),
            "backgrounds": listdir(background_root), "signs": listdir(signs_root)}

def new_generator(tbgenerated=1, wlicence=50, nolicar=75, nothing=50):
    images = []
    labels = []
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
            True: get_img(True, filepath),
            False: {
                True: get_img(False, filepath),
                False: {
                    True: None,
                    False: filepath["signs"][random.randint(0, len(filepath["signs"]))]
                }.get(has_nothing)
            }.get(has_car)
        }.get(has_licence_plate)

        background = background.resize(512, 512)

        if has_licence_plate:
            coordinates = get_coordinates(foreground)
            foreground = combine_pictures(filepath["licenceplates"][random.randint(0,len(filepath["licenceplates"]))], coordinates, foreground)

        if foreground is not None:
            foreground = Image.open(foreground)
            rotation_int = random.randint(-40, 40)
            foreground = foreground.rotate(rotation_int, expand=True)

            carWidth = math.ceil(background.size[0] / random.uniform(1.5, 5.5))
            # Get the precentage change from the width of the car to where it was
            # print(carWidth)
            wpercent = carWidth / float(foreground.size[0])
            # print(wpercent)
            # Use this magic to determine the cars height.
            carHeight = math.ceil(int((float(foreground.size[1]) * float(wpercent))))

            foreground = foreground.resize((carWidth, carHeight), Image.ANTIALIAS)

            offset = (random.randint(0, background.size[0] - foreground.size[0]),
                      random.randint(0, background.size[1] - foreground.size[1]))

            background.paste(foreground,offset,mask=foreground)

        background = apply_filter(background)
        images.append(background)
        labels.append(True if has_licence_plate else False)
    return images, labels


def get_img(w_l, filepath):
    if w_l:
        v = []
        for item in filepath["cars"]:
            if item.startswith("L"):
                v.append(item)
        return v[random.randint(0,len(v))]
    else:
        v = []
        for item in filepath["cars"]:
            if not item.startswith("L"):
                v.append(item)
        return v[random.randint(0,len(v))]


def get_coordinates(car):

    return read_from_file(join(cars_root, "imgSettings.JSON"))[car]


def apply_filter(image):
    choice = random.randint(0,2)
    if choice is 0:
        image.filter(ImageFilter.GaussianBlur(radius=random.randint[2,7]))
    elif choice is 1:
        image = randomNoise(image)

    return image
