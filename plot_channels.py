import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import csv

num_channels = int(sys.argv[1])
data1 = []
data2 = []
window_size = 50

with open("results/" + sys.argv[2] + ".csv") as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        for i in range(0, num_channels):
            if len(data1) == i:
                data1.append([])
            data1[i].append(row[i])

if not sys.argv[3].isdigit():
    with open("results/" + sys.argv[3] + ".csv") as csvfile:
        for row in csv.reader(csvfile, delimiter=","):
            for i in range(0, num_channels):
                if len(data2) == i:
                    data2.append([])
                data2[i].append(row[i])

    points = int(sys.argv[4])
    chan = int(sys.argv[5])
else:
    points = int(sys.argv[3])
    chan = int(sys.argv[4])

dist = []

with open("results/distance.csv") as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        dist.append(float(row[0]))

dist = np.array(dist)
maxI = argrelextrema(dist, np.greater)
maxI = maxI[0]

plt.plot(data1[chan][:points], label=sys.argv[2])

if not sys.argv[3].isdigit():
    plt.plot(data2[chan][:points], label=sys.argv[3])
else:
    for i in range(0, num_channels):
        if not (i == chan):
            plt.plot(data1[i][:points], label=sys.argv[2])

for i in maxI:
    plt.axvline(x = i * window_size, color='r')

#plt.legend(loc='upper left')
plt.axis([0, points, 0, 1.5])
plt.show()

#python plot_channels.py 8 original decoded 500 1
