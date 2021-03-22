#!/usr/bin/env python3
#webio.py

import csv

def get_csv_file(file_path):
    item_list = []
    with open(file_path) as csv_file:
        for line in csv.reader(csv_file, delimiter=','):
            item_list.append(line)

    return item_list


def write_csv_file(file_path, list):
    with open(file_path, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in list:
            writer.writerow(item)
    return
