from keras import optimizers
from keras import regularizers as reg
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten
import metrics as m

def init():
    model = Sequential([

        Conv2D(filters=16, kernel_size=16, strides=4, activation='relu', padding='same', input_shape=(512, 512, 3),
               kernel_regularizer=reg.l2(0.01)), # 256

        Conv2D(filters=64, kernel_size=8, strides=4, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),# 64

        Conv2D(filters=96, kernel_size=8, strides=4, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),# 16

        Conv2D(filters=6, kernel_size=4, strides=4, activation='relu', padding='same', kernel_regularizer=reg.l2(0.01)),# 4

        Dense(100, activation="tanh", kernel_regularizer=reg.l2(0.01)),

        Flatten(input_shape=(1, 1, None)),
        Dense(2, activation='softmax')

    ])

    #optimizer = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9)
    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy', m.f1measure, m.f_half_measure, m.precision, m.recall])

    return model
