from keras import optimizers
from keras import regularizers
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten


def init():
    model = Sequential([

        Conv2D(input_shape=(256, 256, 3),
               filters=12, kernel_size=10, activation='relu', padding='same', strides=1, kernel_regularizer=regularizers.l2(0.1)),  # 256

        Conv2D(filters=24, kernel_size=8, activation='relu', padding='same', strides=2, kernel_regularizer=regularizers.l2(0.1)),  # 128

        Conv2D(filters=24, kernel_size=8, activation='relu', padding='same', strides=1, kernel_regularizer=regularizers.l2(0.1)),  # 128

        Conv2D(filters=32, kernel_size=5, activation='relu', padding='same', strides=2, kernel_regularizer=regularizers.l2(0.1)),  # 64

        Conv2D(filters=32, kernel_size=4, activation='relu', padding='same', strides=1, kernel_regularizer=regularizers.l2(0.1)),  # 64

        Conv2D(filters=64, kernel_size=4, activation='relu', padding='same', strides=2, kernel_regularizer=regularizers.l2(0.1)),  # 32

        Conv2D(filters=64, kernel_size=4, activation='relu', padding='same', strides=1, kernel_regularizer=regularizers.l2(0.1)),  # 32

        Conv2D(filters=128, kernel_size=2, activation='relu', padding='same', strides=2, kernel_regularizer=regularizers.l2(0.1)),  # 16

        Flatten(),

        Dense(1000, activation='relu', kernel_regularizer=regularizers.l2(0.1) ),

        Dense(500, activation='tanh', kernel_regularizer=regularizers.l2(0.1) ),

        Dense(1, activation='hard_sigmoid', )
    ])

    import keras.backend as K

    def myAccuracy(y_true, y_pred):
        diff = K.abs(y_true - y_pred)  # absolute difference between correct and predicted values
        correct = K.less(diff, 0.40)  # tensor with 0 for false values and 1 for true values
        return K.mean(correct)  # sum all 1's and divide by the total.



    optimizer = optimizers.adam(lr=1e-4, decay=1e-6)
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=[myAccuracy, 'accuracy'])

    return model
