from keras import optimizers
from keras import regularizers as reg
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten
import metrics as m

def init():
    model = Sequential([
#h1:w4-5
        Conv2D(filters=128, kernel_size=16, strides=16, activation='relu', padding='valid', input_shape=(128, 128, 3),
               ),#kernel_regularizer=reg.l2(0.)),
        MaxPool2D(padding='same', pool_size=128//16),  # 64 4x20ish

        Flatten(input_shape=(1, 1, None)),
        Dense(1, activation='relu')

    ])

    #optimizer = optimizers.SGD(lr=1e-2, decay=1e-10, momentum=0.9, nesterov=True)
    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy', m.f1measure, m.f_half_measure, m.precision, m.recall])

    return model
