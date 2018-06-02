from keras.layers import Activation, SimpleRNN
from keras.models import Sequential
import numpy as np
import csv
import math
import sys
import h5py

def normalize (data):
    data = list(data)
    c = 0

    while c < channels:
        smallest = -128
        largest = 128

        largest -= smallest

        for point in data:
            point[c] = (point[c] - smallest) / (largest or 1)

        c += 1

    return data

def gestureToList (gesture):
    if gesture == "right":
        return [1, 0, 0]
    elif gesture == "left":
        return [0, 1, 0]
    elif gesture == "fist":
        return [0, 0, 1]

#set parameters for windows
gestures = ["right", "left", "fist"]
channels = 8
sequence_length = 50
samples = []
labels = []

#get data from csv and convert to 2D list
for gesture in gestures:
    with open("extracted/rnn/" + gesture + ".csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        sequence = []

        for i, row in enumerate(reader):
            sequence.append(list(map(float, row)))

            if len(sequence) >= sequence_length:
                samples.append(normalize(sequence))
                print(gestureToList(gesture))
                labels.append(gestureToList(gesture))
                sequence = []

x_train = np.array(samples[:len(samples)//2]).astype("float32")
x_test = np.array(samples[len(samples)//2:]).astype("float32")
y_train = np.array(labels[:len(labels)//2]).astype("float32")
y_test = np.array(labels[len(labels)//2:]).astype("float32")

print(x_train.shape)

#epochs
epochs = None
if len(sys.argv) > 1:
    if sys.argv[1].isdigit():
        epochs = int(sys.argv[1])

if epochs == None:
    epochs = 1000

model = Sequential()
model.add(SimpleRNN(len(gestures), activation="relu", input_shape=(sequence_length, channels)))
model.compile(optimizer='adadelta', loss='mean_squared_error', metrics=['accuracy'])
model.fit(
    x_train,
    y_train,
    epochs = epochs,
    batch_size = len(x_train),
    validation_data = (x_test, y_test)
)
model.save("models/rnn.h5");
