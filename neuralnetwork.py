# Man kan enden give den en filepath til et billed eller et allerede loaded billed,
# eller begge dele, den vil så endten returnere en matrice eller flere.
import numpy as np
import pygame

from PIL import Image


class NeuralLayer:
    matrix = None

    def __init__(self, x, y, z):
        matrix = np.empty((x, y, z))

    @classmethod
    def fromImage(cls, image_or_filepath):
        if isinstance(image_or_filepath, str):
            return np.asarray(Image.open(image_or_filepath))
        else:
            return np.asarray(image_or_filepath)[:, :, :3]



class Filter:
    def apply(self, layer: NeuralLayer):
        raise NotImplementedError()


class FullyConnectedFilter(Filter):

    matrix = None

    def apply(self, layer: NeuralLayer):
        return layer.matrix.dot(self.matrix)


class ConvolutionalFilter(Filter):

    def apply(self, layer: NeuralLayer):
        from math import floor, ceil

        filterSize = 5
        margin = filterSize // 2  # integer division

        for y in range(1+margin, 1080-margin):
            for x in range(1, 1920):
                features = layer.matrix[
                           floor(y-filterSize/2):ceil(y+filterSize/2),
                           floor(x-filterSize/2):ceil(x+filterSize/2)
                           ].dot(filter)


