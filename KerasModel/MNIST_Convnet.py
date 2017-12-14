from keras import optimizers
from keras import regularizers
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten


def init():
    model = Sequential([
        Conv2D(input_shape=(28, 28, 1),
               filters=20, kernel_size=5, activation='relu', padding='same', strides=2, kernel_regularizer=regularizers.l2(0.)),

        Conv2D(filters=40, kernel_size=5, activation='relu', padding='same', strides=2, kernel_regularizer=regularizers.l2(0.)),


        Flatten(),
        Dense(1000, activation='relu', kernel_regularizer=regularizers.l2(0.) ),

        Dense(1000, activation='relu', kernel_regularizer=regularizers.l2(0.) ),

        Dense(10, activation='softmax', kernel_regularizer=regularizers.l2(0.) )
    ])

    optimizer = optimizers.adam(lr=1e-5, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

    return model
