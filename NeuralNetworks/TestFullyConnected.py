import numpy as np

from neuralnetwork import Model, FullyConnectedLayer

model = Model("TestFullyConnected", [
    FullyConnectedLayer(3, 4)
])

if __name__ == '__main__':
    print(model.test(np.random.rand(3)))  # Prints all the outputs of the model, including the input
