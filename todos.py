import csv
import glob
from datetime import datetime
import os
from sys import platform


def string_to_currency(value):
    if value == '':
        return 0.0
    return float(value.replace('.', '').replace(',', '.'))


if platform == 'win32':
    list_of_files = glob.glob('C:/Users/pedra/Downloads/*')
else:
    list_of_files = glob.glob('/Users/Bruno/Downloads/*')

latest_file = max(list_of_files, key=os.path.getctime)

order_day = {}

with open(latest_file, newline='', errors='replace') as money_file:
    csv_reader = csv.reader(money_file, delimiter=';')
    header = True
    for row in csv_reader:
        if header:
            header = False
            pass
        else:
            date = datetime.strptime(row[0], '%d/%m/%Y %H:%M')
            date = date.strftime('%d/%m/%Y')
            total = order_day.get(date, 0)
            total += string_to_currency(row[9])
            order_day[date] = total


now = datetime.now().strftime('%d.%m.%Y-%H.%M.%S')
results = open(f'results/todos-{now}.txt', 'w+')

results.write('Data\t\tTotal\n')

for (date, total) in order_day.items():
    results.write('{}\t{:.2f}\n'.format(date, total).replace('.', ','))

results.close()
if platform == 'win32':
    os.startfile(f'C:/Users/pedra/Code/veganti-delivery/results/todos-{now}.txt')
