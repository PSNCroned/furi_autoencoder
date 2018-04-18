import csv

csv_name = "extracted.csv";

with open (r"C:\Users\Elliot\Desktop\furi\original_datasets\myo_exp.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    i = 0
    limit = 16000
    pointsAdded = 0
    res = ""

    for row in reader:
        if i < limit:
            res += (str(float(row[0])) +
            "," + str(float(row[1])) +
            "," + str(float(row[2])) +
            "," + str(float(row[3])) +
            "," + str(float(row[4])) +
            "," + str(float(row[5])) +
            "," + str(float(row[6])) +
            "," + str(float(row[7])) +
            "\n")
            pointsAdded += 1
        i += 1

    print(pointsAdded)

    with open("extracted/" + csv_name, "w") as newcsv:
        newcsv.write(res)
