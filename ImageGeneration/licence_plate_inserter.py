from PIL import Image, ImageDraw
from os import listdir
from os.path import exists, join
from ImageGeneration.pyImgMarker.image_handler import read_from_file
import random
import cv2
import numpy as np




licence_plate_root = 'licenceplates'
img_root = 'images'
settings = 'imgSettings.JSON'
saved_root = 'combined'


def main():
    coordinates = {}
    cars = []
    licence_plates = []


    if exists(settings):
        coordinates = read_from_file(settings)
    else:
        raise ValueError('You need to have some pictures labeled before starting this shit')

    for image in listdir(licence_plate_root):
        licence_plates.append(image)

    for image in listdir(img_root):
        cars.append(image)

    if len(licence_plates) <= 0:
        raise ValueError('No pictures only with licence plates')

    if len(cars) <= 0:
        raise ValueError('No pictures of cars')

def insert_pictures(cars, coordinates, licence_plates):
    editited = []


    for car in cars:
        car_coordinats = []
        try:
            car_coordinats = coordinates[car]
        except:
            print("Nothing for car: " + car)
            editited.append(Image.open(join(img_root, car)))
            pass

        return combine_pictures(car, car_coordinats, licence_plates)


def combine_pictures(car, car_coordinats, licence_plates):
    editited = []
    for x in range(1, random.randint(0, len(licence_plates) / 2)):
        deformed_license_plate = four_point_transform(Image.open(join(licence_plate_root, "nummerplade" +
                                        str(random.randint(1, len(licence_plates))) + ".png")), car_coordinats)
        image_car = Image.open(img_root, car)



        editited.append()
        pass
    return editited


def sort(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts, bg):
    coord_sorted = sort(pts)
    (tl, tr, br, bl) = coord_sorted

    car_width, car_height = bg.size

    (height, width, channels) = image.shape

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(dst, coord_sorted)
    warped = cv2.warpPerspective(image, M, (car_width, car_height), dst=np.asarray(bg),
                                 borderMode=cv2.BORDER_TRANSPARENT)

    return Image.fromarray(warped)
