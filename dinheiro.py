import csv
import glob
import os


def string_to_currency(value):
    if value == '':
        return 0.0
    return float(value.replace('.', '').replace(',', '.'))

list_of_files = glob.glob('C:/Users/pedra/Downloads/*')
latest_file = max(list_of_files, key=os.path.getctime)


with open(latest_file, newline='', errors='replace') as money_file:
    csv_reader = csv.reader(money_file, delimiter=';')
    header = True
    for row in csv_reader:
        if header:
            header = False
            pass
        else:
            if row[12] == 'Dinheiro':
                print(f'{row[0]}\t\t{row[1]}\t\t{row[9]}')
