import csv
from datetime import datetime
import os
from sys import platform
from configsettings import Configs

configs = Configs('todos')

def string_to_currency(value):
    if value == '':
        return 0.0
    return float(value.replace('.', '').replace(',', '.'))

order_day = {}

with open(configs.latest_file, newline='', errors='replace') as money_file:
    csv_reader = csv.reader(money_file, delimiter=';')
    header = True
    date_index = 0
    total_index = 0
    for row in csv_reader:
        if header:
            date_index = row.index("Data")
            total_index = row.index("Total")
            header = False
            pass
        else:
            date = datetime.strptime(row[date_index], '%d/%m/%Y %H:%M')
            date = date.strftime('%d/%m/%Y')
            total = order_day.get(date, 0)
            total += string_to_currency(row[total_index])
            order_day[date] = total


now = datetime.now().strftime('%d.%m.%Y-%H.%M.%S')
result_file_path = f'{configs.results_path}todos-{now}.txt'
results = open(result_file_path, 'w+')

results.write('Data\t\tTotal\n')

for (date, total) in order_day.items():
    results.write('{}\t{:.2f}\n'.format(date, total).replace('.', ','))

results.close()
if configs.platform == 'windows':
    os.startfile(result_file_path)
