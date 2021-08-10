import csv
import os
from unidecode import unidecode
from datetime import datetime
from configsettings import Configs

configs = Configs('transferencia')

now = datetime.now().strftime('%d.%m.%Y-%H.%M.%S')
result_file_path = f'{configs.results_path}transferencia-{now}.txt'
results = open(result_file_path, 'w+')

with open(configs.latest_file, newline='', errors='replace') as transf_file:
    csv_reader = csv.reader(transf_file, delimiter=';')
    header = True
    date_index = 0
    name_index = 0
    total_index = 0
    for row in csv_reader:
        if header:
            date_index = row.index("Criado em")
            name_index = row.index("Nome")
            total_index = row.index("Total")
            payment_index = row.index("Forma de pagamento")
            header = False
            pass
        else:
            if 'Transf' in row[payment_index] or 'PicPay' in row[payment_index] or 'PIX' in row[payment_index]:
                results.write(f'{row[date_index][:10]}\t{unidecode(row[name_index][:20]).upper().ljust(20)}\t{row[total_index]}\n')


results.close()
if configs.platform == 'windows':
    os.startfile(result_file_path)
