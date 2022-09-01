import csv

with open('data/phone_book.csv', mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        print(row["last_name"]+': '+row["phone_number"])
       