from PIL import Image
from cv2 import getPerspectiveTransform, warpPerspective, BORDER_TRANSPARENT
import numpy as np


def combine_pictures(car, car_coordinats, licence_plate):
    return four_point_transform(Image.open(licence_plate), np.array(car_coordinats), car)


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
    image = np.asarray(image)

    car_width, car_height = bg.size
    (height, width, ch) = image.shape

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]], dtype="float32")

    M = getPerspectiveTransform(dst, coord_sorted)
    warped = warpPerspective(image, M, (car_width, car_height), dst=np.asarray(bg), borderMode=BORDER_TRANSPARENT)

    return Image.fromarray(warped)
