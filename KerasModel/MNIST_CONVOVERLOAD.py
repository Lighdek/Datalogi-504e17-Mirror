from keras import optimizers
from keras import regularizers
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten


def init():
    model = Sequential([
        Conv2D(input_shape=(28, 28, 1),
               filters=20, kernel_size=3, activation='relu', padding='same', strides=1, kernel_regularizer=regularizers.l2(0.)),
        MaxPool2D(padding='same'),  # 14
        Conv2D(filters=40, kernel_size=3, activation='relu', padding='same', strides=1, kernel_regularizer=regularizers.l2(0.)),
        MaxPool2D(padding='same'),  # 7
        Conv2D(filters=80, kernel_size=3, activation='relu', padding='same', strides=1, #4
               kernel_regularizer=regularizers.l2(0.)),
        MaxPool2D(padding='same'),  # 4
        Conv2D(filters=160, kernel_size=3, activation='relu', padding='same', strides=1,  # 4
               kernel_regularizer=regularizers.l2(0.)),
        MaxPool2D(padding='same'),  # 2
        Conv2D(filters=320, kernel_size=2, activation='relu', padding='same', strides=1,  # 4
               kernel_regularizer=regularizers.l2(0.)),
        MaxPool2D(padding='same'),  # 1


        Flatten(),
        Dense(10, activation='softmax', kernel_regularizer=regularizers.l2(0.) )
    ])
    import keras.backend as K

    def myAccuracy(y_true, y_pred):
        diff = K.abs(y_true - y_pred)  # absolute difference between correct and predicted values
        correct = K.less(diff, 0.25)  # tensor with 0 for false values and 1 for true values
        return K.mean(correct)  # sum all 1's and divide by the total.


    optimizer = optimizers.adam(lr=1e-5, decay=1e-6)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=[myAccuracy, 'accuracy'])

    return model
