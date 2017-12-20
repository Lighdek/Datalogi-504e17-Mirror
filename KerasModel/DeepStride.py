import metrics as m
from keras import optimizers
from keras import regularizers
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten, MaxPool2D


def init():
    model = Sequential([

        Conv2D(input_shape=(512, 512, 3),
               filters=12, kernel_size=20, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)),
        MaxPool2D(padding='same'),  # 256

        Conv2D(filters=24, kernel_size=16, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)),
        MaxPool2D(padding='same'),  # 128

        Conv2D(filters=56, kernel_size=5, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)),
        MaxPool2D(padding='same'),  # 64

        Conv2D(filters=78, kernel_size=5, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)),
        MaxPool2D(padding='same'),  # 32

        Conv2D(filters=78, kernel_size=3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)),
        MaxPool2D(padding='same'),  # 16

        Conv2D(filters=78, kernel_size=2, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)),
        MaxPool2D(padding='same'),  # 8

        Conv2D(filters=78, kernel_size=2, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)),
        MaxPool2D(padding='same'),  # 4

        Flatten(),

        Dense(200, activation='tanh', kernel_regularizer=regularizers.l2(0.)),

        Dense(1, activation='hard_sigmoid')
    ])

    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy', m.f1measure, m.f_half_measure, m.precision, m.recall])

    return model
