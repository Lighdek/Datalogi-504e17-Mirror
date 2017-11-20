# Man kan enden give den en filepath til et billed eller et allerede loaded billed,
# eller begge dele, den vil så endten returnere en matrice eller flere.
import numpy as np
import math

class Model:

    name = None
    model = None

    def __init__(self, name: str, model: list) -> None:

        self.name = name

        #if not isinstance(model, list):
        #    raise ValueError("Model expected list of layers, got %s" % repr(model))
        for l in model:
            if not isinstance(l, Layer):
                raise ValueError("Model list must contain layers, got %s" % repr(l))

        self.model = model

        # TODO: load from file: folder+name+ext

    def train(self, input_) -> list:  # TODO: list type???

        outputs: list = self.test(input_)

        deltas = list()

        for layer in reversed(outputs):
            # deltas.insert(0, layer.backpropagate()) # TODO: Backprop params
            pass

        return deltas

    def test(self, input_) -> list:

        outputs = list()
        outputs.append(input_)

        for layer in self.model:
            outputs.append(layer.apply(outputs[-1]))

        return outputs


class Output:
    """
    The output from a Layer
    Used as input for most Layers
    """
    matrix = None

    def __init__(self, x, y, z):
        matrix = np.empty((x, y, z))


class WeightBiasDelta:
    """
    The changes to weights and biases returned from train method
    Is averaged when updating weights of the model
    """

    deltaWeight = None
    deltaBias = None

    def __init__(self) -> None:
        super().__init__()


class Layer:

    def __init__(self, activation = None) -> None:
        print("Initializing layer of type: %s" % repr(self))
        if activation is None:
            print("No activation function set")
        self.activation = activation
        super().__init__()

    def apply(self, input_: Output):
        raise NotImplementedError()

    def backpropagate(self, current: Output, previous: Output):
        raise NotImplementedError()


class FullyConnectedLayer(Layer):
    weights: np.ndarray = None
    biases: np.ndarray = None

    def __init__(self, in_, out_): #,data
        super().__init__()
        weights = np.empty((in_, out_))
        biases = np.empty((out_,))


        # if not isinstance(data, np.ndarray):
        #     raise TypeError("Herro")
        # self.matrix = data
        # if isinstance(data, tuple):
        #     self.matrix = np.empty(data)
        # elif isinstance(data, int):
        #     self.matrix

    def apply(self, input_: np.ndarray):
        print(input_.shape)
        print(input_.shape[0:1])
        assert len(input_.shape) == input_.ndim

        if input_.ndim > 1 or len(input_) > self.weights.shape[1]:
            return ValueError("Input shape %s, expected vector of length (%i)"
                              % (str(input_.shape), self.weights.shape[1]))

        return self.weights.dot(input_) + self.biases

    def backpropagate(self, current: Output, previous: Output):
            pass

    # TODO: turn below code into class InputLayer
    # @classmethod
    # def fromImage(cls, image_or_filepath):
    #     if isinstance(image_or_filepath, str):
    #         return np.asarray(Image.open(image_or_filepath))
    #     else:
    #         return np.asarray(image_or_filepath)[:, :, :3]


class ConvolutionalLayer(Layer):

    stride = None
    kernels = None
    filter_size = None
    bias = None

    def __init__(self, filterSize,stride,kernels):
        super().__init__()

        if filterSize < 0:
            raise ValueError('ConvolutionalLayer filtersize is 0 or less.')

        self.filterSize = filterSize
        self.stride = stride
        self.kernels = kernels
        self.bias = np.random.rand(self.kernels)

    def apply(self, input_: np.ndarray):
        y_num = input_.shape[0]
        x_num = input_.shape[1]
        num_kernels = len(self.kernels)

        input_ = self.applyZeroPadding(input_, self.filter_size)
        output = np.empty(shape=(y_num // self. stride, x_num // self.stride, num_kernels)) # make empty shape dependent on stride

        for feature in range(0, num_kernels):
            assert (self.kernels[feature].shape[0] % 2) != 0 and (self.kernels[feature].shape[1] % 2) != 0  # Todo exception insted
            for ycounter in range(0, y_num):
                for xcounter in range(0, x_num):
                    current_area = input_[ycounter: ycounter + self.filter_size, xcounter: xcounter + self.filter_size]
                    current_kernel = self.kernels[feature]
                    output[ycounter, xcounter, feature] = np.sum(current_area * current_kernel) + self.bias[feature]

        return output

    def applyZeroPadding(self, input_, kernel_size):  # used before input.
        size = kernel_size // 2
        # (z) must not be padded. y x z
        return np.pad(input_, ((size, size), (size, size), (0, 0)), "constant", constant_values=0)

    """from math import floor, ceil

        filterSize = self.filterSize
        margin = filterSize // 2  # integer division

        output = np.empty_like(input_)

        for y in range(1+margin, 1080-margin):
            for y in range(1+margin, 1080-margin):
                for x in range(1, 1920):
                    output[y, x] = input_[
                                   floor(y-filterSize/2):ceil(y+filterSize/2),
                                   floor(x-filterSize/2):ceil(x+filterSize/2)
                                   ].dot(filter)
    """

    def backpropagate(self, current: Output, previous: Output):
        pass


class PoolingLayer(Layer):
    stride = None

    def apply(self, input_: Output):
        y = math.ceil(input_.shape[0] / self.stride)
        x = math.ceil(input_.shape[1] / self.stride)
        z = input_.shape[2]  # feature size

        buffer = np.empty(shape=(y, x, z))

        for yc in range(0, y):
            for xc in range(0, x):
                for zc in range(0, z):
                    buffer[yc][xc][zc] = self.maxpool(self.stride, input_, yc * self.stride, xc * self.stride, zc)

    def maxpool(self, stride, input_, x, y, z):
        buffer = input_[x:x + stride, y:y + stride, z]
        buffer = buffer.flatten()
        return np.amax(buffer, axis=0)

    def backpropagate(self, input_ : Output, output: Output):
        # Backpropagate to/on highest input
        pass