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

    for i in range(input_array.shape[0]):
        x = np.reshape(input_array[i], (1, input_array.shape[1]))
        for j in range(1000):
            broker = np.append(broker, x, axis=0)

            for k in range(input_array.shape[1]):
                broker[0][k] += random.randint(-10, 10)
                broker2[0][k] += random.randint(0, 500)

            x_train = np.append(x_train, broker, axis=0)
            x_train = np.append(x_train, broker2, axis=0)
            y_train = np.append(y_train, y_true, axis=0)
            y_train = np.append(y_train, y_false, axis=0)
            broker = np.delete(broker, 0, axis=0)
            broker2 = np.zeros((1, input_array.shape[1]))

    model = Sequential()
    model.add(Dense(1, input_shape=(x_train.shape[1],), activation='sigmoid'))
    model.compile(optimizer='SGD', loss='binary_crossentropy', metrics=['acc'])
    model.fit(x_train, y_train, epochs=1000, validation_split=0.2)

    print(x_train.shape)
    return model


def to_np(keystroke):
    data = np.array(keystroke.split(","), dtype=int)
    data = data * -1
    data = np.array([data])

    return data


def add_to_file(keystroke, username):
    # data = to_np(keystroke)
    data = keystroke

    try:
        x_train = np.load(f"t4s/model/{username}/x_train.npy")
        x_train = np.append(x_train, data, axis=0)
    except FileNotFoundError:
        x_train = data

    print(x_train.shape[0])
    print(x_train.shape[1])
    np.save(f"t4s/model/{username}/x_train.npy", x_train)

    return
