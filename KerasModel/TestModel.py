from keras import optimizers
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten

model = Sequential([
    Conv2D(filters=8, kernel_size=3, activation='relu', input_shape=(128, 128, 3)),
    MaxPool2D(),
    Conv2D(filters=16, kernel_size=3, activation='relu'),
    MaxPool2D(),
    Conv2D(filters=32, kernel_size=3, activation='relu'),
    MaxPool2D(),
    Conv2D(filters=32, kernel_size=3, activation='relu'),
    MaxPool2D(),
    Conv2D(filters=32, kernel_size=3, activation='relu'),
    MaxPool2D(),
    Conv2D(filters=32, kernel_size=3, activation='relu'),
    MaxPool2D(),
    Conv2D(filters=32, kernel_size=3, activation='relu'),
    MaxPool2D(),
    Conv2D(filters=32, kernel_size=3, activation='relu'),
    MaxPool2D(),

    Flatten(),
    Dense(2, input_shape=(32,), activation='softmax'),

])

if __name__ == '__main__':
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd)