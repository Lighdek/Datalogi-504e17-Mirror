from PIL import Image, ImageFilter
from os import listdir
from os.path import join, dirname,basename
import random
import numpy as np

from ImageGeneration.licence_plate_inserter import combine_pictures
from ImageGeneration.image_effects import randomNoise, change_color
from ImageGeneration.pyImgMarker.image_handler import read_from_file
# The dict with all the pictures in. The key is the foldername,
# and the value is an array with all pictures in said folder


# In here, we get the name for all the folders, this was originally
# intended so that it was possible to search the keynames for the folder
# that resempled the name of the needed folder the most

images_root = join(dirname(__file__), "Images")
cars_root = join(images_root, "car")
licence_plate_root = join(images_root, "licence_plates")
background_root = join(images_root, "backgrounds")
signs_root = join(images_root, "signs")


def find_file_paths():
    return {"cars": listdir(cars_root), "licenceplates": listdir(licence_plate_root),
            "backgrounds": listdir(background_root), "signs": listdir(signs_root)}


def Generator(tbgenerated=1, wlicence=.50, nolicar=.75, nothing=.50, size=(256,256)):
    images = []
    labels = []
    filepath = find_file_paths()

    if any(v < 0.0 or v > 1.0 for v in [wlicence, nolicar, nothing]):
        raise ValueError(f"generator rates must be between 0.0 and 1.0"
                         f"wlicence: {wlicence}"
                         f"nolicar: {nolicar}"
                         f"nothing: {nothing}")

    for x in range(0, tbgenerated):
        chosen_bg = filepath["backgrounds"][random.randint(0, len(filepath["backgrounds"])- 1)]
        background = Image.open(join(background_root, chosen_bg))

        has_licence_plate = True if random.random() < wlicence else False
        has_car = True if random.random() < nolicar else False
        has_nothing = True if random.random() < nothing else False

        chosen_foreground = {
            True: get_img(True, filepath),
            False: {
                True: get_img(False, filepath),
                False: {
                    True: None,
                    False: join(signs_root, filepath["signs"][random.randint(0, len(filepath["signs"]) - 1 )])
                }.get(has_nothing)
            }.get(has_car)
        }.get(has_licence_plate)
        background = background.resize(size)


        if chosen_foreground is not None:
            foreground = Image.open(chosen_foreground)
            if has_licence_plate:
                coordinates = get_coordinates(chosen_foreground)
                foreground = combine_pictures( foreground, coordinates, join(licence_plate_root, filepath["licenceplates"][random.randint(0, len(filepath["licenceplates"]) - 1)]))

            scale = min(background.size[0] / random.uniform(1.5, 3) / foreground.size[0],
                        background.size[1] / random.uniform(1.5, 3) / foreground.size[1])

            rotation_int = random.randint(-40, 40)
            foreground = foreground.rotate(rotation_int, expand=True)

            foreground = foreground.resize((int(foreground.size[0]*scale), int(foreground.size[1]*scale)), Image.ANTIALIAS)

            offset = (random.randint(0, background.size[0] - foreground.size[0]),
                      random.randint(0, background.size[1] - foreground.size[1]))
            try:
                foreground = change_color(foreground, random.random())
            except Exception:
                print(f"forground_data: {list(foreground.getdata())}")
                raise
            background.paste(foreground,offset,mask=foreground)

        background = apply_filter(background)
        images.append(np.asarray(background))
        labels.append(0 if has_licence_plate else 1 if has_car else 2 if not has_nothing else 3)
    return images, labels


def get_img(w_l, filepath):
    v = []
    if w_l:
        for item in filepath["cars"]:
            if item.startswith("L"):
                v.append(item)

    else:
        for item in filepath["cars"]:
            if not item.startswith("L"):
                v.append(item)

    return join(cars_root, v[random.randint(0, len(v) - 1)])


def get_coordinates(car):

    return read_from_file(join(images_root, "imgSettings.JSON"))[basename(car)]


def apply_filter(image):
    choice = random.randint(0,2)
    if choice is 0:
        img = image.filter(ImageFilter.GaussianBlur(radius=(random.randint(1,4))))
    elif choice is 1:
        img = randomNoise(image, random.randint(3, 10))
    else:
        img = image
    return img
