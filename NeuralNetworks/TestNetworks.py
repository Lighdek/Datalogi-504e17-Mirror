import numpy as np

from . import Model, FullyConnectedLayer, ConvolutionalLayer

modelFullyConnected = Model("TestFullyConnected", [
    FullyConnectedLayer(3, 4)
])

#TEMP
kernel1 = np.array([[[2,3],[-1,3],[2,2]],
                   [[2,-1],[1,2],[-1,2]],
                   [[-1,3],[1,1],[2,2]]])

kernel2 = np.array([[[2,3],[-1,2],[0,3]],
                   [[2,-1],[2,2],[2,-1]],
                   [[-1,2],[1,3],[2,2]]])

kernel3 = np.array([[[1,3],[-1,3],[2,2]],
                   [[0,2],[0,5],[-1,2]],
                   [[-1,3],[1,1],[-1,2]]])

lst = [kernel1,kernel2,kernel3]
#ENDTEMP
modelConvolutional = Model("TestConvolutional", [
    ConvolutionalLayer(3, 1, lst)
])

if __name__ == '__main__':
    print(modelFullyConnected.test(np.random.rand(3)))  # Prints all the outputs of the model, including the input
    print(modelConvolutional.test(np.random.rand(4, 4, 2)))
