from keras.models import load_model
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import socket

def main():
    data = []
    window = []
    windows = []
    encoded_windows = []
    distances = []
    local_maxes = []

    interpreting = True
    window_size = 50
    channels = 8
    count = 0
    neighbors = 3

    gestures = ["right", "left", "fist"]
    training = [
        [
            [2.56,  3.99, -0.76, -0.73, -0.66, -0.46, -0.34,  0.16],
            [-1.36, -1.77, -3.38, -0.23, -0.41, -0.6,  -0.78, -1.22],
            [ 1.1,  -0.45, -1.55, -0.77, -0.73, -0.7,  -0.76, -0.89],

            [-0.25, -0.32, -0.54, -0.57, -0.41, -1.93, -1.57, -0.73],
            [-0.72, -0.77, -0.82, -0.52, -1.2,  -2.83, -2.59, -1.14],
            [-0.81, -0.76, -0.84, -0.99, -8.8,  -2.86, -0.69, -0.75],

            [-0.54, -0.3,  -0.73, -0.91, -0.82, -0.83, -0.77,  1.46],
            [-1.23, -0.96, -1.21, -0.75, -0.92, -0.28, -1.14,  8.12],
            [-1.11, -0.57, -1.09, -0.91, -0.86, -0.79, -1.71,  0.81]
        ],
        [0,0,0, 1,1,1, 2,2,2]
    ]

    #load model
    encoder = load_model("models/encoder.h5");
    rnn = load_model("models/rnn.h5");

    #make k-nn model
    knn = KNeighborsClassifier(n_neighbors=neighbors)
    knn.fit(np.array(training[0]), np.array(training[1]))

    #Connect to udp server that's serving live emg data from myo
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock.bind(("localhost", 41234))

    while True:
        #get emg data
        msg, addr = sock.recvfrom(1024)
        msg = msg.decode("utf-8", "strict").split(",")
        data.append(list(map(float, msg)))

        #collect data until full window obtained
        if len(data) == window_size:
            #normalize the data
            normalizeData(data)

            #save as an input window for the model
            for row in data:
                for chan in row:
                    window.append(chan)

            #pass window to the model
            #gesture = rnn.predict(np.array([data]).astype("float"))[0]
            encoded = encoder.predict(np.array([window]).astype("float"))[0]
            encoded_windows.append(encoded)

            mean = np.mean(data, axis=0) * 256 - 128

            data = []
            window = []

            #if not the first window saved
            if len(encoded_windows) != 1:
                index = len(encoded_windows) - 1
                prev_index = index - 1
                prev2_index = prev_index - 1;
                prev3_index = prev2_index - 1;

                #calculate distance between last window and this window
                dist = distance(encoded_windows[prev_index], encoded_windows[index])
                distances.append(dist)

                #if at least three previous windows
                if prev2_index > 0:
                    #determine if the second previous window is a local max
                    ##### The first previous window can't be checked for being a max because
                    ##### it needs the distances of the windows before and after it, and the
                    ##### window after it is the most recently recorded window. A distance
                    ##### value can only be calculated for a window with another window after it.
                    local_max = distances[prev2_index] - distances[prev3_index] > 0 and distances[prev2_index] - distances[prev_index] > 0

                    if local_max:
                        #print(distances[prev2_index])
                        index = prev2_index
                        local_maxes.append(index)

                        #if not the first local max
                        if len(local_maxes) > 1:
                            prev_index = local_maxes[len(local_maxes) - 2]

                            #determine if most recent local max differs by at least 30% from the previous
                            if distances[index] * 0.3 > distances[prev_index]:
                                print(count, "GESTURE STARTED")
                                count += 1

                                if interpreting:
                                    gest = knn.kneighbors(np.array([mean]))
                                    print(gestures[training[1][gest[1][0][0]]])
                            elif distances[prev_index] * 0.3 > distances[index]:
                                print(count, "GESTURE STOPPED")
                                count += 1


def normalizeData (data):
    c = 0
    channels = len(data[0])

    while c < channels:
        smallest = -128
        largest = 128

        largest -= smallest

        for point in data:
            point[c] = (point[c] - smallest) / (largest or 1)

        c += 1

def distance (data1, data2):
    dist = np.linalg.norm(data1 - data2) / np.sqrt(np.linalg.norm(data1) * np.linalg.norm(data2))
    return dist


if __name__ == "__main__": main()
