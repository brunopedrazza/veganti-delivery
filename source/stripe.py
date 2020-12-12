import csv
from datetime import datetime
from datetime import timedelta
import os
from order import Order
from sys import platform
from configsettings import Configs

configs = Configs('stripe')

def string_to_currency(currency_string):
    return float(currency_string.replace('.', '').replace(',', '.'))

date_value = {}

with open(configs.latest_file) as orders_file:
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
result_file_path = f'{configs.results_path}stripe-{now}.txt'
results = open(result_file_path, 'w+')

results.write('Data\t\t\tBruto\t\tTaxa\t\tLiquido\n')

for (date, t_values) in date_value.items():
    bruto, taxa, liquido = t_values
    results.write('{}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\n'
                  .format((date + timedelta(days=1)).strftime('%d/%m/%y'), bruto, taxa, liquido)
                  .replace('.', ','))

results.close()
if configs.platform == 'windows':
    os.startfile(result_file_path)
