from PIL import Image
from help_functions import loadImageMatrix
import random
import math
import numpy as np

def bluring_start(image_to_be_blured):
    pixels = {}
    under_cut = []
    over_cut = []

    picture_matrix = loadImageMatrix(loadedImage=image_to_be_blured,Alpha=False)

    image_size = image_to_be_blured.size

    for y_axis in range(0, len(picture_matrix[:])):

        for x_axis in range(0, len(picture_matrix[y_axis][:])):

            pixels["{},{}".format(x_axis,y_axis)] = Pixel(picture_matrix[y_axis][x_axis][:])

    how_many_pix = 0
    for pi in pixels:
        if pixels.get(pi) is not type(int):
            how_many_pix += 1

    print(how_many_pix)

    print(image_size[0] * image_size[1])

    for index in range(0,random.randint(0,50)):
        tmpo = random.randint(0, image_size[1] - 1)
        tmpq = random.randint(0, image_size[0] - 1)
        pixels.get("{},{}".format(tmpq,tmpo)).is_weighted = True

    for weighted_pix in pixels:

        if pixels.get(weighted_pix).is_weighted == True:
            div_by_hundrd_x = math.ceil(image_size[0] / 10)
            div_by_hundrd_y = math.ceil(image_size[1] / 10)
            radius_x = random.randint(2,div_by_hundrd_x)
            rand_y = random.randint(2,div_by_hundrd_y)

            tmp_coordinats = weighted_pix.split(",")
            tmp_coordinats[0] = int(tmp_coordinats[0])
            tmp_coordinats[1] = int(tmp_coordinats[1])
            # print(tmp_coordinats)
            a = 0
            b = 0
            radius_x = __reccurzion__(a, radius_x, image_size[0])
            rand_y = __reccurzion__(b, rand_y, image_size[1])

            lower_end = tmp_coordinats[0] - math.ceil(radius_x /2 )
            higher_end = tmp_coordinats[0] + math.ceil(radius_x/2)
            for x in range(0, higher_end - lower_end):
                inbetweencalc = -a ** 2 + 2 * a * x + radius_x - x**2
                calc = math.ceil((b + math.sqrt(inbetweencalc))) if inbetweencalc > 0 else math.ceil(b + inbetweencalc)
                over_cut.append(calc)

            get_x = 0

            for x in range(lower_end, higher_end):
                get_y = 0
                #print("{},{}".format( tmp_coordinats[1] - over_cut[get_x], over_cut[get_x] + tmp_coordinats[1]))
                for y in range(tmp_coordinats[1] - over_cut[get_x], over_cut[get_x] + tmp_coordinats[1]):
                    # print("x:{}, y:{}  |  coordinats: {},{} is a {}"
                    #       .format(tmp_coordinats[0], tmp_coordinats[1],
                    #               get_x + tmp_coordinats[0], get_y + tmp_coordinats[1],
                    #               pixels.get("{},{}".format(get_x + tmp_coordinats[0],
                    #                                         get_y + tmp_coordinats[1]))))
                    try:
                        pixels.get("{},{}".format(get_x + tmp_coordinats[0], get_y + tmp_coordinats[1])).tb_blurred = True
                    except AttributeError:
                        print("Index out of range... px{},{} - img_max{},{}".format(get_x + tmp_coordinats[0], get_y + tmp_coordinats[1],image_size[0],image_size[1]))
                    get_y += 1
                get_x += 1
                # Values gotten: 271,787 - 568,60 - '507,72' -  347,36'<- hvorfor er det en fejl? - 468,2



    for tb_blurred in pixels:
        average_color_R = 0
        average_color_G = 0
        average_color_B = 0
        temp_px = pixels.get(tb_blurred)
        if temp_px.tb_blurred == True:
            temp_px.find_neighbors(tb_blurred.split(","), image_size)
            for neighbors in temp_px.neighbors:
                try:
                    average_color_R += pixels.get(neighbors).RGBA[0]
                    average_color_G += pixels.get(neighbors).RGBA[1]
                    average_color_B += pixels.get(neighbors).RGBA[2]
                except AttributeError:
                    print("Index out of range..... ({}) - ({},{})".format(neighbors, image_size[0],image_size[1]))
            temp_px.RGBA[0] = math.ceil(average_color_R / len(temp_px.neighbors))
            temp_px.RGBA[1] = math.ceil(average_color_G / len(temp_px.neighbors))
            temp_px.RGBA[2] = math.ceil(average_color_B / len(temp_px.neighbors))
            # temp_px.RGBA[3] = 255


    new_picture = []
    for x in range(len(picture_matrix)):
        new_picture.append(x)
        new_picture[x] = []
        for y in range(len(picture_matrix[x])):
            new_picture[x].append(y)
            new_picture[x][y] = []
            new_picture[x][y].append(pixels.get("{},{}".format(y,x)).RGBA)

    # for pix in pixels:
    #     de_sht = pix.split(",")
    #     de_sht[0] = int(de_sht[0])
    #     de_sht[1] = int(de_sht[1])
    #     # print("ds1: {}, ds2: {}".format(type(de_sht[0]),type(de_sht[1])))
    #     # print("coordinats: ({}{}), px_rgba({}) - org_rgba({})".format(de_sht[0],de_sht[1],pixels.get(pix).RGBA,picture_matrix[de_sht[0]][de_sht[1]][:]))
    #     try:
    #
    #
    #         picture_matrix[de_sht[1]][de_sht[2]] = pixels.get(pix).RGBA
    #     except Exception as e:
    #         print("Exception: {}\n Was led by trying to force pointer -> ({},{}) | into the matrix... whereas img_max -> ({},{})".format(e,de_sht[0],de_sht[1],image_size[0],image_size[1]))


    return Image.fromarray(np.array(new_picture))







def __reccurzion__(koordinat, size, max_size):
    if (koordinat + math.ceil(size / 2)) > max_size:
        size = __reccurzion__(koordinat, size - 1,max_size)
    return size





class Pixel :
    RGBA = []
    neighbors = []
    is_weighted = False
    tb_blurred = False

    def __init__(self, RGBA):
        self.RGBA = RGBA

    def find_neighbors(self, coordinats, image_size):
        coordinats[0] = int(coordinats[0])
        coordinats[1] = int(coordinats[1])
        nb = []
        if coordinats[0] is not 0:
            nb.append("{},{}".format(coordinats[0] - 1, coordinats[1]))
        if coordinats[1] is not 0:
            nb.append("{},{}".format(coordinats[0], coordinats[1] - 1))

        if coordinats is not [0, 0]:
            nb.append("{},{}".format(coordinats[0] - 1, coordinats[1] - 1))

        if coordinats[0] is not image_size[0]:
            nb.append("{},{}".format(coordinats[0] + 1, coordinats[1]))
        if coordinats[1] is not image_size[1]:
            nb.append("{},{}".format(coordinats[0], coordinats[1] + 1))
        if coordinats is not image_size:
            nb.append("{},{}".format(coordinats[0] + 1, coordinats[1] + 1))
        self.neighbors = nb
