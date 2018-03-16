import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import csv

x_1 = []
x_2 = []
window_size = 50

#data
with open("results/" + sys.argv[1] + ".csv") as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        x_1.append(row[0])

if not sys.argv[2].isdigit():
    with open("results/" + sys.argv[2] + ".csv") as csvfile:
        for row in csv.reader(csvfile, delimiter=","):
            x_2.append(row[0])

    points = int(sys.argv[3])
else:
    points = int(sys.argv[2])

plt.plot(x_1[:points], label=sys.argv[1])

if not sys.argv[2].isdigit():
    plt.plot(x_2[:points], label=sys.argv[2])

#distance
if len(sys.argv) > 4:
    if sys.argv[4]:
        dist = []

        with open("results/distance.csv") as csvfile:
            for row in csv.reader(csvfile, delimiter=","):
                dist.append(float(row[0]))

        dist = np.array(dist)
        maxI = argrelextrema(dist, np.greater)
        maxI = maxI[0]

        for i in maxI:
            plt.axvline(x = i * window_size, color='r')

plt.legend(loc='upper left')
plt.axis([0, points, 0, 1.5])
plt.show()
