import csv

csv_name = "extracted.csv";

with open (r"C:\Users\Elliot\Desktop\furi\original_datasets\temps.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    i = 0
    pointsAdded = 0
    res = ""
    for row in reader:
        res += str(float(row[1])) + "\n"
        pointsAdded += 1

    print(pointsAdded)

    with open("extracted/" + csv_name, "w") as newcsv:
        newcsv.write(res)
