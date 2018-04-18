from keras.models import load_model
import numpy as np
import socket

def main():
    #Connect to udp server that's serving live emg data from myo
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock.bind(("localhost", 41234))

    data = []
    window = []
    windows = []
    encoded_windows = []
    distances = []
    local_maxes = []

    window_size = 50
    channels = 8
    count = 0

    #load model
    encoder = load_model("models/encoder.h5");

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
            encoded = encoder.predict(np.array([window]).astype("float"))[0]
            encoded_windows.append(encoded)

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
                        print(distances[prev2_index])
                        index = prev2_index
                        local_maxes.append(index)

                        #if not the first local max
                        if len(local_maxes) > 1:
                            prev_index = local_maxes[len(local_maxes) - 2]

                            #determine if most recent local max differs by at least 30% from the previous
                            if distances[index] * 0.3 > distances[prev_index]:
                                print(count, "GESTURE STARTED")
                                count += 1
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
