import csv

with open('RegionDataCSV.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i < 20 or (90 < i < 110) or (i>120 and i<140):
            print(i, row)
