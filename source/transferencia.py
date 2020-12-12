import csv
import os
from datetime import datetime
from configsettings import Configs

configs = Configs('transferencia')

now = datetime.now().strftime('%d.%m.%Y-%H.%M.%S')
result_file_path = f'{configs.results_path}transferencia-{now}.txt'
results = open(result_file_path, 'w+')

with open(configs.latest_file, newline='', errors='replace') as transf_file:
    csv_reader = csv.reader(transf_file, delimiter=';')
    header = True
    for row in csv_reader:
        if header:
            header = False
            pass
        else:
            if 'Transf' in row[13] or 'PicPay' in row[13]:
                results.write(f'{row[1][:10]}\t{row[2][:20].upper().ljust(20)}\t{row[10]}\n')


results.close()
if configs.platform == 'windows':
    os.startfile(result_file_path)
