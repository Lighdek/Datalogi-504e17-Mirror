from keras import optimizers
from keras import regularizers as reg
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten
import metrics as m

def init():
    model = Sequential([

        Conv2D(filters=12, kernel_size=3, activation='relu', padding='same', input_shape=(512, 512, 3),
               kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 256

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 128

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 64

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 32

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 16

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 8

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 4

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 2

        Conv2D(filters=16, kernel_size=3, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),
        MaxPool2D(padding='same'),  # 1

        Flatten(input_shape=(1,1,None)),
        Dense(2, activation='softmax')

    ])

    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy', m.f1measure, m.f_half_measure, m.precision, m.recall])

    return model
