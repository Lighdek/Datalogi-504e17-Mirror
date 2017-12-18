from PIL import Image, ImageFilter
from os import listdir
from os.path import join, dirname, basename
import random
import numpy as np

from ImageGeneration.image_effects import randomNoise, change_color
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
    return {"cars": listdir(cars_root), "licenseplates": listdir(licence_plate_root),
            "backgrounds": listdir(background_root), "signs": listdir(signs_root)}


rotate_between = ()


def Generator(tbgenerated=1, max_noise = 4, set_amount_of_noise = False, rotate_degrees=(-30,30),
              size_difference_noise=(1.5, 3), size_difference_license=(1.3, 2),  wlicence=.50,
              nolicar=.75, nothing=.50, size=(512,512), blur = .3, rndom_noise = .3, blur_amount_random = (0, 2),
              noise_amount_random = (3, 10)):
    global rotate_between
    images = []
    labels = []
    rotate_between = rotate_degrees

    filepath = find_file_paths()

    if any(v < 0.0 or v > 1.0 for v in [wlicence, nolicar, nothing, blur, rndom_noise]):
        raise ValueError(f"generator rates must be between 0.0 and 1.0"
                         f"wlicence: {wlicence}"
                         f"nolicar: {nolicar}"
                         f"nothing: {nothing}"
                         f"blur: {blur}"
                         f"rndom_noise: {rndom_noise}")

    for x in range(0, tbgenerated):
        noises = []

        chocen_license_plate = Image.open(join(licence_plate_root, filepath["licenseplates"][random.randint(0, len(filepath["licenseplates"]) - 1 )]))
        background = Image.open(join(background_root,filepath["backgrounds"][random.randint(0, len(filepath["backgrounds"])- 1)]))

        has_licence_plate = True if random.random() < wlicence else False
        noise_loop = True

        while noise_loop:
            if random.random() < nolicar:
                noises.append(Image.open(join(cars_root, filepath["cars"][random.randint(0, len(filepath["cars"]) - 1 )])))

            elif random.random() >= nothing and has_licence_plate is False:
                noises.append(Image.open(join(signs_root, filepath["signs"][random.randint(0, len(filepath["signs"]) - 1)])))

            noise_loop = False if ((set_amount_of_noise is not False or set_amount_of_noise is not None)
                                   and len(noises) >= set_amount_of_noise) or random.randint(0, max_noise) <= len(noises) else True

        background = background.resize(size)

        for noise in noises:
            noise, offset = image_manipulationsss(noise, background.size, size_difference_noise)

            try:
                noise = change_color(noise, random.random())
            except Exception:
                print(f"forground_data: {list(noise.getdata())}")
                raise
            background.paste(noise,offset,mask=noise)

        if has_licence_plate:
            chocen_license_plate, offset = image_manipulationsss(chocen_license_plate, background.size, size_difference_license)
            background.paste(chocen_license_plate, offset, mask=chocen_license_plate)

        background = apply_filter(background, blur, rndom_noise, blur_amount_random, noise_amount_random)

        images.append(np.asarray(background))

        labels.append(has_licence_plate)

    return images, labels


def image_manipulationsss(fg, bgsize, sd):
    rotation_int = random.randint(rotate_between[0], rotate_between[1])
    fg = fg.rotate(rotation_int, expand=True)

    scale = min(bgsize[0] / random.uniform(sd[0], sd[1]) / fg.size[0],
                bgsize[1] / random.uniform(sd[0], sd[1]) / fg.size[1])

    fg = fg.resize((int(fg.size[0] * scale), int(fg.size[1] * scale)), Image.ANTIALIAS)

    offset = (random.randint(0, bgsize[0] - fg.size[0]),
              random.randint(0, bgsize[1] - fg.size[1]))
    return fg, offset


def apply_filter(image, blur, rndom_noise, blur_amount_random, noise_amount_random):
    choice = random.random()
    if choice < blur:
        pass
        #image = image.filter(ImageFilter.GaussianBlur(radius=(random.randint(blur_amount_random[0],blur_amount_random[1]))))
    elif choice < blur + rndom_noise:
        image = randomNoise(image, random.randint(noise_amount_random[0], noise_amount_random[1]))

    return image
