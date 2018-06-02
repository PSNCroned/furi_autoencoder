import csv
import numpy as np

with open (r"C:\Users\Elliot\Desktop\furi\live_myo_data\data\fist.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    sum = [0, 0, 0, 0, 0, 0, 0, 0]
    count = 0

    for row in reader:
        sum[0] += float(row[0])
        sum[1] += float(row[1])
        sum[2] += float(row[2])
        sum[3] += float(row[3])
        sum[4] += float(row[4])
        sum[5] += float(row[5])
        sum[6] += float(row[6])
        sum[7] += float(row[7])
        count += 1

    sum = np.array(sum)
    avg = sum / count
    print(avg)
