import csv

docs = [doc for doc in csv.DictReader(open('data.csv'), quoting=csv.QUOTE_NONE)]
