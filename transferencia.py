import csv
import glob
import os
from datetime import datetime
from configsettings import Configs

configs = Configs()


downloads_path = configs.downloads_path
list_of_files = glob.glob(f'{downloads_path}*')

latest_file = max(list_of_files, key=os.path.getctime)

dates = []
names = []
values = []


with open(latest_file, newline='', errors='replace') as transf_file:
    csv_reader = csv.reader(transf_file, delimiter=';')
    header = True
    for row in csv_reader:
        if header:
            header = False
            pass
        else:
            if 'Transferência' in row[13] or 'PicPay' in row[13]:
                dates.append(row[1][:5])
                names.append(row[2].upper())
                values.append(row[10])
                print(f'{row[1]}\t\t{row[2]}\t\t{row[10]}')

now = datetime.now().strftime('%d.%m.%Y-%H.%M.%S')
results = open(f'results/transferencia-{now}.txt', 'w+')

results.write('DATAS\n')
for date in dates:
    results.write(date + '\n')

results.write('NOMES\n')
for name in names:
    results.write(name + '\n')

results.write('VALORES\n')
for value in values:
    results.write(value + '\n')

results.close()
if configs.platform == 'windows':
    results_path = configs.results_path
    os.startfile(f'{results_path}transferencia-{now}.txt')
