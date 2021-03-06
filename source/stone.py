import csv
from datetime import datetime
from datetime import timedelta
import os
import requests
import json
from order import Order
from holiday import Holiday
from configsettings import Configs

configs = Configs('stone')
date = datetime.now()

ibge_rj = '3304557'
year = date.year
token = configs.holidays_token
uri = f'https://api.calendario.com.br/?json=true&ano={year}&ibge={ibge_rj}&token={token}'

response = requests.get(uri)

national_holidays = []
holiday_dates = []
if response.status_code == 200:
    for holiday in json.loads(response.content):
        if holiday['type_code'] == str(1):
            national_holidays.append(Holiday(
                holiday['date'], holiday['name'], holiday['type'], holiday['type_code']))
            holiday_dates.append(datetime.strptime(
                holiday['date'], '%d/%m/%Y').strftime('%Y-%m-%d'))


def string_to_currency(value):
    if value == '':
        return 0.0
    return float(value.replace('.', '').replace(',', '.'))

is_ant_day = True

while is_ant_day:
    while date.date().day != 5 and date.date().day != 20:
        date += timedelta(days=1)
        is_ant_day = False
    if is_ant_day:
        date += timedelta(days=1)

while date.weekday() == 5 or date.weekday() == 6 or date.strftime('%Y-%m-%d') in holiday_dates:
    date += timedelta(days=1)

with open(configs.latest_file, newline='', errors='replace') as stone_file:
    csv_reader = csv.reader(stone_file, delimiter=';')
    header = True
    stone_ant_orders = []
    stone_orders = []
    for row in csv_reader:
        if header:
            header = False
            pass
        else:
            disponivel = datetime.strptime(row[5], '%d/%m/%Y %H:%M:%S')
            valor_bruto = string_to_currency(row[12])
            if row[3] == 'Quitação de Empréstimo':
                valor_bruto *= -1
            valor_liquido = string_to_currency(row[13])
            if disponivel.date() >= date.date():
                taxa = string_to_currency(row[15])
                stone_order = Order(disponivel, valor_bruto,
                                    taxa, valor_liquido)
                stone_ant_orders.append(stone_order)
            else:
                taxa = 0
                desconto_ant = 0
                if valor_bruto > 0:
                    desconto_ant = string_to_currency(row[14])
                    taxa = string_to_currency(row[15])
                stone_order = Order(disponivel, valor_bruto,
                                    taxa, valor_liquido, desconto_ant)
                stone_orders.append(stone_order)


tax_per_day = 0.062
sum_bruto = sum_liquido = sum_taxa = sum_taxa_antecipacao = 0

for stone_order in stone_ant_orders:
    sum_bruto += stone_order.valor_bruto
    sum_liquido += stone_order.valor_liquido
    sum_taxa += stone_order.taxa

    days = abs((stone_order.disponivel.date() - date.date()).days)
    tax = (tax_per_day * days)/100

    sum_taxa_antecipacao += stone_order.valor_liquido*tax

sum_liquido -= sum_taxa_antecipacao
taxa_emprestimo = 0.1594
emp = taxa_emprestimo * sum_liquido

now = datetime.now().strftime('%d.%m.%Y-%H.%M.%S')
result_file_path = f'{configs.results_path}stone-{now}.txt'
results = open(result_file_path, 'w+')

results.write('Data\t\t\tBruto\t\tTaxa\t\tAntecipação\tEmpréstimo\tLíquido\n')

dict_orders = {}

stone_orders.sort(key=lambda x: x.disponivel)

for stone_order in stone_orders:
    bruto, taxa, liquido, emprestimo, antecipacao = dict_orders.get(
        stone_order.disponivel, (0, 0, 0, 0, 0))
    if stone_order.valor_bruto < 0:
        emprestimo += stone_order.valor_bruto
    else:
        bruto += stone_order.valor_bruto
        taxa += stone_order.taxa
        liquido += stone_order.valor_liquido
        antecipacao += stone_order.desconto_ant
    dict_orders[stone_order.disponivel] = (
        bruto, taxa, liquido, emprestimo, antecipacao)


for (disponivel, t_values) in dict_orders.items():
    if t_values[3] == 0:
        t_values = (t_values[0], t_values[1], t_values[2], -
                    1*taxa_emprestimo*t_values[2], t_values[4])
    results.write('{}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\n'
                  .format(disponivel.strftime('%d/%m/%y'), t_values[0], t_values[1], t_values[4], -1*t_values[3], t_values[2] + t_values[3])
                  .replace('.', ','))

results.write('\n{}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\n'
              .format(date.strftime('%d/%m/%y'), sum_bruto, sum_taxa, sum_taxa_antecipacao, emp, sum_liquido - emp)
              .replace('.', ','))

results.close()
if configs.platform == 'windows':
    os.startfile(result_file_path)
