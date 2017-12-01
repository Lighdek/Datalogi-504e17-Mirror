import os

from PIL import Image
from keras import optimizers
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten
from ImageGeneration import Generator as ImageGenerator
import numpy as np

from help_functions import print_picture, loadImageMatrix


model = Sequential([

    Conv2D(filters=12, kernel_size=3, activation='relu', padding='same', input_shape=(256, 256, 3)),
    MaxPool2D(padding='same'),  # 64

    Conv2D(filters=16, kernel_size=3, activation='relu', padding='same'),
    MaxPool2D(padding='same'),  # 32

    Conv2D(filters=16, kernel_size=3, activation='relu', padding='same'),
    MaxPool2D(padding='same'),  # 16

    Conv2D(filters=16, kernel_size=3, activation='relu', padding='same'),
    MaxPool2D(padding='same'),  # 8

    Conv2D(filters=16, kernel_size=3, activation='relu', padding='same'),
    MaxPool2D(padding='same'),  # 4

    Conv2D(filters=16, kernel_size=3, activation='relu', padding='same'),
    MaxPool2D(padding='same'),  # 2

    Conv2D(filters=16, kernel_size=3, activation='relu', padding='same'),
    MaxPool2D(padding='same'),  # 1

    Flatten(),
    Dense(1, activation='sigmoid',
          kernel_initializer='random_uniform',
          bias_initializer='zeros'),  # activation='softmax'
])


if __name__ == '__main__':
    #optimizer = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    print(model.weights)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])
    print(model.weights)

    print(os.listdir('../ImageGeneration/Images'))

    i=1
    while True:
        images, labels = ImageGenerator.generator([
            "../ImageGeneration/Images/WithLicence",
            "../ImageGeneration/Images/WithoutLicence",
            "../ImageGeneration/Images/Backgrounds"],
            tbgenerated=200)

        print(labels)
        print(np.average(labels))

        model.fit(np.array(images), labels, batch_size=18, epochs=5, verbose=1, validation_split=0.25)
        model.summary()

        def normalized(a, axis=-1, order=2):
            l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
            l2[l2 == 0] = 1
            return a / np.expand_dims(l2, axis)


        if i%10 == 0:
            mw = model.layers[0].get_weights()[0]
            for k in range(mw.shape[3]):
                #thek = (mw[:,:,:,k]+0)*1024
                thek = normalized(normalized(normalized(mw[:,:,:,k]+1, axis=2), axis=1), axis=0)*255 #TODO: testing norm axis=2
                #thek = normalized(mw[:, :, :, k] + 1, axis=2)
                print(thek)
                print_picture(Image.frombuffer("RGB", thek.shape[0:2], thek))

        i += 1
        #model.layers[0].get_weights()[0][:,:,:,0]
        #print_picture(loaded_image=
        #    Image.fromarray(
        #        np.asarray(model.layers[0].get_weights()[0])[:,:,0:3,0])
        #)



    #print(repr(images))

