from keras import optimizers
from keras import regularizers as reg
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten
import metrics as m

def init():
    model = Sequential([
#h1:w4-5
        Conv2D(filters=16, kernel_size=5, activation='relu', padding='same', input_shape=(128, 128, 3),
               ),#kernel_regularizer=reg.l2(0.)),
        MaxPool2D(padding='same', pool_size=4),  # 64 4x20ish

        Conv2D(filters=64, kernel_size=5, activation='relu', padding='same'),# kernel_regularizer=reg.l2(0.)),
        MaxPool2D(padding='same', pool_size=4),  # 32 8x40ish

        Conv2D(filters=128, kernel_size=5, activation='relu', padding='same'),# kernel_regularizer=reg.l2(0.)),
        MaxPool2D(padding='same'),  # 16 16x80ish

        Conv2D(filters=6, kernel_size=3, activation='relu', padding='same'),# kernel_regularizer=reg.l2(0.)),
        MaxPool2D(padding='same'),  # 8  32x160ish

        Conv2D(filters=4, kernel_size=3, activation='relu', padding='same'),# kernel_regularizer=reg.l2(0.)),
        MaxPool2D(padding='same'),  # 4  64x320ish

        Conv2D(filters=4, kernel_size=3, activation='relu', padding='same'), #kernel_regularizer=reg.l2(0.)),
        MaxPool2D(padding='same'),  # 2  128x640ish

        Conv2D(filters=4, kernel_size=3, activation='relu', padding='same'), #kernel_regularizer=reg.l2(0.)),
        MaxPool2D(padding='same'),  # 1

        Flatten(input_shape=(1, 1, None)),
        Dense(1, activation='relu')

    ])

    optimizer = optimizers.SGD(lr=1e-2, decay=1e-10, momentum=0.9, nesterov=True)
    #optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy', m.f1measure, m.f_half_measure, m.precision, m.recall])

    return model
