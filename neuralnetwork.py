# Man kan enden give den en filepath til et billed eller et allerede loaded billed,
# eller begge dele, den vil så endten returnere en matrice eller flere.
import numpy as np

from PIL import Image

class Output:
    """
    The output from a Layer
    Used as input for most Layers
    """
    matrix = None

    def __init__(self, x, y, z):
        matrix = np.empty((x, y, z))

class Layer:
    def apply(self, input_: Output):
        raise NotImplementedError()

    def backpropagate(self, output: Output):
        raise NotImplementedError()


class FullyConnectedLayer(Layer):
    weights = None
    biases = None

    def __init__(self, in_, out_): #,data
        weights = np.empty((in_, out_))
        biases = np.empty((out_,))


        # if not isinstance(data, np.ndarray):
        #     raise TypeError("Herro")
        # self.matrix = data
        # if isinstance(data, tuple):
        #     self.matrix = np.empty(data)
        # elif isinstance(data, int):
        #     self.matrix

    def apply(self, input_: Output):
        return input_.matrix.dot(self.matrix)

    # TODO: turn below code into class InputLayer
    # @classmethod
    # def fromImage(cls, image_or_filepath):
    #     if isinstance(image_or_filepath, str):
    #         return np.asarray(Image.open(image_or_filepath))
    #     else:
    #         return np.asarray(image_or_filepath)[:, :, :3]

class ConvolutionalLayer(Layer):

    def __init__(self, filterSize = 5):
        self.filterSize = filterSize

    def apply(self, input_: Output):
        from math import floor, ceil

        filterSize = self.filterSize
        margin = filterSize // 2  # integer division

        output = np.empty_like(input_)

        for y in range(1+margin, 1080-margin):
            for y in range(1+margin, 1080-margin):
                for x in range(1, 1920):
                    output[y, x] = input_.matrix[
                                   floor(y-filterSize/2):ceil(y+filterSize/2),
                                   floor(x-filterSize/2):ceil(x+filterSize/2)
                                   ].dot(filter)

class PoolingLayer(Layer):
    def apply(self, input_: Output):
        pass

    def backpropagate(self, input_ : Output, output: Output):
        # Backpropagate to/on highest input
        pass