import numpy as np
import random
import math

from help_functions import clamp


def randomNoise(imageMatrix, magnitude = 10):

    output = np.empty_like(imageMatrix)

    for z, y, x in np.ndenumerate(imageMatrix):
        output[x, y, z] = clamp(imageMatrix[z, y, x] + random.randint(-magnitude, magnitude)
                                , 0, 255)

    return output
