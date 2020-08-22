import csv
from datetime import datetime
from datetime import timedelta
import glob
import os
from order import Order
from sys import platform
from configsettings import Configs

configs = Configs()

def string_to_currency(currency_string):
    return float(currency_string.replace('.', '').replace(',', '.'))

downloads_path = configs.downloads_path
list_of_files = glob.glob(f'{downloads_path}*.csv')

latest_file = max(list_of_files, key=os.path.getctime)

date_value = {}

with open(latest_file) as orders_file:
    csv_reader = csv.reader(orders_file, delimiter=';')
    header = True
    orders = []
    for row in csv_reader:
        if header:
            header = False
            pass
        else:
            disponivel = datetime.strptime(row[0], '%d/%m/%Y')
            valor_bruto = string_to_currency(row[1])
            taxa = string_to_currency(row[2])
            valor_liquido = string_to_currency(row[3])
            tipo = row[4]
            if 'Transferência bancária' not in tipo and disponivel >= datetime(2020, 4, 6):
                order = Order(disponivel, valor_bruto, taxa, valor_liquido)
                orders.append(order)

orders.sort(key=lambda x: x.disponivel, reverse=True)

for order in orders:
    disponivel = order.disponivel
    while disponivel.weekday() != 6:
        disponivel += timedelta(days=1)
    bruto, taxa, liquido = date_value.get(disponivel, (0, 0, 0))
    t_values = (bruto + order.valor_bruto, taxa + order.taxa, liquido + order.valor_liquido)
    date_value[disponivel] = t_values


now = datetime.now().strftime('%d.%m.%Y-%H.%M.%S')
results = open(f'results/stripe-{now}.txt', 'w+')

results.write('Data\t\t\tBruto\t\tTaxa\t\tLiquido\n')

for (date, t_values) in date_value.items():
    bruto, taxa, liquido = t_values
    results.write('{}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\n'
                  .format((date + timedelta(days=1)).strftime('%d/%m/%y'), bruto, taxa, liquido)
                  .replace('.', ','))

results.close()
if configs.platform == 'windows':
    results_path = configs.results_path
    os.startfile(f'{results_path}stripe-{now}.txt')
