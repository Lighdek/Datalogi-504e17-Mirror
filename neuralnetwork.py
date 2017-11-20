import numpy as np


class Model:

    name = None
    model = None

    def __init__(self, name: str, model: list) -> None:

        self.name = name

        # if not isinstance(model, list):
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

    def __init__(self, activation=None) -> None:
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
        self.weights = np.random.rand(out_, in_)#empty((out_, in_))
        self.biases = np.empty((out_,))

    def apply(self, input_: np.ndarray):
        assert len(input_.shape) == input_.ndim
        if input_.ndim > 1 or len(input_) > self.weights.shape[1]:
            return ValueError("Input shape %s, expected vector of length (%i)"
                              % (str(input_.shape), self.weights.shape[1]))

        return self.activation(self.weights.dot(input_) + self.biases)

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

    def __init__(self, filterSize=5):
        super().__init__()
        self.filterSize = filterSize

    def apply(self, input_: np.ndarray):
        from math import floor, ceil

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


class PoolingLayer(Layer):
    def apply(self, input_: Output):
        pass

    def backpropagate(self, input_ : Output, output: Output):
        # Backpropagate to/on highest input
        pass
