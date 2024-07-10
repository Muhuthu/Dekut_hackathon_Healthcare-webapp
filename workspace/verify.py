import csv

with open('/home/muhuthu/Documents/medic_kit_hackathon.group20/workspace/dataset/breast_mammogram_dataset.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        print (row)
