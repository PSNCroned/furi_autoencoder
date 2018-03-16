#https://blog.keras.io/building-autoencoders-in-keras.html
#https://arxiv.org/pdf/1801.05394.pdf

from keras.layers import Input, Dense, Activation, Dropout
from keras.models import Model, load_model
from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
import sys
import h5py

def normalizeData (data):
    global channels

    c = 0
    channels = len(data[0])

    while c < channels:
        smallest = data[0][c]
        largest = data[0][c]

        for point in data:
            if point[c] < smallest:
                smallest = point[c]
            if point[c] > largest:
                largest = point[c]

        largest -= smallest

        for point in data:
            point[c] = (point[c] - smallest) / (largest or 1)

        c += 1

csv_name = "extracted.csv";

#set parameters for windows
window_size = 50
overlap = .0
channels = 8

#epochs
if sys.argv[1].isdigit():
    epochs = int(sys.argv[1])
elif len(sys.argv) > 2:
    if sys.argv[2].isdigit():
        epochs = int(sys.argv[2])
else:
    epochs = 5000

data = []
windows = []

#get data from csv and convert to 2D list
with open("extracted/" + csv_name) as csvfile:
    reader = csv.reader(csvfile, delimiter=",")

    for row in reader:
        data.append(list(map(float, row)))

    normalizeData(data)

#create windows from data
win_i = 0
data_i = 0
while data_i + window_size <= len(data):
    win = []
    i = data_i

    while i < data_i + window_size:
        for val in data[i]:
            win.append(val)
        i += 1

    windows.append(win)
    data_i = int((data_i + window_size) - (overlap * window_size))

print("Total windows: " + str(len(windows)))

#convert windows to numpy array
# windows = np.array(windows).astype("float32")
windows_train = np.array(windows[:len(windows)//2]).astype("float32")
windows_test = np.array(windows[len(windows)//2:]).astype("float32")

#set data dimensions for layers
# input_dim = len(windows[0])
input_dim = len(windows_train[0])
encoder_1_dim = math.floor(math.floor(input_dim * .8))
encoder_2_dim = math.floor(math.floor(input_dim * .6))
encoder_3_dim = math.floor(math.floor(input_dim * .4))
encoder_4_dim = math.floor(math.floor(input_dim * .2))
decoder_1_dim = encoder_3_dim
decoder_2_dim = encoder_2_dim
decoder_3_dim = encoder_1_dim
decoder_4_dim = input_dim

#input layers
input_layer = Input(shape=(input_dim,))
encoded_input = Input(shape=(encoder_4_dim,))

#if no argument passed to script
if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1].isdigit()):
    #layer structure
    #encoded_1 = Dense(encoder_1_dim, activation="relu")(input_layer)
    #tanh = Activation("relu")(encoded_1)
    #drop = Dropout(.10)(tanh)

    #encoded_2 = Dense(encoder_2_dim, activation="relu")(drop)
    #tanh = Activation("relu")(encoded_2)
    #drop = Dropout(.10)(tanh)

    #encoded_3 = Dense(encoder_3_dim, activation="relu")(drop)
    #tanh = Activation("relu")(encoded_3)
    #drop = Dropout(.10)(tanh)

    #encoded_4 = Dense(encoder_4_dim, activation="relu")(drop)

    #decoded_1 = Dense(decoder_1_dim, activation="relu")(encoded_input)
    #tanh = Activation("relu")(decoded_1)
    #drop = Dropout(.10)(tanh)

    #decoded_2 = Dense(decoder_2_dim, activation="relu")(drop)
    #tanh = Activation("relu")(decoded_2)
    #drop = Dropout(.10)(tanh)

    #decoded_3 = Dense(decoder_3_dim, activation="relu")(drop)
    #tanh = Activation("relu")(decoded_3)
    #drop = Dropout(.10)(tanh)

    #decoded_4 = Dense(decoder_4_dim, activation="sigmoid")(drop)


    encoded_1 = Dense(encoder_1_dim, activation="relu")(input_layer)
    encoded_2 = Dense(encoder_2_dim, activation="relu")(encoded_1)
    encoded_3 = Dense(encoder_3_dim, activation="relu")(encoded_2)
    encoded_4 = Dense(encoder_4_dim, activation="relu")(encoded_3)
    decoded_1 = Dense(decoder_1_dim, activation="relu")(encoded_input)
    decoded_2 = Dense(decoder_2_dim, activation="relu")(decoded_1)
    decoded_3 = Dense(decoder_3_dim, activation="relu")(decoded_2)
    decoded_4 = Dense(decoder_4_dim, activation="sigmoid")(decoded_3)

    #construct models
    encoder = Model(input_layer, encoded_4)
    decoder = Model(encoded_input, decoded_4)
    autoencoder = Model(input_layer, decoder(encoder(input_layer)))

elif sys.argv[1] == "load":
    #load the autoencoder model and construct the encoder/decoder from it
    encoder = load_model("models/encoder.h5");
    decoder = load_model("models/decoder.h5");
    autoencoder = Model(input_layer, decoder(encoder(input_layer)))

#use stochastic gradient descent and MSE
#   autoencoder.compile(optimizer='sgd', loss='mean_squared_error', metrics=["accuracy"])
autoencoder.compile(optimizer='adadelta', loss='mean_squared_error', metrics=['accuracy'])

#train the autoencoder
autoencoder.fit(
    windows_train, windows_train,
    epochs = epochs,
    batch_size = len(windows_train),
    shuffle = True,
    validation_data = (windows_test, windows_test)
)

#save models
encoder.save("models/encoder.h5");
decoder.save("models/decoder.h5");

#get encoded and decoded data
encoded_data = encoder.predict(windows_test)
decoded_data = decoder.predict(encoded_data)

#calculate distances of encoded
dist = []
for i in range(0, len(encoded_data)):
    if (i < len(encoded_data) - 1):
        dist.append([
            np.linalg.norm(encoded_data[i] - encoded_data[i + 1])
            /
            np.sqrt(np.linalg.norm(encoded_data[i]) * np.linalg.norm(encoded_data[i + 1]))
        ])

#save original and decoded data into csv
def save (filename, data):
    with open ("results/" + filename + ".csv", "w") as csvfile:
        res = ""
        row = ""
        for win in data:
            for i in range(0, len(win)):
                row += str(win[i])
                if (i + 1) % channels == 0 or filename == "distance":
                    res += row + "\n"
                    row = ""
                else:
                    row += ","

        csvfile.write(res)

save("original", windows_test)
save("encoded", encoded_data)
save("decoded", decoded_data)
save("distance", dist)
