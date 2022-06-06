import numpy as np
import random
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense


def generate_model(input_array):
    y_true = np.array([[1]])
    y_false = np.array([[0]])
    x_train = np.empty((0, input_array.shape[1]), int)
    y_train = np.empty((0, 1), int)

    broker = np.empty((0, input_array.shape[1]), int)
    broker2 = np.zeros((1, input_array.shape[1]))
    for i in range(1000):
        broker = np.append(broker, input_array, axis=0)

        for j in range(input_array.shape[1]):
            broker[0][j] += random.randint(-10, 10)
            broker2[0][j] += random.randint(0, 500)

        x_train = np.append(x_train, broker, axis=0)
        x_train = np.append(x_train, broker2, axis=0)
        y_train = np.append(y_train, y_true, axis=0)
        y_train = np.append(y_train, y_false, axis=0)
        broker = np.delete(broker, 0, axis=0)
        broker2 = np.zeros((1, input_array.shape[1]))

    model = Sequential()
    model.add(Dense(1, input_shape=(x_train.shape[1],), activation='sigmoid'))
    model.compile(optimizer='SGD', loss='binary_crossentropy', metrics=['acc'])
    model.fit(x_train, y_train, epochs=100, validation_split=0.2)
    return model


def to_np(keystroke):
    data = np.array(keystroke.split(","), dtype=int)
    data = data * -1
    data = np.array([data])

    return data
