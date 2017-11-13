from PIL import Image
from help_functions import loadImageMatrix, print_picture

import random
import math
import numpy as np

import neuralnetwork

from help_functions import clamp


def randomNoise(imageMatrix, magnitude = 10):

    output = np.empty_like(imageMatrix)

    for x, y, z in np.ndenumerate(imageMatrix):
        output[x, y, z] = clamp(imageMatrix[z, y, x] + random.randint(-magnitude, magnitude)
                                , 0, 255)

    return output


def quickBlur(image, weight = 0.15):

    imageMatrix = loadImageMatrix(loadedImage=image, Alpha=False)
    outputMatrix = np.empty_like(imageMatrix)

    for y in range(imageMatrix.shape[0]):

        accum = imageMatrix[y, 0]
        for x in range(imageMatrix.shape[1]):

            pixel = imageMatrix[y, x]
            accum = accum * (1-weight) + pixel * weight

            outputMatrix[y, x] = accum

    imageMatrix = outputMatrix

    for x in range(imageMatrix.shape[1]):

        accum = imageMatrix[0, x]
        for y in range(imageMatrix.shape[0]):

            pixel = imageMatrix[y, x]
            accum = accum * (1-weight) + pixel * weight

            outputMatrix[y, x] = accum

    return Image.fromarray(np.array(outputMatrix))

#Very slow^tm
def circleBlur(imageMatrix, blurRadius = 5, count = 1, colorbug = False):

    imageMatrix = loadImageMatrix(loadedImage=imageMatrix, Alpha=False)
    print(imageMatrix.shape)
    output = np.empty_like(imageMatrix)

    paddedMatrix = np.pad(imageMatrix, ((blurRadius, blurRadius), (blurRadius, blurRadius), (0, 0)), 'edge')
    print(paddedMatrix.shape)

    count = random.randint(1, count)
    blurRadius = blurRadius#random.randint(1, blurRadius)  #TODO: for each?

    blurMatrix = np.empty((blurRadius*2+1, blurRadius*2+1, 3))
    print(blurMatrix.shape)

    for (y, x, z), v in np.ndenumerate(blurMatrix):
        dist = 1 / (1 + 2*blurRadius)**2  # currently just averaging
        blurMatrix[y, x, z] = dist

    for i in range(0, count):
        print("i=%i/%i" % (i, count))

        # TODO: only iterate over circle bounding box
        for y in range(0, imageMatrix.shape[0]):
            print("y=%i/%i" % (y, paddedMatrix.shape[0]))

            for x in range(0, imageMatrix.shape[1]):

                for z in range(0, paddedMatrix.shape[2]):

                    sum = 0
                    for yy in range(0, blurMatrix.shape[0]):
                        for xx in range(0, blurMatrix.shape[1]):
                            try:
                                sum += paddedMatrix[y + yy, x + xx, z] * blurMatrix[yy, xx, z]
                            except IndexError as e:
                                print(e)
                                #print(sum)

                    output[y, x, z] = sum
                #print(sum)
        paddedMatrix = output
        #print_picture(loaded_image=Image.fromarray(np.array(output)))
    return Image.fromarray(np.array(output))