import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import csv

window_size = int(sys.argv[1])
data = []

with open("results/distance.csv") as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        data.append(float(row[0]))

data = np.array(data)
maxI = argrelextrema(data, np.greater)
maxI = maxI[0]

#plt.plot(list(np.arange(0, len(data) * window_size, window_size)), data, label="distance")

for i in maxI:
    plt.axvline(x = i * window_size, color='r')

plt.legend(loc='upper left')
plt.axis([0, len(data) * window_size, 0, 1.5])
plt.show()

#python dist.py 50 1
