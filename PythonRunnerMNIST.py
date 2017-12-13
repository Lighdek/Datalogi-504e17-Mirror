import numpy as np
import os
import keras
from ImageGeneration import ImageLoader
from KerasModel import MNIST_CONVOVERLOAD as theThing
from keras.datasets import mnist


modelExt = ".hem"
modelFilename = os.path.join(*theThing.__name__.split('.')) + modelExt
print(modelFilename)

img_rows, img_cols = 28, 28

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, 10) #number of classes
y_test = keras.utils.to_categorical(y_test, 10)

if __name__ == '__main__':
    try:
        model = keras.models.load_model(modelFilename)
    except OSError as e:
        print(e)
        model = theThing.init()

    model.summary()


    model.fit(x_train, y_train, batch_size=200, epochs=100, verbose=1, validation_data=(x_test, y_test))

    model.save(modelFilename)
