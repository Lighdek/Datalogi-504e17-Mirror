import os

from PIL import Image
from keras import optimizers
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten
from ImageGeneration import Generator as ImageGenerator
import numpy as np

from KerasModel import printModel
from help_functions import print_picture, loadImageMatrix


def init():
    model = Sequential([

        Conv2D(input_shape=(256, 256, 3),
               filters=12, kernel_size=3, activation='relu', padding='same', strides=2),  # 64

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', strides=2),  # 32

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', strides=2),  # 16

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', strides=2),  # 8

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', strides=2),  # 4

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', strides=2),  # 2

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', strides=2),  # 1

        Flatten(),
        Dense(1, activation='sigmoid', )
    ])

    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    print(model.weights)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

    return model



if __name__ == '__main__':
    model = init()

    i = 1
    while True:
        images, labels = ImageGenerator.Generator(200)

        model.fit(np.array(images), labels, batch_size=150, epochs=1, verbose=1, validation_split=0.25)
        model.summary()

        if i % 25 == 0:
            printModel(model)

        i += 1

        #model.sav
