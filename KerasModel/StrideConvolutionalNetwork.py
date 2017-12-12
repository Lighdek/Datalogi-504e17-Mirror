from keras import optimizers
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten


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
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

    return model
