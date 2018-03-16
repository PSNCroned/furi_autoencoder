from keras.layers import Input, Dense
from keras.models import Model
from keras.datasets import mnist
import numpy as npimport csv
import math

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

#set parameters for windows
window_size = 784
overlap = 0
channels = 1

data = []
windows = []

#get data from csv and convert to 2D list
with open("extracted.csv") as csvfile:
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
windows = np.array(windows).astype("float32")

# this is the size of our encoded representations
encoding_dim = 32  # 32 floats -> compression of factor 24.5, assuming the input is 784 floats

# this is our input placeholder
input_img = Input(shape=(784,))
# "encoded" is the encoded representation of the input
encoded = Dense(encoding_dim, activation='relu')(input_img)
# "decoded" is the lossy reconstruction of the input
decoded = Dense(784, activation='sigmoid')(encoded)

# this model maps an input to its reconstruction
autoencoder = Model(input_img, decoded)

# this model maps an input to its encoded representation
encoder = Model(input_img, encoded)

# create a placeholder for an encoded (32-dimensional) input
encoded_input = Input(shape=(encoding_dim,))
# retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]
# create the decoder model
decoder = Model(encoded_input, decoder_layer(encoded_input))

autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])

(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print(x_train.shape)
print(x_test.shape)

autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))

# encode and decode some digits
# note that we take them from the *test* set
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)

def save (filename, data):
    with open (filename + ".csv", "w") as csvfile:
        res = ""
        row = ""
        for win in data:
            for i in range(0, len(win) - 1):
                row += str(win[i])
                if (i + 1) % 3 == 0:
                    res += row + "\n"
                    row = ""
                else:
                    row += ","

        csvfile.write(res)

save("test_original", x_test[:15]);
save("test_encoded", encoded_imgs[:15]);
save("test_decoded", decoded_imgs[:15]);
